# import os
# from dotenv import load_dotenv
# from googleapiclient.discovery import build
# from transformers import pipeline
# from youtube_transcript_api import YouTubeTranscriptApi

# # Load environment variables
# load_dotenv()

# # Set up YouTube API
# youtube_api_key = os.getenv('YOUTUBE_API_KEY')
# youtube = build('youtube', 'v3', developerKey=youtube_api_key)

# # Set up the summarization pipeline
# summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# def get_video_id(url):
#     # Extract video ID from URL
#     return url.split('v=')[1]

# def get_transcript(video_id):
#     # Fetch the transcript of the video
#     try:
#         transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
#         transcript = ' '.join([t['text'] for t in transcript_list])
#         return transcript
#     except Exception as e:
#         print(f"Error retrieving transcript: {e}")
#         return None

# def summarize_text(text):
#     # Generate summary of the text
#     summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
#     return summary[0]['summary_text']

# def summarize_video(url):
#     video_id = get_video_id(url)
#     transcript = get_transcript(video_id)
#     if transcript:
#         return summarize_text(transcript)
#     else:
#         return "No transcript available or error in fetching transcript."

# # Example usage
# video_url = 'https://youtu.be/rULO-Axqs40?t=12'
# summary = summarize_video(video_url)
# print("Summary:", summary)




# import os
# import csv
# import re
# from dotenv import load_dotenv
# from googleapiclient.discovery import build
# from transformers import pipeline
# from youtube_transcript_api import YouTubeTranscriptApi
# import torch

# # Load environment variables
# load_dotenv()

# # Set up YouTube API
# youtube_api_key = os.getenv('YOUTUBE_API_KEY')
# youtube = build('youtube', 'v3', developerKey=youtube_api_key)

# # Set up the summarization pipeline
# device = 0 if torch.cuda.is_available() else -1  # Use GPU if available
# summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=device)

# def get_video_id(url):
#     # Extract video ID from URL
#     return url.split('v=')[1]

# def get_transcript(video_id):
#     # Fetch the transcript of the video
#     try:
#         transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
#         transcript = ' '.join([t['text'] for t in transcript_list])
#         return transcript
#     except Exception as e:
#         print(f"Error retrieving transcript: {e}")
#         return None

# def preprocess_text(text):
#     # Remove punctuation and other non-essential characters
#     return re.sub(r'[^\w\s]', '', text)

# def summarize_text(text):
#     # Generate summary of the text
#     summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
#     return summary[0]['summary_text']

# def summarize_video(url):
#     video_id = get_video_id(url)
#     transcript = get_transcript(video_id)
#     if transcript:
#         cleaned_text = preprocess_text(transcript)
#         summary = summarize_text(cleaned_text)
#         return summary
#     else:
#         return "No transcript available or error in fetching transcript."

# def save_summary_to_csv(video_url, summary):
#     # Save the summary along with the video URL to a CSV file
#     with open('video_summaries.csv', mode='a', newline='', encoding='utf-8') as file:
#         writer = csv.writer(file)
#         writer.writerow([video_url, summary])

# # Example usage
# video_url =  'https://youtu.be/rULO-Axqs40?t=12'
# summary = summarize_video(video_url)
# print("Summary:", summary)
# save_summary_to_csv(video_url, summary)





# import os
# import csv
# import re
# import torch
# import time  # Import time for handling retry delays
# from dotenv import load_dotenv
# from googleapiclient.discovery import build
# from transformers import pipeline
# from youtube_transcript_api import YouTubeTranscriptApi

# # Load environment variables
# load_dotenv()

# # Set up YouTube API
# youtube_api_key = os.getenv('YOUTUBE_API_KEY')
# youtube = build('youtube', 'v3', developerKey=youtube_api_key)

# # Setup retry mechanism or fallback for summarizer initialization
# def setup_summarizer(retries=3):
#     for attempt in range(retries):
#         try:
#             device = 0 if torch.cuda.is_available() else -1  # Use GPU if available
#             summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=device)
#             return summarizer
#         except RuntimeError as e:
#             print(f"Attempt {attempt+1} failed with error: {e}")
#             if "CUDA-capable device(s) is/are busy or unavailable" in str(e):
#                 print("Waiting for the GPU to be free...")
#                 torch.cuda.empty_cache()
#                 time.sleep(10)  # wait for 10 seconds before retrying
#     print("Falling back to CPU.")
#     return pipeline("summarization", model="facebook/bart-large-cnn", device=-1)  # fallback to CPU

# # Set up the summarization pipeline using the setup function
# summarizer = setup_summarizer()

# def get_video_id(url):
#     # Extract video ID from URL
#     return url.split('v=')[0]

# def get_transcript(video_id):
#     # Fetch the transcript of the video
#     try:
#         transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
#         transcript = ' '.join([t['text'] for t in transcript_list])
#         return transcript
#     except Exception as e:
#         print(f"Error retrieving transcript: {e}")
#         return None

# def preprocess_text(text):
#     # Remove punctuation and other non-essential characters
#     return re.sub(r'[^\w\s]', '', text)

# def summarize_text(text):
#     # Generate summary of the text
#     summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
#     return summary[0]['summary_text']

# def summarize_video(url):
#     video_id = get_video_id(url)
#     transcript = get_transcript(video_id)
#     if transcript:
#         cleaned_text = preprocess_text(transcript)
#         summary = summarize_text(cleaned_text)
#         return summary
#     else:
#         return "No transcript available or error in fetching transcript."

# def save_summary_to_csv(video_url, summary):
#     # Save the summary along with the video URL to a CSV file
#     with open('video_summaries.csv', mode='a', newline='', encoding='utf-8') as file:
#         writer = csv.writer(file)
#         writer.writerow([video_url, summary])

# # Example usage
# # Example usage
# try:
#     video_url = 'https://www.youtube.com/watch?v=f_w0g70KsFI'
#     summary = summarize_video(video_url)
#     print("Summary:", summary)
#     save_summary_to_csv(video_url, summary)
# except ValueError as e:
#     print(e)



# import os
# import csv
# import re
# import torch
# import time
# from dotenv import load_dotenv
# from googleapiclient.discovery import build
# from transformers import pipeline
# from youtube_transcript_api import YouTubeTranscriptApi

# # Load environment variables
# load_dotenv()

# # Set up YouTube API
# youtube_api_key = os.getenv('YOUTUBE_API_KEY')
# youtube = build('youtube', 'v3', developerKey=youtube_api_key)

# # Setup retry mechanism or fallback for summarizer initialization
# def setup_summarizer(retries=3):
#     for attempt in range(retries):
#         try:
#             device = 0 if torch.cuda.is_available() else -1  # Use GPU if available
#             summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=device)
#             return summarizer
#         except RuntimeError as e:
#             print(f"Attempt {attempt+1} failed with error: {e}")
#             if "CUDA-capable device(s) is/are busy or unavailable" in str(e):
#                 print("Waiting for the GPU to be free...")
#                 torch.cuda.empty_cache()
#                 time.sleep(10)  # wait for 10 seconds before retrying
#     print("Falling back to CPU.")
#     return pipeline("summarization", model="facebook/bart-large-cnn", device=-1)  # fallback to CPU

# # Set up the summarization pipeline using the setup function
# summarizer = setup_summarizer()

# def get_video_id(url):
#     # Extract video ID from URL
#     video_id = None
#     if 'youtube.com/watch?v=' in url:
#         video_id = url.split('v=')[1]
#     elif 'youtu.be/' in url:
#         video_id = url.split('youtu.be/')[1]
#     elif 'youtube.com/embed/' in url:
#         video_id = url.split('embed/')[1]
#     else:
#         raise ValueError("Invalid YouTube URL format")
    
#     if '&' in video_id:
#         video_id = video_id.split('&')[0]
    
#     return video_id

# def get_transcript(video_id):
#     # Fetch the transcript of the video
#     try:
#         transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
#         transcript = ' '.join([t['text'] for t in transcript_list])
#         return transcript
#     except Exception as e:
#         print(f"Error retrieving transcript: {e}")
#         return None

# def preprocess_text(text):
#     # Remove punctuation and other non-essential characters
#     return re.sub(r'[^\w\s]', '', text)

# def summarize_text(text):
#     # Generate summary of the text
#     summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
#     return summary[0]['summary_text']

# def summarize_video(url):
#     try:
#         video_id = get_video_id(url)
#     except ValueError as e:
#         return str(e)
    
#     transcript = get_transcript(video_id)
#     if transcript:
#         cleaned_text = preprocess_text(transcript)
#         summary = summarize_text(cleaned_text)
#         return summary
#     else:
#         return "No transcript available or error in fetching transcript."

# def save_summary_to_csv(video_url, summary):
#     # Save the summary along with the video URL to a CSV file
#     with open('video_summaries.csv', mode='a', newline='', encoding='utf-8') as file:
#         writer = csv.writer(file)
#         writer.writerow([video_url, summary])

# # Example usage
# try:
#     video_url = 'https://youtu.be/rULO-Axqs40'
#     summary = summarize_video(video_url)
#     print("Summary:", summary)
#     save_summary_to_csv(video_url, summary)
# except ValueError as e:
#     print(e)




import os
import csv
import re
import torch
import time
from dotenv import load_dotenv
from googleapiclient.discovery import build
from transformers import pipeline
from youtube_transcript_api import YouTubeTranscriptApi

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

def summarize_text(text):
    # Generate summary of the text
    summary = summarizer(text, max_length=200, min_length=60, do_sample=False)
    return summary[0]['summary_text']

def summarize_video(url):
    try:
        video_id = get_video_id(url)
    except ValueError as e:
        return str(e)
    
    transcript = get_transcript(video_id)
    if transcript:
        cleaned_text = preprocess_text(transcript)
        summary = summarize_text(cleaned_text)
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



