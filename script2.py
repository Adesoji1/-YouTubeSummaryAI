# import yt_dlp as youtube_dl
# import speech_recognition as sr
# from transformers import pipeline
# from googleapiclient.discovery import build
# from time import sleep

# # Configuration for YouTube API
# API_KEY = ''
# youtube = build('youtube', 'v3', developerKey=API_KEY)

# def get_video_details(video_id):
#     request = youtube.videos().list(part='snippet', id=video_id)
#     response = request.execute()
#     return response['items'][0]['snippet']['title']

# def download_audio(video_url):
#     ydl_opts = {
#         'format': 'bestaudio/best',
#         'postprocessors': [{
#             'key': 'FFmpegExtractAudio',
#             'preferredcodec': 'wav',  # Change to WAV for compatibility
#             'preferredquality': '192',
#         }],
#         'outtmpl': 'downloaded_audio.%(ext)s',
#         'quiet': True,
#         'cookiefile': 'cookies.txt',  # Using cookies can help avoid some rate limiting issues
#     }
#     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#         ydl.download([video_url])
#     return 'downloaded_audio.wav'  # Update extension to match the new format

# # For mp3 format
# # def download_audio(video_url):
# #     ydl_opts = {
# #         'format': 'bestaudio/best',
# #         'postprocessors': [{
# #             'key': 'FFmpegExtractAudio',
# #             'preferredcodec': 'mp3',
# #             'preferredquality': '192',
# #         }],
# #         'outtmpl': 'downloaded_audio.%(ext)s',
# #         'quiet': True
# #     }
# #     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
# #         ydl.download([video_url])
# #     return 'downloaded_audio.mp3'

# def transcribe_audio(audio_file):
#     recognizer = sr.Recognizer()
#     with sr.AudioFile(audio_file) as source:
#         audio_data = recognizer.record(source)
#         try:
#             text = recognizer.recognize_google(audio_data, language='en-US')  # Specify the language
#             return text
#         except sr.UnknownValueError:
#             return "Audio could not be understood"

# def summarize_text(text):
#     summarizer = pipeline("summarization")
#     summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
#     return summary[0]['summary_text']

# def main(video_url):
#     video_id = video_url.split('=')[1]
#     title = get_video_details(video_id)
#     audio_file = download_audio(video_url)
#     transcript = transcribe_audio(audio_file)
#     summary = summarize_text(transcript)
    
#     print("Video Title:", title)
#     print("Summary:", summary)

# if __name__ == "__main__":
#     video_url = input("Enter YouTube video URL: ")
#     main(video_url)


# import yt_dlp as youtube_dl
# import speech_recognition as sr
# from transformers import pipeline
# from googleapiclient.discovery import build
# from time import sleep

# # Configuration for YouTube API
# API_KEY = ''
# youtube = build('youtube', 'v3', developerKey=API_KEY)

# def get_video_details(video_id):
#     request = youtube.videos().list(part='snippet', id=video_id)
#     response = request.execute()
#     return response['items'][0]['snippet']['title']

# def download_audio(video_url):
#     ydl_opts = {
#         'format': 'bestaudio/best',
#         'postprocessors': [{
#             'key': 'FFmpegExtractAudio',
#             'preferredcodec': 'wav',  # Change to WAV for compatibility
#             'preferredquality': '192',
#         }],
#         'outtmpl': 'downloaded_audio.%(ext)s',
#         'quiet': True,
#         'cookiefile': 'cookies.txt',  # Using cookies can help avoid some rate limiting issues
#     }
#     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#         ydl.download([video_url])
#     return 'downloaded_audio.wav'  # Update extension to match the new format

# def download_audio_with_retries(video_url, max_retries=3):
#     attempt = 0
#     while attempt < max_retries:
#         try:
#             return download_audio(video_url)
#         except youtube_dl.utils.DownloadError as e:
#             if 'HTTP Error 429' in str(e):
#                 sleep(10)  # wait 10 seconds before retrying
#                 attempt += 1
#             else:
#                 raise e
#     raise Exception("Failed to download audio after retries")

# def transcribe_audio(audio_file):
#     recognizer = sr.Recognizer()
#     with sr.AudioFile(audio_file) as source:
#         audio_data = recognizer.record(source)
#         try:
#             text = recognizer.recognize_google(audio_data, language='en-US')  # Specify the language
#             return text
#         except sr.UnknownValueError:
#             return "Audio could not be understood"

# def summarize_text(text):
#     summarizer = pipeline("summarization")
#     summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
#     return summary[0]['summary_text']

# def main(video_url):
#     video_id = video_url.split('=')[1]
#     title = get_video_details(video_id)
#     audio_file = download_audio_with_retries(video_url)
#     transcript = transcribe_audio(audio_file)
#     summary = summarize_text(transcript)
    
#     print("Video Title:", title)
#     print("Summary:", summary)

# if __name__ == "__main__":
#     video_url = input("Enter YouTube video URL: ")
#     main(video_url)


# import yt_dlp as youtube_dl
# import speech_recognition as sr
# from transformers import pipeline
# from googleapiclient.discovery import build
# from time import sleep
# import torch
# import pandas as pd

# # Configuration for YouTube API
# API_KEY = ''
# youtube = build('youtube', 'v3', developerKey=API_KEY)

# def get_video_details(video_id):
#     request = youtube.videos().list(part='snippet', id=video_id)
#     response = request.execute()
#     return response['items'][0]['snippet']['title']

# def download_audio(video_url):
#     ydl_opts = {
#         'format': 'bestaudio/best',
#         'postprocessors': [{
#             'key': 'FFmpegExtractAudio',
#             'preferredcodec': 'wav',  # Change to WAV for compatibility
#             'preferredquality': '192',
#         }],
#         'outtmpl': 'downloaded_audio.%(ext)s',
#         'quiet': True,
#         'cookiefile': 'cookies.txt',  # Using cookies can help avoid some rate limiting issues
#     }
#     with youtube_dl.YoutubeDL(ydl_opts) as ydl:
#         ydl.download([video_url])
#     return 'downloaded_audio.wav'  # Update extension to match the new format

# def download_audio_with_retries(video_url, max_retries=3):
#     attempt = 0
#     while attempt < max_retries:
#         try:
#             return download_audio(video_url)
#         except youtube_dl.utils.DownloadError as e:
#             if 'HTTP Error 429' in str(e):
#                 sleep(10)  # wait 10 seconds before retrying
#                 attempt += 1
#             else:
#                 raise e
#     raise Exception("Failed to download audio after retries")

# def transcribe_audio(audio_file):
#     recognizer = sr.Recognizer()
#     with sr.AudioFile(audio_file) as source:
#         audio_data = recognizer.record(source)
#         try:
#             text = recognizer.recognize_google(audio_data, language='en-US')  # Specify the language
#             return text
#         except sr.UnknownValueError:
#             return "Audio could not be understood"
# def summarize_text(text):
#     # Check if GPU is available and use it
#     device = 0 if torch.cuda.is_available() else -1
#     # Example: Using a different model
#     summarizer = pipeline("summarization", model="google/pegasus-xsum",device=device)
#     summary = summarizer(text, max_length=300, min_length=60, do_sample=False)
#     return summary[0]['summary_text']



# # def summarize_text(text):
# #     # Check if GPU is available and use it
# #     device = 0 if torch.cuda.is_available() else -1
    
# #     summarizer = pipeline("summarization", device=device)
# #     summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
# #     return summary[0]['summary_text']

# def main(video_url):
#     video_id = video_url.split('=')[1]
#     title = get_video_details(video_id)
#     audio_file = download_audio_with_retries(video_url)
#     transcript = transcribe_audio(audio_file)
#     summary = summarize_text(transcript)
    
#     print("Video Title:", title)
#     print("Summary:", summary)

#     # Save results to CSV
#     results = {
#         "YouTube Link": [video_url],
#         "Summary": [summary]
#     }
#     df = pd.DataFrame(results)
#     df.to_csv('youtube_summaries.csv', index=False)

# if __name__ == "__main__":
#     video_url = input("Enter YouTube video URL: ")
#     main(video_url)





import re
import yt_dlp as youtube_dl
import speech_recognition as sr
from transformers import pipeline
from googleapiclient.discovery import build
from time import sleep
import torch
import pandas as pd

# Configuration for YouTube API
API_KEY = ''
youtube = build('youtube', 'v3', developerKey=API_KEY)

def get_video_details(video_id):
    request = youtube.videos().list(part='snippet', id=video_id)
    response = request.execute()
    return response['items'][0]['snippet']['title']

def download_audio(video_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',  # Change to WAV for compatibility
            'preferredquality': '192',
        }],
        'outtmpl': 'downloaded_audio.%(ext)s',
        'quiet': True,
        'cookiefile': 'cookies.txt',  # Using cookies can help avoid some rate limiting issues
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    return 'downloaded_audio.wav'  # Update extension to match the new format

def download_audio_with_retries(video_url, max_retries=3):
    attempt = 0
    while attempt < max_retries:
        try:
            return download_audio(video_url)
        except youtube_dl.utils.DownloadError as e:
            if 'HTTP Error 429' in str(e):
                sleep(10)  # wait 10 seconds before retrying
                attempt += 1
            else:
                raise e
    raise Exception("Failed to download audio after retries")

def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language='en-US')  # Specify the language
            return text
        except sr.UnknownValueError:
            return "Audio could not be understood"
def summarize_text(text):
    # Check if GPU is available and use it
    device = 0 if torch.cuda.is_available() else -1
    # Example: Using a different model
    #Large "google/pegasus-xsum"
    summarizer = pipeline("summarization", model= "google-t5/t5-small",device=device)  
    summary = summarizer(text, max_length=300, min_length=60, do_sample=False)
    return summary[0]['summary_text']



def extract_video_id(video_url):
    # Regex to extract the video ID from different YouTube URL formats
    patterns = [
        r'youtu\.be\/([^#\&\?]{11})',  # Shortened URL
        r'watch\?v=([^#\&\?]{11})',    # Regular URL
        r'embed\/([^#\&\?]{11})'       # Embed URL
    ]

    for pattern in patterns:
        match = re.search(pattern, video_url)
        if match:
            return match.group(1)
    
    raise ValueError("Invalid YouTube URL or video ID format")

def main(video_url):
    try:
        video_id = extract_video_id(video_url)
    except ValueError as e:
        print(e)
        return

    title = get_video_details(video_id)
    audio_file = download_audio_with_retries(video_url)
    transcript = transcribe_audio(audio_file)
    summary = summarize_text(transcript)
    
    print("Video Title:", title)
    print("Summary:", summary)

    # Save results to CSV
    results = {
        "YouTube Link": [video_url],
        "Summary": [summary]
    }
    df = pd.DataFrame(results)
    df.to_csv('youtube_summaries.csv', index=False)

if __name__ == "__main__":
    video_url = input("Enter YouTube video URL: ")
    main(video_url)
