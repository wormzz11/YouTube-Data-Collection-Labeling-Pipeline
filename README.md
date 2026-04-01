# YouTube Data Collection & Labeling Pipeline

<div style="display: flex; gap: 20px;">
<img src="https://github.com/user-attachments/assets/fb173f96-ba64-4959-b8cc-880d14db28f9" width="400"/>
<img src="https://github.com/user-attachments/assets/5917a6af-e8b1-4f7c-aedb-c4d3d6ef9646" width="400"/>
</div>

## Project Overview
This project provides a complete pipeline for collecting YouTube video metadata, organizing it in a structured database, and labeling it through an intuitive Streamlit interface. The goal is to produce high‑quality, theme‑based datasets suitable for machine learning tasks such as classification, retrieval, or recommendation.

## Features
- Fetches video metadata from YouTube using the YouTube Data API  
- Stores and manages video data in a structured SQLite database  
- Provides a user interface for labeling videos with themes  
- Allows assigning relevance labels to videos per theme  
- Supports querying labeled and unlabeled data  
- Prevents duplicate entries using database constraints  
- Enables exporting datasets in CSV/XLSX formats for machine learning use  

## Technologies Used
- Python  
- Pandas (data manipulation and export)  
- Streamlit (user interface)  
- SQLite (data storage)  
- YouTube Data API (data collection)  

## How It Works

**Data Collection**  
- Fetches video metadata from the YouTube Data API based on a user-defined query  

**Data Processing**  
- Extracts relevant fields (video ID, title, thumbnail) and formats them for storage  

**Data Storage**  
- Stores videos in a SQLite database  
- Prevents duplicate entries using a (videoId, theme) uniqueness constraint  

**Data Annotation**  
- Users assign themes and label videos as relevant or irrelevant through the UI  

**Data Export**  
- Labeled data can be exported as CSV or XLSX for machine learning workflows  
- Supports assigning themes during data collection without requiring relevance labels

## Notes & Limitations
-  YouTube API quota may limit the number of videos you can fetch per day
- Thumbnails are stored as URLs, not downloaded
- The system is optimized for supervised dataset creation, not full‑scale crawling

## Setup

1. Clone the repository:
 ```bash
   git clone https://github.com/wormzz11/YouTube-Data-Collection-Labeling-System
   cd YouTube-Data-Collection-Labeling-System
   ```
2. Create and activate a virtual environment:
 ```bash
   python -m venv venv
   venv\Scripts\Activate.ps1
  ```
3. Install dependencies:
 ```bash
   pip install -e .
  ```
4. Configure your YouTube API key:
 ```bash
  Create a file `config/settings.py` and add: 
  YOUTUBE_API_KEY = "<your_api_key_here>"
```
5. Run the application:
 ```bash
   python -m streamlit run app/app.py
 ```
     
