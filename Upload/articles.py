#%%

import os
import sqlalchemy
SQLALCHEMY_SILENCE_UBER_WARNING = 1
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#%%
def load_csv_from_drive(drive_url):
    url='https://drive.google.com/uc?id=' + drive_url.split('/')[-2]
    articles = pd.read_csv(url)
    return articles
#%%
drive_url = 'https://drive.google.com/file/d/1jMwJOvIKZax47YHTn9wJu683uHAiqtes/view?usp=share_link'
articles = load_csv_from_drive(drive_url)

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

#%%
articles.info()

#%%
articles.head()

#%%
articles.select_dtypes(include=['int64']).columns

#%%
articles.select_dtypes(include=['float64']).columns

#%%
articles.select_dtypes(include=['object']).columns

#%%
# Printing the amount of features available in total
count_numerical = len(articles.select_dtypes(include=['int64','float64']).columns)
count_categorical = len(articles.select_dtypes(include=['object']).columns)
count_total = count_categorical + count_numerical
print('Total Features: ', count_categorical, 'categorical', '+',
      count_numerical, 'numerical', '=', count_total, 'features')

#%%
# Detecting the number of missing or null values per variable
pd.concat([articles.isnull().sum(),articles.isna().sum(min_count=1)],keys=['Nulls','Empty'],axis=1).sort_values(by='Nulls', ascending=False)[:20]

#%%
# Uploading data to database
articles.to_sql(name = "articles", con = conn, if_exists = 'fail', index = False) # no index will be uploaded to database as False

#%%
result = conn.execute("SHOW TABLES;").fetchall()
for r in result:
    print(r) # 
