import sqlite3

def db_creator():
    con = sqlite3.connect("data/database.db")
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS yt_rel(
            id INTEGER PRIMARY KEY,
            videoId TEXT UNIQUE,
            title TEXT,
            thumbnail TEXT,
            relevant INTEGER
        )  
    """)
    con.close()


def insert_videos(videos):
    con = sqlite3.connect("data/database.db")
    cur = con.cursor()
    for video in videos:
        videoId = video.get("videoId")
        title = video.get("title")
        thumbnail = video.get("thumbnail")
        cur.execute("""
            INSERT OR IGNORE INTO yt_rel(videoId, title, thumbnail, relevant) VALUES(
                ?, ?,?, ?
                )     
            """, (videoId,title, thumbnail, None))
    con.commit()
    con.close()


def insert_evaluation(evaluated_videos):
    con = sqlite3.connect("data/database.db")
    cur = con.cursor()
    for evaluation in evaluated_videos:
        cur.execute("""
                    UPDATE yt_rel
                    set relevant = ?
                    WHERE videoId = ?
                    """, (evaluation[1], evaluation[0])) 
        
    con.commit()
    con.close()

def quick_inspection():
    con = sqlite3.connect("data/database.db")
    cur = con.cursor()
    res = cur.execute("Select * FROM yt_rel")
    print(res.fetchall())
    con.close()
