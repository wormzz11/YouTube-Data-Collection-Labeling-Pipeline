import sqlite3

def db_creator():
    with sqlite3.connect("data/database.db") as con:
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
  


def insert_videos(videos):
    with sqlite3.connect("data/database.db") as con:
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
   


def insert_evaluation(evaluation):
    with sqlite3.connect("data/database.db") as  con:
        cur = con.cursor()
        cur.execute("""
            UPDATE yt_rel
            set relevant = ?
            WHERE videoId = ?
            """, (evaluation[1], evaluation[0])) 
        
 
def evaluation_count():
    with sqlite3.connect("data/database.db") as con:
        cur = con.cursor()
        cur.execute("""        
        SELECT
            COALESCE(SUM(CASE WHEN relevant IS NOT NULL THEN 1 ELSE 0 END), 0),
            COALESCE(SUM(CASE WHEN relevant IS NULL THEN 1 ELSE 0 END), 0)
        FROM yt_rel      
        """)
        result = cur.fetchone()
        return result   


def load_next_video():
    with sqlite3.connect("data/database.db") as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("""
            SELECT id, videoId, title, thumbnail, relevant
            FROM yt_rel
            WHERE relevant IS NULL
            ORDER BY id ASC
            LIMIT 1
        """)
        return cur.fetchone()
    
import sqlite3

def reset_database():
    with sqlite3.connect("data/database.db") as con:
        cur = con.cursor()
        cur.execute("UPDATE yt_rel SET relevant = NULL")
        con.commit()

def load_adjacent_video(current_id, direction="next"):
    """Load the next or previous video relative to current_id."""
    with sqlite3.connect("data/database.db") as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        if direction == "next":
            cur.execute("""
                SELECT id, videoId, title, thumbnail, relevant
                FROM yt_rel
                WHERE id > ?
                ORDER BY id ASC
                LIMIT 1
            """, (current_id,))
        else:
            cur.execute("""
                SELECT id, videoId, title, thumbnail, relevant
                FROM yt_rel
                WHERE id < ?
                ORDER BY id DESC
                LIMIT 1
            """, (current_id,))
        return cur.fetchone()
 