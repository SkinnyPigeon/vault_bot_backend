from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.schema import CreateSchema
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd
# pd.set_option('display.max_colwidth', -1)
import datetime

import os
from dotenv import load_dotenv
from pathlib import Path

project_folder = os.path.expanduser('~/code/data_vault_maker_backend/')
load_dotenv(os.path.join(project_folder, '.env'))
PASSWORD = os.getenv('PASSWORD')

import random
import string

def create_unique_schema_name(length):
    letters_and_digits = string.ascii_lowercase + string.digits
    return '_' + ''.join((random.choice(letters_and_digits) for i in range(length)))

def setup_save_connection(schema):
    Base = declarative_base()
    metadata = MetaData(schema=schema)
    base = Base(metadata=schema)
    engine = create_engine('postgresql://postgres:{}@localhost:5434/vault_bot'.format(PASSWORD))
    Session = sessionmaker(bind=engine, autoflush=True, autocommit=False)
    session = Session()
    return {'base': base, 'metadata': metadata, 'engine': engine, 'session': session, 'schema': schema}

def create_unique_schema(connection, schema):
    try:
        connection['engine'].execute(CreateSchema(schema))
        return connection
    except:
        return connection

def insert_into_table(connection, hubs, links, satellites):
    save_table = Table('save_table', connection['metadata'],
        Column('id', Integer, primary_key=True),
        Column('hubs', JSON),
        Column('links', JSON),
        Column('satellites', JSON)
    )
    connection['metadata'].create_all(connection['engine'])
    with connection['engine'].connect() as conn:
        conn.execute(
            save_table.insert(),
            hubs = hubs,
            links = links,
            satellites = satellites
        )
    connection['engine'].dispose()

def retrieve_from_table(connection):
    save_table = Table('save_table', connection['metadata'],
        Column('id', Integer, primary_key=True),
        Column('hubs', JSON),
        Column('links', JSON),
        Column('satellites', JSON)
    )
    connection['metadata'].create_all(connection['engine'])
    df = pd.read_sql(connection['session'].query(save_table).statement, con=connection['engine'])
    connection['engine'].dispose()
    return df