from datetime import datetime 


def create_date_query(dateFrom=None, dateTo=None):
    query = {}
    print(dateFrom)
    if dateFrom or dateTo:
        query['Date'] = {}
        if dateFrom:
            query['Date']['$gte'] = datetime.fromisoformat(dateFrom)

        if dateTo:
            query['Date']['$lte'] = datetime.fromisoformat(dateTo)

    return query