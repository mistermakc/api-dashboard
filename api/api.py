from flask import Flask, jsonify
from sqlalchemy import create_engine
from flask_restx import Api, Namespace, Resource

user = "root"
passw = "Pandas2020!"
host = "34.132.33.93"
database = "database"

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = host

api = Api(app, version = '1.0',
    title = 'Capstone API',
    description = """
        Used to communicate between mySQL database and streamlit
        """,
    contact = "max.heilingbrunner@student.ie.edu",
    endpoint = "/api/v1"
)

customers = Namespace('customers',
    description = 'All operations related to customers',
    path='/api/v1')
api.add_namespace(customers)

transactions = Namespace('transactions',
    description = 'All operations related to transactions',
    path='/api/v1')
api.add_namespace(transactions)

def connect():
    db = create_engine(
    'mysql+pymysql://{0}:{1}@{2}/{3}' \
        .format(user, passw, host, database), \
    connect_args = {'connect_timeout': 10})
    conn = db.connect()
    return conn

def disconnect(conn):
    conn.close()

@customers.route("/customers")
class get_all_users(Resource):

    def get(self):
        conn = connect()
        select = """
            SELECT *
            FROM customers
            LIMIT 10;"""
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})

@customers.route("/customers/<string:id>")
@customers.doc(params = {'id': 'The ID of the user'})
class select_user(Resource):

    @api.response(404, "CUSTOMER not found")
    def get(self, id):
        id = str(id)
        conn = connect()
        select = """
            SELECT *
            FROM customers
            WHERE customer_id = '{0}';""".format(id)

        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})
    
@transactions.route("/transactions")
class get_all_transactions(Resource):

    def get(self):
        conn = connect()
        select = """
            SELECT *
            FROM transactions
            LIMIT 10;"""
        result = conn.execute(select).fetchall()
        disconnect(conn)
        return jsonify({'result': [dict(row) for row in result]})

if __name__ == '__main__':
    app.run(debug = True)