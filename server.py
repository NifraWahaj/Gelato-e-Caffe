import json
from flask import Flask, send_file, request, redirect, render_template, jsonify, make_response,url_for
import mysql.connector
import io

app = Flask(__name__, template_folder='FrontEnd/templates', static_folder='FrontEnd/static')

login_user = ''
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="patanahi",
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

@app.route('/Cart')
def cart():
    return render_template('Cart.html')

@app.route('/Reservation', methods=['GET', 'POST'])
def reservation():
    if request.method == 'POST':
        name = request.form['name']
        date = request.form['date']
        time_slot = request.form['time-slot']
        seats = request.form['seats']
        print(name,date,time_slot,seats)
        sql_user = "SELECT UserID FROM User WHERE Email = %s"
        cursor.execute(sql_user, (login_user,))
        user = cursor.fetchone()

        if user:
            user_id = user[0]
            insert_query = "INSERT INTO Reservations (CustomerName, ReservationDate, NumberOfSeats, TimeSlot, UserID) VALUES (%s, %s, %s, %s, %s)"
            values = (name, date, seats, time_slot, user_id)
            cursor.execute(insert_query, values)
            db.commit()

        return "Reservation successfully added to the database!"

    return render_template('Reservation.html')

@app.route('/AdminHome')
def admin_home():
    return render_template('AdminHome.html')

@app.route('/AdminReview')
def admin_review():
    cursor.execute("SELECT COUNT(*) FROM Review")
    total_reviews = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(Rating) FROM Review")
    avg_rating = cursor.fetchone()[0]

    cursor.execute("SELECT Rating, COUNT(*) FROM Review GROUP BY Rating ORDER BY Rating DESC")
    rating_counts = cursor.fetchall()

    # Return the rendered template along with reviews as JSON
    return render_template('AdminReview.html',total_reviews=total_reviews, avg_rating=avg_rating, rating_counts=rating_counts)

@app.route('/admin_reviews_json')
def admin_reviews_json():
    sql_fetch_reviews = "SELECT R.ReviewID, U.UserName, R.Rating, R.Comments, R.entry_date FROM Review R, User U WHERE R.UserID = U.UserID ORDER BY ReviewID DESC"
    cursor.execute(sql_fetch_reviews)
    reviews = cursor.fetchall()

    # Convert the reviews data to a JSON object
    reviews_json = [{'ReviewID': review[0], 'UserName': review[1], 'Rating': review[2], 'Comments': review[3], 'entry_date': review[4]} for review in reviews]

    return jsonify({'reviews': reviews_json})

@app.route('/AdminReservation')
def admin_reservation():
    return render_template('AdminReservation.html')

@app.route('/AdminMenu', methods=['GET'])
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

@app.route('/AdminMenuCategory', methods=['POST'])
def addCategories():
    CategoryName = request.json['categoryName']
    print("CategoryName:", CategoryName)
    sql = "INSERT INTO Category(CategoryName) VALUES (%s)"
    values = (CategoryName,) 
    cursor.execute(sql, values)
    db.commit()

    if cursor.rowcount > 0:
        return jsonify({'redirect_url': url_for('admin_menu')})
    else:
        return jsonify({'msg': "Sorry, the category could not be added"})




@app.route('/AdminMenuItem', methods=['POST'])
def addMenuItems():
    ItemName = request.json['ItemName']
    ItemPrice = request.json['ItemPrice']
    ItemDescription = request.json['ItemDescription']
    ItemCategory = request.json['CategoryName']

    sql1 = "SELECT CategoryID FROM Category WHERE CategoryName=%s"
    values1 = (ItemCategory,)
    cursor.execute(sql1, values1)
    categoryID = cursor.fetchone()

    if categoryID:
        sql2 = "INSERT INTO Menu(MenuItem, Description, Price, CategoryID) VALUES (%s, %s, %s, %s)"
        values2 = (ItemName, ItemDescription, ItemPrice, categoryID[0])
        cursor.execute(sql2, values2)
        db.commit()
        if cursor.rowcount > 0:
            return jsonify({'redirect_url': url_for('admin_menu')})
        else:
            return jsonify({'msg': "Sorry, the Menu Item cannot be added"})
    else:
        return jsonify({'msg': "Sorry, this category does not exist"})



@app.route('/Reviews', methods=['POST'])
def reviews():
    if login_user:
        comment = request.form['comment']
        rating = int(request.form['rating']) 

        sql_user = "SELECT UserID FROM User WHERE Email = %s"
        cursor.execute(sql_user, (login_user,))
        user = cursor.fetchone()

        if user:
            user_id = user[0]

            sql_insert_review = "INSERT INTO Review (UserID, Rating, Comments) VALUES (%s, %s, %s)"
            review_values = (user_id, rating, comment)
            cursor.execute(sql_insert_review, review_values)
            db.commit()

            return review()
        else:
            return "User not found"
    else:
        return "Login required"

@app.route('/Reviews', methods=['GET'])
def review():
    sql_fetch_reviews = "SELECT R.ReviewID ,U.UserName, R.Rating, R.Comments FROM Review R, User U where R.UserID = U.UserID ORDER BY ReviewID DESC"
    cursor.execute(sql_fetch_reviews)
    reviews = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM Review")
    total_reviews = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(Rating) FROM Review")
    avg_rating = cursor.fetchone()[0]

    cursor.execute("SELECT Rating, COUNT(*) FROM Review GROUP BY Rating ORDER BY Rating DESC")
    rating_counts = cursor.fetchall()

    print(reviews)
    return render_template('Reviews.html', reviews=reviews,total_reviews=total_reviews, avg_rating=avg_rating, rating_counts=rating_counts)

if __name__ == '__main__':
    app.run(debug=True)
