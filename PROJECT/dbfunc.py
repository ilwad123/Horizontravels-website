#Ilwad Abdi student id =22014624


import mysql.connector
from mysql.connector import errorcode
import os 
from dotenv import load_dotenv
load_dotenv()
# MYSQL CONFIG VARIABLES
hostname = os.getenv("DB_HOST", "localhost")
username = os.getenv("DB_USER", "root")
passwd   = os.getenv("DB_PASSWORD", "")
db       = os.getenv("DB_NAME", "horizontravels")


def getConnection():    
    try:
        conn = mysql.connector.connect(host=hostname,                              
                              user=username,
                              password=passwd,
                              database=db)  
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('User name or Password is not working')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print('Database does not exist')
        else:
            print(err)                        
    else:  #will execute if there is no exception raised in try block
        return conn   