import os

from flask import Flask
from flask import make_response
import datetime
from flask import request
from client import perform_request_to_config_server as load_config

app = Flask(__name__)
app.debug = True
my_date_format = ""

url = os.environ.get('CONFIG_SERVER_URL')
service = os.environ.get('SERVICE_NAME')
branch = os.environ.get('CONFIG_SERVER_BRANCH')
formatter = os.environ.get('FORMAT_PATTERN')


def call_client(env):
    """"call this method to retrieve the formatter from the CONFIG_SERVER for the requested environment
    
    :argument env = the environment you want to fetch
       
    :return a list of configurations fetched from the repo    
    """
    global my_date_format
    if my_date_format == "":
        my_date_format = load_config(url, service, env, branch)[formatter]
        return my_date_format
    elif my_date_format != "":
        return my_date_format


def refresh_client(env):
    """"call to refresh the formatter from the CONFIG_SERVER for the requested environment

        :argument env = the environment you want to fetch

        :return a list of configurations fetched from the repo    
        """
    global my_date_format
    if my_date_format != "":
        my_date_format = load_config(url, service, env, branch)[formatter]


@app.route('/time/<env>')
def time(env):
    """"Retrieve The time"""
    my_format = call_client(env)
    resp = make_response("The Date is : " + str(
        datetime.datetime.now().strftime(my_format)))
    return resp


@app.route('/refresh/<env>', methods=['POST'])
def refresh(env):
    """"Refresh the service"""
    # my_date_format =
    refresh_client(env)
    return 'Refreshing ' + env + ' configuration...'


@app.route('/shutdown', methods=['POST'])
def shutdown():
    """Shutdown the service"""
    shutdown_server()
    return 'Server shutting down...'


def shutdown_server():
    """"Shutdown the running server that is hosting the service"""
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()