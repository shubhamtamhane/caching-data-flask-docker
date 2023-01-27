# -*- coding: utf-8 -*-

# For this version of python, do not use jwt.decode(token). 
# Instead use token directly, i.e. do not decode it. It is already in string format

# Data source for json file
# https://github.com/json-iterator/test-data/blob/master/large-file.json

# For accessing urls which are protected do the following 
# .../protected?token=token_value


# Importing libraries
from flask import Flask, jsonify, request, make_response
from flask_caching import Cache
import jwt
import datetime
from functools import wraps
from time import sleep
from random import randint
import json  # Json is not used and pandas is used because json does not support loading large files. Pandas does it effectively.
import pandas as pd
import configparser

# Initializing the flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = "secretkey"
app.config['CACHE_TYPE'] = "simple"

# Initialing cache
cache = Cache()
cache.init_app(app)

# Fetching data from the config file named configfile.ini
config = configparser.ConfigParser()
#config.read(R'C:\Users\stamhane.URMC-SH\Desktop\work\work\caching\configfile.ini')
config.read(R'configfile.ini')

cache_time = int(config['VALUES']['CACHE_TIME'])
file_path = config['VALUES']['JSON_FILE_PATH']
user_name = config['VALUES']['USER_NAME']
password_val = config['VALUES']['PASSWORD']

# Function which does token authentication
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({'message': "Token is missing"}), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            # data = token
        
        except:
            return jsonify({'message': "Invalid token"}), 401

        return f(*args, **kwargs)

    return decorated

# For home screen currently a random numner generator is kept just to show that caching works.
# Should be replaced by relevant content later.
@app.route('/')
@cache.cached(timeout=cache_time)
def home_page():
    randnum = randint(1,1000)
    return f'<h1>The number is {randnum}</h1>'
    # return("<h1> Welcome </h1>")

# An unprotected route to show generic content apart from the home page
@app.route('/unprotected')
def unprotected():
    return jsonify({'message': "This content can be viewed by everyone"})


# A protected route with integration of cache to demonstrate combined working of both functionalities.
@app.route('/protected')
@cache.cached(timeout=cache_time)
@token_required
def protected():
    sleep(10)
    return jsonify({'message': "This is secret data"})

# To flush the cache
@app.route('/clearcache')
@token_required
def clear_cache():
    cache.clear()
    return("<h1> Cache cleared </h1>")

# To read the json file. The data being loaded now is a small file but the commented line having "large-file.json"
# can be used for testing purpose. It is a ~24 mb file
@app.route('/readfile')
@cache.cached(timeout=cache_time)
@token_required
def read_json_file():
    sleep(10)  # In case of large file, this line can be removed
    try:
        # df = pd.read_json('large-file.json')
        df = pd.read_json(file_path)
        json_file = df.to_json(orient="records")  # For viewing data in different format, orient can be changed.
        # return jsonify(json_file)        
        return json_file

    except:
        return("The json file was unable to load. Please visit /failed_commands to debug.")

# Shows where the file is present
@app.route('/failed_commands')
@token_required
def failed_commands():
    filepath = '<h4>' + file_path + '</h4>'
    s = '<h1> The file path is </h1> \n'
    return(s + filepath + "<h1> Please check the file </h1>")

# To generate token and login, this route is to be used. Currently, token is set to be valid for 60 minutes
@app.route('/login')
def login():
    auth = request.authorization
    if auth and auth.username == user_name and auth.password == password_val:
        token = jwt.encode({'user': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)},app.config['SECRET_KEY'])
        # print("token is ", token)
        # print("type of token is ", type(token))
        return jsonify({'token': token})


    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required"'})


if __name__== '__main__':
    app.run(debug=True, host='0.0.0.0')