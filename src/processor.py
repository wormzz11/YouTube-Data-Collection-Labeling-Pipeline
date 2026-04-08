def processing(response):
    processed_data = []
    for item in response.get("items"):
        video_id = item.get("id", {}).get("videoId")
        title = item.get("snippet", {}).get("title")
        description = item.get("snippet", {}).get("description")
        snippet = item.get("snippet")
        thumbnails = snippet.get("thumbnails")
        thumbnail = (
            thumbnails.get("maxres", {}).get("url") or
            thumbnails.get("high", {}).get("url") or
            thumbnails.get("medium", {}).get("url") or
            thumbnails.get("default", {}).get("url") 
        )
        

        if video_id and title and thumbnail and description:
            video_data = {
                    "title" : title,
                    "videoId" : video_id,
                    "thumbnail" : thumbnail,
                    "description" : description
                }
                
            processed_data.append(video_data)
    return processed_data
            

import sqlite3

DB_PATH = "data/database.db"

with sqlite3.connect(DB_PATH) as con:
    cur = con.cursor()
    cur.execute("""
        UPDATE yt_rel AS target
        SET description = (
            SELECT source.description
            FROM yt_rel AS source
            WHERE source.videoId = target.videoId
              AND source.theme IS NULL
            LIMIT 1
        )
        WHERE target.theme IS NOT NULL
          AND target.description IS NULL;
    """)
    con.commit()