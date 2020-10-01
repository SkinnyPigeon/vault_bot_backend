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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5001')