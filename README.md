export CUDA_LAUNCH_BLOCKING=1
python your_script.py


# YouTube Video Summarizer

This repository contains Python scripts to summarize YouTube videos using two different approaches. The scripts extract transcripts from YouTube videos and use pre-trained AI models to generate concise summaries. The resulting summaries are saved in a CSV file along with the corresponding YouTube video URLs.

## Approaches

### Approach 1: YouTube Transcript API and BART Summarization

1. **Fetch Transcript**: Uses the `YouTubeTranscriptApi` to fetch video transcripts.
2. **Preprocessing**: Cleans the transcript text.
3. **Summarization**: Uses the BART model (`facebook/bart-large-cnn`) to summarize the cleaned transcript.
4. **CSV Export**: Saves the summary and video URL to a CSV file.

```python
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

def setup_summarizer(retries=3):
    for attempt in range(retries):
        try:
            device = 0 if torch.cuda.is_available() else -1
            summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=device)
            return summarizer
        except RuntimeError as e:
            if "CUDA-capable device(s) is/are busy or unavailable" in str(e):
                torch.cuda.empty_cache()
                time.sleep(10)
    return pipeline("summarization", model="facebook/bart-large-cnn", device=-1)

summarizer = setup_summarizer()

def get_video_id(url):
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
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = ' '.join([t['text'] for t in transcript_list])
        return transcript
    except Exception as e:
        return None

def preprocess_text(text):
    return re.sub(r'[^\w\s]', '', text)

def summarize_text(text):
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
```

### Approach 2: Audio Transcription and T5 Summarization

1. **Download Audio**: Uses `yt-dlp` to download the audio of a YouTube video.
2. **Transcription**: Uses the `speech_recognition` library to transcribe the audio.
3. **Summarization**: Uses the T5 model (`google-t5/t5-small`) to summarize the transcript.
4. **CSV Export**: Saves the summary and video URL to a CSV file.

```python
import re
import yt_dlp as youtube_dl
import speech_recognition as sr
from transformers import pipeline
from googleapiclient.discovery import build
from time import sleep
import torch
import pandas as pd

API_KEY = 'YOUR_API_KEY'
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
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'outtmpl': 'downloaded_audio.%(ext)s',
        'quiet': True,
        'cookiefile': 'cookies.txt',
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])
    return 'downloaded_audio.wav'

def download_audio_with_retries(video_url, max_retries=3):
    attempt = 0
    while attempt < max_retries:
        try:
            return download_audio(video_url)
        except youtube_dl.utils.DownloadError as e:
            if 'HTTP Error 429' in str(e):
                sleep(10)
                attempt += 1
            else:
                raise e
    raise Exception("Failed to download audio after retries")

def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language='en-US')
            return text
        except sr.UnknownValueError:
            return "Audio could not be understood"

def summarize_text(text):
    device = 0 if torch.cuda.is_available() else -1
    summarizer = pipeline("summarization", model="google-t5/t5-small", device=device)
    summary = summarizer(text, max_length=300, min_length=60, do_sample=False)
    return summary[0]['summary_text']

def extract_video_id(video_url):
    patterns = [
        r'youtu\.be\/([^#\&\?]{11})',
        r'watch\?v=([^#\&\?]{11})',
        r'embed\/([^#\&\?]{11})'
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

    results = {
        "YouTube Link": [video_url],
        "Summary": [summary]
    }
    df = pd.DataFrame(results)
    df.to_csv('youtube_summaries.csv', index=False)

if __name__ == "__main__":
    video_url = input("Enter YouTube video URL: ")
    main(video_url)
```

## Future Work

1. **Application Development**: Build a web application or a desktop application that allows users to input YouTube URLs and get summaries directly.
2. **Language Support**: Enhance the script to support multiple languages for transcription and summarization.
3. **Batch Processing**: Add functionality to process multiple videos at once.
4. **Error Handling**: Improve error handling and logging mechanisms for more robust and user-friendly interactions.
5. **Real-time Summarization**: Explore possibilities for real-time video summarization during live streams.
6. **User Interface**: Develop a graphical user interface (GUI) for non-technical users.
7. **Performance Optimization**: Optimize the scripts for faster execution and lower resource consumption.

## Requirements

- Python 3.11+
- `torch`
- `transformers`
- `youtube_transcript_api`
- `google-api-python-client`
- `yt-dlp`
- `speechrecognition`
- `pandas`
- `ffmpeg`

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/YouTubeVideoSummarizer.git
cd YouTubeVideoSummarizer
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Set up your environment variables in a `.env` file:

```
YOUTUBE_API_KEY=YOUR_API_KEY
```

4. Run the script:

```bash
python script_name.py
```

Replace `script_name.py` with the appropriate script you want to run.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

This README provides an overview of the YouTube video summarization project, details on the two approaches used, and outlines future work for further development and enhancement