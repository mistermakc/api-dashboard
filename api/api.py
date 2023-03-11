# Importing required modules
from flask import Flask, jsonify, current_app, request
from sqlalchemy import create_engine
from flask_restx import Api, Namespace, Resource

# Defining login credentials for mysql database
user = "root"
passw = "Pandas2020!"
host = "34.132.33.93"
database = "database"

# Defining API key for authentication
api_key = "IEMCSBT23"

# Define decorator for checking API key
def require_api_key(func):
    def wrapper(*args, **kwargs):
        provided_key = request.headers.get('X-API-KEY')
        if provided_key == api_key:
            return func(*args, **kwargs)
        else:
            return {'message': 'Invalid API key'}, 401
    return wrapper


# Define section revenue for api user interface
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = host

# Creating the api V1
api = Api(app, version = '1.0',
    title = 'H&M API (Capstone)',
    description = """
        Used to communicate between mySQL database and streamlit
        """,
    contact = "max.heilingbrunner@student.ie.edu",
    endpoint = "/api/v1"
)

# Defining section revenue for api user interface
revenue = Namespace('Revenue',
    description = "Data about H&M's revenue",
    path='/api/v1')
api.add_namespace(revenue)

# Defining section marketing for api user interface
marketing = Namespace('Marketing',
    description = "Data about H&M's marketing",
    path='/api/v1')
api.add_namespace(marketing)

# Defining section resources for api user interface
resources = Namespace('Resources',
    description = "Data about H&M's resources",
    path='/api/v1')
api.add_namespace(resources)

# Defining section products for api user interface
products = Namespace('Products',
    description = "Data about H&M's products",
    path='/api/v1')
api.add_namespace(products)

# Defining function to connect to database and execute query
def connect(query):
    db = create_engine(
    'mysql+pymysql://{0}:{1}@{2}/{3}' \
        .format(user, passw, host, database), \
    connect_args = {'connect_timeout': 10})
    with current_app.app_context():
        with db.connect() as connection:
            results = connection.execute(query)
            # Defining path based on output: if empty, do not return results
            if results.returns_rows:
                output = [dict(row) for row in results]
                if output:
                    return jsonify(output)
                else: 
                    return ({"message": "No results found"})
            connection.close()

@revenue.route("/sales_growth")
class get_sg(Resource):
    @require_api_key
    def get(self):
        # Defining SQL query to get the data
        query = """
            SELECT *
            FROM kpi_sales_growth;
            """
        
        # Calling connect function to execute query and return JSON response
        sales_growth = connect(query)

        # Returning the result as a JSON object
        return sales_growth
    
@revenue.route("/average_order_value")
class get_aov(Resource):
    def get(self):
        # Defining SQL query to get the data
        query = """
            SELECT *
            FROM kpi_average_order_value;
            """
        
        # Calling connect function to execute query and return JSON response
        sales_growth = connect(query)

        # Returning the result as a JSON object
        return sales_growth
    
@marketing.route("/fashion_news_effectiveness")
class get_fne(Resource):
    def get(self):
        # Defining SQL query to get the data
        query = """
            SELECT *
            FROM kpi_fashion_news_effectiveness;
            """
        
        # Calling connect function to execute query and return JSON response
        sales_growth = connect(query)

        # Returning the result as a JSON object
        return sales_growth
    
@marketing.route("/fashion_news_frequency")
class get_fnf(Resource):
    def get(self):
        # Defining SQL query to get the data
        query = """
            SELECT *
            FROM kpi_fashion_news_frequency;
            """
        
        # Calling connect function to execute query and return JSON response
        sales_growth = connect(query)

        # Returning the result as a JSON object
        return sales_growth
    
@resources.route("/inventory_turnover")
class get_it(Resource):
    def get(self):
        # Defining SQL query to get the data
        query = """
            SELECT *
            FROM kpi_inventory_turnover;
            """
        
        # Calling connect function to execute query and return JSON response
        sales_growth = connect(query)

        # Returning the result as a JSON object
        return sales_growth
    
@resources.route("/customer_retentation_rate")
class get_crr(Resource):
    def get(self):
        # Defining SQL query to get the data
        query = """
            SELECT *
            FROM kpi_customer_retention;
            """
        
        # Calling connect function to execute query and return JSON response
        sales_growth = connect(query)

        # Returning the result as a JSON object
        return sales_growth
    
@products.route("/product_sales")
class get_ps(Resource):
    def get(self):
        # Defining SQL query to get the data
        query = """
            SELECT *
            FROM kpi_product_sales;
            """
        
        # Calling connect function to execute query and return JSON response
        sales_growth = connect(query)

        # Returning the result as a JSON object
        return sales_growth

if __name__ == '__main__':
    app.run(debug = True)