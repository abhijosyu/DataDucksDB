-- CREATE DATABASE
DROP DATABASE IF EXISTS DiningDucks;
CREATE DATABASE DiningDucks;
USE DiningDucks;


-- USER TABLE
DROP TABLE IF EXISTS User;
CREATE TABLE User (
                      user_id INT AUTO_INCREMENT PRIMARY KEY,
                      name VARCHAR(100),
                      email VARCHAR(100) UNIQUE,
                      role VARCHAR(50) -- reviewer, employee, admin, company
);

-- COMPANY TABLE
DROP TABLE IF EXISTS Company;
CREATE TABLE Company (
                         company_id INT AUTO_INCREMENT PRIMARY KEY,
                         name VARCHAR(100)
);


-- RESTAURANT LOCATION
DROP TABLE IF EXISTS RestaurantLocation;
CREATE TABLE RestaurantLocation (
                                    location_id INT AUTO_INCREMENT PRIMARY KEY,
                                    company_id INT,
                                    address VARCHAR(255),
                                    city VARCHAR(100),
                                    price_range VARCHAR(50),
                                    FOREIGN KEY (company_id) REFERENCES Company(company_id)
);


-- CATEGORY (food, service, etc.)
DROP TABLE IF EXISTS Category;
CREATE TABLE Category (
                          category_id INT AUTO_INCREMENT PRIMARY KEY,
                          name VARCHAR(100)
);


-- CUSTOMER REVIEW
DROP TABLE IF EXISTS CustomerReview;
CREATE TABLE CustomerReview (
                                review_id INT AUTO_INCREMENT PRIMARY KEY,
                                user_id INT, location_id INT, review_text TEXT,
                                review_date DATETIME, FOREIGN KEY (user_id) REFERENCES User(user_id),
                                FOREIGN KEY (location_id) REFERENCES RestaurantLocation(location_id)
);


-- REVIEW RATINGS (per category)
DROP TABLE IF EXISTS Rating;
CREATE TABLE Rating (
                        rating_id INT AUTO_INCREMENT PRIMARY KEY,
                        review_id INT, category_id INT,
                        score INT CHECK (score BETWEEN 1 AND 5),
                        FOREIGN KEY (review_id) REFERENCES CustomerReview(review_id),
                        FOREIGN KEY (category_id) REFERENCES Category(category_id)
);


-- EMPLOYEE REVIEW
DROP TABLE IF EXISTS EmployeeReview;
CREATE TABLE EmployeeReview (
                                emp_review_id INT AUTO_INCREMENT PRIMARY KEY,
                                user_id INT,
                                location_id INT,
                                review_text TEXT,
                                review_date DATETIME,
                                FOREIGN KEY (user_id) REFERENCES User(user_id),
                                FOREIGN KEY (location_id) REFERENCES RestaurantLocation(location_id)
);


-- EMPLOYEE RATINGS
DROP TABLE IF EXISTS EmployeeRating;
CREATE TABLE EmployeeRating (
                                emp_rating_id INT AUTO_INCREMENT PRIMARY KEY,
                                emp_review_id INT,
                                category_id INT,
                                score INT CHECK (score BETWEEN 1 AND 5),
                                FOREIGN KEY (emp_review_id) REFERENCES EmployeeReview(emp_review_id),
                                FOREIGN KEY (category_id) REFERENCES Category(category_id)
);


-- PHOTOS
DROP TABLE IF EXISTS Photo;
CREATE TABLE Photo (
                       photo_id INT AUTO_INCREMENT PRIMARY KEY,
                       location_id INT,
                       url VARCHAR(255),
                       FOREIGN KEY (location_id) REFERENCES RestaurantLocation(location_id)
);


-- COMPLAINTS (For admin, help desk)
DROP TABLE IF EXISTS Complaint;
CREATE TABLE Complaint (
                           complaint_id INT AUTO_INCREMENT PRIMARY KEY,
                           user_id INT,
                           description TEXT,
                           status VARCHAR(50),
                           FOREIGN KEY (user_id) REFERENCES User(user_id)
);


-- FLAGS (admin)
DROP TABLE IF EXISTS Flag;
CREATE TABLE Flag (
                      flag_id INT AUTO_INCREMENT PRIMARY KEY,
                      admin_id INT, review_id INT, reason TEXT,
                      FOREIGN KEY (admin_id) REFERENCES User(user_id),
                      FOREIGN KEY (review_id) REFERENCES CustomerReview(review_id)
);


-- TAG
DROP TABLE IF EXISTS Tag;
CREATE TABLE Tag (
                     tag_id INT AUTO_INCREMENT PRIMARY KEY,
                     tag_name VARCHAR(100) UNIQUE
);


-- COMPANY-TAG BRIDGE TABLE
DROP TABLE IF EXISTS CompanyTag;
CREATE TABLE CompanyTag (
                            company_id INT,
                            tag_id INT,
                            PRIMARY KEY (company_id, tag_id),
                            FOREIGN KEY (company_id) REFERENCES Company(company_id),
                            FOREIGN KEY (tag_id) REFERENCES Tag(tag_id)
);


