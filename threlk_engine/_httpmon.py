def parse(hits):
    for hit in hits:
        package = {}
        try:
            data_source = hit['_source']
            event_data = {
                "elastic_id": hit['_id'],
            }
            event_data = {**package, **data_source['result']}
            package = {
                "EVENT_DATA": event_data,
                "EVENT_TYPE": "HTTP_MONITOR"
            }
        except Exception as e:
            pass
        yield package