def processing(response):
    processed_data = []
    for item in response.get("items"):
        video_id = item.get("id", {}).get("videoId")
        title = item.get("snippet", {}).get("title")
        snippet = item.get("snippet")
        thumbnails = snippet.get("thumbnails")
        thumbnail = (
            thumbnails.get("maxres", {}).get("url") or
            thumbnails.get("high", {}).get("url") or
            thumbnails.get("medium", {}).get("url") or
            thumbnails.get("default", {}).get("url") 
        )
        

        if video_id and title and thumbnail:
            video_data = {
                    "title" : title,
                    "videoId" : video_id,
                    "thumbnail" : thumbnail
                }
                
            processed_data.append(video_data)
    return processed_data
            
