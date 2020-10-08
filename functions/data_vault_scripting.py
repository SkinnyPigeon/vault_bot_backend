hubs = {
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

import os
from pathlib import Path

project_folder = os.path.expanduser('~/code/data_vault_generator/')



def data_vault_boilerplate(output_file, schema, database):
    class_prefix = schema.upper()
    setup = """
# Imports

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String, Numeric, DateTime, TimeStamp, Text, ForeignKey, create_engine

import os
from dotenv import load_dotenv
from pathlib import Path

project_folder = os.path.expanduser('~/code/data_vault_generator/')
load_dotenv(os.path.join(project_folder, '.env'))
PASSWORD = os.getenv('PASSWORD')

engine = create_engine('postgresql://postgres:{{}}@localhost:5434/{database}'.format(PASSWORD), echo='debug')

def get_class_by_tablename(table_fullname, Base):
  for class_name in Base._decl_class_registry.values():
    if hasattr(class_name, '__table__') and class_name.__table__.fullname == table_fullname:
      return class_name

# Column Types

column_types = {{
    'integer': Integer,
    'string': String,
    'varchar': String,
    'numeric': Numeric,
    'datetime': DateTime,
    'text': Text,
    'timestamp without time zone': 'TimeStamp'
}}

# HUBS
    """.format(schema=schema, class_prefix=class_prefix, database=database)
    f = open('./output_data_vault_files/{output_file}.py'.format(schema=schema, output_file=output_file), 'w')
    f.write(setup)
    f.close()


def hubs_scripting(hubs):
    print(hubs)

hubs_scripting(hubs)

data_vault_boilerplate("test", "public", "vault_bot_out")