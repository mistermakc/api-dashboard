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
    customers = pd.read_csv(url)
    print(url)
    return customers
#%%
drive_url = 'https://drive.google.com/file/d/1AEznJVubr_k9t_Z7oM69RjUmhXfSDXv_/view?usp=share_link'
customers = load_csv_from_drive(drive_url)

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
customers.info()

#%%
f, ax = plt.subplots(figsize=(10, 6))
sns.histplot(customers['age'], color='#4B2362')

#%%
customers.head()

#%%
customers.select_dtypes(include=['int64']).columns

#%%
customers.select_dtypes(include=['float64']).columns

#%%
customers.select_dtypes(include=['object']).columns

#%%
customers["club_member_status"].unique()

#%%
# Printing the amount of features available in total
count_numerical = len(customers.select_dtypes(include=['int64','float64']).columns)
count_categorical = len(customers.select_dtypes(include=['object']).columns)
count_total = count_categorical + count_numerical
print('Total Features: ', count_categorical, 'categorical', '+',
      count_numerical, 'numerical', '=', count_total, 'features')

#%%
# Detecting the number of missing or null values per variable
pd.concat([customers.isnull().sum(),customers.isna().sum(min_count=1)],keys=['Nulls','Empty'],axis=1).sort_values(by='Nulls', ascending=False)[:20]

#%%
# Encoding "Fashion News Frequency" variable
def encode_fashion(x):
    if x == 'NONE' or x == 'None':
        return 0
    if x == 'Regularly':
        return 1
    if x == 'Monthly':
        return 2
    if x == 'nan':
        return ""
    
customers['fashion_news_frequency'] = customers['fashion_news_frequency'].transform(encode_fashion)
customers

#%%
# Imputing missing values
customers["Active"] = customers["Active"].fillna(0)
customers["FN"] = customers["FN"].fillna(0)
customers["fashion_news_frequency"] = customers["fashion_news_frequency"].interpolate(method ='pad', limit_direction ='forward')
customers["club_member_status"] = customers["club_member_status"].fillna("INACTIVE")
customers["age"] = customers["age"].interpolate(method ='pad', limit_direction ='forward')

#%%
# Encoding "Club Member Status" variable
def encode_club(x):
    if x == 'INACTIVE':
        return 0
    if x == 'ACTIVE':
        return 1
    if x == 'LEFT CLUB':
        return 3
    if x == 'PRE-CREATE':
        return 4
    
customers['club_member_status'] = customers['club_member_status'].transform(encode_club)
customers

#%%
# Transforming "Active", "FN", "fashion_news_frequency", and "age" variable
customers['Active'] = customers['Active'].astype(int)
customers['FN'] = customers['FN'].astype(int)
customers['fashion_news_frequency'] = customers['fashion_news_frequency'].astype(int)
customers['age'] = customers['age'].astype(int)
customers['club_member_status'] = customers['club_member_status'].astype(int)

#%%
customers['fashion_news_frequency'].unique()

#%%
pd.concat([customers.isnull().sum(),customers.isna().sum(min_count=1)],keys=['Nulls','Empty'],axis=1).sort_values(by='Nulls', ascending=False)[:20]

#%%
# Decoding "Fashion News Frequency" variable
def decode_fashion(x):
    if x == 0:
        return 'NONE'
    if x == 1:
        return 'Regularly'
    if x == 2:
        return 'Monthly'
    
customers['fashion_news_frequency'] = customers['fashion_news_frequency'].transform(decode_fashion)
customers

#%%
# Decoding "Club Member Status" variable
def decode_club(x):
    if x == 0:
        return 'INACTIVE'
    if x == 1:
        return 'ACTIVE'
    if x == 3:
        return 'LEFT CLUB'
    if x == 4:
        return 'PRE-CREATE'
    
customers['club_member_status'] = customers['club_member_status'].transform(decode_club)
customers

#%%
# Uploading data to database
customers.to_sql(name = "customers", con = conn, if_exists = 'replace', index = False) # no index will be uploaded to database as False

#%%
result = conn.execute("SHOW TABLES;").fetchall()
for r in result:
    print(r) # 
