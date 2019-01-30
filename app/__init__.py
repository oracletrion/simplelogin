from flask import Flask, jsonify, render_template, url_for, request, session, redirect, Markup, flash
from flask_pymongo import PyMongo
import bcrypt
from app import model

def create_app():
    app = Flask(__name__, template_folder='../templates')

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
        
        login_user = model.findOne(mongo, request.form['username'])

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
            
            existing_user = model.findOne(mongo, request.form['username'])

            if existing_user is None:
                model.userInsert(mongo, request.form['username'], request.form['pass'])
                session['username'] = request.form['username']
                return redirect(url_for('index'))
        
            
            return 'That username already exists!'

        return render_template('register.html')

    @app.route('/reset', methods=['POST'])
    def reset():
        model.resetPass(mongo, session['username'], request.form['pass'])
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

        
    return app