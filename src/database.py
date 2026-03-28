import sqlite3

con = sqlite3.connect("data/database.db")

cur = con.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS yt_rel(
        id INTEGER PRIMARY KEY,
        videoId TEXT UNIQUE,
        title TEXT,
        relevant INTEGER
    )
""")

cur.execute("""
    INSERT into yt_rel(videoId, title, relevant) VALUES(
        'test123', 
        'machine learning',
        1)     
""")
take = cur.execute("""SELECT * FROM yt_rel""")
list = cur.fetchall()
print(list)
con.close()