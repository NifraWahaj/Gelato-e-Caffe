import json
from flask import Flask, send_file, request, redirect, render_template, jsonify, make_response,url_for
import mysql.connector
import io
from datetime import datetime
from flask import redirect, url_for, jsonify
from flask import session

app = Flask(__name__, template_folder='FrontEnd/templates', static_folder='FrontEnd/static')

login_user = ''

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="r13Bne3@7",
    database="gelatoecaffee"
)
cursor = db.cursor()
@app.route('/')
def homepage():
    is_logged_in = 'login_user' in session
    return render_template('Home.html', is_logged_in=is_logged_in)


@app.route('/logout')
def handle_logout():

    # session.pop('is_logged_in', None) to remove the 'is_logged_in' key
    session.pop('login_user', None) 
    session.clear() 
    return redirect(url_for('homepage'))

@app.route('/SignUp', methods=['GET'])
def signup():
    return render_template('SignUp.html')

@app.route('/LogIn', methods=['GET'])
def login():
    return render_template('LogIn.html')

# SIGN UP STORED PROCEDURE
@app.route('/SignUp', methods=['POST'])
def handle_signup():
    try:
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        obj = db.cursor()
        args = [email]
        obj.callproc('GetUserByEmail', args)
        result = obj.fetchone()

        print(f"Result: {result}")

        # resultnone
        if result is not None and result[0] is not None:
            return jsonify({'msg': 'User already exists'}), 400

        # insert a new user
        obj = db.cursor()
        args = [username, email, password]
        obj.callproc('InsertUser', args)
        db.commit()

        global login_user
        login_user = email

        return jsonify({'success': True}), 200

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return jsonify({'error': str(err)}), 500

# LOGIN STORED PROCEDURE 
@app.route('/LogIn', methods=['POST'])
def handle_login():
    try:
        email = request.form['email'].strip()
        password = request.form['password'].strip()

        cursor.callproc('GetUserByEmailAndPassword', (email, password)) #works
        results = cursor.stored_results()
        for result in results:
            user=result.fetchone()
        print(user)
        if user:
            
            global login_user
            login_user = email
            session['login_user'] = email  # Store user information in session
           # print(login_user)

            if user[0] == 1:
                return admin_home()
            else:
                return homepage()
        else:
            error_message = "Invalid email or password. Please try again."
            return jsonify({'error': error_message}), 401

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return jsonify({'error': str(err)}), 500

# MENU STORED PROCEDURE DONE
@app.route('/menu', methods=['GET'])
def handle_menu():
    is_logged_in = 'login_user' in session
    cursor.callproc("GetAllMenuItems")
    results_menu = cursor.stored_results()
    for result_menu in results_menu:
        menu = result_menu.fetchall()

    cursor.callproc("GetAllCategories")
    results_categories = cursor.stored_results()
    categories = []
    for result_categories in results_categories:
        for row in result_categories.fetchall():
            categories.append(row)

    default_category = categories[0][1] if categories else None

    return render_template('Menu.html', menu=menu, categories=categories, default_category=default_category, is_logged_in=is_logged_in)

##  instead of 'already exists in the cart' its inserting duplicates   -- Fixed
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if login_user:
        item_id = request.json['itemId']
        print(item_id)
        
        cursor.callproc("GetUserByEmail", (login_user,))
        results = cursor.stored_results()
        for result in results:
            user = result.fetchone()

        if user:
            #sql = "SELECT * FROM Cart WHERE UserID=%s and MItemID=%s"
            #values = (user[0], item_id)
            #cursor.execute(sql, values)
            #exist = cursor.fetchone()

            cursor.callproc("GetCartByUserIDAndMItemID", (user[0], item_id))
            exists = cursor.stored_results()
            for exist in exists:
                existing = exist.fetchone()
            if existing:
                return jsonify({'msg': ' already exists in the cart'})
            else:
                #insert_query = "INSERT INTO Cart (UserID, MItemID) VALUES (%s, %s)"
                #values = (user[0], item_id)
                #cursor.execute(insert_query, values)
                cursor.callproc("InsertIntoCart", (user[0], item_id))
                db.commit()

                return jsonify({'msg': ' added to cart successfully'})
        else:
            return jsonify({'msg': 'User not found'}), 400
    else:
        return jsonify({'msg': 'Login is required for adding item to cart'}), 401

# Cart STORED PROCEDURE DONE
@app.route('/Cart')
def cart():
    is_logged_in = 'login_user' in session
    if login_user:
        cursor.callproc("GetUserByEmail", (login_user,))
        results = cursor.stored_results()
        for result in results:
            user = result.fetchone()

        cursor.callproc("GetMenuAndCartByUserID", (user[0],))
        results_menu_cart = cursor.stored_results()

        # first result set 
        result_menu_cart = next(results_menu_cart, None)
        print(result_menu_cart)
        if result_menu_cart:
            cart = result_menu_cart.fetchall()
        else:
            cart = []
    

        cursor.callproc("CalculateTotalPrice", (user[0],))
        results_total_price = cursor.stored_results()

        result_total_price = next(results_total_price, None)

        if result_total_price:
            total_price = result_total_price.fetchone()[0]
        else:
            total_price = 0 

        total_price = total_price if total_price is not None else 0

        tax = total_price % 2 if total_price else 0
        return render_template('Cart.html', cart=cart, total=total_price, tax=tax, is_logged_in=is_logged_in)
    else:
        return redirect(url_for('login'))

# remove_from_cart STORED PROCEDURE DONE
@app.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    if login_user:
        item_id = request.json['itemId']
        print(item_id)

        cursor.callproc("GetUserByEmail", (login_user,))
        results = cursor.stored_results()
        for result in results:
            user = result.fetchone()

        if user:
            #sql = "Delete FROM Cart WHERE UserID=%s and MItemID=%s"
            #values = (user[0], item_id)
            #cursor.execute(sql, values)
            cursor.callproc("DeleteCartItem", (user[0], item_id))
            db.commit()
            return jsonify({'redirect_url': url_for('cart')})
        else:
            return jsonify({'msg': 'User not found'}), 400
    else:
        return jsonify({'msg': 'Login is required for adding item to cart'}), 401

# change_quanity STORED PROCEDURE DONE
@app.route('/change_quanity', methods=['POST'])
def change_quanity():
    if login_user:
        item_id = request.json['itemId']
        quantity = request.json['quantity']
        print(item_id)
        
        cursor.callproc("GetUserByEmail", (login_user,))
        results = cursor.stored_results()
        for result in results:
            user = result.fetchone()

        if user:
            #sql = "UPDATE Cart SET Quantity =%s WHERE UserID=%s and MItemID=%s"
            #values = (quantity, user[0], item_id)
            #cursor.execute(sql, values)
            cursor.callproc("UpdateCartQuantity", (quantity, user[0], item_id))
            db.commit()
            return jsonify({'redirect_url': url_for('cart')})
        else:
            return jsonify({'msg': 'User not found'}), 400
    else:
        return jsonify({'msg': 'Login is required for adding item to cart'}), 401

#not working even without procedures
@app.route('/checkout', methods=['POST'])
def checkout():
    is_logged_in = 'login_user' in session
    if is_logged_in:
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

# RESERVATION STORED PROCEDURE DONE
@app.route('/Reservation', methods=['GET', 'POST'])
def reservation():
    is_logged_in = 'login_user' in session
    if request.method == 'POST':
        if is_logged_in:
            name = request.form['name']
            date = request.form['date']
            time_slot = request.form['time-slot']
            seats = request.form['seats']
            #print(name,date,time_slot,seats)

            cursor.callproc("GetUserByEmail", (login_user,)) #
            results = cursor.stored_results()
            for result in results:
                user=result.fetchone()
            
           

            cursor.callproc("GetAvailableTable", (seats, date, time_slot)) #
            results = cursor.stored_results()
            for result in results:
                table = result.fetchone()
           
            if user:
                if table:
                    table_id = table[0]
                    user_id = user[0]
                    #print("hehe:",name, date, seats, time_slot, user_id, table_id)

                    cursor.callproc("InsertReservation", (name, date, seats, time_slot, user_id, table_id)) #

                    #insert_query = "INSERT INTO Reservations (CustomerName, ReservationDate, NumberOfSeats, TimeSlot, UserID, TableID) VALUES (%s, %s, %s, %s, %s, %s)"
                  
                    db.commit()

                    return render_template('Reservation.html',table_Number=table_id,is_logged_in=is_logged_in)

                else:
                    return "No available tables for the requested number of seats."
            else:
                return "User not found"
        else:
            return "Login required"
    else:
        return render_template('Reservation.html',is_logged_in=is_logged_in)
   
@app.route('/AdminHome')
def admin_home():
    is_logged_in = 'login_user' in session  
    return render_template('AdminHome.html',is_logged_in=is_logged_in)

# ADMINREVIEW STORED PROCEDURE DONE
@app.route('/AdminReview')
def admin_review():
    is_logged_in = 'login_user' in session  

    cursor.callproc("GetReviewCount") #
    results = cursor.stored_results()
    for result in results:
        total_reviews = result.fetchone()[0]

    cursor.callproc("CalculateAverageRating")
    results = cursor.stored_results()
    for result in results:
        avg_rating = result.fetchone()[0]

    cursor.callproc("GetReviewCounts")
    results = cursor.stored_results()
    rating_counts = []
    for result in results:
        for row in result.fetchall():
            rating_counts.append(row)


    #
    selected_month = request.args.get('month', 'all')

    if selected_month == 'all':
        sql_top_items = """
            SELECT m.MenuItem, SUM(o.Quantity) as TotalQuantity
            FROM Orders o
            JOIN Menu m ON o.MItemID = m.MItemID
            GROUP BY o.MItemID
            ORDER BY TotalQuantity DESC
            LIMIT 10
        """
        cursor.execute(sql_top_items)
    else:
        sql_top_items = """
            SELECT m.MenuItem, SUM(o.Quantity) as TotalQuantity
            FROM Orders o
            JOIN Menu m ON o.MItemID = m.MItemID
            WHERE MONTH(o.TimeDate) = %s
            GROUP BY o.MItemID
            ORDER BY TotalQuantity DESC
            LIMIT 10
        """
        cursor.execute(sql_top_items, (selected_month,))

    top_items = cursor.fetchall()

    item_labels = [item[0] for item in top_items]
    item_quantities = [item[1] for item in top_items]
        

    return render_template('AdminReview.html',total_reviews=total_reviews, avg_rating=avg_rating, rating_counts=rating_counts, item_labels=item_labels, item_quantities=item_quantities, top_items=top_items,is_logged_in=is_logged_in)

# admin_reviews_json STORED PROCEDURE DONE
@app.route('/admin_reviews_json')
def admin_reviews_json():
    cursor.callproc("GetReviewsWithUsers")
    results = cursor.stored_results()

    reviews = []
    for result in results:
        for review in result.fetchall():
            reviews.append({
                'ReviewID': review[0],
                'UserName': review[1],
                'Rating': review[2],
                'Comments': review[3],
                'entry_date': review[4]
            })

    return jsonify({'reviews': reviews})

# AdminReservation STORED PROCEDURE DONE
@app.route('/AdminReservation')
def admin_reservation():
    is_logged_in = 'login_user' in session  
    cursor.callproc("GetReservationsWithTables")
    results = cursor.stored_results()

    reservations = []
    for result in results:
        for reservation in result.fetchall():
            reservations.append(reservation)

    return render_template('AdminReservation.html', reservations=reservations,is_logged_in=is_logged_in)

# AdminReservation STORED PROCEDURE -search_query proc left
@app.route('/AdminMenu', methods=['GET'])
def admin_menu():
    is_logged_in = 'login_user' in session  
    cursor.callproc("GetAllMenuItems")
    results_menu = cursor.stored_results()

    menu = []
    for result in results_menu:
        for item in result.fetchall():
            menu.append(item)

    cursor.callproc("GetAllCategories")
    results_categories = cursor.stored_results()

    categories = []
    for result in results_categories:
        for category in result.fetchall():
            categories.append(category)

    #first category as default 
    cursor.callproc("GetFirstCategoryName")
    result_first_category = cursor.stored_results()

    for result in result_first_category:
        default_category_tuple = result.fetchone()
        default_category = default_category_tuple[0] if default_category_tuple else None
        break 

    search_query = request.args.get('search-query', '')

    if search_query:
            sql = f"""
                SELECT Menu.*, Category.CategoryName
                FROM Menu
                JOIN Category ON Menu.CategoryID = Category.CategoryID
                WHERE Menu.MenuItem LIKE '{search_query}'
            """
            print(f"Search Query SQL: {sql}")
    


    #print(f"Final SQL: {sql}")

    return render_template('AdminMenu.html', menu=menu, default_category=default_category, categories=categories,is_logged_in=is_logged_in)

# AdminMenuCategory STORED PROCEDURE DONE
@app.route('/AdminMenuCategory', methods=['POST'])
def addCategories():
    CategoryName = request.json['categoryName']
    print("CategoryName:", CategoryName)
    
    cursor.callproc("InsertCategory", (CategoryName,))
    db.commit()

    if cursor.rowcount > 0:
        return jsonify({'redirect_url': url_for('admin_menu')})
    else:
        return jsonify({'msg': "Sorry, the category could not be added"})

# AdminMenuItem STORED PROCEDURE DONE
@app.route('/AdminMenuItem', methods=['POST'])
def addMenuItems():
    ItemName = request.json['ItemName']
    ItemPrice = request.json['ItemPrice']
    ItemDescription = request.json['ItemDescription']
    ItemCategory = request.json['CategoryName']

  
    cursor.callproc('GetCategoryIdByCategoryName', (ItemCategory,))

    results = cursor.stored_results()
    for result in results:
            categoryID=result.fetchone()

    if categoryID:
        cursor.callproc("InsertMenu", (ItemName, ItemDescription, ItemPrice, categoryID[0]))
        db.commit()
        if cursor.rowcount > 0:
            return jsonify({'redirect_url': url_for('admin_menu')})
        else:
            return jsonify({'msg': "Sorry, the Menu Item cannot be added"})
    else:
        return jsonify({'msg': "Sorry, this category does not exist"})


# Reviews STORED PROCEDURE DONE
@app.route('/Reviews', methods=['POST'])
def reviews():

    if login_user:
        comment = request.form['comment']
        rating = int(request.form['rating']) 

        cursor.callproc("GetUserByEmail", (login_user,))
        results = cursor.stored_results()
        for result in results:
            user = result.fetchone()
        

        if user:
            user_id = user[0]

            insert_review_proc = "InsertReview"
            review_values = (user_id, rating, comment)

            cursor.callproc(insert_review_proc, review_values)
            db.commit()

            return review()
        else:
            return "User not found"
    else:
        return "Login required"

# Reviews STORED PROCEDURE DONE
@app.route('/Reviews', methods=['GET'])
def review():
    is_logged_in = 'login_user' in session  

    cursor.callproc("FetchReviews")
    results = cursor.stored_results()

    # Fetch the results from the stored procedure
    reviews = []
    for result in results:
        for review in result.fetchall():
            reviews.append(review)

    cursor.callproc("GetReviewCount") #
    results = cursor.stored_results()
    for result in results:
        total_reviews = result.fetchone()[0]

    cursor.callproc("CalculateAverageRating")
    results = cursor.stored_results()
    for result in results:
        avg_rating = result.fetchone()[0]

    cursor.callproc("GetReviewCounts")
    results = cursor.stored_results()
    rating_counts = []
    for result in results:
        for row in result.fetchall():
            rating_counts.append(row)

    print(reviews)
    return render_template('Reviews.html', reviews=reviews,total_reviews=total_reviews, avg_rating=avg_rating, rating_counts=rating_counts,is_logged_in=is_logged_in)


if __name__ == '__main__':
    app.run(debug=True)
