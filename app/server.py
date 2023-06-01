import os
import threading
from flask import Flask,  request, session
from logger import myLogger
from flask_pymongo import PyMongo
from file_helper import save_file
from flask_cors import CORS
from data import insertBulk, get_gmv,get_order_count, get_median_sales, get_user_retention,get_avg_order_value,get_total_docs,get_products_with_count, get_orders,get_orders_by_month, get_top_selling_products

LOGGER = myLogger()


UPLOAD_FOLDER = './tmp'
ABS_UPLOAD_FOLDER_PATH = os.path.abspath(UPLOAD_FOLDER)
ALLOWED_EXTENSIONS = set(['xlsx', 'xlsb'])

app = Flask(__name__)
cors = CORS(app, resources={r"/": {"origins": "*"}})
app.config['SECRET_KEY'] = "!5CP7k0Dw9RhJ#XzL@!b"
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['UPLOAD_FOLDER'] = ABS_UPLOAD_FOLDER_PATH
app.config["MONGO_URI"] = "mongodb://app-mongo-1:27017/pharma"
# app.config["MONGO_URI"] = "mongodb://localhost:27017/pharma"
app.config['SESSION_TYPE'] = 'filesystem'

CORS(app, expose_headers='Authorization')

mongo = PyMongo(app)

try:
    mongo.db.command('ping')
    print("🚀 Connected to MongoDB!")
except:
    print("😞 Could not connect to MongoDB.")

@app.route("/", methods=['GET', 'POST'])
def test():
    return "Server is up and running 🚀..."

@app.route("/ping", methods=['GET', 'POST'])
def ping():
    return "Server is up and running 🚀..."


@app.route("/db-status", methods=['GET', 'POST'])
def dbStatus():
    return mongo.db.command('ping')


################################### DATA ###################################


@app.route('/upload', methods=['POST'])
def fileUpload():
    try:
        files = request.files

        file_path = save_file(files, 'file1',
                              ABS_UPLOAD_FOLDER_PATH)
  
        LOGGER.success(
            "Uploading done. Processing started..")
        LOGGER.info("thread created.")
        thread = threading.Thread(target=insertBulk, kwargs={
            'db': mongo.db, 
            "file_path": file_path,
            "logger": LOGGER
        })
        thread.start()

        response = "Uploading done. Processing started. It will take few minutes."
        return response
    except Exception as e:
        print(e)
        LOGGER.error(e)





################################### DASHBOARD ###################################
@app.route('/totaldocs', methods=['GET'])
def total_docs():
    return get_total_docs(db=mongo.db)

@app.route('/gmv', methods=['GET'])
def gmv():
    args = request.args
    dateFrom = args.get("dateFrom", default=None, type=str)
    dateTo = args.get("dateTo", default=None, type=str)
    return get_gmv(db=mongo.db, dateFrom=dateFrom, dateTo=dateTo)
   

@app.route('/ordercount', methods=['GET'])
def order_count():
    args = request.args
    dateFrom = args.get("dateFrom", default=None, type=str)
    dateTo = args.get("dateTo", default=None, type=str)

    return get_order_count(db=mongo.db, dateFrom=dateFrom, dateTo=dateTo)

@app.route('/mediansales', methods=['GET'])
def median_sales():
    args = request.args
    dateFrom = args.get("dateFrom", default=None, type=str)
    dateTo = args.get("dateTo", default=None, type=str)

    return get_median_sales(db=mongo.db, dateFrom=dateFrom, dateTo=dateTo)


@app.route('/userretention', methods=['GET'])
def user_retention():
    args = request.args
    dateFrom = args.get("dateFrom", default=None, type=str)
    dateTo = args.get("dateTo", default=None, type=str)

    return get_user_retention(db=mongo.db, dateFrom=dateFrom, dateTo=dateTo)

@app.route('/avgordervalues', methods=['GET'])
def avg_order_values():
    args = request.args
    dateFrom = args.get("dateFrom", default=None, type=str)
    dateTo = args.get("dateTo", default=None, type=str)

    return get_avg_order_value(db=mongo.db, dateFrom=dateFrom, dateTo=dateTo)

@app.route('/productswithcount', methods=['GET'])
def products_with_count():
    args = request.args
    dateFrom = args.get("dateFrom", default=None, type=str)
    dateTo = args.get("dateTo", default=None, type=str)

    return get_products_with_count(db=mongo.db, dateFrom=dateFrom, dateTo=dateTo)

@app.route('/orders', methods=['GET'])
def orders():
    args = request.args
    dateFrom = args.get("dateFrom", default=None, type=str)
    dateTo = args.get("dateTo", default=None, type=str)

    return get_orders(db=mongo.db, dateFrom=dateFrom, dateTo=dateTo)

@app.route('/orders-by-month', methods=['GET'])
def orders_by_month():
    return get_orders_by_month(db=mongo.db)

@app.route('/top-selling-products', methods=['GET'])
def top_selling_products():
    args = request.args
    dateFrom = args.get("dateFrom", default=None, type=str)
    dateTo = args.get("dateTo", default=None, type=str)

    return get_top_selling_products(db=mongo.db, dateFrom=dateFrom, dateTo=dateTo)
    

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000, use_reloader=True)