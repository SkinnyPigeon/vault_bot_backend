
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
for keys, values in {}.items():
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
for keys, values in {}.items():
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
        

hub_time = get_class_by_tablename("public.hub_time", Base)
hub_person = get_class_by_tablename("public.hub_person", Base)
hub_object = get_class_by_tablename("public.hub_object", Base)
hub_location = get_class_by_tablename("public.hub_location", Base)
hub_event = get_class_by_tablename("public.hub_event", Base)

# Links

person_time_link={'__tablename__': 'person_time_link',
'__table_args__':{'schema': 'public'},
'id': Column(column_types['integer'], primary_key=True),
'person_id': Column(column_types['integer'], ForeignKey(hub_person.id)),
'time_id': Column(column_types['integer'], ForeignKey(hub_time.id))}

person_time = type('PUBLIC_Person_Time_Link',(Base,),person_time_link)

#

person_object_link={'__tablename__': 'person_object_link',
'__table_args__':{'schema': 'public'},
'id': Column(column_types['integer'], primary_key=True),
'person_id': Column(column_types['integer'], ForeignKey(hub_person.id)),
'object_id': Column(column_types['integer'], ForeignKey(hub_object.id))}

person_object = type('PUBLIC_Person_Object_Link',(Base,),person_object_link)

#

person_location_link={'__tablename__': 'person_location_link',
'__table_args__':{'schema': 'public'},
'id': Column(column_types['integer'], primary_key=True),
'person_id': Column(column_types['integer'], ForeignKey(hub_person.id)),
'location_id': Column(column_types['integer'], ForeignKey(hub_location.id))}

person_location = type('PUBLIC_Person_Location_Link',(Base,),person_location_link)

#

person_event_link={'__tablename__': 'person_event_link',
'__table_args__':{'schema': 'public'},
'id': Column(column_types['integer'], primary_key=True),
'person_id': Column(column_types['integer'], ForeignKey(hub_person.id)),
'event_id': Column(column_types['integer'], ForeignKey(hub_event.id))}

person_event = type('PUBLIC_Person_Event_Link',(Base,),person_event_link)

###

object_time_link={'__tablename__': 'object_time_link',
'__table_args__':{'schema': 'public'},
'id': Column(column_types['integer'], primary_key=True),
'object_id': Column(column_types['integer'], ForeignKey(hub_object.id)),
'time_id': Column(column_types['integer'], ForeignKey(hub_time.id))}

object_time = type('PUBLIC_Object_Time_Link',(Base,),object_time_link)

#

object_location_link={'__tablename__': 'object_location_link',
'__table_args__':{'schema': 'public'},
'id': Column(column_types['integer'], primary_key=True),
'object_id': Column(column_types['integer'], ForeignKey(hub_object.id)),
'location_id': Column(column_types['integer'], ForeignKey(hub_location.id))}

object_location = type('PUBLIC_Object_Location_Link',(Base,),object_location_link)

#

object_event_link={'__tablename__': 'object_event_link',
'__table_args__':{'schema': 'public'},
'id': Column(column_types['integer'], primary_key=True),
'object_id': Column(column_types['integer'], ForeignKey(hub_object.id)),
'event_id': Column(column_types['integer'], ForeignKey(hub_event.id))}

object_event = type('PUBLIC_Object_Event_Link',(Base,),object_event_link)

###

time_location_link={'__tablename__': 'time_location_link',
'__table_args__':{'schema': 'public'},
'id': Column(column_types['integer'], primary_key=True),
'time_id': Column(column_types['integer'], ForeignKey(hub_time.id)),
'location_id': Column(column_types['integer'], ForeignKey(hub_location.id))}

time_location = type('PUBLIC_Time_Location_Link',(Base,),time_location_link)

#

time_event_link={'__tablename__': 'time_event_link',
'__table_args__':{'schema': 'public'},
'id': Column(column_types['integer'], primary_key=True),
'time_id': Column(column_types['integer'], ForeignKey(hub_time.id)),
'event_id': Column(column_types['integer'], ForeignKey(hub_event.id))}

time_event = type('PUBLIC_Time_Event_Link',(Base,),time_event_link)

###

location_event_link={'__tablename__': 'location_event_link',
'__table_args__':{'schema': 'public'},
'id': Column(column_types['integer'], primary_key=True),
'location_id': Column(column_types['integer'], ForeignKey(hub_location.id)),
'event_id': Column(column_types['integer'], ForeignKey(hub_event.id))}

location_event = type('PUBLIC_Location_Event_Link',(Base,),location_event_link)

###

# Satellites
    
new_satellite={'__tablename__':'sat_object_diagnostic_details',
'__table_args__':{'schema':  'public'},
'id': Column(column_types['integer'], primary_key=True),
'source_table': Column(column_types['string']),
'hub_id': Column(column_types['integer'], ForeignKey(hub_object.id))}

columns = []
for keys, values in {'lfdnr': {'data_type': 'integer'}, 'dkey1': {'data_type': 'varchar'}}.items():
    columns.append({keys: Column(column_types[values['data_type']])})
for column in columns:
    new_satellite.update(column)


object_diagnostic_details = type('PUBLIC_Sat_Object_Diagnostic_Details',(Base,), new_satellite)
            
new_satellite={'__tablename__':'sat_event_episode_type',
'__table_args__':{'schema':  'public'},
'id': Column(column_types['integer'], primary_key=True),
'source_table': Column(column_types['string']),
'hub_id': Column(column_types['integer'], ForeignKey(hub_event.id))}

columns = []
for keys, values in {'falar': {'data_type': 'varchar'}, 'bekat': {'data_type': 'varchar'}, 'einzg': {'data_type': 'varchar'}, 'statu': {'data_type': 'varchar'}, 'krzan': {'data_type': 'varchar'}, 'storn': {'data_type': 'varchar'}, 'casetx': {'data_type': 'varchar'}, 'fatnx': {'data_type': 'varchar'}}.items():
    columns.append({keys: Column(column_types[values['data_type']])})
for column in columns:
    new_satellite.update(column)


event_episode_type = type('PUBLIC_Sat_Event_Episode_Type',(Base,), new_satellite)
            
new_satellite={'__tablename__':'sat_time_episode_date',
'__table_args__':{'schema':  'public'},
'id': Column(column_types['integer'], primary_key=True),
'source_table': Column(column_types['string']),
'hub_id': Column(column_types['integer'], ForeignKey(hub_time.id))}

columns = []
for keys, values in {'enddt': {'data_type': 'timestamp without time zone'}, 'erdat': {'data_type': 'timestamp without time zone'}, 'begdt': {'data_type': 'timestamp without time zone'}, 'enddtx': {'data_type': 'varchar'}}.items():
    columns.append({keys: Column(column_types[values['data_type']])})
for column in columns:
    new_satellite.update(column)


time_episode_date = type('PUBLIC_Sat_Time_Episode_Date',(Base,), new_satellite)
            
Base.metadata.create_all(engine)
    