package main

// func IsNonCanonicalCharacter(byte c) bool {
// 	// We remove all non-ASCII characters, including non-printable ASCII
// 	// characters.
// 	//
// 	// Note, we don't remove backslashes like PHP stripslashes(), which among
// 	// other things converts "\\0" to the \0 character. Instead, we remove
// 	// backslashes and zeros (since the string "\\0" =(remove backslashes)=> "0").
// 	// However, this has the adverse effect that we remove any legitimate zeros
// 	// from a string.
// 	//
// 	// We also remove forward-slash, because it is common for some servers to
// 	// collapse successive path components, eg, a//b becomes a/b.
// 	//
// 	// We also remove the questionmark character, since some severs replace
// 	// invalid high-bytes with a questionmark. We are already stripping the
// 	// high-bytes so we also strip the questionmark to match.
// 	//
// 	// We also move the percent character, since some servers strip it when
// 	// there's a malformed sequence.
// 	//
// 	// For instance: new String("http://localhost:8000?x") => new
// 	// String("http:localhost:8x").
// 	return (c == '\\' || c == '0' || c == '\0' || c == '/' || c == '?' ||
// 			c == '%' || c >= 127);
// }

// func IsRequiredForInjection(byte c) bool {
// 	return (c == '\'' || c == '"' || c == '<' || c == '>');
// }

// func IsTerminatingCharacter(byte c) bool {
// 	return (c == '&' || c == '/' || c == '"' || c == '\'' || c == '<' ||
// 			c == '>' || c == ',' || c == ';');
// }

// func IsSlash(byte c) bool {
// 	return (c == '/' || c == '\\');
// }

// func IsHTMLQuote(byte c) bool {
// 	return (c == '"' || c == '\'');
// }

// func IsJSNewline(byte c) bool {
// 	// Per ecma-262 section 7.3 Line Terminators.
// 	return (c == '\n' || c == '\r' || c == 0x2028 || c == 0x2029);
// }
