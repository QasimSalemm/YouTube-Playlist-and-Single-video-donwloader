# YouTube-Playlist-and-Single-video-donwloader
This Python script is a command-line tool for downloading YouTube videos and playlists. Here's a breakdown of its functionality:

1. **Dependencies**:
   -  `requests`: for making HTTP requests.
   - `tqdm`: for displaying progress bars during downloads.
   - `pytube`: a library for downloading YouTube videos.

2. **Constants**:
   - `DOWNLOADS_DIRECTORY`: the directory where downloaded files will be saved.
   - `MAX_RETRIES`: the maximum number of retries for HTTP requests.
   - `CHUNK_SIZE`: the size of the data chunks for downloading.
   - `SKIP_ALL` and `OVERRIDE_ALL`: flags for skipping or overriding existing downloads.

3. **Utility Functions**:
   - `create_directory(directory)`: creates a directory if it doesn't exist.
   - `sanitize_filename(filename)`: sanitizes a filename to remove invalid characters.
   - `generate_output_filename(video, playlist_title, current_video_number)`: generates the output filename.
   - `download_video(video, output_path, playlist_title, current_video_number)`: downloads a single video.
   - `download_playlist(playlist_url, output_path, start_skip, end_skip)`: downloads a playlist.

4. **Main Functionality**:
   - The script presents a menu with options:
     1. Download Single Video
     2. Download Playlist
     3. Skip All Downloaded Videos in Playlist
     4. Override All Downloaded Videos in Playlist
     5. Skip a Range of Videos in Playlist
     6. Exit

5. **Execution**:
   - The script continuously prompts the user for input based on the selected options.
   - It handles user input and executes the corresponding actions, such as downloading videos or playlists, skipping downloads, overriding existing downloads, or exiting the application.

This script provides a flexible and interactive way to download YouTube videos and playlists from the command line, with options to manage existing downloads and handle errors gracefully.
