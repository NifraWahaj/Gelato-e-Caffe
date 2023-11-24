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
-- Insert data into the User table
INSERT INTO User (UserName, Email, Password) VALUES
('Admin', 'admin@example.com', '1234'),
('User1', 'user1@example.com', 'password1'),
('User2', 'user2@example.com', 'password2'),
('User3', 'user3@example.com', 'password3'),
('User4', 'user4@example.com', 'password4'),
('User5', 'user5@example.com', 'password5');

-- Insert data into the Category table
INSERT INTO Category (CategoryName) VALUES
('Coffee'),
('Gelato'),
('Drinks'),
('Brunch'),
('Desserts');

-- Insert data into the Menu table
INSERT INTO Menu (MenuItem, Description, Price, CategoryID) VALUES
('Espresso', 'Strong black coffee', 3, 1),
('Cappuccino', 'Espresso with steamed milk', 4, 1),
('Chocolate Gelato', 'Rich chocolate ice cream', 5, 2),
('Iced Tea', 'Chilled tea with ice', 2, 3),
('Pancakes', 'Fluffy pancakes with syrup', 7, 4);

-- Insert data into the Review table
INSERT INTO Review (UserID, Rating, Comments) VALUES
(5, 5, 'Great coffee!'),
(2, 4, 'Love the gelato!'),
(3, 3, 'Decent drinks.'),
(4, 5, 'Best brunch in town!'),
(5, 4, 'Yummy desserts!');


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

-- Insert data into the Orders table
INSERT INTO Orders (OrderID, UserID, MItemID) VALUES
(1, 3, 1),
(2, 2, 3),
(3, 3, 5),
(4, 4, 2),
(5, 5, 4);

select * from Menu;
select * from Review;

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

CREATE TABLE Tables (   -- it will be like hard coded so i have allowed upto 15 seats so just make sure to insert only upto 15 seats from here.
    TableID INT AUTO_INCREMENT PRIMARY KEY,
    NumberOfSeats INT NOT NULL
);

insert into Tables (NumberOfSeats) values(1),(2),(2),(2),(3),(3); 
select * from Reservations;
select * from Tables;
select * from Category;
select * from Menu;
select * from Review;
select * from User;
select * from Orders;
select * from Cart;
