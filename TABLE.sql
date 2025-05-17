DROP DATABASE horizontravels;
CREATE DATABASE horizontravels;
USE horizontravels;
CREATE TABLE flight(
FlightID INT auto_increment NOT NULL,
Destination VARCHAR(64) NOT NULL,
Destination_Time  time not null , 
Arrival VARCHAR(64) NOT NULL,
Arrival_Time time NOT NULL,
PRIMARY KEY (FlightID)
);
CREATE TABLE customer(
CustID  INT(10)  primary key NOT NULL auto_increment,
Fname VARCHAR(30) NOT NULL,
Sname VARCHAR(30) NOT NULL,
Email VARCHAR(120) NOT NULL UNIQUE,
username VARCHAR(30) NOT NULL UNIQUE,
password_hash VARCHAR(256)NOT NULL UNIQUE,
usertype VARCHAR(8) DEFAULT'standard'

);
CREATE TABLE plane_cost(
price INT NOT NULL,
FlightID INT NOT NULL,
foreign key (FlightID) references flight(FlightID)
);
CREATE TABLE flight_payment (
    paymentID INT AUTO_INCREMENT PRIMARY KEY,
    CustID INT NOT NULL,
    cardNo VARCHAR(16) NOT NULL UNIQUE,
    cardname VARCHAR(256) NOT NULL,
    expirydate VARCHAR(5) NOT NULL, 
    totalprice INT NOT NULL,
    FOREIGN KEY (CustID) REFERENCES customer(CustID)
        ON DELETE CASCADE 
        ON UPDATE CASCADE
);

CREATE TABLE Ticket_details (
    BookingID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    CustID INT NOT NULL,
    FlightID INT NOT NULL,
    paymentID INT NOT NULL,
    Departure_date DATE NOT NULL,
    Arrival_date DATE NOT NULL,
    totalseats INT NOT NULL,
    class VARCHAR(256) NOT NULL,
    totalprice INT NOT NULL,
    FOREIGN KEY (CustID) REFERENCES customer(CustID),
    FOREIGN KEY (FlightID) REFERENCES flight(FlightID),
    FOREIGN KEY (paymentID) REFERENCES flight_payment(paymentID)
);


INSERT INTO customer(CustID,Fname,Sname,Email,username,password_hash)VALUES
(1,'James','David','JD@yahoo.com','test','1way'),
(2,'Mark','Smith','marksmith@uwe.ac.uk','red','gdghs'),
(3,'Hamda','Yusuf','Hamda@yahoo.com','sdfg','sghsg'),
(4,'Tyrese','Clark','Ty@gmail.com','sdfres','sde3'),
(5,'K','S','KS@yahoo.com','gdgsh','ddd'),
(6,'Mike','David','MD@yahoo.com','dsweds','we23'),
(7,'Ana','D','AnaD@yahoo.com','sfdgss','der4'),
(8,'Kultuma','M','KutulmaM@yahoo.com','wdfre34','gfdfg89'),
(9,'Najma','O','NajmaO@yahoo.com','sfgdf67','sdfe12');
INSERT INTO flight(FlightID,Destination,Destination_time,Arrival,Arrival_time)VALUES
(1,'Newcastle','16:45','Bristol','18:00'),
(2,'Bristol','8:00','Newcastle','09:15'),
(3,'Cardiff','06:00','Edinburgh','07:30'),
(4,'Bristol','11:30','Manchester','12:30'),
(5,'Manchester','12:20','Bristol','13:20'),
(6,'Bristol','07:40','London','08:20'),
(7,'London','11:00','Manchester','12:20'),
(8,'Manchester','12:20','Glasgow','13:30'),
(9,'Bristol','07:40','Glasgow','08:45'),
(10,'Glasgow','14:30','Newcastle','15:45'),
(11,'Newcastle','16:15','Manchester','17:05'),
(12,'Manchester','18:25','Bristol','19:30'),
(13,'Bristol','06:20','Manchester','07:20'),
(14,'Portsmouth','12:00','Dundee','14:00'),
(15,'Dundee','10:00','Portsmouth','12:00'),
(16,'Edinburgh','18:30','Cardiff','20:00'),
(17,'Southampton','12:00','Manchester','13:30'),
(18,'Manchester','19:00','Southampton','20:30'),
(19,'Birmingham','16:00','Newcastle','17:30'),
(20,'Newcastle','06:00','Birmingham','07:30'),
(21,'Aberdeen','07:00','Portsmouth','09:00');
INSERT INTO plane_cost(price,flightID)VALUES
(80,1),
(80,2),
(80,3),
(60,4),
(60,5),
(60,6),
(75,7),
(75,8),
(90,9),
(75,10),
(75,11),
(60,12),
(60,13),
(100,14),
(100,15),
(75,16),
(75,17),
(70,18),
(75,19),
(75,20),
(75,21);

SELECT * FROM customer;
