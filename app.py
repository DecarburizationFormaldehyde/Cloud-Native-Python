import random
from sqlite3.dbapi2 import apilevel
from tarfile import data_filter
from time import strftime, gmtime
from flask import render_template, redirect, session, url_for,abort

from flask import Flask, render_template, request,jsonify,make_response
import sqlite3

from flask_cors import CORS,cross_origin

from pymongo import MongoClient

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'
CORS(app)

@app.route('/api/v1/info')
def home_index():
    api_list = []
    db=connection.cloud_native.apirelease
    for row in db.find():
        api_list.append(str(row))
    return jsonify({'api_version':api_list}),200

@app.route('/api/v1/users', methods=['GET'])
def get_users():
    return list_users();

def list_users():
    api_list = []
    db=connection.cloud_native.users
    for row in db.find():
        api_list.append(str(row))
    return jsonify({'userlist':api_list}),200

@app.route('/api/v1/users/<userid>', methods=['GET'])
def get_user(userid):
    return list_user(userid)

def list_user(userid):
    api_list = []
    db = connection.cloud_native.users
    for i in db.find({'id':int(userid)}):
        api_list.append(str(i))
    if api_list == []:
        abort(404)
    return jsonify({'user':api_list})

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
        'name':request.json.get('name'),
        'id':random.randint(1,1000)
    }
    result = add_user(user)
    return  jsonify({'status':result,'username':user['username'],'email':user['email'],'password':user['password'],'name':user['name'],"password":user['password']}),201

@app.errorhandler(400)
def invaild_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)

def add_user(new_user):
    api_list = []
    db=connection.cloud_native.users
    user = db.find({'$or': [{"username":new_user['username']},{"email":new_user['email']}]})
    for i in user:
        print(str(i))
        api_list.append(str(i))
    if api_list==[]:
        db.insert_one(new_user)
        return "Success"
    else:
        abort(409)

@app.route('/api/v1/users', methods=['DELETE'])
def delete_user():
    if not request.json or not 'username' in request.json:
        abort(400)
    user=request.json.get('username')
    return jsonify({'status':del_user(user)}),200

def del_user(del_user):
    db = connection.cloud_native.users
    api_list=[]
    for i in db.find({'username':del_user}):
        api_list.append(str(i))
    if api_list == []:
        abort(404)
    else:
        db.delete_one({'username':del_user})
        return "Success"

@app.route('/api/v1/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = {}
    if not request.json:
        abort(400)
    user['id']=user_id
    key_list= request.json.keys()
    for i in key_list:
        user[i]=request.json[i]
    print(user)
    return jsonify({'status':upd_user(user)}),200

def upd_user(user):
    api_list = []
    print(user)
    db_user=connection.cloud_native.users
    users=db_user.find({'id':int(user['id'])})
    for i in users:
        api_list.append(str(i))
    if api_list == []:
        abort(409)
    else:
        db_user.update_one({'id':int(user['id'])},{'$set':user},upsert=False)
        return "Success"

@app.route('/api/v2/tweets', methods=['GET'])
def get_tweets():
    return list_tweets()

def list_tweets():
    api_list=[]
    db=connection.cloud_native.tweets
    for row in db.find():
        api_list.append(str(row))
    return jsonify({'tweets_list':api_list})

@app.route('/api/v2/tweets', methods=['POST'])
def add_tweets():
    user_tweet={}
    if not request.json or not 'username' in request.json or not 'body' in request.json:
        print(request)
        abort(400)
    user_tweet['username']=request.json.get('username')
    user_tweet['body']=request.json.get('body')
    user_tweet['creat_at']=strftime("%Y-%m-%dT %H:%M:%SZ", gmtime())
    print(user_tweet)
    result=add_tweet(user_tweet)
    return jsonify({'status':result,"username":user_tweet['username'],'body':user_tweet['body']}),200

def add_tweet(new_tweets):
    api_list=[]
    print(new_tweets)
    db_user=connection.cloud_native.users
    db_tweet=connection.cloud_native.tweets
    user=db_user.find({'username':new_tweets['username']})
    for i in user:
        api_list.append(str(i))
    if api_list == []:
        abort(404)
    else:
        db_tweet.insert_one(new_tweets)
        return "success"

@app.route('/api/v2/tweets/<int:id>', methods=['GET'])
def get_tweet(id):
    return list_tweet(id)

def list_tweet(user_id):
    db=connection.cloud_native.tweets
    api_list=[]
    tweet=db.find({'id':int(user_id)})
    for i in tweet:
        api_list.append(str(i))
    if api_list == []:
        abort(404)
    return jsonify({'tweet':api_list})

@app.route('/adduser')
def adduser():
    return render_template('adduser.html')

@app.route("/addtweets")
def addtweetsjs():
    return render_template("addtweets.html")

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/addname')
def addname():
    if request.args.get('yourname'):
        session['name'] = request.args.get('yourname')
        return redirect(url_for('main'))
    else:
        return render_template("addname.html",session=session)

@app.route('/clear')
def clearsession():
    session.clear()
    return redirect(url_for('main'))


connection=MongoClient("mongodb://localhost:27017")
def create_mongodatabase():
    try:
        dbnames=connection.list_database_names()
        if 'cloud_native' not in dbnames:
            db=connection.cloud_native.users
            db_tweets=connection.cloud_native.tweets
            db_api=connection.cloud_native.apirelease

            db.insert_one({
                "email":"eric.strom@google.com",
                "id": 33,
                "name": "Eric stromberg",
                "password": "eric@123",
                "username": "eric.strom"
            })

            db_tweets.insert_one({
                "body": "New blog post,Launch your app with the AWS Startup Kit!  # AWS",
                "id": 18,
                "timestamp": "2017-03-11T06:39:40Z",
                "tweetedby": "eric.strom"
            })

            db_api.insert_one({
                "buildtime": "2017-01-01 10:00:00",
                "links": "/api/v1/users",
                "methods": "get, post, put, delete",
                "version": "v1"
            })
            db_api.insert_one({
                "buildtime": "2017-02-11 10:00:00",
                "links": "api/v2/tweets",
                "methods": "get, post",
                "version": "2017-01-10 10:00:00"
            })
            print("Database Initialize completed!")
        else:
            print("Database already Initialized!")
    except:
        print("Database Initialize failed!")


if __name__ == '__main__':
    create_mongodatabase()
    app.run(host='0.0.0.0', port=50000, debug=True)