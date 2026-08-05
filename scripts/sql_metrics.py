import pandas as pd


def load_query(query_name):

    with open(f"../queries/{query_name}.sql","r") as f:

        return f.read()


def execute_query(engine,query_name):

    query=load_query(query_name)

    return pd.read_sql(query,engine)