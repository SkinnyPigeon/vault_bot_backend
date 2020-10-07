from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from pathlib import Path
import os
import json

FLASK_DEBUG=1
project_folder = os.path.expanduser('~/code/data_vault_maker_backend/')
load_dotenv(os.path.join(project_folder, '.env'))
PASSWORD = os.getenv('PASSWORD')

app = Flask(__name__)
app.config['ERROR_404_HELP'] = False
CORS(app)

from functions.connect_to_db import setup_connection, select_table_classes, show_table_names, show_table_columns
from functions.process_data_vault import control_objects_starter, fill_hubs, select_satellite_names, link_generator, fill_satellites
from functions.save_to_db import create_unique_schema_name, setup_save_connection, create_unique_schema, insert_into_table

@app.route('/')
def hello():
    return {"Hello": "Welcome to VaultBot"}

@app.route('/connect', methods=['post'])
def connect():
    req_data = request.get_json()
    connection = setup_connection(req_data['schema'], req_data['database'])
    tables = select_table_classes(connection['base'])
    table_names = show_table_names(tables)
    connection['engine'].dispose()
    return json.dumps(table_names)

@app.route('/table', methods=['post'])
def table():
    req_data = request.get_json()
    connection = setup_connection(req_data['schema'], req_data['database'])
    columns = show_table_columns(connection['base'], req_data['table'])
    connection['engine'].dispose()
    return json.dumps(columns)

@app.route('/satellite', methods=['post'])
def satellite():
    req_data = request.get_json()
    print(req_data)
    hubs, links, satellites = control_objects_starter(req_data['table'])
    hubs = fill_hubs(hubs, req_data)
    satellite_names = select_satellite_names(req_data)
    links['links'] = link_generator(satellite_names)
    satellites['satellites'] = fill_satellites(satellite_names, req_data)

    print("HUBS: {}".format(hubs))
    print("LINKS: {}".format(links))
    print("SATELLITES: {}".format(satellites))

    if req_data['saveSchema'] == None:
        schema_name = create_unique_schema_name(5)
    else:
        schema_name = req_data['saveSchema']
    connection = setup_save_connection(schema_name)
    connection = create_unique_schema(connection, schema_name)
    insert_into_table(connection, hubs, links, satellites)
    connection['engine'].dispose()

    req_data['saveSchema'] = schema_name

    return req_data

@app.route('/vaultbot', methods=['post'])
def vaultbot():
    req_data = request.get_json()

    return req_data

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5001')