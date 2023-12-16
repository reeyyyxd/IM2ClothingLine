from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
import pymysql



app = Flask(__name__)
app.secret_key = '123123'

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "jasminrap"
# app.config['MYSQL_PASSWORD'] = "1234"
# app.config['MYSQL_PASSWORD'] = "ellan"
app.config['MYSQL_DB'] = "JJRREClothingLine"


def get_mysql_connection():
    return pymysql.connect(host=app.config['MYSQL_HOST'],
                           user=app.config['MYSQL_USER'],
                           password=app.config['MYSQL_PASSWORD'],
                           database=app.config['MYSQL_DB'],
                           cursorclass=pymysql.cursors.DictCursor)
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

        connection = get_mysql_connection()
        cursor = connection.cursor()

        # Check if the username already exists
        cursor.execute("SELECT * FROM customers WHERE username=%s", (uname,))
        row = cursor.fetchone()

        if not row:
            # Generate a verification code
            verification_code = generate_verification_code()

            # Insert new record into the customers table
            cursor.execute("INSERT INTO customers VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                           (uname, fname, lname, pwd, phone, email, uType, verification_code, vUser))

            connection.commit()
            connection.close()

            return ("<script language='javascript'>alert('Registration successful. Redirecting to login.');"
                    " window.location.href = '/login';</script>")
        else:
            return ("<script language='javascript'>alert('Username exists');"
                    " window.location.href = '/register';</script>")

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
    if request.method == 'POST' and 'btnLogin' in request.form:
        username = request.form['username']
        password = request.form['password']

        connection = get_mysql_connection()
        cursor = connection.cursor()

        # Check if user is verified
        cursor.execute("SELECT *, IF(verificationCode IS NULL, 1, 0) AS verifiedUser FROM customers WHERE username=%s",
                       (username,))
        row = cursor.fetchone()

        if row and row['verifiedUser'] == 0:
            if row['password'] != password:
                return "<script language='javascript'>alert('Password is incorrect.'); window.history.back();</script>"

            if row['userType'] == 0:
                session['username'] = row['username']
                return redirect(url_for('addCart'))
            else:
                session['username'] = row['username']
                return redirect(url_for('admin'))

        elif row and row['verifiedUser'] == 1:
            return ("<script language='javascript'>alert('Wait for the admin to verify your account.');"
                    " window.history.back();</script>")
        else:
            return "<script language='javascript'>alert('Username not existing.'); window.history.back();</script>"

    return render_template('login.html')

#pra mo push
#rey
@app.route("/addCart", methods=['GET', 'POST'])
def addCart():
    connection = get_mysql_connection()
    cursor = connection.cursor()

    # Fetch product
    cursor.execute("SELECT * FROM product")
    all_product = cursor.fetchall()

    # Fetch Category
    all_categories = all_product  # Assuming all products are also categories

    if request.method == 'POST' and 'submit' in request.form:
        productname = request.form['txtProductName']
        description = request.form['txtDescription']
        quantity = int(request.form['txtQuantity'])

        cursor.execute("SELECT * FROM product WHERE UPPER(product_name) = UPPER(%s) AND description = %s",
                       (productname, description))
        row = cursor.fetchone()

        if row:
            productID = row['product_id']
            price = row['price']

            cursor.execute("SELECT * FROM inventory WHERE prod_id=%s", (productID,))
            row_inventory = cursor.fetchone()

            if row_inventory['stock'] >= quantity:
                total_payment = price * quantity

                # Decrease the stock in inventory
                new_stock = row_inventory['stock'] - quantity

                # Check if there is enough stock to fulfill the order
                if new_stock >= 0:
                    cursor.execute("UPDATE inventory SET stock = %s WHERE prod_id = %s", (new_stock, productID))

                    cursor.execute("SELECT * FROM payment WHERE username=%s", (session['username'],))
                    row_payment = cursor.fetchone()

                    if row_payment:
                        total_payment += row_payment['totalAmountPayment']
                        cursor.execute("UPDATE payment SET totalAmountPayment = %s WHERE username = %s",
                                       (total_payment, session['username']))
                    else:
                        # Check if the user has a record in the payment table
                        cursor.execute("SELECT * FROM payment WHERE username = %s", (session['username'],))
                        existing_payment_row = cursor.fetchone()

                        if existing_payment_row:
                            # Update existing record
                            cursor.execute("UPDATE payment SET totalAmountPayment = %s WHERE username = %s",
                                           (total_payment, session['username']))
                        else:
                            # Insert new record
                            cursor.execute("INSERT INTO payment (totalAmountPayment, username) VALUES (%s, %s)",
                                           (total_payment, session['username']))

                    connection.commit()
                    session['payment'] = total_payment

                    return ("<script language='javascript'>alert('Item/s added to cart');"
                            "window.location.href = "
                            "'/addCart';</script>")
                else:
                    # Insufficient stock, return JSON response for JavaScript alert
                    return "<script language='javascript'>alert('Not enough stock/s');</script>"
            else:
                # Insufficient stock, return JSON response for JavaScript alert
                return "<script language='javascript'>alert('Not enough stock/s');</script>"
        else:
            # Product not found, return JSON response for JavaScript alert
            return "<script language='javascript'>alert('Product not found');</script>"

    connection.close()

    return render_template('addCart.html', all_product=all_product, all_categories=all_categories)


#rey
@app.route("/checkout", methods=['GET', 'POST'])
def checkout():
    connection = get_mysql_connection()
    cursor = connection.cursor()

    if request.method == 'POST' and 'btnOrder' in request.form:
        payment = float(request.form['money'])

        balance = 0
        cursor.execute("SELECT * FROM payment WHERE username=%s", (session['username'],))
        row = cursor.fetchone()

        if row['totalAmountPayment'] > payment:
            return "<script language='javascript'>alert('Insufficient Funds'); window.history.back();</script>"
        elif row['totalAmountPayment'] < payment:
            balance = payment - row['totalAmountPayment']
            cursor.execute("UPDATE payment SET totalAmountPayment=0 WHERE username=%s", (session['username'],))
            connection.commit()
            return ("<script language='javascript'>"
                    "alert('Thank you for purchasing from us. Your change is P" + str(balance) + "');"
                                                                                                 "window.location.href "
                                                                                                 "= '/addCart';"
                                                                                                 "</script>")
    connection.close()

    return render_template('checkout.html')



#jobeteezy
@app.route("/admin")
def admin():
    if 'Username' in session:
        return render_template('admin.html')
    else:
        return redirect(url_for('login'))

#rey
@app.route("/verification", methods=['GET', 'POST'])
def email_verification():
    connection = get_mysql_connection()
    cursor = connection.cursor()

    # Verify Email
    if request.method == 'POST' and 'btnVerify' in request.form:
        verification_code = request.form['verificationCode']
        username = request.form['username']

        cursor.execute("SELECT * FROM customers WHERE username=%s AND verificationCode=%s",
                       (username, verification_code))
        row = cursor.fetchone()

        if row:
            # Update the user's verification status
            cursor.execute("UPDATE customers SET verificationCode='', verifiedUser=0 WHERE username=%s", (username,))

            connection.commit()

            render_template('verification.html')

            return ("<script language='javascript'>alert('Customer has been verified.');"
                    " window.history.back();</script>")

        else:
            return ("<script language='javascript'>alert('Invalid verification code. Please try again.');"
                    " window.history.back();</script>")

    # Fetch Registered Users
    users = fetch_registered_users(cursor)

    connection.close()

    return render_template('verification.html', users=users)


def fetch_registered_users(cursor):
    cursor.execute("SELECT *, IF(verificationCode IS NULL, 1, 0) AS verifiedUser FROM customers")
    return cursor.fetchall()

#jobeteezy
@app.route("/storage")
def storage():
    connection = get_mysql_connection()
    cursor = connection.cursor()

    # Fetch product and inventory data
    cursor.execute("SELECT * FROM product")
    prod_result = cursor.fetchall()

    display_data = []
    for p_row in prod_result:
        cursor.execute("SELECT * FROM inventory WHERE inventory_id=%s AND prod_id=%s",
                       (p_row['inventory_id'], p_row['product_id']))
        inven_row = cursor.fetchone()

        if inven_row:
            display_data.append({
                'product_id': p_row['product_id'],
                'product_name': p_row['product_name'],
                'price': p_row['price'],
                'stock': inven_row['stock']
            })

    connection.close()

    return render_template('storage.html', storage_data=display_data)
    return render_template('checkout.html')


@app.route("/update_product", methods=['PUT'])
def update_product():
    data = request.get_json()

    product_id = data.get('product_id')
    new_name = data.get('new_name')
    new_price = data.get('new_price')
    new_quantity = data.get('new_quantity')

    connection = get_mysql_connection()
    cursor = connection.cursor()

    # Update product information
    cursor.execute("UPDATE product SET product_name=%s, price=%s WHERE product_id=%s",
                   (new_name, new_price, product_id))

    # Update inventory information
    cursor.execute("UPDATE inventory SET stock=%s WHERE prod_id=%s", (new_quantity, product_id))

    connection.commit()
    connection.close()

    return jsonify({'message': 'Product updated successfully'})


@app.route("/delete_product/<int:product_id>", methods=['DELETE'])
def delete_product(product_id):
    connection = get_mysql_connection()
    cursor = connection.cursor()

    # Delete product
    cursor.execute("DELETE FROM product WHERE product_id=%s", (product_id,))

    # Delete inventory
    cursor.execute("DELETE FROM inventory WHERE prod_id=%s", (product_id,))

    connection.commit()
    connection.close()

    return jsonify({'message': 'Product deleted successfully'})

#rhyss
@app.route("/addStorage", methods=['GET', 'POST'])
def addStorage():
    connection = get_mysql_connection()
    cursor = connection.cursor()

    if request.method == 'POST' and 'btnAddtoStorage' in request.form:
        product_name = request.form['txtProductName']
        description = request.form['txtDescription']
        stock = int(request.form['txtStock'])
        price = float(request.form['txtPrice'])
        product_id = 0

        cursor.execute("SELECT * FROM product")
        prod_result = cursor.fetchall()

        for row in prod_result:
            if product_name.upper() == row['product_name'].upper():
                product_id = row['product_id']
                cursor.execute("SELECT stock FROM inventory WHERE prod_id=%s", (product_id,))
                inventory_row = cursor.fetchone()

                if inventory_row:
                    stock += inventory_row['stock']
                    cursor.execute("UPDATE inventory SET stock=%s WHERE prod_id=%s", (stock, product_id))
                    connection.commit()
                    return render_template('addstorage.html', message='Updated Stock')

        cursor.execute("INSERT INTO product (product_name, description, price, inventory_id) VALUES (%s, %s, %s, %s)",
                       (product_name, description, price, 1))
        connection.commit()

        product_id = cursor.lastrowid
        cursor.execute("INSERT INTO inventory (inventory_id, stock, prod_id) VALUES (1, %s, %s)", (stock, product_id))
        connection.commit()

        return "<script language='javascript'>alert('Item Added'); window.history.back();</script>"

    connection.close()

    return render_template('addstorage.html')


if __name__ =='__main__':
    app.run(debug=True)



