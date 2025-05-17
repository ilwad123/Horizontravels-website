#Ilwad Abdi student id =22014624

from flask import Flask, render_template, request, session, redirect, url_for,flash,jsonify
from passlib.hash import sha256_crypt
import hashlib
import gc
import dbfunc, mysql.connector
from functools import wraps
from datetime import datetime
import os

from mysql.connector import errorcode
hostname = os.getenv("DB_HOST", "localhost")
username = os.getenv("DB_USER", "root")
passwd   = os.getenv("DB_PASSWORD", "")
db       = os.getenv("DB_NAME", "horizontravels")

def getConnection():
    try:
        conn = mysql.connector.connect(
            host=hostname,
            user=username,
            password=passwd,
            database=db
        )
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('User name or Password is not working')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print('Database does not exist')
        else:
            print(err)
        return None
    
app=Flask(__name__)
app.secret_key = 'This is my Secret Key'


@app.route('/')
def Home():
    conn = dbfunc.getConnection()
    if conn:
        dbcursor = conn.cursor()
        dbcursor.execute('SELECT DISTINCT Destination FROM flight;')
        rows = dbcursor.fetchall()
        dbcursor.close()
        conn.close()
        cities = [row[0] for row in rows]
        return render_template('Home.html', departurelist=cities)
    else:
        return 'DB Connection Error'

@app.route('/Policy')
def Policy():
    return render_template('Policy.html')
 
@app.route('/adminuser')
def adminuser():
    return render_template('adminuser.html')

@app.route('/Register')
def Register():
  return render_template("Signup.html")

@app.route('/Login1')
def Login1():
    return render_template("Login.html")    

@app.route('/mybooking')
def mybooking():
      return redirect(url_for('generateuserrecord'))
  


@app.route('/bookingstart')
def bookingstart():
    return render_template("bookingstart.html")

@app.route('/adminreport')
def adminreport():
    return render_template('generateadminreport')

@app.route('/termsandcondition')
def termsandconditions():
    return render_template("termsandcondition.html")

@app.route('/updaterecord')
def updaterecord():
    return redirect(url_for("updaterecord.html"))


@app.route('/deleterecord')
def deleterecord():
    return redirect(url_for('generatedeleterecord'))



@app.route('/Signup/', methods=["POST" , "GET"])
def Signup():
    error = ''
    print('Sign up start')
    try:
        if request.method == "POST":     
            Fname=request.form['Fname']  
            Sname=request.form['Sname']  
            username = request.form['username']
            password = request.form['password']
            email = request.form['email']                             
            if username != None and password != None and email != None:           
                conn = getConnection()
                if conn != None:    #Checking if connection is None           
                    if conn.is_connected(): #Checking if connection is established
                        print('MySQL Connection is established')                          
                        dbcursor = conn.cursor()    #Creating cursor object 
                        #here we should check if username / email already exists                                                           
                        password = sha256_crypt.hash((str(password)))           
                        Verify_Query = "SELECT * FROM customer WHERE username = %s;"
                        dbcursor.execute(Verify_Query,(username,))
                        rows = dbcursor.fetchall()           
                        if dbcursor.rowcount > 0:   #this means there is a user with same name
                            print('username already taken, please choose another')
                            error = "User name already taken, please choose another"
                            return render_template("Signup.html", error=error)    
                        else:   #this means we can add new user    
                            dbcursor.execute("INSERT INTO customer (Fname,Sname,username, password_hash, \
                                 email) VALUES (%s, %s, %s, %s, %s)", (Fname, Sname, username, password, email))                
                            conn.commit()  #saves data in database              
                            print("Thanks for registering!")
                            dbcursor.close()
                            conn.close()
                            gc.collect()                      
                            session['logged_in'] = True     #session variables
                            session['username'] = username
                            session['usertype'] = 'standard'   #default all users are standard
                            return render_template("Login.html",\
                             message='User registered successfully and logged in..')
                    else:                        
                        print('Connection error')
                        return 'DB Connection Error'
                else:                    
                    print('Connection error')
                    return 'DB Connection Error'
            else:                
                print('empty parameters')
                return render_template("Signup.html", error=error)
        else:            
            return render_template("Signup.html", error=error)        
    except Exception as e:                
        return render_template("Signup.html", error=e)    

    return render_template("Signup.html", error=error)




@app.route('/Login' , methods=["GET","POST"])
def Login():
    form={}
    error = ''
    try:	
        if request.method == "POST":            
            username = request.form['username']
            password = request.form['password']            
            form = request.form
            print('login start 1.1')
            
            if username != None and password != None:  #check if un or pw is none          
                conn = getConnection()
                if conn != None:    #Checking if connection is None                    
                    if conn.is_connected(): #Checking if connection is established                        
                        print('MySQL Connection is established')                          
                        dbcursor = conn.cursor()    #Creating cursor object                                                 
                        dbcursor.execute("SELECT password_hash, usertype,CustID \
                            FROM customer WHERE username = %s;", (username,))                                                
                        data = dbcursor.fetchone()
                        #print(data[0])
                        if dbcursor.rowcount < 1: #this mean no user exists                         
                            error = "User / password does not exist, login again"
                            return render_template("Login.html", error=error)
                        else:                            
                            #data = dbcursor.fetchone()[0] #extracting password   
                            # verify passowrd hash and password received from user                                                             
                            if sha256_crypt.verify(request.form['password'], str(data[0])):                                
                                session['logged_in'] = True     #set session variables
                                session['username'] = request.form['username']
                                session['CustID']=str(data[2])
                                session['usertype'] = str(data[1])                          
                                print("You are now logged in")
                                if (session['usertype'] == 'standard'):
                                     print('standard')
                                     return redirect(url_for('Home'))
                                    #  return render_template('Home.html', \
                                    #       username=username, data='this is user specific data',\
                                    #       usertype=session['usertype'])
                                elif (session['usertype'] =='Admin'):
                                    print('admin')
                                    return render_template('adminuser.html', \
                                          username=username, data='this is user specific data',\
                                          usertype=session['usertype'])
                                
                            else:
                                error = "Invalid credentials username/password, try again."                               
                    gc.collect()
                    print('login start 1.10')
                    return render_template("Login.html", form=form, error=error)
    except Exception as e:                
        error = str(e) + " Invalid credentials, try again."
        return render_template("Login.html", form=form, error = error)   
    
    return render_template("Login.html", form=form, error = error)

def Login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:            
            print("You need to login first")
            #return redirect(url_for('login', error='You need to login first'))
            return redirect(url_for("Login.html", error='You need to login first'))  
    return wrap

def standard_user_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if ('logged_in' in session) and (session['usertype'] == 'standard'):
            return f(*args, **kwargs)
        else:            
            print("You need to login first as standard user")
            #return redirect(url_for('login', error='You need to login first as standard user'))
            return redirect(url_for('Login', error='You need to login first as standard user'))    
    return wrap

def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if ('logged_in' in session) and (session['usertype'] == 'Admin'):
            return f(*args, **kwargs)
        else:            
            print("You need to login first as admin user")
            #return redirect(url_for('login', error='You need to login first as admin user'))
            return render_template('Login.html', error='You need to login first as admin user')    
    return wrap

     
@app.route("/logout/")
@Login_required
def logout():    
    session.clear()    #clears session variables
    print("You have been logged out!")
    gc.collect()
    return redirect(url_for('Home', optionalmessage='You have been logged out'))
	
@app.route('/cities')
def cities():
	conn = dbfunc.getConnection()
	if conn != None:    #Checking if connection is None         
		print('MySQL Connection is established')                          
		dbcursor = conn.cursor()    #Creating cursor object            
		dbcursor.execute('SELECT DISTINCT Destination FROM flight;')   
		#print('SELECT statement executed successfully.')             
		rows = dbcursor.fetchall()                                    
		dbcursor.close()              
		conn.close() #Connection must be 
		cities = []
		for city in rows:
			city = str(city).strip("(")
			city = str(city).strip(")")
			city = str(city).strip(",")
			city = str(city).strip("'")
			cities.append(city)
		return render_template('Home.html', departurelist=cities)
	else:
		print('DB connection Error')
		return 'DB Connection Error'
	
@app.route ('/returncity/', methods = ['POST', 'GET'])
def ajax_returncity():   
	print('/returncity') 

	if request.method == 'GET':
		deptcity = request.args.get('q')
		conn = dbfunc.getConnection()
		if conn != None:    #Checking if connection is None         
			print('MySQL Connection is established')                          
			dbcursor = conn.cursor()    #Creating cursor object            
			dbcursor.execute('SELECT DISTINCT Arrival FROM flight WHERE Destination = %s;', (deptcity,))   
			#print('SELECT statement executed successfully.')             
			rows = dbcursor.fetchall()
			total = dbcursor.rowcount                                    
			dbcursor.close()              
			conn.close() #Connection must be closed			
			return jsonify(returncities=rows, size=total)
		else:
			print('DB connection Error')
			return jsonify(returncities='DB Connection Error')

@app.route('/selectBooking/', methods=["POST", "GET"])
def selectBooking():
    if request.method == "POST":
        Destination = request.form['departureslist']
        Arrival = request.form['arrivalslist']
        Departure_date = request.form['Departure_date']
        Arrival_date = request.form['Arrival_date']
        Adultseat = request.form['Adultseat']
        Childseat = request.form['Childseat']
        Class=request.form['Class']
        lookupdata = [Destination, Arrival, Departure_date, Arrival_date, Adultseat, Childseat,Class]
        conn = dbfunc.getConnection()
        if conn != None:
            print('MySQL Connection is established')
            dbcursor = conn.cursor()
            dbcursor.execute('SELECT flight.*, plane_cost.price FROM flight INNER JOIN plane_cost ON flight.FlightID=plane_cost.FlightID WHERE Destination = %s AND Arrival = %s;', (Destination, Arrival))   
            rows = dbcursor.fetchall()
            datarows=[]			
            for row in rows:
                price=row[5]
                data = list(row)
                fare = (float(price) * float(Adultseat)) + (float(price) * 0.5 * float(Childseat))
				#print(fare)
                if Class=="Business":
                    fare*=2
                else:
                    fare
                data.append(fare)
                datarows.append(data)			
            dbcursor.close()              
            conn.close() #Connection must be closed
			#print(datarows)
			#print(len(datarows))	
            return render_template('bookingstart.html', resultset=datarows, lookupdata=lookupdata)
        else:
            print('DB connection Error')
            return redirect(url_for('cities'))
   


    
	
#fix booking 
#place prices in the same table 
#add if statement for class 
#

@app.route ('/booking_confirm/', methods = ['POST', 'GET'])
def booking_confirm():
    if request.method == "POST":
        if  not 'username' in session:
           return redirect(url_for('Login'))		
	   #print('booking confirm initiated')
        flightID= request.form['bookingchoice']		
        Destination = request.form['deptcity']
        Arrival = request.form['arrivcity']
        Departure_date = request.form['Departure_date']
        Arrival_date = request.form['Arrival_date']
        Adultseat = request.form['Adultseat']
        Childseat = request.form['Childseat']
        totalprice = request.form['totalprice']
        cardNo = request.form['cardNo']
        cardname=request.form['cardname']
        expirydate=request.form['expirydate'] 
        CVVs=request.form['CVV']
        
        Class=request.form['Class']
        CustID=session['CustID']
        totalseats = int(Adultseat) + int(Childseat)
        bookingdata = [flightID, Destination, Arrival, Departure_date, Arrival_date, Adultseat, Childseat, totalprice]
        conn = dbfunc.getConnection()
        if conn != None:    #Checking if connection is None         
           print('MySQL Connection is established wewerr')                          
           dbcursor = conn.cursor()
           print('==================')#Creating cursor object   
           # Insert payment
           dbcursor.execute('''
                INSERT INTO flight_payment (CustID, cardNo, cardname, expirydate, CVV, totalprice)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (CustID, cardNo, cardname, expirydate, CVVs, totalprice))
        # Get paymentID
           dbcursor.execute('SELECT LAST_INSERT_ID();')
           paymentID = dbcursor.fetchone()[0]
           # Insert ticket with paymentID
           dbcursor.execute('''
            INSERT INTO Ticket_details (
                CustID, FlightID, Departure_date, Arrival_date,
                totalseats, class, totalprice, paymentID
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ''', (CustID, flightID, Departure_date, Arrival_date,
            totalseats, Class, totalprice, paymentID))
           print('Booking statement executed successfully.')
           conn.commit()	
		   #dbcursor.execute('SELECT AUTO_INCREMENT - 1 FROM information_schema.TABLES WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s;', ('TEST_DB', 'bookings'))   
           dbcursor.execute('SELECT LAST_INSERT_ID();')
		   #print('SELECT statement executed successfully.')             
           rows = dbcursor.fetchone()
		  #print ('row count: ' + str(dbcursor.rowcount))
           BookingID = rows[0]
           bookingdata.append(BookingID)
           dbcursor.execute('SELECT * FROM flight WHERE FlightID = %s;', (flightID,))   			
           rows = dbcursor.fetchall()
           Destination_time = rows[0][2]
           Arrival_time = rows[0][4]
           bookingdata.append(Destination_time)
           bookingdata.append(Arrival_time)
		#print(bookingdata)
		#print(len(bookingdata))
           cardNo = cardNo[-4:-1]
           print(cardNo)
           dbcursor.execute
           dbcursor.close()              
           conn.close() #Connection must be closed
           return render_template('booking_confirm.html', resultset=bookingdata, cardNo=cardNo)
    else:
        print('DB connection Error')
        return redirect(url_for('cities'))

 

@app.route ('/dumpsVar/', methods = ['POST', 'GET'])
def dumpVar():
	if request.method == 'POST':
		result = request.form
		output = "<H2>Data Received: </H2></br>"
		output += "Number of Data Fields : " + str(len(result))
		for key in list(result.keys()):
			output = output + " </br> " + key + " : " + result.get(key)
		return output
	else:
		result = request.args
		output = "<H2>Data Received: </H2></br>"
		output += "Number of Data Fields : " + str(len(result))
		for key in list(result.keys()):
			output = output + " </br> " + key + " : " + result.get(key)
		return output  


@app.route('/generateuserrecord/', methods=['GET','POST'])
def generateuserrecord():
    if 'CustID' not in session:
        session['CustID'] = '0'
    CustID = session['CustID']
    if 'username' not in session:
        session['username'] = 'guest'
    conn = dbfunc.getConnection()
    if conn:
        print('Generate Connection is established')
        dbcursor = conn.cursor()
        dbcursor.execute('SELECT Ticket_details.BookingID, Ticket_details.Departure_date, Ticket_details.Arrival_date, flight.Destination, flight.Arrival, Ticket_details.FlightID, Ticket_details.totalprice, Ticket_details.class FROM Ticket_details INNER JOIN flight ON Ticket_details.FlightID = flight.FlightID WHERE CustID = %s', (CustID,))
        rows = dbcursor.fetchall()
        datarows = []
        for row in rows:
            data = list(row)
            datarows.append(data)
        dbcursor.close()
        conn.close()
        return render_template('mybooking.html', datarows=datarows, username=session['username'])
    else:
        print('DB connection Error')
        flash('Error connecting to the database.')
        return redirect(url_for('Home'))
    
# @app.route('/generateuserrecord/' , methods= ['POST', 'GET'])
# def generateuserrecord():
#     if not 'CustID' in session:
#         session['CustID']='0'
#     CustID=session['CustID']
#     if not 'username' in session:
#         session['username']='guest'
#     conn = dbfunc.getConnection()
#     if conn != None:
#         print(' Generate Connection is established ')
#         dbcursor = conn.cursor()
#         # dbcursor.execute('SELECT Ticket_details.BookingID, Ticket_details.Departure_date, Ticket_details.Arrival_date, flight.Destination, flight.Arrival, Ticket_details.FlightID, Ticket_details.totalprice, Ticket_details.class FROM Ticket_details INNER JOIN flight ON Ticket_details.FlightID = flight.FlightID WHERE CustID=CustID')
#         dbcursor.execute('SELECT Ticket_details.BookingID, Ticket_details.Departure_date, Ticket_details.Arrival_date, flight.Destination, flight.Arrival, Ticket_details.FlightID, Ticket_details.totalprice, Ticket_details.class FROM Ticket_details,flight WHERE Ticket_details.FlightID = flight.FlightID AND Ticket_details.CustID = %s;',(CustID,))

#         rows = dbcursor.fetchall()
#         datarows = []			
#         for row in rows:
#             data = list(row)
#             datarows.append(data)
#             # print(datarows)
#         dbcursor.close()             
#         conn.close() 
        
#         return render_template('mybooking.html', datarows=rows , username=session['username'])
#     else:
#         print('DB connection Error')
#         return redirect(url_for('Home'))
    
@app.route('/deletebooking', methods= ['POST', 'GET'] )
def deletebooking():
    print("h")
    BookingID=request.form['BookingID']
    conn = dbfunc.getConnection()
    if conn != None:
        dbcursor = conn.cursor()
       #dbcursor.execute('INSERT INTO cancelled (CustID, FlightID, Departure_date, Arrival_date, totalseats, class, totalprice) VALUES (%s, %s, %s, %s, %s, %s, %s)',bookingid)
       # Delete the booking from the 'Ticket_details' table
       #dbcursor.execute("DELETE FROM Ticket_details WHERE BookingID=%s AND Departure_date=%s AND Arrival_date=%s AND Destination=%s AND Arrival=%s AND Flight ID=%s AND totalprice=%s AND Class=%s;" , BookingID)
        dbcursor.execute("DELETE FROM Ticket_details WHERE BookingID=%s", (BookingID,))
        conn.commit()
        dbcursor.close()
        conn.close()
        flash('Booking canceled successfully.', "success")
        return redirect(url_for('mybooking'))
    else:
        flash("Something went wrong.", "error")
        return redirect(url_for('Home'))
     
@app.route('/generateadminreport')
def generateadminreport():
    conn = dbfunc.getConnection()
    if conn != None:
        print(' Generate Connection is established ')
        dbcursor = conn.cursor()
        # dbcursor.execute('SELECT Ticket_details.BookingID, Ticket_details.Departure_date, Ticket_details.Arrival_date, flight.Destination, flight.Arrival, Ticket_details.FlightID, Ticket_details.totalprice, Ticket_details.class FROM Ticket_details INNER JOIN flight ON Ticket_details.FlightID = flight.FlightID WHERE CustID=CustID')
        dbcursor.execute('SELECT Ticket_details.CustID,Ticket_details.BookingID, Ticket_details.Departure_date, Ticket_details.Arrival_date, flight.Destination, flight.Arrival, Ticket_details.FlightID, Ticket_details.totalprice, Ticket_details.class FROM Ticket_details,flight WHERE Ticket_details.FlightID = flight.FlightID')

        rows = dbcursor.fetchall()
        datarows = []			
        for row in rows:
            data = list(row)
            datarows.append(data)
            # print(datarows)
        dbcursor.close()             
        conn.close() 
        
        return render_template('adminreport.html', datarows=rows)
    else:
        print('DB connection Error')
        return redirect(url_for('Home'))
    
@app.route('/showupdatepage')
def showupdatepage():
    return render_template('updaterecord.html')

@app.route('/addrecordpage')
def addrecordpage():
    return render_template('addrecord.html')

@app.route('/generateupdaterecord', methods=["POST", "GET"])
def generateupdaterecord():
    print('generate')
    print(request.method)
    if request.method == "POST":
        Destination = request.form['Destination']
        Arrival = request.form['Arrival']
        Destination_time = request.form['Destination_time']
        Arrival_time = request.form['Arrival_time']
        price = request.form['price']
        print('form')
        conn = dbfunc.getConnection()
        if conn != None:
            print('Connection is established')
            dbcursor = conn.cursor()
            # Insert into flight table
            dbcursor.execute("INSERT INTO flight (Destination, Destination_time, Arrival, Arrival_time) VALUES \
             (%s, %s, %s, %s)", (Destination, Destination_time, Arrival, Arrival_time))
            #get the last inserted FlightID
            FlightID = dbcursor.lastrowid
            # Insert into plane_cost table
            dbcursor.execute("""
                INSERT INTO plane_cost (price, FlightID)
                VALUES (%s, %s)
            """, (price, FlightID))
            conn.commit()
            dbcursor.close()
            conn.close()
            flash('Journey successfully added.', 'success')
            return render_template('updaterecord.html')
        else:
            print('DB connection Error')
            flash('DB connection Error', 'error')
            return redirect(url_for('Home'))
    else:
        print('Invalid request method')
        return redirect(url_for('Home'))
@app.route('/addrecord', methods=["POST", "GET"])
def addrecord():
    print('generate')
    print(request.method)
    if request.method == "POST":
        Fname = request.form['Fname']
        Sname = request.form['Sname']
        email= request.form['email']
        username=request.form['username']
        password_hash = request.form['password_hash']
        print('form')
        conn = dbfunc.getConnection()
        if conn != None:
            print('Connection is established')
            dbcursor = conn.cursor()
            dbcursor.execute("INSERT INTO customer (Fname, Sname, email,username, password_hash) VALUES \
             (%s, %s, %s, %s,%s)", (Fname, Sname, email,username, password_hash))
            conn.commit()
            dbcursor.close()
            conn.close()
            flash('New user added.')
            return render_template('addrecord.html')
        else:
            print('DB connection Error')
            return redirect(url_for('Home'))
    else:
        print('Invalid request method')
        return redirect(url_for('Home'))

    
@app.route('/generatedeleterecord', methods=["POST", "GET"])
def generatedeleterecord():
    print('delete')
    if request.method == "POST":
        FlightID = request.form['FlightID']
        print('form')
        conn = dbfunc.getConnection()
        if conn != None:
            print('Connection is established')
            dbcursor = conn.cursor()
            dbcursor.execute("DELETE FROM plane_cost WHERE FlightID=%s;", (FlightID,))
            # Delete from flight table
            dbcursor.execute("DELETE FROM flight WHERE FlightID=%s;", (FlightID,))
            conn.commit()
            dbcursor.close()
            conn.close()
            flash('Journey successfully deleted.', 'success')
            return redirect(url_for('showdeleteflights'))
        else:
            print('DB connection Error')
            return redirect(url_for('Home'))
    else:
        print('Invalid request method')
        return redirect(url_for('Home'))

@app.route('/showdeletepage')
def showdeleteflights():
    conn = dbfunc.getConnection()
    if conn:
        dbcursor = conn.cursor()
        dbcursor.execute('SELECT FlightID, Destination, Destination_time, Arrival, Arrival_time FROM flight')
        rows = dbcursor.fetchall()
        dbcursor.close()
        conn.close()
        return render_template('deleterecord.html', datarows=rows)
    else:
        flash('DB connection Error', 'error')
        return redirect(url_for('Home'))

   
def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if ('logged_in' in session) and (session['usertype'] == 'admin'):
            return f(*args, **kwargs)
        else:            
            print("You need to login first as admin user")
            return render_template('Login.html', error='You need to login first as admin user')    
    return wrap



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)



