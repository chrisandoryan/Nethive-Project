# import csv
# import numpy as np
# import pandas as pd
# from fuzzywuzzy import process
# from fuzzywuzzy import fuzz
# import sqlparse
# import re

# # https://www.shanelynn.ie/summarising-aggregation-and-grouping-data-in-python-pandas/

# HTTP_LOG_FILE = "./data_temp/GET_http.csv"
# SQL_LOG_FILE = "./data_temp/LOG_mysql.csv"
# AGGREGATED_LOG_FILE = "./data_temp/AGG.csv"

# JOIN_HELPER = 1

# hlog = open(HTTP_LOG_FILE, 'r')
# hlog_reader = pd.read_csv(HTTP_LOG_FILE) # csv.DictReader(hlog) # csv.reader(hlog, delimiter=',')
# hlog_reader['payload'] = hlog_reader['payload'].astype(str) 
# hlog_reader.drop_duplicates(subset=["payload"], inplace=True)


# slog = open(SQL_LOG_FILE, 'r')
# slog_reader = pd.read_csv(SQL_LOG_FILE) # csv.DictReader(slog) # csv.reader(slog, delimiter=',')
# slog_reader['query'] = slog_reader['query'].astype(str) 
# slog_reader.drop_duplicates(subset=["query"], inplace=True)


# # print(hlog_reader.head())

# # hlog_grouptimestamp = hlog_reader.groupby(['timestamp'])

# hlog_grouptimestamp = hlog_reader.groupby(['timestamp'])
# # print(hlog_grouptimestamp.head())

# # print(hlog_grouptimestamp['payload'].head())

# slog_grouptimestamp = slog_reader.groupby(['timestamp'])
# # print(slog_grouptimestamp['query'].head())

# print("Combining...")

# # result = pd.concat([g[1].merge(categories, how='outer', on='ts') for g in [hlog_grouptimestamp, slog_grouptimestamp]])
# # hlog_grouptimestamp.apply(Output=[process.extract(i, hlog_reader['payload'], limit=3) for i in slog_reader['query']])
# # slog_grouptimestamp = {}

# # print([i for i in slog_grouptimestamp.get_group(key) for key, item in slog_grouptimestamp)
# # for row in slog_grouptimestamp.itertuples():
# #     print((row.Index, row.query, row.query))

# # result = pd.concat([hlog_grouptimestamp, slog_grouptimestamp], axis=1)
# # print(result)
# def get_sql_where_value(token):
#     # only work for single WHERE value comparison rn
#     return re.search(r"'.*'", token).group()

# def get_sql_where_token(tokens):
#     for t in tokens:
#         if type(t) is sqlparse.sql.Where:
#             return t

# def get_loose_timestamp_data(r, df):
#     loose_timestamp = []
#     for i in list(range(-r, r + 1)):
#         timestamp = df['timestamp'] + i

#         slog = slog_grouptimestamp.get_group(timestamp) if timestamp in slog_grouptimestamp.groups else pd.DataFrame()

#         subts = [(timestamp, skey, srow['query']) for skey, srow in slog.iterrows() if df['payload'] in srow['query']]

#         loose_timestamp = list(set(loose_timestamp) | set(subts))

#     return loose_timestamp

# def get_similar(df):
#     # print(df.head())
#     # return
#     # print([srow['query'] for (skey, srow) in slog_grouptimestamp])
#     # for skey, srow in slog_grouptimestamp.get_group(df['timestamp']).iterrows():
#     #     print(srow['query'])
#     # print([srow['query'] for skey, srow in slog_grouptimestamp.get_group(df['timestamp']).iterrows()] if df['timestamp'] in slog_grouptimestamp.groups else (0, 0))
#     # res = process.extractOne(df['payload'], [i for (skey, srow) in slog_grouptimestamp for i in srow['query']])
#     # result = process.extractOne(df['payload'], {idx: el for idx, el in enumerate([srow['query'] for skey, srow in slog_grouptimestamp.get_group(df['timestamp']).iterrows()] if df['timestamp'] in slog_grouptimestamp.groups else [])}) 
#     # print(result) #score_cutoff=90)
#     loose_timestamp = get_loose_timestamp_data(3, df)
#     # print(len(loose_timestamp))

#     for ts, idx, q in loose_timestamp:
#         # print("'%s'" % df['payload'])
#         query = q
#         query = sqlparse.parse(query)
#         # print(type(query[0].tokens[-1]) is sqlparse.sql.Where)
#         query = get_sql_where_value(str(get_sql_where_token(query[0].tokens)))
#         # print(query)
#         reformatted = "'%s'" % df['payload']
#         if reformatted == query:
#             # print(df['payload'])
#             # print("Tuple: ",)
#             # print((ts, idx, qry))
#             # print(slog_grouptimestamp.get_group(ts).to_string())
#             # https://stackoverflow.com/questions/47665812/index-out-of-bound-when-iterrow-how-is-this-possible
#             sdata = slog_grouptimestamp.get_group(ts).loc[idx,:] if ts in slog_grouptimestamp.groups else None
#             sdata['jh'] = JOIN_HELPER
#             df['jh'] = JOIN_HELPER
#             # print("Query in sdata: ",)
#             # print(sdata['timestamp'], sdata['query'])
#             # combined = pd.concat([df, sdata], axis=1, sort=False, ignore_index=True)
#             # print(combined)
#             sdata = pd.DataFrame(sdata).transpose()
#             df = pd.DataFrame(df).transpose()
#             joined = pd.merge(left=df, right=sdata, how='outer', on='jh')
#             joined.drop(['jh'], axis=1, inplace=True)
#             # print(joined.to_string())
#             # input()
#             with open(AGGREGATED_LOG_FILE, 'a') as f:
#                 joined.to_csv(f, encoding='utf-8', index=False, header=f.tell()==0)

#         else:
#             print("NOT MATCHED")
#             print("'%s'" % df['payload'])
#             print("'%s'" % query)
#             # input()
#     #print([df['payload'] in query for query in loose_timestamp])

#     # if result is not None:
#     #     query, score, index = result
#     #     sdata = slog_grouptimestamp.get_group(df['timestamp']).iloc[index,:] if df['timestamp'] in slog_grouptimestamp.groups else None
#     #     df = pd.DataFrame(df).transpose()
#     #     sdata = pd.DataFrame(sdata).transpose()
#     #     print(df)
#     #     print(sdata)
#     #     # df.reset_index(drop=True, inplace=True)
#     #     # sdata.reset_index(drop=True, inplace=True)
#     #     # l1 = df.values.tolist()
#     #     # l2 = sdata.values.tolist()
#     #     # for i in range(len(l1)):
#     #     #     l1[i].extend(l2[i])
#     #     # done = pd.DataFrame(l1, columns=df.columns.tolist() + sdata.columns.tolist())
#     #     # print(done)
#     #     # combined = pd.concat([df, sdata], axis=1, sort=False, ignore_index=True)
#     #     # print(sdata.to_frame())
#     #     # joined = pd.merge(left=df, right=sdata, how='outer', on='timestamp')
#     #     # with open(AGGREGATED_LOG_FILE, 'a') as f:
#     #     #     joined.to_csv(f, encoding='utf-8', index=False, header=f.tell()==0)
#     #     # print(df.to_frame()[:,-1])
#     #     # test = pd.merge(df.to_frame(), sdata.to_frame())
#     #     # print(test)
#     #     # print(df.to_frame().join(sdata))
#     # # return res
#     # else:
#     #     print("Not correlated")

# for hkey, hrow in hlog_grouptimestamp:
#     # print(hrow)
#     # input()
#     hrow.apply(get_similar, axis=1)
#     # hrow['correlate'] = process.extractOne(hrow['payload'], [srow['query'] for skey, srow in slog_grouptimestamp.get_group(hrow['timestamp']).iterrows()] if hrow['timestamp'] in slog_grouptimestamp.groups else [])
# #     for row in hrow['payload']:
# #         print(row)
# #         # hrow['correlate'] = process.extractOne(row, [srow['query'] for skey, srow in slog_grouptimestamp.get_group(hrow['timestamp']).iterrows()] if hrow['timestamp'] in slog_grouptimestamp.groups else [])
# # #     # hrow.apply(Output=[process.extract(payload, [], limit=1) for (key, payload) in hrow['payload'].iteritems()])
# #         input()

# # for row in hlog_reader:
# #     if row['timestamp'] not in hlog_grouptimestamp:
# #         hlog_grouptimestamp[row['timestamp']] = []
# #     hlog_grouptimestamp[row['timestamp']].append(row)

# # for row in slog_reader:
# #     if row['timestamp'] not in slog_grouptimestamp:
# #         slog_grouptimestamp[row['timestamp']] = []
# #     slog_grouptimestamp[row['timestamp']].append(row)

# # keys = list(hlog_grouptimestamp.keys() | slog_grouptimestamp.keys())

# print("Done :)")

# # for k in keys:
# #     print(len(hlog_grouptimestamp[k]))
# #     input()
# #     print(len(slog_grouptimestamp[k]))
# #     input()
# # np.corrcoef(
# #     [hlog_grouptimestamp.get(x, 0) for x in keys],
# #     [slog_grouptimestamp.get(x, 0) for x in keys])[0, 1]

# # for c in correlated:
# #     df = pd.DataFrame(c)
# #     corr = df.corr()
# #     print(corr)
# # df = pd.DataFrame(correlated)
# # corr = df.corr()
# # print(corr)

# # for row in slog_reader:
# #     correlated[row['timestamp']]