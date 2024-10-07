import os
import random
import subprocess
import time
import yt_dlp
from pytube import Search
from threading import Thread

# Progress hook to track download progress and estimate time
def download_progress_hook(d):
    if d['status'] == 'downloading':
        total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate')
        downloaded_bytes = d.get('downloaded_bytes', 0)
        download_speed = d.get('speed', 0)
        elapsed_time = d.get('elapsed', 0)
        
        if download_speed > 0:
            remaining_bytes = total_bytes - downloaded_bytes
            remaining_time = remaining_bytes / download_speed
            print(f"Time remaining: {remaining_time // 60} min {remaining_time % 60:.2f} sec")
        else:
            print(f"Downloaded: {downloaded_bytes / total_bytes * 100:.2f}%")

# Function to print characters with delay for typing effect
def slow_char_print(message, delay=0.01):
    for char in message:
        print(char, end="", flush=True)  # Print each character
        time.sleep(delay)
    print()  # Print a newline at the end

# Banner for script
def print_banner():
    RED = "\33[91m"
    BLUE = "\33[94m"
    GREEN = "\033[32m"
    YELLOW = "\033[93m"
    PURPLE = '\033[0;35m' 
    CYAN = "\033[36m"
    END = "\033[0m"
    
    font = f""" 
    {RED}       

 ██▀███  ▓█████▄ ▒██   ██▒ ███▄ ▄███▓ ▄▄▄       ██▀███   █    ██   █████▒
▓██ ▒ ██▒▒██▀ ██▌▒▒ █ █ ▒░▓██▒▀█▀ ██▒▒████▄    ▓██ ▒ ██▒ ██  ▓██▒▓██   ▒ 
▓██ ░▄█ ▒░██   █▌░░  █   ░▓██    ▓██░▒██  ▀█▄  ▓██ ░▄█ ▒▓██  ▒██░▒████ ░ 
▒██▀▀█▄  ░▓█▄   ▌ ░ █ █ ▒ ▒██    ▒██ ░██▄▄▄▄██ ▒██▀▀█▄  ▓▓█  ░██░░▓█▒  ░ 
░██▓ ▒██▒░▒████▓ ▒██▒ ▒██▒▒██▒   ░██▒ ▓█   ▓██▒░██▓ ▒██▒▒▒█████▓ ░▒█░    
░ ▒▓ ░▒▓░ ▒▒▓  ▒ ▒▒ ░ ░▓ ░░ ▒░   ░  ░ ▒▒   ▓▒█░░ ▒▓ ░▒▓░░▒▓▒ ▒ ▒  ▒ ░    
  ░▒ ░ ▒░ ░ ▒  ▒ ░░   ░▒ ░░  ░      ░  ▒   ▒▒ ░  ░▒ ░ ▒░░░▒░ ░ ░  ░      
  ░░   ░  ░ ░  ░  ░    ░  ░      ░     ░   ▒     ░░   ░  ░░░ ░ ░  ░ ░    
   ░        ░     ░    ░         ░         ░  ░   ░        ░             
          ░                                                              
"""

    slow_char_print(font)  # Print the ASCII art with typing effect
    time.sleep(1)  # Optional pause before showing the next part
    slow_char_print("\033[38;5;196mThis script is created by\033[0m", delay=0.09)
    slow_char_print("\033[38;5;196m\033[1m----->RDX MARUF<----\033[0m", delay=0.09)
    slow_char_print("\033[38;5;32m\033[1mTelegram:@rdxmaruf07 \033[0m", delay=0.09)
    slow_char_print("\033[38;5;32m\033[1mInstragram:@rdxmaruf07 \033[0m", delay=0.09)
# Function to play random songs


# Function to download video or playlist
def download_video(url, format_choice, cookies_file):
    ydl_opts = {
        'format': format_choice,
        'outtmpl': '%(title)s.%(ext)s',
        'noplaylist': False if 'playlist' not in url else True,
        'cookiefile': cookies_file,  # Using the provided cookies file
        'progress_hooks': [download_progress_hook],  # Hook for progress tracking
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Main Function
def main():
    print_banner()
    
    # Get the video/playlist URL
    url = input("Enter the YouTube video or playlist URL: ")
    
    # Choose format
    print("Choose download format:")
    formats = {
        "1": "audio only (mp3)",
        "2": "video (low quality, 360p)",
        "3": "video (medium quality, 720p)",
        "4": "video (high quality, 1080p)",
    }
    
    for key, value in formats.items():
        print(f"{key}. {value}")
    
    format_choice = input("Enter your format choice (1/2/3/4): ")

    # Mapping user's choice to actual format
    format_map = {
        "1": "bestaudio[ext=mp3]/bestaudio/best",
        "2": "bestvideo[height<=360]+bestaudio/best[height<=360]",
        "3": "bestvideo[height<=720]+bestaudio/best[height<=720]",
        "4": "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
    }

    chosen_format = format_map.get(format_choice, "bestaudio[ext=mp3]/bestaudio/best")

    # Starting random songs in a separate thread
    song_thread = Thread(target=play_random_songs)
    song_thread.start()

    # Start downloading the video/playlist
    download_video(url, chosen_format, 'cookies.txt')

    # Wait for the song thread to finish
    song_thread.join()

if __name__ == "__main__":
    main()
