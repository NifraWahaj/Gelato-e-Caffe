create database gelatoecaffè;
use gelatoecaffè;

create table User(
UserID int auto_increment primary key,
UserName varchar(250) Not NUll,
Email varchar(250) unique Not NULL,
password varchar(250) Not NULL
);

create table Category(
CategoryID int auto_increment primary key,
CategoryName varchar(250) unique not null 
);
drop table Category;

create table Menu(
MItemID int auto_increment primary key,
MenuItem varchar(250) unique not null,
Description varchar(250) not null,
Price int not null,
CategoryID int not null,
FOREIGN KEY (CategoryID) REFERENCES Category(CategoryID) ON DELETE CASCADE ON UPDATE CASCADE
);
drop table Menu;

CREATE TABLE Review (
    ReviewID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    Rating INT NOT NULL,
    Comments VARCHAR(250),
    entry_date DATE DEFAULT (CURRENT_DATE) Not Null,
    FOREIGN KEY (UserID) REFERENCES User(UserID) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Cart (
    CartID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    MItemID INT NOT NULL,
    Quantity INT NOT NULL default 1,
    FOREIGN KEY (UserID) REFERENCES User(UserID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (MItemID) REFERENCES Menu(MItemID) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Orders (
    OrderID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    MItemID INT NOT NULL,
    Quantity INT NOT NULL,
    TimeDate datetime NOT NULL,
    FOREIGN KEY (UserID) REFERENCES User(UserID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (MItemID) REFERENCES Menu(MItemID) ON DELETE CASCADE ON UPDATE CASCADE
);

drop table Orders;

INSERT INTO User (UserName, Email, Password) VALUES
('Admin', 'admin@example.com', '1234'),
('User1', 'user1@example.com', 'password1'),
('User2', 'user2@example.com', 'password2'),
('User3', 'user3@example.com', 'password3'),
('User4', 'user4@example.com', 'password4'),
('User5', 'user5@example.com', 'password5');


INSERT INTO Category (CategoryName) VALUES
('Coffee'),
('Gelato'),
('Drinks'),
('Brunch'),
('Desserts');


INSERT INTO Menu (MenuItem, Description, Price, CategoryID) VALUES
('Espresso', 'Strong black coffee', 3, 1),
('Cappuccino', 'Espresso with steamed milk', 4, 1),
('Chocolate Gelato', 'Rich chocolate ice cream', 5, 2),
('Iced Tea', 'Chilled tea with ice', 2, 3),
('Pancakes', 'Fluffy pancakes with syrup', 7, 4);


INSERT INTO Review (UserID, Rating, Comments) VALUES
(5, 5, 'Great coffee!'),
(2, 4, 'Love the gelato!'),
(3, 3, 'Decent drinks.'),
(4, 5, 'Best brunch in town!'),
(5, 4, 'Yummy desserts!');

select * from Review;
INSERT INTO Review (UserID, Rating, Comments, entry_date) VALUES
(5, 1, 'Needs improvement in service', '2023-10-20'),
(2, 4, 'Great service!', '2023-01-01'),
(2, 5, 'Excellent experience', '2023-01-02'),
(3, 3, 'Average food quality', '2023-01-03'),
(4, 4, 'Loved the ambiance', '2023-10-04'),
(5, 2, 'Disappointed with the menu', '2023-10-05'),
(6, 5, 'Best coffee ever!', '2023-04-06'),
(4, 4, 'Friendly staff', '2023-08-07'),
(2, 3, 'Could improve cleanliness', '2023-09-08'),
(5, 5, 'Amazing desserts!', '2023-11-09'),
(4, 4, 'Good selection of drinks', '2023-06-10'),
(3, 3, 'Satisfactory experience', '2023-05-11'),
(2, 5, 'Top-notch service', '2023-02-12'),
(6, 4, 'Impressed by the variety', '2023-06-13'),
(5, 2, 'Expected better quality', '2023-08-14'),
(5, 5, 'Would definitely recommend', '2023-04-15'),
(6, 4, 'Pleasant atmosphere', '2023-05-16'),
(3, 3, 'Decent pricing', '2023-03-17'),
(4, 5, 'Exceptional taste!', '2023-08-18'),
(3, 4, 'Good place for meetings', '2023-07-19'),
(5, 3, 'Needs improvement in service', '2023-10-20');


INSERT INTO Orders (UserID, MItemID, Quantity, TimeDate) VALUES
(1, 3, 2, '2023-11-25 12:30:00'),
(2, 3, 1, '2023-11-25 13:45:00'),
(2, 3, 10, '2023-11-25 13:45:00'),
(3, 4, 3, '2023-11-25 14:30:00'),
(4, 2, 1, '2023-11-25 15:15:00'),
(5, 5, 2, '2023-11-25 16:00:00');

INSERT INTO Cart (UserID, MItemID, Quantity) VALUES
(1, 1, 2),
(2, 3, 1),
(3, 5, 3),
(4, 2, 1),
(5, 4, 2);

CREATE TABLE Reservations (
    ReservationID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    TableID INT NOT NULL,
    CustomerName VARCHAR(255) NOT NULL,
    ReservationDate DATE NOT NULL,
    NumberOfSeats INT NOT NULL ,
    TimeSlot ENUM(
        '9:00am - 9:50am', '10:00am - 10:50am', '11:00am - 11:50am',
        '12:00pm - 12:50pm', '1:00pm - 1:50pm', '2:00pm - 2:50pm',
        '3:00pm - 3:50pm', '4:00pm - 4:50pm', '5:00pm - 5:50pm',
        '6:00pm - 6:50pm', '7:00pm - 7:50pm', '8:00pm - 8:50pm', '9:00pm - 9:50pm'
    ),
	FOREIGN KEY (UserID) REFERENCES User(UserID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (TableID) REFERENCES Tables(TableID) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Tables (   
    TableID INT AUTO_INCREMENT PRIMARY KEY,
    NumberOfSeats INT NOT NULL
);

INSERT INTO Reservations (UserID, TableID, CustomerName, ReservationDate, NumberOfSeats, TimeSlot) VALUES
(2, 1, 'John Doe', '2023-12-05', 2, '7:00pm - 7:50pm'),
(3, 3, 'Jane Smith', '2023-12-06', 4, '6:00pm - 6:50pm'),
(4, 2, 'Alice Johnson', '2023-12-07', 2, '8:00pm - 8:50pm'),
(5, 4, 'Bob Williams', '2023-12-08', 3, '7:00pm - 7:50pm'),
(6, 5, 'Eva Davis', '2023-12-09', 2, '5:00pm - 5:50pm');

insert into Tables (NumberOfSeats) values(1),(2),(2),(2),(3),(3); 

select * from Reservations;
select * from Tables;
select * from Category;
select * from Menu;
select * from Review;
select * from User;
select * from Orders;
select * from Cart;


-- ========================= SignUp ===============================
DELIMITER //

CREATE PROCEDURE InsertUser(IN userNameParam VARCHAR(255), IN emailParam VARCHAR(255), IN passwordParam VARCHAR(255))
BEGIN
    INSERT INTO User (UserName, Email, Password)
    VALUES (userNameParam, emailParam, passwordParam);
END //

DELIMITER ;
CALL InsertUser('Jane', 'jane@example.com', 'jane0909');
select * from user;
-- ========================= LogIn ===============================

DROP PROCEDURE IF EXISTS GetUserByEmailAndPassword;
DELIMITER //
CREATE PROCEDURE GetUserByEmailAndPassword( IN userEmail VARCHAR(250),
    IN userPassword VARCHAR(250))
BEGIN
   SELECT *
    FROM User
     WHERE Email = userEmail AND password = userPassword;
END //
DELIMITER ;

CALL GetUserByEmailAndPassword('user1@example.com', 'password1');

SHOW PROCEDURE STATUS LIKE 'GetUserByEmailAndPassword';

-- ========================= menu ===============================
-- sql = "SELECT * FROM Menu"

-- sql = "SELECT * FROM Category"

-- ========================= add_to_cart ===============================
-- this is returning the entire table instead of just userID
--   sql_user = "SELECT UserID FROM User WHERE Email = %s"
DROP PROCEDURE IF EXISTS GetUserByEmail;
DELIMITER 
CREATE PROCEDURE GetUserByEmail(IN userEmail VARCHAR(250))
BEGIN
    SELECT UserID
    FROM User
    WHERE Email = userEmail;
END 
DELIMITER ;
CALL GetUserByEmail('user1@example.com');

SELECT UserID
FROM User
WHERE Email = 'user1@example.com';

--  sql = "SELECT * FROM Cart WHERE UserID=%s and MItemID=%s"
DROP PROCEDURE IF EXISTS GetCartByUserIDAndMItemID;
DELIMITER //
CREATE PROCEDURE GetCartByUserIDAndMItemID(
    IN userIdParam INT,
    IN mItemIdParam INT
)
BEGIN
    SELECT *
    FROM Cart
    WHERE UserID = userIdParam AND MItemID = mItemIdParam;
END //
DELIMITER ;
CALL GetCartByUserIDAndMItemID(1,1);

-- insert_query = "INSERT INTO Cart (UserID, MItemID) VALUES (%s, %s)"
DELIMITER //
CREATE PROCEDURE InsertIntoCart(IN userIdParam INT, IN mItemIdParam INT)
BEGIN
    INSERT INTO Cart (UserID, MItemID) VALUES (userIdParam, mItemIdParam);
END //
DELIMITER ;

CALL InsertIntoCart(6, 3); 
SELECT * FROM Cart;

-- ========================= Cart ===============================

-- sql_user = "SELECT UserID FROM User WHERE Email = %s"
CALL GetUserByEmail('user1@example.com');

-- sql = "SELECT m.*,c.Quantity FROM Menu m, Cart c WHERE UserID=%s and m.MItemID=c.MItemID"
DROP PROCEDURE IF EXISTS GetMenuAndCartByUserID;

DELIMITER //
CREATE PROCEDURE GetMenuAndCartByUserID(IN userId INT)
BEGIN
    SELECT m.*, c.Quantity
    FROM Menu m
    JOIN Cart c ON m.MItemID = c.MItemID
    WHERE c.UserID = userId;
END //
DELIMITER ;
CALL GetMenuAndCartByUserID(1);

-- sql = "SELECT SUM(m.Price * c.Quantity) AS TotalPrice FROM Cart c, Menu m WHERE UserID=%s and m.MItemID=c.MItemID"
DROP PROCEDURE IF EXISTS CalculateTotalPrice;

DELIMITER //
CREATE PROCEDURE CalculateTotalPrice(IN userId INT)
BEGIN
    SELECT SUM(m.Price * c.Quantity) AS TotalPrice
    FROM Cart c
    JOIN Menu m ON c.MItemID = m.MItemID
    WHERE c.UserID = userId;
END //
DELIMITER ;

CALL CalculateTotalPrice(1); 
SHOW PROCEDURE STATUS LIKE 'CalculateTotalPrice';

-- ========================= remove_from_cart ===============================

-- sql_user = "SELECT UserID FROM User WHERE Email = %s"
CALL GetUserByEmail('user1@example.com');

-- sql = "Delete FROM Cart WHERE UserID=%s and MItemID=%s"
DELIMITER //
CREATE PROCEDURE DeleteCartItem(
    IN userIdParam INT,
    IN mItemIdParam INT
)
BEGIN
    DELETE FROM Cart
    WHERE UserID = userIdParam AND MItemID = mItemIdParam;
END //

DELIMITER ;

CALL DeleteCartItem(1, 1);
Delete FROM Cart ;
SHOW PROCEDURE STATUS LIKE 'DeleteCartItem';

-- ========================= change_quanity ===============================

-- sql_user = "SELECT UserID FROM User WHERE Email = %s"
CALL GetUserByEmail('user1@example.com');

-- sql = "UPDATE Cart SET Quantity =%s WHERE UserID=%s and MItemID=%s"

DELIMITER //
DROP PROCEDURE IF EXISTS UpdateCartQuantity;
CREATE PROCEDURE UpdateCartQuantity(
    IN cartQuantity INT,
    IN userIdParam INT,
    IN mItemIdParam INT
)
BEGIN
    UPDATE Cart
    SET Quantity = cartQuantity
    WHERE UserID = userIdParam AND MItemID = mItemIdParam;
END //
DELIMITER ;

CALL UpdateCartQuantity(33, 2, 3);
select * from Cart;

-- ========================= checkout ===============================

-- stored procedures for checkout
 -- sql_user = "SELECT UserID FROM User WHERE Email = %s"
CALL GetUserByEmail('user1@example.com');

 -- cart_items_query = "SELECT MItemID, Quantity FROM Cart WHERE UserID = %s"
 DROP PROCEDURE IF EXISTS GetCartItems;
DELIMITER //
CREATE PROCEDURE GetCartItems(IN userIdParam INT)
BEGIN
    SELECT MItemID, Quantity
    FROM Cart
    WHERE UserID = userIdParam;
END //
DELIMITER ;
CALL GetCartItems(2);

-- insert_order_query = "INSERT INTO Orders (UserID, MItemID, Quantity, TimeDate) VALUES (%s, %s, %s, %s)"
DROP PROCEDURE IF EXISTS InsertOrder;

DELIMITER //
CREATE PROCEDURE InsertOrder(
    IN pUserID INT,
    IN pMItemID INT,
    IN pQuantity INT,
    IN pTimeDate DATETIME
)
BEGIN
    INSERT INTO Orders (UserID, MItemID, Quantity, TimeDate)
    VALUES (pUserID, pMItemID, pQuantity, pTimeDate);
END //
DELIMITER ;

CALL InsertOrder(1, 3, 2, '2012-12-12 12:12:12');
select * from Orders;

--  delete_cart_query = "DELETE FROM Cart WHERE UserID = %s"
DROP PROCEDURE IF EXISTS DeleteCartByUserID;
DELIMITER //
CREATE PROCEDURE DeleteCartByUserID(IN userIdToDelete INT)
BEGIN
    DELETE FROM Cart WHERE UserID = userIdToDelete;
END //
DELIMITER ;

CALL DeleteCartByUserID(2);
select * from CART;

-- ========================= Reservation ===============================

--  sql_user = "SELECT UserID FROM User WHERE Email = %s"
CALL GetUserByEmail('user1@example.com');

-- "SELECT TableID FROM Tables WHERE NumberOfSeats >= %s AND TableID NOT IN (SELECT TableID FROM Reservations WHERE ReservationDate = %s AND TimeSlot = %s) ORDER BY NumberOfSeats ASC LIMIT 1", (seats, date, time_slot))
DELIMITER //
CREATE PROCEDURE GetAvailableTable(
    IN seats INT,
    IN date DATE,
    IN time_slot ENUM(
        '9:00am - 9:50am', '10:00am - 10:50am', '11:00am - 11:50am',
        '12:00pm - 12:50pm', '1:00pm - 1:50pm', '2:00pm - 2:50pm',
        '3:00pm - 3:50pm', '4:00pm - 4:50pm', '5:00pm - 5:50pm',
        '6:00pm - 6:50pm', '7:00pm - 7:50pm', '8:00pm - 8:50pm', '9:00pm - 9:50pm'
    )
)
BEGIN
    SELECT TableID
    FROM Tables
    WHERE NumberOfSeats >= seats
        AND TableID NOT IN (
            SELECT TableID
            FROM Reservations
            WHERE ReservationDate = date AND TimeSlot = time_slot
        )
    ORDER BY NumberOfSeats ASC
    LIMIT 1;
END //
DELIMITER ;
CALL GetAvailableTable(3, '2023-12-01', '12:00pm - 12:50pm');


--  insert_query = "INSERT INTO Reservations (CustomerName, ReservationDate, NumberOfSeats, TimeSlot, UserID, TableID) VALUES (%s, %s, %s, %s, %s, %s)"
DELIMITER //
CREATE PROCEDURE InsertReservation(
    IN customerName VARCHAR(255),
    IN reservationDate DATE,
    IN numberOfSeats INT,
    IN timeSlot ENUM(
        '9:00am - 9:50am', '10:00am - 10:50am', '11:00am - 11:50am',
        '12:00pm - 12:50pm', '1:00pm - 1:50pm', '2:00pm - 2:50pm',
        '3:00pm - 3:50pm', '4:00pm - 4:50pm', '5:00pm - 5:50pm',
        '6:00pm - 6:50pm', '7:00pm - 7:50pm', '8:00pm - 8:50pm', '9:00pm - 9:50pm'
    ),
    IN userID INT,
    IN tableID INT
)
BEGIN
    INSERT INTO Reservations (CustomerName, ReservationDate, NumberOfSeats, TimeSlot, UserID, TableID)
    VALUES (customerName, reservationDate, numberOfSeats, timeSlot, userID, tableID);
END //

DELIMITER ;

CALL InsertReservation('Peter Parker', '2023-12-02', 3, '6:00pm - 6:50pm', 4, 1);
select * from Reservations;

-- ========================= Reservation ===============================

-- "SELECT COUNT(*) FROM Review"
DELIMITER //
CREATE PROCEDURE GetReviewCount()
BEGIN
    SELECT COUNT(*) AS ReviewCount FROM Review;
END //
DELIMITER ;

CALL GetReviewCount();

-- SELECT AVG(Rating) FROM Review"
DROP PROCEDURE IF EXISTS CalculateAverageRating;
DELIMITER //
CREATE PROCEDURE CalculateAverageRating()
BEGIN
    SELECT AVG(Rating) AS AverageRating
    FROM Review;
END //
DELIMITER ;

CALL CalculateAverageRating();

-- "SELECT Rating, COUNT(*) FROM Review GROUP BY Rating ORDER BY Rating DESC")
DROP PROCEDURE IF EXISTS GetReviewCounts;

DELIMITER //
CREATE PROCEDURE GetReviewCounts()
BEGIN
    SELECT Rating, COUNT(*) AS Count
    FROM Review
    GROUP BY Rating
    ORDER BY Rating DESC;
END //
DELIMITER ;

CALL GetReviewCounts();

--  sql_top_items = "SELECT m.MenuItem, SUM(o.Quantity) as TotalQuantity FROM Orders oJOIN Menu m ON o.MItemID = m.MItemID GROUP BY o.MItemID ORDER BY TotalQuantity DESC LIMIT 10"
-- all MONTHS
DROP PROCEDURE IF EXISTS GetTop10Items;
DELIMITER //
CREATE PROCEDURE GetTop10Items()
BEGIN
    SELECT m.MenuItem, SUM(o.Quantity) as TotalQuantity
    FROM Orders o
    JOIN Menu m ON o.MItemID = m.MItemID
    GROUP BY o.MItemID
    ORDER BY TotalQuantity DESC
    LIMIT 10;
END //
DELIMITER ;

CALL GetTop10Items();
SELECT * FROM MENU;

-- sql_top_items = "SELECT m.MenuItem, SUM(o.Quantity) as TotalQuantity FROM Orders o JOIN Menu m ON o.MItemID = m.MItemID WHERE MONTH(o.TimeDate) = %s GROUP BY o.MItemID ORDER BY TotalQuantity DESC LIMIT 10"
DELIMITER //
CREATE PROCEDURE GetTop10ItemsByMonth(IN monthParam INT)
BEGIN
    SELECT m.MenuItem, SUM(o.Quantity) as TotalQuantity
    FROM Orders o
    JOIN Menu m ON o.MItemID = m.MItemID
    WHERE MONTH(o.TimeDate) = monthParam
    GROUP BY o.MItemID
    ORDER BY TotalQuantity DESC
    LIMIT 10;
END //
DELIMITER ;
CALL GetTop10ItemsByMonth(11);

-- "SELECT MONTH(TimeDate) as month, SUM(Quantity * Price) as amount FROM Orders o JOIN Menu m ON o.MItemID = m.MItemID GROUP BY month ORDER BY month"
DELIMITER //

CREATE PROCEDURE GetMonthlyAmounts()
BEGIN
    SELECT MONTH(o.TimeDate) as month, SUM(o.Quantity * m.Price) as amount
    FROM Orders o
    JOIN Menu m ON o.MItemID = m.MItemID
    GROUP BY month
    ORDER BY month;
END //

DELIMITER ;
CALL GetMonthlyAmounts();
select * from Orders;

-- ========================= admin_reviews_json ===============================

-- SELECT R.ReviewID, U.UserName, R.Rating, R.Comments, R.entry_date FROM Review R, User U WHERE R.UserID = U.UserID ORDER BY ReviewID DESC"

DELIMITER //
CREATE PROCEDURE GetReviewsWithUsers()
BEGIN
    SELECT R.ReviewID, U.UserName, R.Rating, R.Comments, R.entry_date
    FROM Review R
    JOIN User U ON R.UserID = U.UserID
    ORDER BY R.ReviewID DESC;
END //
DELIMITER ;

CALL GetReviewsWithUsers();

-- ========================= AdminReservation ===============================

-- "SELECT * FROM Reservations r, Tables t where r.TableID = t.TableID Order by ReservationDate, TimeSlot"
DROP PROCEDURE IF EXISTS GetReservationsWithTables;

DELIMITER //

CREATE PROCEDURE GetReservationsWithTables()
BEGIN
    SELECT *
    FROM Reservations r
    JOIN Tables t ON r.TableID = t.TableID
    ORDER BY r.ReservationDate, r.TimeSlot;
END //

DELIMITER ;
CALL GetReservationsWithTables();
select * from Reservations;

-- ========================= AdminMenu ===============================

-- sql = "SELECT * FROM Menu"
DELIMITER //
CREATE PROCEDURE GetAllMenuItems()
BEGIN
    SELECT *
    FROM Menu;
END //
DELIMITER ;

CALL GetAllMenuItems();

-- sql = "SELECT * FROM Category"
DELIMITER //
CREATE PROCEDURE GetAllCategories()
BEGIN
    SELECT *
    FROM Category;
END //
DELIMITER ;
CALL GetAllCategories();

-- sql_default_category = "SELECT CategoryName FROM Category LIMIT 1"
DELIMITER //
CREATE PROCEDURE GetFirstCategoryName()
BEGIN
    SELECT CategoryName
    FROM Category
    LIMIT 1;
END //
DELIMITER ;

CALL GetFirstCategoryName();

--  sql = """ SELECT Menu.*, Category.CategoryName FROM Menu JOIN Category ON Menu.CategoryID = Category.CategoryID WHERE Menu.MenuItem LIKE '{search_query}' """

DROP PROCEDURE IF EXISTS GetMenuBySearchQuery;

DELIMITER //
CREATE PROCEDURE GetMenuBySearchQuery(IN searchQuery VARCHAR(250))
BEGIN
    SELECT Menu.*, Category.CategoryName
    FROM Menu
    JOIN Category ON Menu.CategoryID = Category.CategoryID
    WHERE Menu.MenuItem LIKE searchQuery;
END //

DELIMITER ;

CALL GetMenuBySearchQuery('%Espresso%');

-- ========================= AdminMenuCategory ===============================

--  sql = "INSERT INTO Category(CategoryName) VALUES (%s)"
DELIMITER //
CREATE PROCEDURE InsertCategory(IN categoryName VARCHAR(250))
BEGIN
    INSERT INTO Category (CategoryName) VALUES (categoryName);
END //
DELIMITER ;

CALL InsertCategory('Contorni');
select * from Category;

-- ========================= AdminMenuItem ===============================

-- sql1 = "SELECT CategoryID FROM Category WHERE CategoryName=%s"
DELIMITER //
CREATE PROCEDURE GetCategoryIdByCategoryName(IN categoryNameParam VARCHAR(250))
BEGIN
    SELECT CategoryID
    FROM Category
    WHERE CategoryName = categoryNameParam;
END //
DELIMITER ;

CALL GetCategoryIdByCategoryName('Contorni');

-- sql2 = "INSERT INTO Menu(MenuItem, Description, Price, CategoryID) VALUES (%s, %s, %s, %s)"
DROP PROCEDURE IF EXISTS InsertMenu;

DELIMITER //
CREATE PROCEDURE InsertMenu(
    IN p_MenuItem VARCHAR(250),
    IN p_Description VARCHAR(250),
    IN p_Price INT,
    IN p_CategoryID INT
)
BEGIN
    INSERT INTO Menu(MenuItem, Description, Price, CategoryID)
    VALUES (p_MenuItem, p_Description, p_Price, p_CategoryID);
END //
DELIMITER ;

CALL InsertMenu('Verdure Grigliate', 'Grilled medley of zucchini, peppers, and eggplant, infused with a touch of olive oil', 11, 6);
select * from menu;

-- ========================= Reviews/POST ===============================

-- ql_insert_review = "INSERT INTO Review (UserID, Rating, Comments) VALUES (%s, %s, %s)"

DELIMITER //
CREATE PROCEDURE InsertReview(
    IN userIdParam INT,
    IN ratingParam INT,
    IN commentsParam VARCHAR(250)
)
BEGIN
    INSERT INTO Review (UserID, Rating, Comments)
    VALUES (userIdParam, ratingParam, commentsParam);
END //
DELIMITER ;

CALL InsertReview(3, 5, 'Tastes like pure magic; absolute foodie paradise!');
select * from Review;

-- ========================= Reviews/GET ===============================

--  sql_fetch_reviews = "SELECT R.ReviewID ,U.UserName, R.Rating, R.Comments FROM Review R, User U where R.UserID = U.UserID ORDER BY ReviewID DESC LIMIT 5"
DELIMITER //
DROP PROCEDURE IF EXISTS FetchReviews;

CREATE PROCEDURE FetchReviews()
BEGIN
    SELECT R.ReviewID, U.UserName, R.Rating, R.Comments
    FROM Review R
    JOIN User U ON R.UserID = U.UserID
    ORDER BY ReviewID DESC
    LIMIT 5;
END //
DELIMITER ;

CALL FetchReviews();

-- SELECT COUNT(*) FROM Review"
CALL GetReviewCount();

-- "SELECT AVG(Rating) FROM Review"
CALL CalculateAverageRating();

-- SELECT Rating, COUNT(*) FROM Review GROUP BY Rating ORDER BY Rating DESC
CALL GetReviewCounts();
