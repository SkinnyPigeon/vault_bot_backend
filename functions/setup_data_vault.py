from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.schema import CreateSchema
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd
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

def setup_dv_connection(schema):
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
    

def get_hub_keys(hubs):
    hub_keys = {
        "hub_time": {},
        "hub_person": {},
        "hub_object": {},
        "hub_location": {},
        "hub_event": {}
    }
    for row in hubs:
        for hub in row['hubs']:
            keys = hub['keys']
            for key in keys:
                hub_keys[hub['hub']].update({key: hub['data_types'][key]})
    return hub_keys

connection = setup_dv_connection("_490u7")
df = retrieve_from_table(connection)
hub_keys = get_hub_keys(df['hubs'])
print(hub_keys)
{
    'hub_time': {
        'einri': {'data_type': 'varchar'}, 
        'falnr': {'data_type': 'varchar'}, 
        'patnr': {'data_type': 'integer'}, 
        'pernr': {'data_type': 'varchar'}
    }, 
    'hub_person': {
        'id': {'data_type': 'integer'}
    }, 
    'hub_object': {
        'einri': {'data_type': 'varchar'}, 
        'patnr': {'data_type': 'integer'}, 
        'falnr': {'data_type': 'varchar'}, 
        'pernr': {'data_type': 'varchar'}
    }, 
    'hub_location': {
        'patnr': {'data_type': 'integer'}
    }, 
    'hub_event': {
        'einri': {'data_type': 'varchar'}, 
        'falnr': {'data_type': 'varchar'}, 
        'patnr': {'data_type': 'integer'}, 
        'pernr': {'data_type': 'varchar'}
    }
}
