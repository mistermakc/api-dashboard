#%%

import os
import sqlalchemy
SQLALCHEMY_SILENCE_UBER_WARNING = 1
import pandas as pd

#%%

def connect_tcp_socket() -> sqlalchemy.engine.base.Engine:
    """ Initializes a TCP connection pool for a Cloud SQL instance of MySQL. """
    db_host = "34.132.33.93" # e.g. '34.132.33.93' ('172.17.0.1' if deployed to GAE Flex)
    db_user = "root" # e.g. 'my-db-user'
    db_pass = "Pandas2020!" # e.g. 'my-db-password'
    db_name = "database" # e.g. 'my-database'
    db_port = 3306 # e.g. 3306

    engine = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL.create(
            drivername="mysql+pymysql",
            username=db_user,
            password=db_pass,
            host=db_host,
            port=db_port,
            database=db_name,
        ),
    )
    return engine

#%%
engine = connect_tcp_socket() 
conn = engine.connect()

#%%
result = conn.execute("SHOW TABLES;").fetchall()
for r in result:
    print(r)