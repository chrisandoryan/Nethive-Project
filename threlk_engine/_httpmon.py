def parse(hits):
    for hit in hits:
        package = {}
        try:
            data = hit['_source']
            package = {
                "elastic_id": hit['_id'],
            }
            package = {**package, **data['result']}
        except Exception as e:
            pass
        yield package