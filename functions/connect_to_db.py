from sqlalchemy import create_engine, MetaData, inspect
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import load_only, sessionmaker, defer
import pandas as pd
from tabulate import tabulate

import os
from dotenv import load_dotenv
from pathlib import Path

project_folder = os.path.expanduser('~/code/data_vault_maker_backend/')
load_dotenv(os.path.join(project_folder, '.env'))
PASSWORD = os.getenv('PASSWORD')

def setup_connection(schema, database):
    metadata = MetaData(schema=schema)
    Base = automap_base(metadata=metadata)
    engine = create_engine('postgresql://postgres:{password}@localhost:5434/{database}'.format(password=PASSWORD, database=database))
    Base.prepare(engine, reflect=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    return {'base': Base, 'metadata': metadata, 'engine': engine, 'session': session}

def select_table_classes(base):
    tables = {}
    for class_name in base._decl_class_registry.values():
        if hasattr(class_name, '__table__'):
            tables.update({class_name.__table__.fullname: class_name})
    return tables

def select_table_class_by_name(base, tablename):
    print("SELECTING TABLE")
    for class_name in base._decl_class_registry.values():
        if hasattr(class_name, '__table__') and class_name.__table__.fullname == tablename:
            return class_name

def show_table_names(tables):
    return {"tableNames": list(tables.keys())}

def show_table_columns(base, table):
    table = select_table_class_by_name(base, table)
    data = {}
    for column in table.__table__.columns:
        data.update({column.name: str(column.type).lower()})
    # return {"columnNames": list(table.__table__.columns.keys())}
    return data