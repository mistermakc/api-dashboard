#%%

import sqlalchemy

engine = sqlalchemy.create_engine("sqlite:///paymepal.db")

connection = engine.connect()

with engine.connect() as connection:
    query = "SELECT * FROM transactions"

    result = connection.execute(query)

    for row in result:
        print(row)
# %%
