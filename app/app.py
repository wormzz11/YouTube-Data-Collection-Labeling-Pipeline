import  streamlit as st
import sqlite3
from src.database import insert_evaluation

con = sqlite3.connect("data/database.db")
cur = con.cursor()

cur.execute("""SELECT id, videoId, title, thumbnail 
FROM yt_rel
WHERE relevant IS NULL
ORDER BY id
LIMIT 1
""")
video = cur.fetchone()


st.image(video[3], video[2])
id =  video[1]


if st.button("doge"):
    evaluation = (id, 1)
    insert_evaluation(evaluation)

  

if st.button("cate"):
    evaluation = (id, 0)
    insert_evaluation(evaluation)









#test = [(1, 'E8HxOFUKbWo', 'DOG FUNNY REACTION PART 3 #dog #funny #trendingshorts #doge',
#'https://i.ytimg.com/vi/E8HxOFUKbWo/hqdefault.jpg', None), 
#(2, '7P4OxUN4Jd0', 'FUNNIEST Viral Dogs EVER!!', 'https://i.ytimg.com/vi/7P4OxUN4Jd0/hqdefault.jpg', None),
#(3, 'naR2ydaEv_g', 'The dog came home with a new friend#funnydog #funnyvideos #funny #dog #foryou #usa🇺🇸 #fyp', 'https://i.ytimg.com/vi/naR2ydaEv_g/hqdefault.jpg', None), 
#(4, 'tq3bYPLBcA4', 'Dogs', 'https://i.ytimg.com/vi/tq3bYPLBcA4/hqdefault.jpg', None)]


