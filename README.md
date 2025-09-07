# Youtube_to_voice_clips — Densest Spoken Segments Extractor

Extract the densest spoken segments from a YouTube video or an audio file using yt-dlp
 to fetch audio and OpenAI Whisper
 to transcribe, then score windows by word density (words/sec) and save the top-N clips.

## Features

Download best-quality audio from YouTube and convert to MP3

Or use a local audio file (MP3/WAV/M4A…)

Transcribe with Whisper, compute words/sec, and export the top-N dense clips

Re-transcribe each exported clip for a quick preview in the terminal

Note: This script loads the large Whisper model by default (big download, high RAM/VRAM). You can change it in the code to medium, small, or base if you prefer.

## Requirements

```python 
Python 3.9–3.12
```
FFmpeg installed and available on your PATH (the ffmpeg binary)

## Install FFmpeg

### macOS (Homebrew):

```python 
brew install ffmpeg
```

### Ubuntu/Debian:

```python
sudo apt-get update && sudo apt-get install -y ffmpeg
```

### Windows (winget):

```python
winget install Gyan.FFmpeg
```

## Quickstart (clone → venv → install → run)
### 1) Clone
```python
git clone <YOUR_REPO_URL>.git
cd <YOUR_REPO_NAME>
```

### 2) Create & activate a virtual environment
```python
python3 -m venv .venv
```

### macOS/Linux
```python
source .venv/bin/activate
```
### Windows (PowerShell)
```python
 .\.venv\Scripts\Activate.ps1
 ```

## 3) Install dependencies
```python
pip install -U pip
pip install -r requirements.txt
```

### Minimal requirements.txt to include
```python
yt-dlp
openai-whisper
```
## Optional helper (still requires ffmpeg binary above):
Whisper will install PyTorch automatically. If you need a specific CUDA/MPS build, install PyTorch first from pytorch.org, then run pip install -r requirements.txt.

## Usage
### CLI
```python
python3 main.py (-y YOUTUBE_URL | -a AUDIO_PATH) [-o OUTPUT_DIR] [-n N] [-d DURATION]
```

### Arguments

-y, --youtube_url (mutually exclusive with -a) — YouTube video URL to download.

-a, --audio_path (mutually exclusive with -y) — Path to an existing audio file.

-o, --output_dir — Directory to write clips into (created if missing). If omitted, clips are saved under a folder named after the source audio.

-n — Max number of clips to keep (default: 5).

-d, --duration — Target clip duration in seconds (default: 10).

### Examples

#### Download from YouTube and extract clips (macOS/Linux):

```
source .venv/bin/activate
python3 main.py -y "https://www.youtube.com/watch?v=dQw4w9WgXcQ&t=1s" -o clips -n 5 -d 12
```


#### Use a local audio file (Windows PowerShell):

```python
.\.venv\Scripts\Activate.ps1
python3 .\main.py -a "C:\path\to\talk.mp3" -o clips -n 8 -d 15
```

## Notes

Current version uses the large Whisper model, which can require ~10–11 GB of VRAM/RAM. If you run into memory limits, change the model in main.py to medium, small, or base.

## License
This project is licensed under the [MIT License](./LICENSE).

## Ethical Use & Disclaimer
This is a learning project. Please use it responsibly.

- Only download/transcribe content you **own** or have **explicit permission** to use.
- Respect platform Terms of Service (e.g., YouTube) and local copyright laws.
- The authors are not responsible for how this software is used.
- Provided **as is**, without warranty; see the MIT license for details.