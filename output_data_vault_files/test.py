
# Imports

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String, Numeric, DateTime, Text, ForeignKey, create_engine
from sqlalchemy.types import TIMESTAMP
import os
from dotenv import load_dotenv
from pathlib import Path

project_folder = os.path.expanduser('~/code/data_vault_generator/')
load_dotenv(os.path.join(project_folder, '.env'))
PASSWORD = os.getenv('PASSWORD')

engine = create_engine('postgresql://postgres:{}@localhost:5434/vault_bot_out'.format(PASSWORD), echo='debug')

def get_class_by_tablename(table_fullname, Base):
  for class_name in Base._decl_class_registry.values():
    if hasattr(class_name, '__table__') and class_name.__table__.fullname == table_fullname:
      return class_name

# Column Types

column_types = {
    'integer': Integer,
    'string': String,
    'varchar': String,
    'numeric': Numeric,
    'datetime': DateTime,
    'text': Text,
    'timestamp without time zone': TIMESTAMP
}

# HUBS
    
hub_time={'__tablename__': 'hub_time',
'__table_args__':{'schema':'public'},
'id': Column(column_types['integer'], primary_key=True)}

primary_keys = []
for keys, values in {'einri': {'data_type': 'varchar'}, 'falnr': {'data_type': 'varchar'}, 'patnr': {'data_type': 'integer'}, 'pernr': {'data_type': 'varchar'}}.items():
    primary_keys.append({keys: Column(column_types[values['data_type']])})
for key in primary_keys:
    hub_time.update(key)

time = type('PUBLIC_Hub_Time',(Base,),hub_time)
        
hub_person={'__tablename__': 'hub_person',
'__table_args__':{'schema':'public'},
'id': Column(column_types['integer'], primary_key=True)}

primary_keys = []
for keys, values in {'pid': {'data_type': 'integer'}}.items():
    primary_keys.append({keys: Column(column_types[values['data_type']])})
for key in primary_keys:
    hub_person.update(key)

person = type('PUBLIC_Hub_Person',(Base,),hub_person)
        
hub_object={'__tablename__': 'hub_object',
'__table_args__':{'schema':'public'},
'id': Column(column_types['integer'], primary_key=True)}
primary_keys = []
for keys, values in {'einri': {'data_type': 'varchar'}, 'patnr': {'data_type': 'integer'}, 'falnr': {'data_type': 'varchar'}, 'pernr': {'data_type': 'varchar'}}.items():
    primary_keys.append({keys: Column(column_types[values['data_type']])})
for key in primary_keys:
    hub_object.update(key)

object = type('PUBLIC_Hub_Object',(Base,),hub_object)
        
hub_location={'__tablename__': 'hub_location',
'__table_args__':{'schema':'public'},
'id': Column(column_types['integer'], primary_key=True)}
primary_keys = []
for keys, values in {'patnr': {'data_type': 'integer'}}.items():
    primary_keys.append({keys: Column(column_types[values['data_type']])})
for key in primary_keys:
    hub_location.update(key)

location = type('PUBLIC_Hub_Location',(Base,),hub_location)
        
hub_event={'__tablename__': 'hub_event',
'__table_args__':{'schema':'public'},
'id': Column(column_types['integer'], primary_key=True)}
primary_keys = []
for keys, values in {'einri': {'data_type': 'varchar'}, 'falnr': {'data_type': 'varchar'}, 'patnr': {'data_type': 'integer'}, 'pernr': {'data_type': 'varchar'}}.items():
    primary_keys.append({keys: Column(column_types[values['data_type']])})
for key in primary_keys:
    hub_event.update(key)

event = type('PUBLIC_Hub_Event',(Base,),hub_event)
        
Base.metadata.create_all(engine)