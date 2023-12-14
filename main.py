from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
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

mysql=MySQL(app)

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
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']

        con = mysql.connection
        cursor = con.cursor()

        # Check if user is verified
        sql = f"SELECT *, IF(verificationCode IS NULL, 1, 0) AS verifiedUser FROM customers WHERE username='{uname}'"
        cursor.execute(sql)
        row = cursor.fetchone()

        if row and row[8] == 0:  # Assuming 'userType' is the 9th column (index 8)
            if row[3] != pwd:  # Assuming 'password' is the 4th column (index 3)
                return "<script language='javascript'>alert('Password not existing');</script>"
            else:
                if row[6] == 0:  # Assuming 'userType' is the 7th column (index 6)
                    session['username'] = row[0]  # Assuming 'username' is the 1st column (index 0)
                    return redirect('/addCart')
                elif row[6] == 1:  # Assuming 'userType' is the 7th column (index 6)
                    session['Username'] = row[0]  # Assuming 'username' is the 1st column (index 0)
                    return redirect('/admin')
                else:
                    return "<script language='javascript'>alert('Invalid user type');</script>"
        else:
            # User is not verified
            return "<script language='javascript'>alert('Wait for the admin to verify your account.');</script>"

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
    if 'Username' in session:
        return render_template('admin.html', username=session['Username'])
    else:
        return redirect(url_for('login'))

#rey
@app.route("/verification")
def email_verification():

    return render_template('verification.html')


#jobeteezy
@app.route("/storage")
def storage():
    cursor = mysql.connection.cursor()

    # Fetch product and inventory data from the database
    sql = "SELECT * FROM product"
    cursor.execute(sql)
    product_data = cursor.fetchall()

    display = []
    for p_row in product_data:
        sql = "SELECT * FROM inventory WHERE inventory_id = %s AND prod_id = %s"
        cursor.execute(sql, (p_row[4], p_row[0]))
        inventory_data = cursor.fetchone()

        if inventory_data:
            display.append({
                'product_id': p_row[0],
                'product_name': p_row[1],
                'price': p_row[3],
                'quantity': inventory_data[1],
            })

    return render_template('storage.html', display=display)

#rhyss
@app.route("/addStorage")
def addStorage():
    return render_template('addstorage.html')


if __name__ =='__main__':
    app.run(debug=True)



