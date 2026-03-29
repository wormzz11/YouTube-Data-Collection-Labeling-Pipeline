from config.settings import YOUTUBE_API_KEY
from googleapiclient.discovery import build

def title_fetcher(query, quantity):

    if not isinstance(query, str):
        raise TypeError("Query must be a string")
    
    if not isinstance(quantity, int):
        raise TypeError("Quantity must be an integer")
    
    if  quantity <= 0:
        raise ValueError("Quantity must be greater than 0" )
    
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

    request  = youtube.search().list(
        part =  "snippet",
        maxResults=quantity,
        q=query,
        relevanceLanguage = "en",
        fields ="items(id(videoId),snippet(title, thumbnails))",
        type = "video"
    )
    response = request.execute()
    print("Succesfuly fetched data from {} videos".format(quantity))
    return response

    
    





