from os import abort

from flask import Flask, render_template, request,jsonify,make_response
import json
import sqlite3

app = Flask(__name__)

@app.route('/api/V1/info')
def home_index():
    conn = sqlite3.connect('identifier.sqlite')
    print("Opened database successfully")
    api_list = []
    cursor = conn.execute("SELECT buildtime,version,methods,links FROM apirelease")
    for row in cursor:
        a_dic={}
        a_dic['buildtime']=row[1]
        a_dic['version']=row[0]
        a_dic['methods']=row[2]
        a_dic['links']=row[3]
        api_list.append(a_dic)
    conn.close()
    return jsonify({'api_version':api_list}),200

@app.route('/api/v1/users', methods=['GET'])
def get_users():
    return list_users();

def list_users():
    conn = sqlite3.connect('identifier.sqlite')
    print("Opened database successfully")
    api_list = []
    cursor = conn.execute("SELECT username,full_name,emailid,password,id FROM users")
    for row in cursor:
        a_dic={}
        a_dic['username']=row[0]
        a_dic['full_name']=row[1]
        a_dic['email']=row[2]
        a_dic['password']=row[3]
        a_dic['id']=row[4]
        api_list.append(a_dic)
    conn.close()
    return jsonify({'userlist':api_list}),200

@app.route('/api/v1/users/<userid>', methods=['GET'])
def get_user(userid):
    return list_user(userid)

def list_user(userid):
    conn = sqlite3.connect('identifier.sqlite')
    user = None
    print("Opened database successfully")
    cursor = conn.execute("SELECT * FROM users where id=?",(userid,))
    data = cursor.fetchall()
    if len(data) != 0:
        user = {}
        user['username']=data[0][0]
        user['email']=data[0][1]
        user['password']=data[0][2]
        user['id']=data[0][3]
    conn.close()
    return jsonify({'user':user})

@app.errorhandler(404)
def page_not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/api/v1/users', methods=['POST'])
def create_user():
    if not request.json or not 'username' in request.json or not 'email' in request.json or not 'password' in request.json:
        abort(400)
    user={
        'username':request.json.get('username'),
        'email':request.json.get('email'),
        'password':request.json.get('password'),
        'name':request.json.get('name')
    }
    return  jsonify({'status':add_user(user)}),201

@app.errorhandler(400)
def invaild_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

def add_user(new_user):
    conn = sqlite3.connect('identifier.sqlite')
    print("Opened database successfully")
    api_list = []
    cursor = conn.cursor()
    cursor.execute("SELECT * from users where id=? or emailid=?",(new_user['username'],new_user['email']))
    data = cursor.fetchall()
    if len(data) != 0:
        abort(409)
    else:
        cursor.execute("Insert into users (username,emailid,password,full_name) values (?,?,?,?)",(new_user['username'],new_user['email'],new_user['password'],new_user['name']))
        conn.commit()
        return "success"
    conn.close()
    return jsonify(a_dict)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=50000, debug=True)