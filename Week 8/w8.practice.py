import sqlite3

#need to connect or create a database

conn = sqlite3.connect('example.db')

#create a cursor object
cur= conn.cursor()

# Create a tablle
cur.execute('''CREATE TABLE IF NOT EXISTS users
               (id INTEGER PRIMARY KEY,
                name TEXT, 
                age INTEGER)
            ''')

#INSERT DATA- A ROW INTO THE TABLE
cur.execute("INSERT INTO users (name, age) VALUES (?, ?)", ('Albert', 38))

cur.executemany("INSERT INTO users (name, age) VALUES (?, ?)", [('Alice', 30), ('Bob', 80)])
                            
#changes to be saved by using 'commit'
conn.commit()

#Query the database
cur.execute("SELECT * FROM users")

print(cur.fetchall())

#Close the connection
conn.close()