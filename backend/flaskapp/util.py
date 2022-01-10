
def recordToJson(list):
    payload = []
    for record in list:
        d = {}
        for column in record.__table__.columns:
            d[column.name] = str(getattr(record, column.name))
        payload.append(d)

    return payload

def recordToJson2(record):
    d = {}
    for column in record.__table__.columns:
        d[column.name] = str(getattr(record, column.name))

    return d

NOT_DELETED = 0
DELETED = 1
NOT_EXPIRED = 0
EXPIRED = 1