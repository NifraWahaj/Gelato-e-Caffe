import json
from flask import Flask, send_file, request, redirect, render_template, jsonify, make_response
import mysql.connector
import io

app = Flask(__name__, template_folder='FrontEnd/templates', static_folder='FrontEnd/static')

login_user = ''
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="r13Bne3@7",
    database="gelatoecaffè"
)
cursor = db.cursor()

@app.route('/')
def homepage():
    return render_template('Home.html')

@app.route('/SignUp', methods=['GET'])
def signup():
    return render_template('SignUp.html')

@app.route('/LogIn', methods=['GET'])
def login():
    return render_template('LogIn.html')

@app.route('/SignUp', methods=['POST'])
def handle_signup():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    sql = "INSERT INTO User (UserName, Email, password) VALUES (%s, %s, %s)"
    values = (username, email, password)
    cursor.execute(sql, values)
    db.commit()

    global login_user 
    login_user = email
    return handle_menu()
    
@app.route('/LogIn', methods=['POST'])
def handle_login():
    email = request.form['email']
    password = request.form['password']

    sql = "SELECT * FROM User WHERE Email=%s and password=%s"
    values = (email, password)
    cursor.execute(sql, values)
    user = cursor.fetchone()

    if user:
        global login_user
        login_user = email

        if user[0]=='1':
            return '' #return render_template('admin.html')
        else:
            return handle_menu()
    else:
        print('Error---------------------------------------------------------------------------------------')

@app.route('/menu', methods=['GET'])
def handle_menu():
    sql = "SELECT * FROM Menu"
    cursor.execute(sql)
    menu = cursor.fetchall()
    print("menu",menu)
    sql = "SELECT * FROM Category"
    cursor.execute(sql)
    categories = cursor.fetchall()
    print("categories",categories)
    return render_template('Menu.html', menu=menu, categories=categories)

@app.route('/AdminHome')
def admin_home():
    return render_template('AdminHome.html')

@app.route('/AdminMenu')
def admin_menu():
    sql = "SELECT * FROM Menu"
    cursor.execute(sql)
    menu = cursor.fetchall()
    #print("menu", menu)  #debug

    sql = "SELECT * FROM Category"
    cursor.execute(sql)
    categories = cursor.fetchall()
    #print("categories", categories)  # debug

    return render_template('AdminMenu.html', menu=menu, categories=categories)

@app.route('/Reviews', methods=['GET'])
def reviews():
    return render_template('Reviews.html')

if __name__ == '__main__':
    app.run(debug=True)
