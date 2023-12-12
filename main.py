from flask import Flask, render_template
from flask_mysqldb import MySQL
import pymysql
from dotenv import load_dotenv
from os import getenv

#haha

app = Flask(__name__)

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "jasminrap"
# app.config['MYSQL_PASSWORD'] = "1234"
app.config['MYSQL_DB'] = "JJRREClothingLine"



@app.route("/")
def welcome():
    return render_template('welcome.html')

@app.route("/register")
def register():
    return render_template('register.html')


@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/addCart")
def addCart():
    return render_template('addCart.html')

@app.route("/checkout")
def checkout():
    return render_template('checkout.html')


@app.route("/admin")
def admin():
    return render_template('admin.html')

@app.route("/verification")
def email_verification():

    return render_template('verification.html')


@app.route("/storage")
def storage():
    return render_template('storage.html')

@app.route("/addStorage")
def addStorage():
    return render_template('addstorage.html')


if __name__ =='__main__':
    app.run(debug=True)



