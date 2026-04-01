import sqlite3

DB_PATH = "data/database.db"

def db_creator():
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS yt_rel(
                id        INTEGER PRIMARY KEY,
                videoId   TEXT,
                title     TEXT,
                thumbnail TEXT,
                relevant  INTEGER,
                theme     TEXT,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(videoId, theme)
            )
        """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_yt_rel_theme_relevant ON yt_rel(theme, relevant)")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_yt_rel_videoId ON yt_rel(videoId)")
        cur.execute("""
            CREATE TRIGGER IF NOT EXISTS trg_yt_rel_updated_at
            AFTER UPDATE ON yt_rel
            FOR EACH ROW
            BEGIN
              UPDATE yt_rel SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
            END;
        """)
        con.commit()

def insert_videos(videos):
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        for video in videos:
            videoId = video.get("videoId")
            title = video.get("title")
            thumbnail = video.get("thumbnail")
            cur.execute("""
                INSERT OR IGNORE INTO yt_rel(videoId, title, thumbnail, relevant, theme)
                VALUES(?, ?, ?, NULL, NULL)
            """, (videoId, title, thumbnail))
        con.commit()

def insert_evaluation(evaluation):
    videoId, relevancy, theme = evaluation
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        if theme is None:
            cur.execute("SELECT id FROM yt_rel WHERE videoId = ? AND theme IS NULL", (videoId,))
            existing = cur.fetchone()
            if existing:
                cur.execute("UPDATE yt_rel SET relevant = ?, updated_at = CURRENT_TIMESTAMP WHERE videoId = ? AND theme IS NULL",
                            (relevancy, videoId))
            else:
                cur.execute("""
                    INSERT INTO yt_rel(videoId, title, thumbnail, relevant, theme)
                    VALUES(?, ?, ?, ?, NULL)
                """, (videoId, None, None, relevancy))
        else:
            cur.execute("UPDATE yt_rel SET relevant = ?, updated_at = CURRENT_TIMESTAMP WHERE videoId = ? AND theme = ?",
                        (relevancy, videoId, theme))
            if cur.rowcount == 0:
                cur.execute("""
                    INSERT INTO yt_rel(videoId, title, thumbnail, relevant, theme)
                    SELECT videoId, title, thumbnail, ?, ?
                    FROM yt_rel
                    WHERE videoId = ? AND theme IS NULL
                """, (relevancy, theme, videoId))
                cur.execute("SELECT id FROM yt_rel WHERE videoId = ? AND theme = ?", (videoId, theme))
                if cur.fetchone() is None:
                    cur.execute("""
                        INSERT INTO yt_rel(videoId, title, thumbnail, relevant, theme)
                        VALUES(?, ?, ?, ?, ?)
                    """, (videoId, None, None, relevancy, theme))
        con.commit()

def evaluation_count(theme=None):
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        if theme is not None:
            cur.execute("""
                SELECT
                    COALESCE(SUM(CASE WHEN relevant IS NOT NULL THEN 1 ELSE 0 END), 0)
                FROM yt_rel
                WHERE theme = ?
            """, (theme,))
            labeled = cur.fetchone()[0]
            cur.execute("""
                SELECT
                    COALESCE(COUNT(1), 0)
                FROM yt_rel AS base
                WHERE base.theme IS NULL
                  AND base.videoId NOT IN (SELECT videoId FROM yt_rel WHERE theme = ?)
            """, (theme,))
            unlabeled = cur.fetchone()[0]
        else:
            cur.execute("""
                SELECT
                    COALESCE(SUM(CASE WHEN relevant IS NOT NULL THEN 1 ELSE 0 END), 0),
                    COALESCE(SUM(CASE WHEN relevant IS NULL THEN 1 ELSE 0 END), 0)
                FROM yt_rel
                WHERE theme IS NULL
            """)
            row = cur.fetchone()
            labeled, unlabeled = row[0], row[1]
        return (int(labeled), int(unlabeled))

def load_next_video():
    with sqlite3.connect(DB_PATH) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("""
            SELECT id, videoId, title, thumbnail, relevant, theme
            FROM yt_rel
            WHERE relevant IS NULL AND theme IS NULL
            ORDER BY id ASC
            LIMIT 1
        """)
        return cur.fetchone()

def load_next_video_for_theme(theme):
    with sqlite3.connect(DB_PATH) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("""
            SELECT id, videoId, title, thumbnail, NULL as relevant, NULL as theme
            FROM yt_rel
            WHERE theme IS NULL
              AND videoId NOT IN (
                SELECT videoId FROM yt_rel WHERE theme = ?
              )
            ORDER BY id ASC
            LIMIT 1
        """, (theme,))
        return cur.fetchone()

def load_video_by_id(video_id):
    with sqlite3.connect(DB_PATH) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("""
            SELECT id, videoId, title, thumbnail, relevant, theme
            FROM yt_rel
            WHERE id = ?
            LIMIT 1
        """, (video_id,))
        return cur.fetchone()

def load_video_by_videoId(video_id):
    with sqlite3.connect(DB_PATH) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("""
            SELECT id, videoId, title, thumbnail, relevant, theme
            FROM yt_rel
            WHERE videoId = ? AND theme IS NULL
            LIMIT 1
        """, (video_id,))
        return cur.fetchone()

def load_adjacent_video(current_id, direction="next", theme=None):
    with sqlite3.connect(DB_PATH) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        if direction == "next":
            cur.execute("""
                SELECT id, videoId, title, thumbnail, NULL as relevant, NULL as theme
                FROM yt_rel
                WHERE theme IS NULL
                  AND id > ?
                ORDER BY id ASC
                LIMIT 1
            """, (current_id,))
        else:
            cur.execute("""
                SELECT id, videoId, title, thumbnail, NULL as relevant, NULL as theme
                FROM yt_rel
                WHERE theme IS NULL
                  AND id < ?
                ORDER BY id DESC
                LIMIT 1
            """, (current_id,))
        return cur.fetchone()

def load_adjacent_labeled_for_theme(current_id, direction="next", theme=None):
    with sqlite3.connect(DB_PATH) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        if direction == "next":
            cur.execute("""
                SELECT id, videoId, title, thumbnail, relevant, theme
                FROM yt_rel
                WHERE theme = ?
                  AND id > ?
                ORDER BY id ASC
                LIMIT 1
            """, (theme, current_id))
        else:
            cur.execute("""
                SELECT id, videoId, title, thumbnail, relevant, theme
                FROM yt_rel
                WHERE theme = ?
                  AND id < ?
                ORDER BY id DESC
                LIMIT 1
            """, (theme, current_id))
        return cur.fetchone()

def load_first_labeled_for_theme(theme):
    with sqlite3.connect(DB_PATH) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("""
            SELECT id, videoId, title, thumbnail, relevant, theme
            FROM yt_rel
            WHERE theme = ?
            ORDER BY id ASC
            LIMIT 1
        """, (theme,))
        return cur.fetchone()

def load_video_theme_status(video_id, theme):
    with sqlite3.connect(DB_PATH) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("""
            SELECT id, relevant FROM yt_rel WHERE videoId = ? AND theme = ? LIMIT 1
        """, (video_id, theme))
        return cur.fetchone()

def reset_database():
    with sqlite3.connect(DB_PATH) as con:
        cur = con.cursor()
        cur.execute("DELETE FROM yt_rel WHERE theme IS NOT NULL")
        cur.execute("UPDATE yt_rel SET relevant = NULL")
        con.commit()
