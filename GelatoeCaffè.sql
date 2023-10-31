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
CategoryName varchar(250) not null
);

create table Menu(
MItemID int auto_increment primary key,
MenuItem varchar(250) not null,
Description varchar(250) not null,
Price int not null,
CategoryID int not null,
FOREIGN KEY (CategoryID) REFERENCES Category(CategoryID) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Review (
    ReviewID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT NOT NULL,
    Rating INT NOT NULL,
    Comments VARCHAR(250),
    FOREIGN KEY (UserID) REFERENCES User(UserID) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE Orders (
    OrderID INT NOT NULL,
    UserID INT NOT NULL,
    MItemID INT NOT NULL,
    FOREIGN KEY (UserID) REFERENCES User(UserID) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (MItemID) REFERENCES Menu(MItemID) ON DELETE CASCADE ON UPDATE CASCADE
);


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
(1, 5, 'Great coffee!'),
(2, 4, 'Love the gelato!'),
(3, 3, 'Decent drinks.'),
(4, 5, 'Best brunch in town!'),
(5, 4, 'Yummy desserts!');

-- Insert data into the Orders table
INSERT INTO Orders (OrderID, UserID, MItemID) VALUES
(1, 1, 1),
(2, 2, 3),
(3, 3, 5),
(4, 4, 2),
(5, 5, 4);




