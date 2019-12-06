def parse(hits):
    for hit in hits:
        package = {}
        try:
            data = hit['_source']
            package = {
                "elastic_id": hit['_id'],
                "command": data['command'],
                "workdir": data['cwd'],
                "hostname": data['host']['name'],
                "exectime": data['log_time'],
                "executor": data['user'],
                "type": data['log_type'],
                "source": data['log']['file']['path']
            }
        except Exception as e:
            pass

        yield package