import os
import http
import requests
from tqdm import tqdm                                     # if you get 400 error install pytubefix library
from pytube import YouTube, Playlist                      # from pytubefix import YouTube, Playlist 
from pytube.exceptions import VideoUnavailable            # from pytube.exceptions import VideoUnavailable

DOWNLOADS_DIRECTORY = 'downloads'
MAX_RETRIES = 30
CHUNK_SIZE = 10240  # Adjust chunk size for faster download
SKIP_ALL = False
OVERRIDE_ALL = False

class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    BOLD = '\033[1m'
    END = '\033[0m'

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def sanitize_filename(filename):
    return ''.join(c for c in filename if c.isalnum() or c in [' ', '_', '-'])

def generate_output_filename(video, playlist_title=None, current_video_number=None):
    sanitized_title = sanitize_filename(video.title)
    if playlist_title is not None and current_video_number is not None:
        return f'{playlist_title}__{current_video_number}__{sanitized_title}.mp4'
    else:
        return f'{sanitized_title}.mp4'

def download_video(video, output_path, playlist_title=None, current_video_number=None):
    try:
        output_filename = generate_output_filename(video, playlist_title, current_video_number)
        output_directory = os.path.join(output_path, sanitize_filename(playlist_title)) if playlist_title else output_path
        output_filepath = os.path.join(output_directory, output_filename)
        create_directory(output_directory)
        if os.path.exists(output_filepath):
            global SKIP_ALL
            global OVERRIDE_ALL
            if SKIP_ALL or OVERRIDE_ALL:
                user_choice = 's' if SKIP_ALL else 'o'
            else:
                user_choice = input(f'{Color.YELLOW}The file {output_filename} already exists. What do you want to do? (o: overwrite, s: skip): {Color.END}')
            if user_choice.lower() == 'o':
                pass
            elif user_choice.lower() == 's':
                print(f"{Color.YELLOW}Skipping {output_filename}. Video already downloaded.{Color.END}")
                print("----------------------------")
                return
            else:
                print(f"{Color.RED}Invalid choice. Skipping download.{Color.END}")
                print("----------------------------")
                return
        temp_file_path = f'{output_filepath}.part'
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
        video_stream = video.streams.get_highest_resolution()
        response = requests.get(video_stream.url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        with tqdm(total=total_size, unit='B', unit_scale=True, desc=f'{Color.BOLD}Downloading Video {current_video_number}{Color.END}') as progress_bar:
            with open(output_filepath, 'wb') as file:
                for data in response.iter_content(chunk_size=CHUNK_SIZE):  # Use larger chunk size
                    file.write(data)
                    progress_bar.update(len(data))
        print(f'\n{Color.GREEN}Downloaded Video {current_video_number}: {output_filename}{Color.END}')
        print(f'{Color.GREEN}Saved to: {os.path.abspath(output_filepath)}{Color.END}')
        print("----------------------------")
    except KeyboardInterrupt:
        print("----------------------------")
        print(f'\n{Color.RED}Download of {output_filename} canceled by the user.{Color.END}')
        os.remove(f'{output_filepath}.part')
        print(f"{Color.RED}Canceled download.{Color.END}")
    except VideoUnavailable:
        print("----------------------------")
        print(f"{Color.RED}Video {output_filename} is unavailable.{Color.END}")

def download_playlist(playlist_url, output_path=DOWNLOADS_DIRECTORY, start_skip=None, end_skip=None):
    global SKIP_ALL
    global OVERRIDE_ALL
    for attempt in range(MAX_RETRIES):
        try:
            playlist = Playlist(playlist_url)
            print("----------------------------")
            print(f'{Color.BOLD}{Color.PURPLE}Playlist: {playlist.title}{Color.END}')
            print(f'{Color.CYAN}Number of Videos: {len(playlist)}{Color.END}')
            print("----------------------------")
            num_skipped = 0
            for index, video in enumerate(playlist.videos, start=1):
                if start_skip is not None and end_skip is not None and start_skip <= index <= end_skip:
                    num_skipped += 1
                    print(f"{Color.YELLOW}Skipping video {index} (Manually specified){Color.END}")
                    continue
                download_video(video, output_path, playlist.title, index)
            break  # Break the loop if successful
        except (ValueError, VideoUnavailable, requests.RequestException, http.client.RemoteDisconnected) as e:
            print(f"{Color.RED}An error occurred: {str(e)}{Color.END}")
            if attempt < MAX_RETRIES - 1:
                print("----------------------------")
                print(f"{Color.RED}Retrying ({attempt + 1}/{MAX_RETRIES})...{Color.END}")
                print("----------------------------")
            else:
                print("----------------------------")
                print(f"{Color.RED}Max retries reached. Exiting.{Color.END}")
                print("----------------------------")
                break

if __name__ == "__main__":
    print(f"{Color.BOLD}{Color.RED}\nWelcome to the YouTube Video Downloader!{Color.END}")
    create_directory(DOWNLOADS_DIRECTORY)
    while True:
        print("\nOptions:\n")
        print(f"1. Download Single Video")
        print("2. Download Playlist")
        print("3. Skip All Downloaded Videos in Playlist")
        print("4. Override All Downloaded Videos in Playlist")
        print("5. Skip a Range of Videos in Playlist")
        print("6. Exit")
        print("----------------------------")
        choice = input("Enter your choice (1/2/3/4/5/6): ")
        print("----------------------------")
        if choice == '1':
            video_url = input("Enter YouTube video URL: ")
            yt = YouTube(video_url)
            download_video(yt, DOWNLOADS_DIRECTORY)
        elif choice == '2':
            playlist_url = input("Enter YouTube playlist URL: ")
            download_playlist(playlist_url, DOWNLOADS_DIRECTORY)
        elif choice == '3':
            SKIP_ALL = True
            print(f"{Color.BOLD}{Color.YELLOW}Skipping all downloads{Color.END}")
        elif choice == '4':
            OVERRIDE_ALL = True
            print(f"{Color.BOLD}{Color.YELLOW}Overriding all downloads.{Color.END}")
        elif choice == '5':
            playlist_url = input("Enter YouTube playlist URL: ")
            start_skip = int(input("Enter the start index of the range to skip (0-based): "))
            end_skip = int(input("Enter the end index of the range to skip (0-based): "))
            download_playlist(playlist_url, DOWNLOADS_DIRECTORY, start_skip, end_skip)
        elif choice == '6':
            print(f"{Color.RED}Exiting the application.{Color.END}")
            print("----------------------------")
            break
        else:
            print(f"{Color.RED}Invalid choice. Enter a valid option.{Color.END}")
            print("----------------------------")
