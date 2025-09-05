import yt_dlp
import whisper
import os
import utils
import argparse

def run(args):
    # Optional args: None if not provided
    youtube_url = args.youtube_url
    output_path = args.output_dir
    audio_path = args.audio_path

    # Always present because of defaults
    n = args.n
    duration = args.duration

    if youtube_url:
        ydl_options = {
        "format": "bestaudio/best",   # get best available audio
        "outtmpl": "%(title)s.%(ext)s",  # output filename
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",   # force mp3
            "preferredquality": "192", # kbps
        }],
    }
        with yt_dlp.YoutubeDL(ydl_options) as ydl:
            info = ydl.extract_info(youtube_url,download=True)
            base, _ = os.path.splitext(ydl.prepare_filename(info))
            filename = base + ".mp3"

        
        base_name = os.path.splitext(filename)[0] if not output_path else output_path
             
    else:  # audio_path mode
        filename = audio_path
        base_name = os.path.splitext(filename)[0] if not output_path else output_path

    os.makedirs(base_name,exist_ok=True)


    model = whisper.load_model("large")
    result = model.transcribe(filename, word_timestamps=True)


    all_words = []
    for seg in result["segments"]:
        all_words.extend(seg["words"])


    clips = []
    start_idx = 0

    for i in range(len(all_words)):
        clip_duration = all_words[i]["end"] - all_words[start_idx]["start"]
        if clip_duration >= duration:
            text = " ".join(w["word"] for w in all_words[start_idx:i+1])
            words = len(text.split())
            density = words / clip_duration
            clips.append((
                density,
                text,
                all_words[start_idx]["start"],
                all_words[i]["end"]
            ))
            start_idx = i + 1



    clips.sort(key = lambda x: x[0], reverse=True)
    top = clips[:n]


    for j,(density, text, ts_start, ts_end) in enumerate(top,1):

        output_file = os.path.join(
            base_name,
            f"{ts_start:.2f}-{ts_end:.2f}.mp3"
        )
        pad = 0.1
        utils.extract_clip(filename,ts_start,ts_end+pad,output_file)
        clip_result = model.transcribe(output_file)
        print(f"[{ts_start:.2f}-{ts_end:.2f}] ({density:.2f} w/s) → {output_file}")
        print(clip_result["text"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "program to download and extract dense clips from youtube or mp3 file")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-y", "--youtube_url", type=str, help="URL to YouTube video")
    group.add_argument("-a", "--audio_path", type=str, help="Path of audio file")

    parser.add_argument(
        "-o", "--output_dir",
          type=utils.valid_dir, 
          help="Output Directory Path (will be created if missing)")

    parser.add_argument("-n",type=int, default=5, help="Number of Maximum Clips to extract")
    parser.add_argument("-d","--duration",type=int, default=10, help="Targeted Duration of clips")

    args = parser.parse_args()

    run(args)






