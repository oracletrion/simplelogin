from flask import Flask, jsonify, render_template, url_for, request, session, redirect, Markup, flash
from flask_pymongo import PyMongo
import sys
import bcrypt

def findOne(mongo, username):
    users = mongo.db.users
    return users.find_one({'name' : username})



def userInsert(mongo, username, password):
    if sys.version_info[0] < 3:
        return 'Please use python 3.6.4'
    else:
        users = mongo.db.users
        hashpass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        users.insert({'name' : username, 'password' : hashpass.decode('utf-8')}) #works only in python3
        #users.insert({'name' : request.form['username'], 'password' : hashpass}) #this works only in python2


def resetPass(mongo, username, password):
    users = mongo.db.users
    reuser = users.find_one({'name' : session['username']})
    hashpass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    reuser['password'] = hashpass.decode('utf-8')
    users.save(reuser)