/*
 * Copyright (C) 2011 Adam Barth. All Rights Reserved.
 * Copyright (C) 2011 Daniel Bates (dbates@intudata.com).
 *
 * Redistribution and use in source and binary forms, with or without
 * modification, are permitted provided that the following conditions
 * are met:
 * 1. Redistributions of source code must retain the above copyright
 *    notice, this list of conditions and the following disclaimer.
 * 2. Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the
 *    documentation and/or other materials provided with the distribution.
 *
 * THIS SOFTWARE IS PROVIDED BY APPLE INC. ``AS IS'' AND ANY
 * EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
 * IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
 * PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL APPLE INC. OR
 * CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
 * EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
 * PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
 * PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
 * OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
 * (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
 * OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 */

#include "third_party/blink/renderer/core/html/parser/xss_auditor.h"

#include <memory>

#include "third_party/blink/renderer/core/dom/document.h"
#include "third_party/blink/renderer/core/frame/local_frame.h"
#include "third_party/blink/renderer/core/frame/settings.h"
#include "third_party/blink/renderer/core/html/html_param_element.h"
#include "third_party/blink/renderer/core/html/link_rel_attribute.h"
#include "third_party/blink/renderer/core/html/parser/html_document_parser.h"
#include "third_party/blink/renderer/core/html/parser/html_parser_idioms.h"
#include "third_party/blink/renderer/core/html/parser/text_resource_decoder.h"
#include "third_party/blink/renderer/core/html/parser/xss_auditor_delegate.h"
#include "third_party/blink/renderer/core/html_names.h"
#include "third_party/blink/renderer/core/inspector/console_message.h"
#include "third_party/blink/renderer/core/loader/document_loader.h"
#include "third_party/blink/renderer/core/loader/mixed_content_checker.h"
#include "third_party/blink/renderer/core/svg_names.h"
#include "third_party/blink/renderer/core/xlink_names.h"
#include "third_party/blink/renderer/platform/instrumentation/use_counter.h"
#include "third_party/blink/renderer/platform/network/encoded_form_data.h"
#include "third_party/blink/renderer/platform/text/decode_escape_sequences.h"
#include "third_party/blink/renderer/platform/wtf/text/ascii_ctype.h"

namespace {

// SecurityOrigin::urlWithUniqueSecurityOrigin() can't be used cross-thread, or
// we'd use it instead.
const char kURLWithUniqueOrigin[] = "data:,";

const char kSafeJavaScriptURL[] = "javascript:void(0)";

}  // namespace

namespace blink {

using namespace html_names;

static bool IsNonCanonicalCharacter(UChar c) {
  // We remove all non-ASCII characters, including non-printable ASCII
  // characters.
  //
  // Note, we don't remove backslashes like PHP stripslashes(), which among
  // other things converts "\\0" to the \0 character. Instead, we remove
  // backslashes and zeros (since the string "\\0" =(remove backslashes)=> "0").
  // However, this has the adverse effect that we remove any legitimate zeros
  // from a string.
  //
  // We also remove forward-slash, because it is common for some servers to
  // collapse successive path components, eg, a//b becomes a/b.
  //
  // We also remove the questionmark character, since some severs replace
  // invalid high-bytes with a questionmark. We are already stripping the
  // high-bytes so we also strip the questionmark to match.
  //
  // We also move the percent character, since some servers strip it when
  // there's a malformed sequence.
  //
  // For instance: new String("http://localhost:8000?x") => new
  // String("http:localhost:8x").
  return (c == '\\' || c == '0' || c == '\0' || c == '/' || c == '?' ||
          c == '%' || c >= 127);
}

static bool IsRequiredForInjection(UChar c) {
  return (c == '\'' || c == '"' || c == '<' || c == '>');
}

static bool IsTerminatingCharacter(UChar c) {
  return (c == '&' || c == '/' || c == '"' || c == '\'' || c == '<' ||
          c == '>' || c == ',' || c == ';');
}

static bool IsSlash(UChar c) {
  return (c == '/' || c == '\\');
}

static bool IsHTMLQuote(UChar c) {
  return (c == '"' || c == '\'');
}

static bool IsJSNewline(UChar c) {
  // Per ecma-262 section 7.3 Line Terminators.
  return (c == '\n' || c == '\r' || c == 0x2028 || c == 0x2029);
}

static bool StartsHTMLOpenCommentAt(const String& string, wtf_size_t start) {
  return (start + 3 < string.length() && string[start] == '<' &&
          string[start + 1] == '!' && string[start + 2] == '-' &&
          string[start + 3] == '-');
}

static bool StartsHTMLCloseCommentAt(const String& string, wtf_size_t start) {
  return (start + 2 < string.length() && string[start] == '-' &&
          string[start + 1] == '-' && string[start + 2] == '>');
}

static bool StartsSingleLineCommentAt(const String& string, wtf_size_t start) {
  return (start + 1 < string.length() && string[start] == '/' &&
          string[start + 1] == '/');
}

static bool StartsMultiLineCommentAt(const String& string, wtf_size_t start) {
  return (start + 1 < string.length() && string[start] == '/' &&
          string[start + 1] == '*');
}

static bool StartsOpeningScriptTagAt(const String& string, wtf_size_t start) {
  if (start + 6 >= string.length())
    return false;
  // TODO(esprehn): StringView should probably have startsWith.
  StringView script("<script");
  return EqualIgnoringASCIICase(StringView(string, start, script.length()),
                                script);
}

static bool StartsClosingScriptTagAt(const String& string, wtf_size_t start) {
  if (start + 7 >= string.length())
    return false;
  // TODO(esprehn): StringView should probably have startsWith.
  StringView script("</script");
  return EqualIgnoringASCIICase(StringView(string, start, script.length()),
                                script);
}

// If other files need this, we should move this to
// core/html/parser/html_parser_idioms.h
template <wtf_size_t inlineCapacity>
bool ThreadSafeMatch(const Vector<UChar, inlineCapacity>& vector,
                     const QualifiedName& qname) {
  return EqualIgnoringNullity(vector, qname.LocalName().Impl());
}

static bool HasName(const HTMLToken& token, const QualifiedName& name) {
  return ThreadSafeMatch(token.GetName(), name);
}

static bool FindAttributeWithName(const HTMLToken& token,
                                  const QualifiedName& name,
                                  wtf_size_t& index_of_matching_attribute) {
  // Notice that we're careful not to ref the StringImpl here because we might
  // be on a background thread.
  const String& attr_name = name.NamespaceURI() == xlink_names::kNamespaceURI
                                ? "xlink:" + name.LocalName().GetString()
                                : name.LocalName().GetString();

  for (wtf_size_t i = 0; i < token.Attributes().size(); ++i) {
    if (EqualIgnoringNullity(token.Attributes().at(i).NameAsVector(),
                             attr_name)) {
      index_of_matching_attribute = i;
      return true;
    }
  }
  return false;
}

static bool IsNameOfInlineEventHandler(const Vector<UChar, 32>& name) {
  const wtf_size_t kLengthOfShortestInlineEventHandlerName =
      5;  // To wit: oncut.
  if (name.size() < kLengthOfShortestInlineEventHandlerName)
    return false;
  return name[0] == 'o' && name[1] == 'n';
}

static bool IsDangerousHTTPEquiv(const String& value) {
  String equiv = value.StripWhiteSpace();
  return DeprecatedEqualIgnoringCase(equiv, "refresh") ||
         DeprecatedEqualIgnoringCase(equiv, "set-cookie");
}

static inline String Decode16BitUnicodeEscapeSequences(const String& string) {
  // Note, the encoding is ignored since each %u-escape sequence represents a
  // UTF-16 code unit.
  return DecodeEscapeSequences<Unicode16BitEscapeSequence>(string,
                                                           UTF8Encoding());
}

static inline String DecodeStandardURLEscapeSequences(
    const String& string,
    const WTF::TextEncoding& encoding) {
  // We use DecodeEscapeSequences() instead of DecodeURLEscapeSequences()
  // (declared in weborigin/kurl.h) to avoid platform-specific URL decoding
  // differences (e.g. KURLGoogle).
  return DecodeEscapeSequences<URLEscapeSequence>(string, encoding);
}

static String FullyDecodeString(const String& string,
                                const WTF::TextEncoding& encoding) {
  wtf_size_t old_working_string_length;
  String working_string = string;
  do {
    old_working_string_length = working_string.length();
    working_string = Decode16BitUnicodeEscapeSequences(
        DecodeStandardURLEscapeSequences(working_string, encoding));
  } while (working_string.length() < old_working_string_length);
  working_string.Replace('+', ' ');
  return working_string;
}

// XSSAuditor's task is to determine how much of any given content came
// from a reflection vs. what occurs normally on the page. It must do
// this in face of an attacker avoiding detection by splicing on page
// content in such a way as to remain syntactically valid. The next two
// functions apply heurisitcs to get the longest possible fragment in
// face of such trickery.

static void TruncateForSrcLikeAttribute(String& decoded_snippet) {
  // In HTTP URLs, characters in the query string (following the first ?),
  // in the fragment (following the first #), or even in the path (typically
  // following the third slash but subject to generous interpretation of a
  // lack of leading slashes) may be merely ignored by an attacker's server
  // when a remote script or script-like resource is requested. Hence these
  // are places where organic page content may be spliced.
  //
  // In DATA URLS, the payload starts at the first comma, and the the first
  //  "/*", "//", or "<!--" may introduce a comment, which can then be used
  // to splice page data harmlessly onto the end of the payload.
  //
  // Also, DATA URLs may use the same string literal tricks as with script
  // content itself. In either case, content following this may come from the
  // page and may be ignored when the script is executed. Also, any of these
  // characters may now be represented by the (enlarged) set of html5 entities.
  //
  // For simplicity, we don't differentiate based on URL scheme, and stop at
  // any of the following:
  //   - the first &, since it might be part of an entity for any of the
  //     subsequent punctuation.
  //   - the first # or ?, since the query and fragment can be ignored.
  //   - the third slash, since this typically starts the path, but account
  //     for a possible lack of leading slashes following the scheme).
  //   - the first slash, <, ', or " once a comma is seen, since we
  //     may now be in a data URL payload.
  int slash_count = 0;
  bool comma_seen = false;
  bool colon_seen = false;
  for (wtf_size_t current_length = 0,
                  remaining_length = decoded_snippet.length();
       remaining_length; ++current_length, --remaining_length) {
    UChar current_char = decoded_snippet[current_length];
    if (current_char == ':' && !colon_seen) {
      if (remaining_length > 1 && !IsSlash(decoded_snippet[current_length + 1]))
        ++slash_count;
      if (remaining_length > 2 && !IsSlash(decoded_snippet[current_length + 2]))
        ++slash_count;
      colon_seen = true;
    }
    if (current_char == '&' || current_char == '?' || current_char == '#' ||
        (IsSlash(current_char) && (comma_seen || ++slash_count > 2)) ||
        (current_char == '<' && comma_seen) ||
        (current_char == '\'' && comma_seen) ||
        (current_char == '"' && comma_seen)) {
      decoded_snippet.Truncate(current_length);
      return;
    }
    if (current_char == ',')
      comma_seen = true;
  }
}

static void TruncateForScriptLikeAttribute(String& decoded_snippet) {
  // Beware of trailing characters which came from the page itself, not the
  // injected vector. Excluding the terminating character covers common cases
  // where the page immediately ends the attribute, but doesn't cover more
  // complex cases where there is other page data following the injection.
  //
  // Generally, these won't parse as javascript, so the injected vector
  // typically excludes them from consideration via a single-line comment or
  // by enclosing them in a string literal terminated later by the page's own
  // closing punctuation. Since the snippet has not been parsed, the vector
  // may also try to introduce these via entities. As a result, we'd like to
  // stop before the first "//", the first <!--, the first entity, or the first
  // quote not immediately following the first equals sign (taking whitespace
  // into consideration).
  //
  // To keep things simpler, we don't try to distinguish between
  // entity-introducing amperands vs. other uses, nor do we bother to check for
  // a second slash for a comment, nor do we bother to check for !-- following a
  // less-than sign. We stop instead on any ampersand slash, or less-than sign.
  wtf_size_t position = 0;
  if ((position = decoded_snippet.Find("=")) != kNotFound &&
      (position = decoded_snippet.Find(IsNotHTMLSpace<UChar>, position + 1)) !=
          kNotFound &&
      (position = decoded_snippet.Find(
           IsTerminatingCharacter,
           IsHTMLQuote(decoded_snippet[position]) ? position + 1 : position)) !=
          kNotFound) {
    decoded_snippet.Truncate(position);
  }
}

static void TruncateForSemicolonSeparatedScriptLikeAttribute(
    String& decoded_snippet) {
  // Same as script-like attributes, but semicolons can introduce page data.
  TruncateForScriptLikeAttribute(decoded_snippet);
  wtf_size_t position = decoded_snippet.Find(";");
  if (position != kNotFound)
    decoded_snippet.Truncate(position);
}

static bool IsSemicolonSeparatedAttribute(
    const HTMLToken::Attribute& attribute) {
  return ThreadSafeMatch(attribute.NameAsVector(), svg_names::kValuesAttr);
}

static bool IsSemicolonSeparatedValueContainingJavaScriptURL(
    const String& value) {
  Vector<String> value_list;
  value.Split(';', value_list);
  for (wtf_size_t i = 0; i < value_list.size(); ++i) {
    String stripped = StripLeadingAndTrailingHTMLSpaces(value_list[i]);
    if (ProtocolIsJavaScript(stripped))
      return true;
  }
  return false;
}
