from flask import Flask, jsonify, render_template, url_for, request, session, redirect, Markup, flash
from flask_pymongo import PyMongo
import bcrypt



app = Flask(__name__)

app.config['MONGO_DBN'] = 'mongoapidb'
app.config['MONGO_URI'] = 'mongodb://nachos:cheese1@ds111025.mlab.com:11025/mongoapidb'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
mongo = PyMongo(app) 

#login

@app.route('/')
def index():
    if 'username' in session:

        mess = "<h3>You are logged in as " + session['username'] +"</h3>"
        messages = Markup(mess)
        
        flash(messages)
        return render_template('logout.html')

    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})

    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
            session['username'] = request.form['username']
            
            mess = "<h3>You are logged in as " + session['username'] +"</h3>"
            messages = Markup(mess)
        
            flash(messages)
            return render_template('logout.html')#redirect(url_for('index'))
          

    session.pop('username', None)
    message = Markup("<h1>Incorrect Username and/or Password</h1>")    
    flash(message)
    return render_template('index.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            
            users.insert({'name' : request.form['username'], 'password' : hashpass.decode('utf-8')}) #works only in python3
            #users.insert({'name' : request.form['username'], 'password' : hashpass}) #this works only in python2
            session['username'] = request.form['username']
            return redirect(url_for('index'))
     
        
        return 'That username already exists!'

    return render_template('register.html')

@app.route('/reset', methods=['POST'])
def reset():
    users = mongo.db.users
    reuser = users.find_one({'name' : session['username']})
    hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
    reuser['password'] = hashpass.decode('utf-8')
    users.save(reuser)
    mess = "<h3>You are logged in as " + session['username'] +"</h3>"
    messages = Markup(mess)
        
    flash(messages)
    return render_template('logout.html')
    


@app.route('/sign_out')
def sign_out():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/change.html')
def change():
    return render_template('change.html')

if __name__ == '__main__':
    app.run(debug=False)