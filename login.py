from flask import Flask, jsonify, request, json
from datetime import datetime
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import (create_access_token)

import psycopg2
app = Flask(__name__)

#app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = ''
#app.config['MYSQL_DB'] = 'nodejs_login1'
#app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['JWT_SECRET_KEY'] = 'secret'

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

CORS(app)
try:
    conn = psycopg2.connect("dbname ='' user='' host='' password='' ")
except:
    print('Not able to connect server')

@app.route('/users/register', ethods=['POST'])
def register():
    cur = conn.cursor()
    first_name = request.get_json()['first_name']
    last_name = request.get_json()['last_name']
    email = request.get_json()['email']
    password = bcrypt.generate_password_hash(request.get_json()['password']).decode('utf-8')
    created = datetime.utcnow()

    cur.execute("INSERT INTO users (first_name, last_name, email, password, created) VALUES ('" +
                str(first_name) + "', '" +
                str(last_name) + "', '" +
                str(email) + "', '" +
                str(password) + "', '" +
                str(created) + "')")


    result = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': password,
        'created': created
    }

    return jsonify({'result': result})


@app.route('/users/login', methods=['POST'])
def login():
    cur = conn.cursor()
    email = request.get_json()['email']
    password = request.get_json()['password']
    result = ""

    cur.execute("SELECT * FROM users where email = '" + str(email) + "'")
    rv = cur.fetchone()

    if bcrypt.check_password_hash(rv['password'], password):
        access_token = create_access_token(
            identity={'first_name': rv['first_name'], 'last_name': rv['last_name'], 'email': rv['email']})
        result = access_token
    else:
        result = jsonify({"error": "Invalid username and password"})

    return result


if __name__ == '__main__':
    app.run(debug=True)