def parse(hits):
    for hit in hits:
        package = {}
        try:
            data_source = hit['_source']
            event_data = {
                "elastic_id": hit['_id'],
                "command": data_source['command'],
                "workdir": data_source['cwd'],
                "hostname": data_source['host']['name'],
                "exectime": data_source['log_time'],
                "executor": data_source['user'],
                "type": data_source['log_type'],
                "source": data_source['log']['file']['path']
            }
            package = {
                "EVENT_DATA": event_data,
                "EVENT_TYPE": "BASH_MONITOR"
            }
        except Exception as e:
            pass

        yield package