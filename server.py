import json
from flask import Flask, send_file, request, redirect, render_template, jsonify, make_response,url_for
import mysql.connector
import io
from datetime import datetime

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

        if user[0]==1:
            return admin_home()
        else:
            return homepage()
    else:
        print('Error---------------------------------------------------------------------------------------')

@app.route('/menu', methods=['GET'])
def handle_menu():
    sql = "SELECT * FROM Menu"
    cursor.execute(sql)
    menu = cursor.fetchall()
    print("menu", menu)
    sql = "SELECT * FROM Category"
    cursor.execute(sql)
    categories = cursor.fetchall()
    print("categories", categories)

    #first category as default category
    default_category = categories[0][1] if categories else None

    return render_template('Menu.html', menu=menu, categories=categories, default_category=default_category)


@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if login_user:
        item_id = request.json['itemId']
        print(item_id)
        sql_user = "SELECT UserID FROM User WHERE Email = %s"
        cursor.execute(sql_user, (login_user,))
        user = cursor.fetchone()
        if user:
            sql = "SELECT * FROM Cart WHERE UserID=%s and MItemID=%s"
            values = (user[0], item_id)
            cursor.execute(sql, values)
            exist = cursor.fetchone()
            if exist:
                return jsonify({'msg': ' already exists in the cart'})
            else:
                insert_query = "INSERT INTO Cart (UserID, MItemID) VALUES (%s, %s)"
                values = (user[0], item_id)
                cursor.execute(insert_query, values)
                db.commit()
                return jsonify({'msg': ' added to cart successfully'})
        else:
            return jsonify({'msg': 'User not found'}), 400
    else:
        return jsonify({'msg': 'Login is required for adding item to cart'}), 401


@app.route('/Cart')
def cart():
    if login_user:
        sql_user = "SELECT UserID FROM User WHERE Email = %s"
        cursor.execute(sql_user, (login_user,))
        user = cursor.fetchone()
        sql = "SELECT m.*,c.Quantity FROM Menu m, Cart c WHERE UserID=%s and m.MItemID=c.MItemID"
        values = (user[0],)
        cursor.execute(sql, values)
        cart = cursor.fetchall()
        
        sql = "SELECT SUM(m.Price * c.Quantity) AS TotalPrice FROM Cart c, Menu m WHERE UserID=%s and m.MItemID=c.MItemID"
        values = (user[0],)
        cursor.execute(sql, values)
        total = cursor.fetchone()
        total_price = total[0] if total and total[0] is not None else 0
        tax = total_price % 2 if total_price else 0
        return render_template('Cart.html', cart=cart, total=total_price, tax=tax)
    else:
        return "Login required"

@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    if login_user:
        item_id = request.json['itemId']
        print(item_id)
        sql_user = "SELECT UserID FROM User WHERE Email = %s"
        cursor.execute(sql_user, (login_user,))
        user = cursor.fetchone()
        if user:
            sql = "Delete FROM Cart WHERE UserID=%s and MItemID=%s"
            values = (user[0], item_id)
            cursor.execute(sql, values)
            db.commit()
            return jsonify({'redirect_url': url_for('cart')})
        else:
            return jsonify({'msg': 'User not found'}), 400
    else:
        return jsonify({'msg': 'Login is required for adding item to cart'}), 401

@app.route('/change_quanity', methods=['POST'])
def change_quanity():
    if login_user:
        item_id = request.json['itemId']
        quantity = request.json['quantity']
        print(item_id)
        sql_user = "SELECT UserID FROM User WHERE Email = %s"
        cursor.execute(sql_user, (login_user,))
        user = cursor.fetchone()
        if user:
            sql = "UPDATE Cart SET Quantity =%s WHERE UserID=%s and MItemID=%s"
            values = (quantity, user[0], item_id)
            cursor.execute(sql, values)
            db.commit()
            return jsonify({'redirect_url': url_for('cart')})
        else:
            return jsonify({'msg': 'User not found'}), 400
    else:
        return jsonify({'msg': 'Login is required for adding item to cart'}), 401

@app.route('/checkout', methods=['POST'])
def checkout():
    if login_user:
        sql_user = "SELECT UserID FROM User WHERE Email = %s"
        cursor.execute(sql_user, (login_user,))
        user = cursor.fetchone()

        cart_items_query = "SELECT MItemID, Quantity FROM Cart WHERE UserID = %s"
        cursor.execute(cart_items_query, (user[0],))
        cart_items = cursor.fetchall()

        if cart_items:
            order_time = datetime.now()
            insert_order_query = "INSERT INTO Orders (UserID, MItemID, Quantity, TimeDate) VALUES (%s, %s, %s, %s)"
            for item in cart_items:
                values = (user[0], item[0], item[1], order_time)
                cursor.execute(insert_order_query, values)
            db.commit()

            delete_cart_query = "DELETE FROM Cart WHERE UserID = %s"
            cursor.execute(delete_cart_query, (user[0],))
            db.commit()

            return jsonify({'redirect_url': url_for('cart')})
        else:
            return jsonify({'msg': 'Cart is empty'}), 400
        
    else:
        return jsonify({'msg': 'Login is required for checkout'}), 401


@app.route('/Reservation', methods=['GET', 'POST'])
def reservation():
    if request.method == 'POST':
        if login_user:
            name = request.form['name']
            date = request.form['date']
            time_slot = request.form['time-slot']
            seats = request.form['seats']
            print(name,date,time_slot,seats)
            sql_user = "SELECT UserID FROM User WHERE Email = %s"
            cursor.execute(sql_user, (login_user,))
            user = cursor.fetchone()
            cursor.execute("SELECT TableID FROM Tables WHERE NumberOfSeats >= %s AND TableID NOT IN (SELECT TableID FROM Reservations WHERE ReservationDate = %s AND TimeSlot = %s) ORDER BY NumberOfSeats ASC LIMIT 1", (seats, date, time_slot))
            table = cursor.fetchone()
            if user:
                if table:
                    table_id = table[0]
                    user_id = user[0]
                    print("hehe:",name, date, seats, time_slot, user_id, table_id)
                    insert_query = "INSERT INTO Reservations (CustomerName, ReservationDate, NumberOfSeats, TimeSlot, UserID, TableID) VALUES (%s, %s, %s, %s, %s, %s)"
                    values = (name, date, seats, time_slot, user_id, table_id)
                    cursor.execute(insert_query, values)
                    db.commit()

                    return render_template('Reservation.html',table_Number=table_id)

                else:
                    return "No available tables for the requested number of seats."
            else:
                return "User not found"
        else:
            return "Login required"
    else:
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

    return render_template('AdminReview.html',total_reviews=total_reviews, avg_rating=avg_rating, rating_counts=rating_counts)

@app.route('/admin_reviews_json')
def admin_reviews_json():
    sql_fetch_reviews = "SELECT R.ReviewID, U.UserName, R.Rating, R.Comments, R.entry_date FROM Review R, User U WHERE R.UserID = U.UserID ORDER BY ReviewID DESC"
    cursor.execute(sql_fetch_reviews)
    reviews = cursor.fetchall()

    reviews_json = [{'ReviewID': review[0], 'UserName': review[1], 'Rating': review[2], 'Comments': review[3], 'entry_date': review[4]} for review in reviews]

    return jsonify({'reviews': reviews_json})

@app.route('/AdminReservation')
def admin_reservation():
    sql = "SELECT * FROM Reservations r, Tables t where r.TableID = t.TableID Order by ReservationDate, TimeSlot"
    cursor.execute(sql)
    reservations = cursor.fetchall()
    return render_template('AdminReservation.html', reservations=reservations)

@app.route('/AdminMenu', methods=['GET'])
def admin_menu():
    sql = "SELECT * FROM Menu"
    cursor.execute(sql)
    menu = cursor.fetchall()

    sql = "SELECT * FROM Category"
    cursor.execute(sql)
    categories = cursor.fetchall()

    #first category as default 
    sql_default_category = "SELECT CategoryName FROM Category LIMIT 1"
    cursor.execute(sql_default_category)
    default_category_tuple = cursor.fetchone()
    default_category = default_category_tuple[0] if default_category_tuple else None

    search_query = request.args.get('search-query', '')

    if search_query:
            sql = f"""
                SELECT Menu.*, Category.CategoryName
                FROM Menu
                JOIN Category ON Menu.CategoryID = Category.CategoryID
                WHERE Menu.MenuItem LIKE '{search_query}'
            """
            print(f"Search Query SQL: {sql}")
    

    print(f"Final SQL: {sql}")

    return render_template('AdminMenu.html', menu=menu, default_category=default_category, categories=categories)


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
    sql_fetch_reviews = "SELECT R.ReviewID ,U.UserName, R.Rating, R.Comments FROM Review R, User U where R.UserID = U.UserID ORDER BY ReviewID DESC LIMIT 5"
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
