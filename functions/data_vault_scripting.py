import os
from pathlib import Path

project_folder = os.path.expanduser('~/code/data_vault_maker_backend/')

def data_vault_boilerplate(output_file, schema, database):
    class_prefix = schema.upper()
    setup = """
# Imports

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from sqlalchemy import Column, Integer, String, Numeric, DateTime, Text, ForeignKey, create_engine
from sqlalchemy.types import TIMESTAMP

import os
from dotenv import load_dotenv
from pathlib import Path

project_folder = os.path.expanduser('~/code/data_vault_maker_backend/')
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
    'timestamp without time zone': TIMESTAMP
}}

# HUBS
    """.format(schema=schema, class_prefix=class_prefix, database=database)
    f = open('./output_data_vault_files/{output_file}.py'.format(schema=schema, output_file=output_file), 'w')
    f.write(setup)
    f.close()


def hubs_scripting(output_file, hubs, schema):
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
        f = open('./output_data_vault_files/{output_file}.py'.format(schema=schema, output_file=output_file), 'a+')
        f.write(hub_text)
        f.close()

# hubs_scripting("test", hubs, "public")