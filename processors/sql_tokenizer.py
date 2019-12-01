import urllib.parse

import re
import numpy
import networkx as nx

class FeatureExtractor:
    
    DANGEROUS_TOKEN = ["rename", "drop", "delete", "insert", "create", "exec", "update", "union", "set", "alter", "database", "and", "or", "information_schema", "load_file", "select", "shutdown", "cmdshell", "hex", "ascii"]

    SQL_TOKEN = ["where", "table", "like",
    "select", "update", "and", "or", "set", "in", "having", "values", "into",
    "alter", "as", "create", "revoke", "deny", "convert", "exec", "concat",
    "char", "tuncat", "ASCII", "any", "asc", "desc", "check", "group by",
    "order by", "delete from", "insert into", "drop table", "union",
    "join"]

    SQL_SPECIAL_CHAR = ["--", "#", "/*", "'", "''", "||", "\\", "=", "/**/","@@"]

    PUNCTUATION = ["<", ">", "*", ";", "_", "-", "(",")", "=", "{", "}", "@", ".", ",", "&", "[", "]", "+", "-", "?", "%", "!", ":", "\\", "/"]

    query_for_inspection = ""

    def __init__(self, query):
        super().__init__()
        self.query_for_inspection = query

    def special_char_freq(self):
        # (dangerous characters) like (--, #, /*, ', '', ||, \\, =, /**/,@@)
        return

    def dangerous_token_freq(self):
        # (dangerous tokens) like (rename, drop, delete, insert, create, exec, update, union, set, Alter, database, and, or, etc.)
        return

    def punctuations_freq(self):
        return
        
    def sql_token_freq(self):
        return


reserved = ['ACCESSIBLE', 'ACCOUNT', 'ACTION', 'ADD', 'ADMIN', 'AFTER', 'AGAINST', 'AGGREGATE', 'ALGORITHM', 'ALL', 'ALTER', 'ALWAYS', 'ANALYSE', 'ANALYZE', 'AND', 'ANY', 'AS', 'ASC', 'ASCII', 'ASENSITIVE', 'AT', 'AUTHORS', 'AVG', 'BACKUP', 'BEFORE', 'BEGIN', 'BETWEEN', 'BIGINT', 'BINARY', 'BINLOG', 'BIT', 'BLOB', 'BLOCK', 'BOOL', 'BOOLEAN', 'BOTH', 'BTREE', 'BUCKETS', 'BY', 'BYTE', 'CACHE', 'CALL', 'CASCADE', 'CASCADED', 'CASE', 'CAST', 'CHAIN', 'CHANGE', 'CHANGED', 'CHANNEL', 'CHAR', 'CHARACTER', 'CHARSET', 'CHECK', 'CHECKSUM', 'CIPHER', 'CLIENT', 'CLONE', 'CLOSE', 'COALESCE', 'CODE', 'COLLATE', 'COLLATION', 'COLUMN', 'COLUMNS', 'COMMENT', 'COMMIT', 'COMMITTED', 'COMPACT', 'COMPLETION', 'COMPONENT', 'COMPRESSED', 'COMPRESSION', 'CONCURRENT', 'CONCAT', 'CONDITION', 'CONNECTION', 'CONSISTENT', 'CONSTRAINT', 'CONTAINS', 'CONTEXT', 'CONTINUE', 'CONTRIBUTORS', 'CONVERT', 'CPU', 'CREATE', 'CROSS', 'CUBE', 'CURRENT', 'CURSOR', 'DATA', 'DATABASE', 'DATABASES', 'DATAFILE', 'DATE', 'DATETIME', 'DAY', 'DBMS_PIPE.RECEIVE_MESSAGE', 'DEALLOCATE', 'DEC', 'DECIMAL', 'DECLARE', 'DEFAULT', 'DEFINER', 'DEFINITION', 'DELAYED', 'DELETE', 'DESC', 'DESCRIBE', 'DESCRIPTION', 'DETERMINISTIC', 'DIAGNOSTICS', 'DIRECTORY', 'DISABLE', 'DISCARD', 'DISK', 'DISTINCT', 'DISTINCTROW', 'DIV', 'DO', 'DOUBLE', 'DROP', 'DUAL', 'DUMPFILE', 'DUPLICATE', 'DYNAMIC', 'EACH', 'ELSE', 'ELSEIF', 'EMPTY', 'ENABLE', 'ENCLOSED', 'ENCRYPTION', 'END', 'ENDS', 'ENGINE', 'ENGINES', 'ENUM', 'ERROR', 'ERRORS', 'ESCAPE', 'ESCAPED', 'EVENT', 'EVENTS', 'EVERY', 'EXCEPT', 'EXCHANGE', 'EXCLUDE', 'EXP', 'ELT', 'EXECUTE', 'EXISTS', 'EXIT', 'EXPANSION', 'EXPIRE', 'EXPLAIN', 'EXPORT', 'EXTENDED', 'FALSE', 'FAST', 'FAULTS', 'FETCH', 'FIELDS', 'FILE', 'FILTER', 'FIRST', 'FIXED', 'FLOAT', 'FLOOR', 'FLUSH', 'FOLLOWING', 'FOLLOWS', 'FOR', 'FORCE', 'FOREIGN', 'FORMAT', 'FOUND', 'FROM', 'FULL', 'FULLTEXT', 'FUNCTION', 'GENERAL', 'GENERATED', 'GEOMCOLLECTION', 'GEOMETRY', 'GEOMETRYCOLLECTION', 'GET', 'GLOBAL', 'GRANT', 'GRANTS', 'GROUP', 'GROUPING', 'GROUPS', 'HANDLER', 'HASH', 'HAVING', 'HELP', 'HISTOGRAM', 'HISTORY', 'HOST', 'HOSTS', 'HOUR', 'IDENTIFIED', 'IF', 'IGNORE', 'IMPORT', 'IN', 'INDEX', 'INDEXES', 'INFILE', 'INNER', 'INNOBASE', 'INNODB', 'INOUT', 'INSENSITIVE', 'INSERT', 'INSTALL', 'INSTANCE', 'INT', 'INTEGER', 'INTERVAL', 'INTO', 'INVISIBLE', 'INVOKER', 'IO', 'IPC', 'IS', 'ISOLATION', 'ISSUER', 'ITERATE', 'JOIN', 'JSON', 'KEY', 'KEYS', 'KILL', 'LAG', 'LANGUAGE', 'LAST', 'LEAD', 'LEADING', 'LEAVE', 'LEAVES', 'LEFT', 'LESS', 'LEVEL', 'LIKE', 'LIMIT', 'LINEAR', 'LINES', 'LINESTRING', 'LIST', 'LOAD', 'LOCAL', 'LOCALTIME', 'LOCALTIMESTAMP', 'LOCK', 'LOCKED', 'LOCKS', 'LOGFILE', 'LOGS', 'LONG', 'LONGBLOB', 'LONGTEXT', 'LOOP', 'MASTER', 'MATCH', 'MAXVALUE', 'MEDIUM', 'MEDIUMBLOB', 'MEDIUMINT', 'MEDIUMTEXT', 'MEMORY', 'MERGE', 'MICROSECOND', 'MIDDLEINT', 'MIGRATE', 'MINUTE', 'MOD', 'MODE', 'MODIFIES', 'MODIFY', 'MONTH', 'MULTILINESTRING', 'MULTIPOINT', 'MULTIPOLYGON', 'MUTEX', 'NAME', 'NAMES', 'NATIONAL', 'NATURAL', 'NCHAR', 'NDB', 'NDBCLUSTER', 'NESTED', 'NEVER', 'NEW', 'NEXT', 'NO', 'NODEGROUP', 'NONE', 'NOT', 'NOWAIT', 'NTILE', 'NULL', 'NULLS', 'NUMBER', 'NUMERIC', 'NVARCHAR', 'OF', 'OFFSET', 'MD5', 'ON', 'ONE', 'ONLY', 'OPEN', 'OPTIMIZE', 'OPTION', 'OPTIONALLY', 'OPTIONS', 'OR', 'ORDER', 'ORDINALITY', 'OTHERS', 'OUT', 'OUTER', 'OUTFILE', 'OVER', 'OWNER', 'PAGE', 'PARSER', 'PARTIAL', 'PARTITION', 'PARTITIONING', 'PARTITIONS', 'PASSWORD', 'PATH', 'PERSIST', 'PHASE', 'PLUGIN', 'PLUGINS', 'POINT', 'POLYGON', 'PORT', 'PRECEDES', 'PRECEDING', 'PRECISION', 'PREPARE', 'PRESERVE', 'PREV', 'PRIMARY', 'PRIVILEGES', 'PROCEDURE', 'PROCESS', 'PROCESSLIST', 'PROFILE', 'PROFILES', 'PROXY', 'PURGE', 'QUARTER', 'QUERY', 'QUICK', 'RANGE', 'RANK', 'READ', 'READS', 'REAL', 'REBUILD', 'RECOVER', 'RECURSIVE', 'REDOFILE', 'REDUNDANT', 'REFERENCE', 'REFERENCES', 'REGEXP', 'RELAY', 'RELAYLOG', 'RELEASE', 'RELOAD', 'REMOTE', 'REMOVE', 'RENAME', 'REORGANIZE', 'REPAIR', 'REPEAT', 'REPEATABLE', 'REPLACE', 'REPLICATION', 'REQUIRE', 'RESET', 'RESIGNAL', 'RESOURCE', 'RESPECT', 'RESTART', 'RESTORE', 'RESTRICT', 'RESUME', 'RETURN', 'RETURNS', 'REUSE', 'REVERSE', 'REVOKE', 'RIGHT', 'RLIKE', 'ROLE', 'ROLLBACK', 'ROLLUP', 'ROTATE', 'ROUTINE', 'ROW', 'ROWS', 'RTREE', 'SAVEPOINT', 'SCHEDULE', 'SCHEMA', 'SCHEMAS', 'SECOND', 'SECURITY', 'SELECT', 'SLEEP', 'SENSITIVE', 'SEPARATOR', 'SERIAL', 'SERIALIZABLE', 'SERVER', 'SESSION', 'SET', 'SHARE', 'SHOW', 'SHUTDOWN', 'SIGNAL', 'SIGNED', 'SIMPLE', 'SKIP', 'SLAVE', 'SLOW', 'SMALLINT', 'SNAPSHOT', 'SOCKET', 'SOME', 'SONAME', 'SOUNDS', 'SOURCE', 'SPATIAL', 'SPECIFIC', 'SQL', 'SQLEXCEPTION', 'SQLSTATE', 'SQLWARNING', 'SRID', 'SSL', 'STACKED', 'START', 'STARTING', 'STARTS', 'STATUS', 'STOP', 'STORAGE', 'STORED', 'STRING', 'SUBJECT', 'SUBPARTITION', 'SUBPARTITIONS', 'SUPER', 'SUSPEND', 'SWAPS', 'SWITCHES', 'SYSTEM', 'TABLE', 'TABLES', 'TABLESPACE', 'TEMPORARY', 'TEMPTABLE', 'TERMINATED', 'TEXT', 'THAN', 'THEN', 'TIES', 'TIME', 'TIMESTAMP', 'TIMESTAMPADD', 'TIMESTAMPDIFF', 'TINYBLOB', 'TINYINT', 'TINYTEXT', 'TO', 'TRAILING', 'TRANSACTION', 'TRIGGER', 'TRIGGERS', 'TRUE', 'TRUNCATE', 'TYPE', 'TYPES', 'UNBOUNDED', 'UNCOMMITTED', 'UNDEFINED', 'UNDO', 'UNDOFILE', 'UNICODE', 'UNINSTALL', 'UNION', 'UNIQUE', 'UNKNOWN', 'UNLOCK', 'UNSIGNED', 'UNTIL', 'UPDATE', 'UPGRADE', 'USAGE', 'USE', 'USER', 'USING', 'VALIDATION', 'VALUES', 'VARBINARY', 'VARCHAR', 'VARCHARACTER', 'VARIABLES', 'VARYING', 'VCPU', 'VIEW', 'VIRTUAL', 'VISIBLE', 'WAIT', 'WARNINGS', 'WEEK', 'WHEN', 'WHERE', 'WHILE', 'WINDOW', 'WITH', 'WITHOUT', 'WORK', 'WRAPPER', 'WRITE', 'XA', 'XID', 'XML', 'XOR', 'YEAR', 'ZEROFILL']

token = ['HEX', 'DEC', 'INT', 'IPADDR', 'CHR', 'STR', 'NEQ', 'AND', 'OR', 'CMTST', 'CMEND', 'TLDE', 'EXCLM', 'ATR', 'HASH', 'DLLR', 'PRCNT', 'XOR', 'BITAND', 'BITOR', 'STAR', 'MINUS', 'PLUS', 'EQ', 'LPRN', 'RPRN', 'LCBR', 'RCBR', 'LSQBR', 'RSQBR', 'BSLSH', 'CLN', 'SMCLN', 'DQUT', 'SQUT', 'LT', 'GT', 'CMMA', 'DOT', 'QSTN', 'SLSH', 'DSCMT']

# https://codereview.stackexchange.com/questions/180567/checking-for-balanced-brackets-in-python with modification
def convert_orphan_parentheses(expression):
    opening = tuple('(')
    closing = tuple(')')
    mapping = dict(zip(opening, closing))
    queue = []
    expression = list(expression)
    for i, letter in enumerate(expression):
        if letter in opening:
            queue.append({'c': mapping[letter], 'idx': i})
        elif letter in closing:
            if not queue or letter != queue.pop()['c']:
                if letter is ')':
                    expression[i] = ' RPRN '
                elif letter is '(':
                    expression[i] = ' LPRN '
    
    for x in queue:
        if x['c'] is '(':
            expression[x['idx']] = ' RPRN '
        elif x['c'] is ')':
            expression[x['idx']] = ' LPRN '

    return ''.join(expression)

def tokenize(payload):
    # unquoted = urllib.unquote(payload)
    unquoted = urllib.parse.parse_qs(payload.decode('unicode_escape')) # .decode('unicode_escape'))
    # generalize/normalize query by converting into meaningful token (based on query normalization scheme - SqliGoT (1))
    for key, value in unquoted.items():
        # loop over similar query param names (e.g name=ando&name=kevin)
        for q in value:
                extractor = FeatureExtractor(q)
                # q = q.decode("utf-8")
                # split query structure by empty comment occurences
                q = q.split('/**/')
                for nq in q:
                        # nq = "-3022'))) OR (SELECT (CASE WHEN (7359=7359) THEN NULL ELSE CAST((CHR(120)||CHR(104)||CHR(111)||CHR(82)) AS NUMERIC) END)) IS NULL AND ((('"
                        # nq = '-2932") UNION ALL SELECT 1099,1099,1099,1099,1099,1099,1099-- -----CRDk'
                        raw = nq

                        # step 2.d from (1)
                        nq = re.sub(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', 'IPADDR', nq)
                        # step 1 from (1)
                        nq = re.sub(r'[\r\n\t]', ' Space ', nq)
                        # step 2.b from (1)
                        nq = re.sub(r'\b\d*\.\d+\b', ' DEC ', nq)
                        # step 2.c from (1)
                        nq = re.sub(r'\b[0-9]+\b', ' INT ', nq)
                        # step 2.a from (1)
                        nq = re.sub(r'\b0x[0-9A-Fa-f]+\b', ' HEX ', nq)
                        # step 2.e from (1)
                        nq = re.sub(r'\'[a-zA-Z]\'', ' CHR ', nq)

                        # step 2.f from (1) need improvement
                        # nq = re.sub(r'(?<=")[a-zA-Z]+(?=")', ' STR ', nq)

                        # step 9 from (1) convert query payload to uppercase
                        nq = nq.upper()
                        # tokenization of special characters
                        nq = re.sub(r'(!=|<>)', ' NEQ ', nq)
                        nq = nq.replace('&&', ' AND ')
                        nq = nq.replace('||', ' OR ')
                        nq = nq.replace('/*', ' CMTST ')
                        nq = nq.replace('*/', ' CMTEND ')
                        # added dash comment unspecified on (1)
                        nq = re.sub(r'-- (.*?)', ' DSCMT ', nq)
                        nq = nq.replace('~', ' TLDE ')
                        nq = nq.replace('!', ' EXCLM ')
                        nq = nq.replace('@', ' ATR ')
                        nq = nq.replace('#', ' HASH ')
                        nq = nq.replace('$', ' DLLR ')
                        nq = nq.replace('%', ' PRCNT ')
                        nq = nq.replace('^', ' XOR ')
                        nq = nq.replace('&', ' BITAND ')
                        nq = nq.replace('|', ' BITOR ')
                        nq = nq.replace('*', ' STAR ')
                        nq = nq.replace('-', ' MINUS ')
                        nq = nq.replace('+', ' PLUS ')
                        nq = nq.replace('=', ' EQ ')
                        nq = nq.replace('{', ' LCBR ')
                        nq = nq.replace('}', ' RCBR ')
                        nq = nq.replace('[', ' LSQBR ')
                        nq = nq.replace(']', ' RSQBR ')
                        
                        # nb_rep = 1
                        # while(nb_rep):
                        #         (nq, nb_rep) = re.subn(r'\([^()]*\)', '\1', nq)

                        nq = convert_orphan_parentheses(nq)

                        # https://stackoverflow.com/questions/39026120/how-can-i-remove-text-within-multi-layer-of-parentheses-python
                        nq = " ".join(re.split(r'(?:[()])', nq))

                        nq = nq.replace('\\', ' BSLSH ')
                        nq = nq.replace(':', ' CLN ')
                        nq = nq.replace(';', ' SMCLN ')
                        nq = nq.replace('"', ' DQUT ')
                        nq = nq.replace('\'', ' SQUT ')
                        nq = nq.replace('<', ' LT ')
                        nq = nq.replace('<', ' GT ')
                        nq = nq.replace(',', ' CMMA ')
                        nq = nq.replace('.', ' DOT ')
                        nq = nq.replace('?', ' QSTN ')
                        nq = nq.replace('/', ' SLSH ')
                        nq = nq.replace('/', ' SLSH ')
                        nq = nq.replace('`', ' BTCK ')

                        nq = nq.split()

                        for i, nd in enumerate(nq):
                            if nd not in reserved and nd not in token:
                                nq[i] = ' STR '

                        nq = ' '.join(nq)
                    
                        # step 10 from (1) multiple spaces into single space
                        nq = ' '.join(nq.split())

                        # print(nq) # tokenized payload
                        cent = graph_of_tokens(nq, 5, "proportional", "directed")
                        # print(cent) # centrality of payload

                        # collect data for model training
                        sample = {
                            'payload': raw,
                            'payload_length': len(raw),
                            'token': nq,
                            'centrality': cent,
                        }

                        yield sample
                    
# wd_size: window size
# w_mode: weight mode (uniform | proportional)
# g_type: graph type (undirected | directed)
def graph_of_tokens(payload, wd_size, w_mode, g_type):
    tokens = payload.split(" ")
    t_length = len(tokens)
    vertices = sorted(set(tokens))
    # print(vertices)
    A = numpy.zeros((t_length, t_length))
    for i in range(t_length):
        if i + wd_size <= t_length:
            p = i + wd_size
        else:
            p = t_length
        for j in range(i + 1, p):
            if w_mode is 'proportional':
                A[i, j] = A[i, j] + i + wd_size - j
            else:
                A[i,j] = A[i, j] + 1
            if g_type is 'undirected':
                A[j,i] = A[i,j]
    # print(A)
    cent = measure_centrality(A, g_type)
    return cent

# 4.3.5. Centrality measure - Page 16, SQLiGoT
def measure_centrality(A, g_type):
    # which one is better? between: 
    # 1. using module from python networkx
    # https://networkx.github.io/documentation/latest/reference/generated/networkx.convert_matrix.from_numpy_array.html
    G = nx.from_numpy_array(A)
    degree_centrality = nx.degree_centrality(G)
    return degree_centrality
    # 2. self recode from SQLiGoT paper
    # if g_type is 'directed':
    #     # Since self loops are allowed in graph of tokens, weight of the loop needs to be added twice while computing degree centrality.
    #     deg_cent = numpy.zeros(numpy.shape(A))
    #     for i in range(len(A)):
    #         for j in range(len(A[i])):
    #             deg_cent[i,i] = A[i,i] + A[i,j]
    #     # print(deg_cent)
    # else:
    #     deg_cent = numpy.zeros(numpy.shape(A))
    #     curr_row = 0
    #     curr_col = 0
    #     for i in range(len(A)):
    #         curr_row = i
    #         for j in range(len(A)):
    #             curr_col = j
    #             print("Outdegree", "A[{},{}]".format(curr_row, curr_col))
    #         print("Indegree", "A[{},{}]".format(curr_row, curr_col))
