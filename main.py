import yt_dlp
import whisper
import subprocess
import utils



url = "https://www.youtube.com/watch?v=8_GgeASwHwQ"

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
    info = ydl.extract_info(url,download=True)
    filename = ydl.prepare_filename(info).replace(info["ext"], "mp3")

model = whisper.load_model("large")
result = model.transcribe(filename, word_timestamps=True)

all_words = []
for seg in result["segments"]:
    all_words.extend(seg["words"])


clips = []
start_idx = 0

for i in range(len(all_words)):
    duration = all_words[i]["end"] - all_words[start_idx]["start"]
    if duration >= 10:
        text = " ".join(w["word"] for w in all_words[start_idx:i+1])
        words = len(text.split())
        density = words / duration
        clips.append((
            density,
            text,
            all_words[start_idx]["start"],
            all_words[i]["end"]
        ))
        start_idx = i + 1



clips.sort(key = lambda x: x[0], reverse=True)

top = clips[:3]

#for seg in top_segments:
#    print(f"{seg[1]}s - {seg[2]}s:", seg[0])


for j,(density, text, ts_start, ts_end) in enumerate(top,1):

    output_file = f"{j}.mp3"
    pad = 0.1
    utils.extract_clip(filename,ts_start,ts_end+pad,output_file)
    result = model.transcribe(output_file)
    print(f"[{ts_start:.2f}-{ts_end:.2f}] ({density:.2f} w/s) → {output_file}")
    print(result["text"])





