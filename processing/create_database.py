import sqlite3

conn = sqlite3.connect('stats.sqlite')

c = conn.cursor()
c.execute('''
            CREATE TABLE stats
            (id INTEGER PRIMARY KEY ASC,
            num_tests_results INTEGER NOT NULL,
            num_users INTEGER NOT NULL,
            num_positive_tests INTEGER NOT NULL,
            num_negative_tests INTEGER NOT NULL,
            highest_positive_occuring_age INTEGER NOT NULL,
            last_updated VARCHAR(100) NOT NULL)
            ''')

conn.commit()
conn.close()