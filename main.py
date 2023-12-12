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
# app.config['MYSQL_PASSWORD'] = "ellan"
app.config['MYSQL_DB'] = "JJRREClothingLine"
#hehe


@app.route("/")
def welcome():
    return render_template('welcome.html')

#ellan
@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        uname = request.form['txtUname']
        fname = request.form['txtFname']
        lname = request.form['txtLname']
        pwd = request.form['txtPwd']
        phone = request.form['phoneNumber']
        email = request.form['emailAddress']
        uType = 0
        vUser = 1
#hello
        con = mysql.connection
        cursor = con.cursor()

        sql_check_username = f"SELECT * FROM customers WHERE username='{uname}'"
        cursor.execute(sql_check_username)
        row = cursor.fetchone()

        if not row:
            verification_code = generate_verification_code()
            sql_insert_customer = f"INSERT INTO customers VALUES ('{uname}', '{fname}', '{lname}', '{pwd}', '{phone}', '{email}', '{uType}', '{verification_code}', '{vUser}')"
            cursor.execute(sql_insert_customer)
            con.commit()

            return redirect(url_for('welcome'))  # Redirect to the welcome page or any other page after registration
        else:
            return "<script language='javascript'>alert('Username already exists');</script>"

    return render_template('register.html')

def generate_verification_code():
    import random
    import string

    characters = string.ascii_letters + string.digits
    code_length = 8
    code = ''.join(random.choice(characters) for _ in range(code_length))
    return code

#ellan
@app.route("/login")
def login():
    return render_template('login.html')

#rey
@app.route("/addCart")
def addCart():
    return render_template('addCart.html')

#rey
@app.route("/checkout")
def checkout():
    return render_template('checkout.html')


#jobeteezy
@app.route("/admin")
def admin():
    return render_template('admin.html')

#rey
@app.route("/verification")
def email_verification():

    return render_template('verification.html')


#jobeteezy
@app.route("/storage")
def storage():
    return render_template('storage.html')

#rhyss
@app.route("/addStorage")
def addStorage():
    return render_template('addstorage.html')


if __name__ =='__main__':
    app.run(debug=True)



