import os
import csv
import re
import torch
import time
from dotenv import load_dotenv
from googleapiclient.discovery import build
from transformers import pipeline
from youtube_transcript_api import YouTubeTranscriptApi
import isodate  # For parsing ISO 8601 durations

# Load environment variables
load_dotenv()

# Set up YouTube API
youtube_api_key = os.getenv('YOUTUBE_API_KEY')
youtube = build('youtube', 'v3', developerKey=youtube_api_key)

# Setup retry mechanism or fallback for summarizer initialization
def setup_summarizer(retries=3):
    for attempt in range(retries):
        try:
            device = 0 if torch.cuda.is_available() else -1  # Use GPU if available
            summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=device)
            return summarizer
        except RuntimeError as e:
            print(f"Attempt {attempt+1} failed with error: {e}")
            if "CUDA-capable device(s) is/are busy or unavailable" in str(e):
                print("Waiting for the GPU to be free...")
                torch.cuda.empty_cache()
                time.sleep(10)  # wait for 10 seconds before retrying
    print("Falling back to CPU.")
    return pipeline("summarization", model="facebook/bart-large-cnn", device=-1)  # fallback to CPU

# Set up the summarization pipeline using the setup function
summarizer = setup_summarizer()

def get_video_id(url):
    # Extract video ID from URL
    video_id = None
    if 'youtube.com/watch?v=' in url:
        video_id = url.split('v=')[1]
    elif 'youtu.be/' in url:
        video_id = url.split('youtu.be/')[1]
    elif 'youtube.com/embed/' in url:
        video_id = url.split('embed/')[1]
    else:
        raise ValueError("Invalid YouTube URL format")
    
    if '&' in video_id:
        video_id = video_id.split('&')[0]
    
    return video_id

def get_video_details(video_id):
    request = youtube.videos().list(
        part="contentDetails",
        id=video_id
    )
    response = request.execute()
    if 'items' in response and len(response['items']) > 0:
        return response['items'][0]['contentDetails']
    else:
        raise ValueError("No video details found for the given ID")

def get_transcript(video_id):
    # Fetch the transcript of the video
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = ' '.join([t['text'] for t in transcript_list])
        return transcript
    except Exception as e:
        print(f"Error retrieving transcript: {e}")
        return None

def preprocess_text(text):
    # Remove punctuation and other non-essential characters
    return re.sub(r'[^\w\s]', '', text)

def summarize_text(text, max_length, min_length):
    # Generate summary of the text
    summary = summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
    return summary[0]['summary_text']

def summarize_video(url):
    try:
        video_id = get_video_id(url)
    except ValueError as e:
        return str(e)
    
    try:
        video_details = get_video_details(video_id)
        duration = isodate.parse_duration(video_details['duration']).total_seconds()
    except Exception as e:
        return f"Error retrieving video details: {e}"
    
    transcript = get_transcript(video_id)
    if transcript:
        cleaned_text = preprocess_text(transcript)
        
        # Determine summary length based on video duration
        max_length = min(int(duration // 10), 200)  # Adjust max length based on duration
        min_length = max(int(max_length // 2), 30)  # Ensure min length is at least half of max length
        
        # Ensure max_length is greater than min_length
        if min_length >= max_length:
            min_length = max_length - 10  # Adjust min_length to be smaller than max_length
            if min_length < 30:
                min_length = 30  # Set a minimum threshold for min_length

        summary = summarize_text(cleaned_text, max_length=max_length, min_length=min_length)
        return summary
    else:
        return "No transcript available or error in fetching transcript."

def save_summary_to_csv(video_url, summary):
    # Save the summary along with the video URL to a CSV file
    file_exists = os.path.isfile('video_summaries.csv')
    with open('video_summaries.csv', mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['YouTube Link', 'Summary'])
        writer.writerow([video_url, summary])

# Example usage
try:
    video_url = 'https://youtu.be/rULO-Axqs40'
    summary = summarize_video(video_url)
    print("Summary:", summary)
    save_summary_to_csv(video_url, summary)
except ValueError as e:
    print(e)
