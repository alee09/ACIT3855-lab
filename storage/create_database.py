import sqlite3

from app import report_rapid_test_reading

conn = sqlite3.connect('readings.sqlite')

c = conn.cursor()
c.execute('''
          CREATE TABLE User
          (personal_health_number VARCHAR(12) PRIMARY KEY NOT NULL,
              first_name VARCHAR(50) NOT NULL,
              last_name VARCHAR(50) NOT NULL,
              postal_code VARCHAR(7) NOT NULL,
              street VARCHAR(30) NOT NULL,
              city VARCHAR(30) NOT NULL,
              prov VARCHAR(30) NOT NULL,
              country VARCHAR(30) NOT NULL,
              age INTEGER NOT NULL,
              password varchar(500) NOT NULL,
              trace_id VARCHAR(50) NOT NULL,
              date_created VARCHAR(100) NOT NULL)
          ''')

c.execute('''
            CREATE TABLE rapid_test
            (personal_health_number VARCHAR(12) PRIMARY KEY NOT NULL,
            manName VARCHAR(250) NOT NULL,
            homePage VARCHAR(250) NOT NULL,
            result_date VARCHAR(100) NOT NULL,
            result VARCHAR(10) NOT NULL,
            tests_taken INTEGER NOT NULL,
            current_date VARCHAR(100) NOT NULL,
            trace_id VARCHAR(50) NOT NULL)
'''
)

conn.commit()
conn.close()