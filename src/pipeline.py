from  src.fetch import  title_fetcher
from  src.processor import processing
from src.database import db_creator, insert_videos, quick_inspection

db_creator()
data = title_fetcher("Dogs", 3)
processed_data =processing(data)
insert_videos(processed_data)
quick_inspection()




