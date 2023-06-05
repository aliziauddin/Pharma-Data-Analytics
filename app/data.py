import statistics
import time
import pandas as pd
from file_helper import remove_file
from data_helper import create_date_query
from datetime import datetime, timedelta

def insertBulk(db, file_path, logger):
    logger.info("insertBulk - start execution")
    start_time = time.time()

    df = pd.read_csv(file_path)
    df = df.fillna("")
    df['Date'] = pd.to_datetime(df['Date'])
    logger.info("Adding data in bulk")
    data_dict = df.to_dict("records")
    db.sales.insert_many(data_dict)
    logger.success("Successfully added")
    remove_file(file_path)

    end_time = time.time()  
    elapsed_time = end_time - start_time  
    logger.info(f"insertBulk - end execution (Elapsed Time: {elapsed_time:.2f} seconds)")

    return True

def get_total_docs(db,dateFrom=None, dateTo=None, logger=None):
    logger.info("get_total_docs - start execution")
    start_time = time.time()

    query = create_date_query(dateFrom, dateTo)
    total_count = db.sales.count_documents(query)

    end_time = time.time()  
    elapsed_time = end_time - start_time  
    logger.info(f"get_total_docs - end execution (Elapsed Time: {elapsed_time:.2f} seconds)")
    return {"count": total_count}

def get_gmv(db,dateFrom=None, dateTo=None, logger=None):
    logger.info("get_gmv - start execution")
    start_time = time.time()

    query = create_date_query(dateFrom, dateTo)
    pipeline = []
    if dateFrom or dateTo:
        pipeline.append({"$match": query})
    pipeline.append(
        {"$group": {"_id": None, "total_gmv": {"$sum": "$GMV"}}}
    )  
    result = list(db.sales.aggregate(pipeline))

    if result:
        total_gmv = result[0]['total_gmv']
        res = {"total_gmv": total_gmv}
    else:
        res = {"total_gmv": 0}

    end_time = time.time()  
    elapsed_time = end_time - start_time  
    logger.info(f"get_gmv - end execution (Elapsed Time: {elapsed_time:.2f} seconds)")

    return res

def get_order_count(db,dateFrom=None, dateTo=None,logger=None):
    logger.info("get_order_count - start execution")
    start_time = time.time()

    query = create_date_query(dateFrom, dateTo)
    order_count = len(db.sales.distinct("Order_ID", query))

    end_time = time.time()  
    elapsed_time = end_time - start_time  
    logger.info(f"get_order_count - end execution (Elapsed Time: {elapsed_time:.2f} seconds)")

    return {"order_count": order_count}

def get_median_sales(db,dateFrom=None, dateTo=None,logger=None):
    logger.info("get_median_sales - start execution")
    start_time = time.time()

    query = create_date_query(dateFrom, dateTo)
    pipeline = []
    if dateFrom or dateTo:
        pipeline.append({"$match": query})
    pipeline.append(
        {"$group": {"_id": "$Order_ID", "sales": {"$push": "$GMV"}}}
    )
    pipeline.append(
        {"$project": {"median_sales": {"$toDouble": {"$sum": "$sales"}}}}
    )
    result = list(db.sales.aggregate(pipeline))
    median_sales = [doc['median_sales'] for doc in result]
    overall_median = statistics.median(median_sales)

    end_time = time.time()  
    elapsed_time = end_time - start_time  
    logger.info(f"get_median_sales - end execution (Elapsed Time: {elapsed_time:.2f} seconds)")

    return {"median_sales": overall_median}

def get_user_retention(db,dateFrom=None, dateTo=None, logger=None):
    logger.info("get_user_retention - start execution")
    start_time = time.time()

    date_from = datetime.fromisoformat(dateFrom)
    date_to = datetime.fromisoformat(dateTo)
    previous_month_from = date_from - timedelta(days=31) 
    previous_month_to = previous_month_from + timedelta(days=31)  
   
    pipeline = [
        {"$match": {"Date": {"$gte": previous_month_from, "$lte": previous_month_to}}},
        {"$group": {"_id": "$User_ID"}},
        {"$group": {"_id": None, "previous_month_users": {"$push": "$_id"}}},
        {"$lookup": {
            "from": "sales",
            "let": {"previous_month_users": "$previous_month_users"},
            "pipeline": [
                {"$match": {"Date": {"$gte": date_from, "$lte": date_to}}},
                {"$match": {"$expr": {"$in": ["$User_ID", "$$previous_month_users"]}}},
                {"$group": {"_id": "$User_ID"}}
            ],
            "as": "current_month_users"
        }},
        {"$project": {
            "previous_month_count": {"$size": "$previous_month_users"},
            "current_month_count": {"$size": "$current_month_users"}
        }},
        {"$project": {
            "retention_percentage": {
                "$multiply": [
                    {"$divide": ["$current_month_count", "$previous_month_count"]},
                    100
                ]
            }
        }}
    ]
    result = list(db.sales.aggregate(pipeline))
    retention_percentage = result[0]['retention_percentage']

    end_time = time.time()  
    elapsed_time = end_time - start_time  
    logger.info(f"get_user_retention - end execution (Elapsed Time: {elapsed_time:.2f} seconds)")

    return {"user_retention_percent":retention_percentage}


def get_avg_order_value(db,dateFrom=None, dateTo=None,logger=None):
    logger.info("get_avg_order_value - start execution")
    start_time = time.time()
    query = create_date_query(dateFrom, dateTo)
    pipeline = []
    if dateFrom or dateTo:
        pipeline.append({"$match": query})
    pipeline.append( {"$group": {
            "_id": "$Order_ID",
            "total_gmv": {"$sum": "$GMV"},
            "count": {"$sum": 1}
        }})
    pipeline.append  ( 
        {"$group": {
            "_id": None,
            "total_gmv": {"$sum": "$total_gmv"},
            "distinct_sales_count": {"$sum": 1}
        }})
    

    result = list(db.sales.aggregate(pipeline))
    end_time = time.time()  
    elapsed_time = end_time - start_time  
    logger.info(f"get_avg_order_value - end execution (Elapsed Time: {elapsed_time:.2f} seconds)")

    if result:
        total_gmv = result[0]['total_gmv']
        distinct_sales_count = result[0]['distinct_sales_count']
        if distinct_sales_count > 0:
            return {"avg_order_sales":  total_gmv / distinct_sales_count } 
        
    return {"avg_order_sales":0}

def get_products_with_count(db,dateFrom=None, dateTo=None,logger=None):
    logger.info("get_products_with_count - start execution")
    start_time = time.time()
    query = create_date_query(dateFrom, dateTo)
    pipeline = []
    if dateFrom or dateTo:
        pipeline.append({"$match": query})
    pipeline += [
        {"$group": {
            "_id": "$Product",
            "count": {"$sum": 1}
        }},
        {"$project": {
        "_id": 0,
        "Product": "$_id",
        "Count": "$count"
    }},
     {"$sort": {"Count": -1}}
    ]
    result = list(db.sales.aggregate(pipeline))

    end_time = time.time()  
    elapsed_time = end_time - start_time  
    logger.info(f"get_products_with_count - end execution (Elapsed Time: {elapsed_time:.2f} seconds)")

    return result[:10]

def get_orders(db,dateFrom=None, dateTo=None, logger=None):
    logger.info("get_orders - start execution")
    start_time = time.time()
    query = create_date_query(dateFrom, dateTo) 
    pipeline = []
    if dateFrom or dateTo:
        pipeline.append({"$match": query})
    pipeline += [
        {
            "$group": {
                "_id": "$Order_ID",
                "GMV": {"$sum": "$GMV"},

            }
        },
        {
            "$project": {
                "_id": 0,
                "Order_ID": "$_id",
                "GMV": 1,

            }
        },
         {"$sort": {"GMV": -1}}
    ]
    result = list(db.sales.aggregate(pipeline))

    end_time = time.time()  
    elapsed_time = end_time - start_time  
    logger.info(f"get_orders - end execution (Elapsed Time: {elapsed_time:.2f} seconds)")

    return result[:10]

def get_orders_by_month(db, logger=None):
    logger.info("get_orders_by_month - start execution")
    start_time = time.time()
    pipeline = [
        {
            "$group": {
                "_id": {
                    "$dateToString": {
                        "format": "%Y-%m",
                        "date": "$Date"
                    }
                },
                "count": {"$sum": 1}
            }
        },
        {
        "$project": {
            "_id": 0,  
            "Month": "$_id",  
            "Count": "$count"  
            }
        },
        {
            "$sort": {"Month": 1}
        }
    ]

    result = list(db.sales.aggregate(pipeline))

    end_time = time.time()  
    elapsed_time = end_time - start_time  
    
    logger.info(f"get_orders_by_month - end execution (Elapsed Time: {elapsed_time:.2f} seconds)")

    return result

def get_top_selling_products(db,dateFrom=None, dateTo=None,logger=None):
    logger.info("get_top_selling_products - start execution")
    start_time = time.time()

    query = create_date_query(dateFrom, dateTo) 
    pipeline = []
    if dateFrom or dateTo:
        pipeline.append({"$match": query})
    pipeline += [
        {
            "$group": {
                "_id": "$Product", 
                "totalSales": { "$sum": "$GMV" }, 
                "averageSales": { "$avg": "$GMV" }, 
                "orderCount": { "$sum": 1 }
                }
        },
        {
            "$sort": { "totalSales": -1 } 
        }
    ]

    results= list(db.sales.aggregate(pipeline))
    end_time = time.time()  
    elapsed_time = end_time - start_time  
    
    logger.info(f"get_top_selling_products - end execution (Elapsed Time: {elapsed_time:.2f} seconds)")
    

    return results[:10]