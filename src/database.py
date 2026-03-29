import sqlite3


videos = [{'title': 'A bad day to use python', 'videoId': 'mx3g7XoPVNQ'}, {'title': '25 Tips &amp; Tricks in Python', 'videoId': 's_oXtdhqXR8'}, {'title': 'Python Full Course for Beginners', 'videoId': 'K5KVEU3aaeQ'}, {'title': 'you need to learn Python RIGHT NOW!! // EP 1', 'videoId': 'mRMmlo_Uqcs'}, {'title': 'Python in 100 Seconds', 'videoId': 'x7X9w_GIm1s'}]






def db_creator():
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
    con.close()





def insert_videos(videos):
    con = sqlite3.connect("data/database.db")
    cur = con.cursor()
    for video in videos:
        videoId = video.get("videoId")
        title = video.get("title")
        relevant =  1

        cur.execute("""
            INSERT OR IGNORE INTO yt_rel(videoId, title, relevant) VALUES(
                ?, ?,?
                )     
            """, (videoId,title, relevant))
    con.commit()
    con.close()

