import mysql.connector 
 
db_conn = mysql.connector.connect(host="localhost", user="user", 
password="password", database="events")   
 
db_cursor = db_conn.cursor() 
 
db_cursor.execute(''' 
          CREATE TABLE User 
          (personal_health_number VARCHAR(12) NOT NULL,  
           first_name VARCHAR(250) NOT NULL, 
           last_name VARCHAR(250) NOT NULL, 
           postal_code varchar(7) NOT NULL, 
           street VARCHAR(30) NOT NULL, 
           city VARCHAR(30) NOT NULL, 
           province VARCHAR(30) NOT NULL,
           country VARCHAR(30) NOT NULL,
           age INTEGER NOT NULL,
           password VARCHAR(500) NOT NULL,
           trace_id VARCHAR(50) NOT NULL,
           date_created VARCHAR(100) NOT NULL,
           CONSTRAINT User_pk PRIMARY KEY (personal_health_number)) 
          ''') 
 
db_cursor.execute(''' 
          CREATE TABLE rapid_test 
          (personal_health_number VARCHAR(12) NOT NULL,
           manName VARCHAR(250) NOT NULL, 
           homePage VARCHAR(250) NOT NULL, 
           result_date VARCHAR(250) NOT NULL, 
           rapid_test_result VARCHAR(10) NOT NULL, 
           num_tests_taken INTEGER NOT NULL, 
           date VARCHAR(100) NOT NULL, 
           trace_id VARCHAR(50) NOT NULL,
           CONSTRAINT rapid_test_pk PRIMARY KEY (personal_health_number)) 
          ''') 
 
db_conn.commit() 
db_conn.close() 