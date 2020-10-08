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


def hubs_scripting(hubs, schema):
    class_prefix = schema.upper()
    for keys, values in hubs.items():
        class_variable = keys[4:]
        class_name = "{class_prefix}_".format(class_prefix=class_prefix) + keys.replace('_', ' ').title().replace(' ', '_')
        hub_text = """
{hub_name}={{'__tablename__': '{hub_name}',
'__table_args__':{{'schema':'{schema}'}},
'id': Column(column_types['integer'], primary_key=True)}}
primary_keys = []
for keys, values in {values}.items():
    primary_keys.append({{keys: Column(column_types[values['data_type']])}})
for key in primary_keys:
    {hub_name}.update(key)

{class_variable} = type('{class_name}',(Base,),{hub_name})
        """.format(hub_name=keys, schema=schema, values=values, class_variable=class_variable, class_name=class_name)
        print(hub_text)
hubs_scripting(hubs, "public")

# data_vault_boilerplate("test", "public", "vault_bot_out")

# hub_time={'__tablename__': 'hub_time',
# '__table_args__':{'schema':'fcrb'},
# 'id': Column(column_types['integer'], primary_key=True)}

# keys = [{'einri': Column(String)},{'patnr': Column(Integer)},{'falnr': Column(String)},{'pernr': Column(String)},{'orgid': Column(String)},{'vppid': Column(Integer)}]
# for key in keys:
#     hub_time.update(key)

# time = type('FCRB_Hub_Time',(Base,),hub_time)