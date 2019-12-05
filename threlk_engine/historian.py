def parse(hits):
    for hit in hits:
        data = hit['_source']
        package = {
            "command": data['command'],
            "workdir": data['cwd'],
            "hostname": data['host']['name'],
            "exectime": data['log_time'],
            "executor": data['user'],
            "type": data['log_type'],
            "source": data['log']['file']['path']
        }
        yield package