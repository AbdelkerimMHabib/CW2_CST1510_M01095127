import sqlite3

#need to connect or create a database

conn = sqlite3.connect('University.db')

#create a cursor object
cur= conn.cursor()

# Create a tablle
cur.execute('''CREATE TABLE IF NOT EXISTS users
               (id INTEGER PRIMARY KEY,
                name TEXT,
                email TEXT,
                age INTEGER,
                MISIS TEXT)
            ''')

#INSERT DATA- A ROW INTO THE TABLE
cur.execute("INSERT INTO users (name, email, age, MISIS) VALUES (?, ?, ?, ?)", ('Albert', 'albert@example.com', 38, 'M12345678'))

cur.executemany("INSERT INTO users (name, email, age, MISIS) VALUES (?, ?, ?, ?)", [('Alice', 'alice@example.com', 30, 'M87654321'), ('Bob', 'bob@example.com', 80, 'M13579246')])
                            
#changes to be saved by using 'commit'
conn.commit()

#Query the database
cur.execute("SELECT * FROM users")

print(cur.fetchall())


cur.execute("UPDATE users SET age = 40 WHERE name = 'albert'")

conn.commit()


conn.close()