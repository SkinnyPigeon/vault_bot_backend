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


def create_hubs(output_file, schema, hubs):
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



def create_links(output_file, schema):
    class_prefix = schema.upper()
    links = """

hub_time = get_class_by_tablename("{schema}.hub_time", Base)
hub_person = get_class_by_tablename("{schema}.hub_person", Base)
hub_object = get_class_by_tablename("{schema}.hub_object", Base)
hub_location = get_class_by_tablename("{schema}.hub_location", Base)
hub_event = get_class_by_tablename("{schema}.hub_event", Base)

# Links

person_time_link={{'__tablename__': 'person_time_link',
'__table_args__':{{'schema': '{schema}'}},
'id': Column(column_types['integer'], primary_key=True),
'person_id': Column(column_types['integer'], ForeignKey(hub_person.id)),
'time_id': Column(column_types['integer'], ForeignKey(hub_time.id))}}

person_time = type('{class_prefix}_Person_Time_Link',(Base,),person_time_link)

#

person_object_link={{'__tablename__': 'person_object_link',
'__table_args__':{{'schema': '{schema}'}},
'id': Column(column_types['integer'], primary_key=True),
'person_id': Column(column_types['integer'], ForeignKey(hub_person.id)),
'object_id': Column(column_types['integer'], ForeignKey(hub_object.id))}}

person_object = type('{class_prefix}_Person_Object_Link',(Base,),person_object_link)

#

person_location_link={{'__tablename__': 'person_location_link',
'__table_args__':{{'schema': '{schema}'}},
'id': Column(column_types['integer'], primary_key=True),
'person_id': Column(column_types['integer'], ForeignKey(hub_person.id)),
'location_id': Column(column_types['integer'], ForeignKey(hub_location.id))}}

person_location = type('{class_prefix}_Person_Location_Link',(Base,),person_location_link)

#

person_event_link={{'__tablename__': 'person_event_link',
'__table_args__':{{'schema': '{schema}'}},
'id': Column(column_types['integer'], primary_key=True),
'person_id': Column(column_types['integer'], ForeignKey(hub_person.id)),
'event_id': Column(column_types['integer'], ForeignKey(hub_event.id))}}

person_event = type('{class_prefix}_Person_Event_Link',(Base,),person_event_link)

###

object_time_link={{'__tablename__': 'object_time_link',
'__table_args__':{{'schema': '{schema}'}},
'id': Column(column_types['integer'], primary_key=True),
'object_id': Column(column_types['integer'], ForeignKey(hub_object.id)),
'time_id': Column(column_types['integer'], ForeignKey(hub_time.id))}}

object_time = type('{class_prefix}_Object_Time_Link',(Base,),object_time_link)

#

object_location_link={{'__tablename__': 'object_location_link',
'__table_args__':{{'schema': '{schema}'}},
'id': Column(column_types['integer'], primary_key=True),
'object_id': Column(column_types['integer'], ForeignKey(hub_object.id)),
'location_id': Column(column_types['integer'], ForeignKey(hub_location.id))}}

object_location = type('{class_prefix}_Object_Location_Link',(Base,),object_location_link)

#

object_event_link={{'__tablename__': 'object_event_link',
'__table_args__':{{'schema': '{schema}'}},
'id': Column(column_types['integer'], primary_key=True),
'object_id': Column(column_types['integer'], ForeignKey(hub_object.id)),
'event_id': Column(column_types['integer'], ForeignKey(hub_event.id))}}

object_event = type('{class_prefix}_Object_Event_Link',(Base,),object_event_link)

###

time_location_link={{'__tablename__': 'time_location_link',
'__table_args__':{{'schema': '{schema}'}},
'id': Column(column_types['integer'], primary_key=True),
'time_id': Column(column_types['integer'], ForeignKey(hub_time.id)),
'location_id': Column(column_types['integer'], ForeignKey(hub_location.id))}}

time_location = type('{class_prefix}_Time_Location_Link',(Base,),time_location_link)

#

time_event_link={{'__tablename__': 'time_event_link',
'__table_args__':{{'schema': '{schema}'}},
'id': Column(column_types['integer'], primary_key=True),
'time_id': Column(column_types['integer'], ForeignKey(hub_time.id)),
'event_id': Column(column_types['integer'], ForeignKey(hub_event.id))}}

time_event = type('{class_prefix}_Time_Event_Link',(Base,),time_event_link)

###

location_event_link={{'__tablename__': 'location_event_link',
'__table_args__':{{'schema': '{schema}'}},
'id': Column(column_types['integer'], primary_key=True),
'location_id': Column(column_types['integer'], ForeignKey(hub_location.id)),
'event_id': Column(column_types['integer'], ForeignKey(hub_event.id))}}

location_event = type('{class_prefix}_Location_Event_Link',(Base,),location_event_link)

###

# Satellites
    """.format(schema=schema, class_prefix=class_prefix)
    f = open('./output_data_vault_files/{output_file}.py'.format(schema=schema, output_file=output_file), 'a+')
    f.write(links)
    f.close()

# check = {
#     "satellites": [
#         {
#             "satellite": "sat_event_episode_type", 
#             "columns": [
#                 "falar", "bekat", "einzg", "statu", "krzan", "storn", "casetx", "fatnx"
#             ], 
#             "hub": "hub_event", 
#             "hub_id": 0, 
#             "data_types": {
#                 "falar": {"data_type": "varchar"}, 
#                 "bekat": {"data_type": "varchar"}, 
#                 "einzg": {"data_type": "varchar"}, 
#                 "statu": {"data_type": "varchar"}, 
#                 "krzan": {"data_type": "varchar"}, 
#                 "storn": {"data_type": "varchar"}, 
#                 "casetx": {"data_type": "varchar"}, 
#                 "fatnx": {"data_type": "varchar"}
#             }, 
#             "source_table": "fcrb.episode"
#         }, 
#         {
#             "satellite": "sat_time_episode_date", 
#             "columns": [
#                 "enddt", "erdat", "begdt", "enddtx"
#             ], 
#             "hub": "hub_time", 
#             "hub_id": 0, 
#             "data_types": {
#                 "enddt": {"data_type": "timestamp without time zone"}, 
#                 "erdat": {"data_type": "timestamp without time zone"}, 
#                 "begdt": {"data_type": "timestamp without time zone"}, 
#                 "enddtx": {"data_type": "varchar"}
#             }, 
#             "source_table": "fcrb.episode"
#         }
#     ]
# }

# check2 = {"satellites": [{"satellite": "sat_object_diagnostic_details", "columns": ["lfdnr", "dkey1"], "hub": "hub_object", "hub_id": 0, "data_types": {"lfdnr": {"data_type": "integer"}, "dkey1": {"data_type": "varchar"}}, "source_table": "fcrb.diagnostic"}]}

# satellites = {0: check, 1: check2}

def create_satellites(output_file, schema, satellites):
    class_prefix = schema.upper()
    for keys, values in satellites.items():
        for satellite in values['satellites']:
            class_variable = satellite['satellite'][4:]
            class_name = "{class_prefix}_".format(class_prefix=class_prefix) + satellite['satellite'].replace('_', ' ').title().replace(' ', '_')
            satellite_text = """
new_satellite={{'__tablename__':'{satellite_name}',
'__table_args__':{{'schema':  '{schema}'}},
'id': Column(column_types['integer'], primary_key=True),
'source_table': Column(column_types['string']),
'hub_id': Column(column_types['integer'], ForeignKey({hub}.id))}}

columns = []
for keys, values in {data_types}.items():
    columns.append({{keys: Column(column_types[values['data_type']])}})
for column in columns:
    new_satellite.update(column)


{class_variable} = type('{class_name}',(Base,), new_satellite)
            """.format(satellite_name=satellite['satellite'], schema=schema, hub=satellite['hub'], data_types=satellite['data_types'], class_variable=class_variable, class_name=class_name)
            print(satellite_text)
            f = open('./output_data_vault_files/{output_file}.py'.format(schema=schema, output_file=output_file), 'a+')
            f.write(satellite_text)
            f.close()

def finish_data_vault_script(output_file, schema):
    base_text = """
Base.metadata.create_all(engine)
    """
    f = open('./output_data_vault_files/{output_file}.py'.format(schema=schema, output_file=output_file), 'a+')
    f.write(base_text)
    f.close()

# finish_data_vault_script("test", "public")

# create_satellites("test", "public", satellites)
# new_satellite={'__tablename__':'sat_object_diagnostic_details',
# '__table_args__':{'schema':  schema},
# 'id': Column(column_types['integer'], primary_key=True),
# 'source_table': Column(column_types['string']),
# 'hub_id': Column(column_types['integer'], ForeignKey(hub_object.id))}

# columns = [{'lfdnr': Column(column_types['integer'])},{'dkey1': Column(column_types['varchar'])}]
# for column in columns:
#     new_satellite.update(column)

# object_diagnostic_details = type('FCRB_Sat_Object_Diagnostic_Details',(base,),new_satellite)