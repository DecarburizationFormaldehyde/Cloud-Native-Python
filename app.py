import random
from os.path import exists
from sqlite3.dbapi2 import apilevel

from flask import flash
from time import strftime, gmtime
from flask import render_template, redirect, session, url_for,abort

from flask import Flask, render_template, request,jsonify,make_response
import sqlite3

from flask_cors import CORS,cross_origin

from pymongo import MongoClient
import bcrypt

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

@app.route('/api/v1/session-user', methods=['GET'])
def get_session_user():
    # 检查用户是否已登录
    if 'username' in session and session.get('logged_in'):
        return jsonify({'username': session['username']}), 200
    else:
        return jsonify({'error': 'Not logged in'}), 401

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
        # 对密码进行哈希处理
        if 'password' in new_user and new_user['password']:
            new_user['password'] = bcrypt.hashpw(new_user['password'].encode('utf-8'), bcrypt.gensalt())
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
        # 如果更新包含密码，需要进行哈希处理
        if 'password' in user and user['password']:
            user['password'] = bcrypt.hashpw(user['password'].encode('utf-8'), bcrypt.gensalt())
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
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('index.html',name=session['logged_in'])
@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/login', methods=['POST', 'GET'])
def do_admin_login():
    if request.method == 'POST':
        users = connection.cloud_native.users
        api_list=[]
        login_user=users.find({'username':request.form['username']})
        for i in login_user:
            api_list.append(i)
        print(api_list)
        if api_list != []:
            # 验证密码
            user = api_list[0]
            # 确保密码是字节类型用于bcrypt验证
            password_from_db = user['password']
            if isinstance(password_from_db, str):
                password_from_db = password_from_db.encode('utf-8')
            if bcrypt.checkpw(request.form['password'].encode('utf-8'), password_from_db):
                session['logged_in'] = user['username']
                session['username']=user['username']
                return redirect(url_for('index'))
            return 'Invalid username/password!'
        else:
            flash("Invalid Authentication")

        return 'Invalid User!'
    else:
        if not session.get('logged_in'):
            return render_template('login.html')
        else:
            return redirect(url_for('index'))

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        users = connection.cloud_native.users
        api_list=[]
        existing_user = users.find({'username': request.form['username']})
        for i in existing_user:
            api_list.append(i)
        if api_list == []:
            users.insert_one(
                {
                    'email':request.form['email'],
                    'id':random.randint(1,1000),
                    "name":request.form['name'],
                    'username': request.form['username'],
                    'password': bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
                }
            )
            session['username']=request.form['username']
            return redirect(url_for('home'))
        return 'That username already exists!'
    else:
        return render_template('signup.html')

@app.route('/profile',methods=['GET', 'POST'])
def profile():
    if request.method =='POST':
        users=connection.cloud_native.users
        api_list=[]
        existing_users=users.find({'username':session['username']})
        for i in existing_users:
            api_list.append(i)
        user={}
        if api_list != []:
            print(request.form['email'])
            user['email']=request.form['email']
            user['username']=request.form['username']
            user['password']=bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.update_one({'username':session['username']},{'$set':user})
        else:
            return 'Invalid User!'
        return redirect(url_for('index'))
    else:
        users=connection.cloud_native.users
        user=[]
        existing_users=users.find({'username':session['username']})
        for i in existing_users:
            user.append(i)
        return render_template('profile.html',name=user[0]['name'],username=user[0]['username'],email=user[0]['email'],password=user[0]['password'])

@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect(url_for('home'))

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
                "password": bcrypt.hashpw("eric@123".encode('utf-8'), bcrypt.gensalt()),
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