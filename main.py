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
result = model.transcribe(filename)
segments = result["segments"]

scored_segments = []


## for seg in segments:
##     duration  = seg["end"]-seg["start"]
##     words = len(seg["text"].split())
##     density = words / duration if duration > 0 else 0
## 
##     if duration >= 5:
##         scored_segments.append((density,seg))


start = 0
end = 0
while end < len(segments):
    duration = segments[end]["end"] - segments[start]["start"]
    if duration < 10:
        end+=1
        continue

    text = " ".join([segments[x]["text"] for x in range(start,end+1)])
    density = len(text.split())/duration
    scored_segments.append((
        density,
        text,
        segments[start]["start"],
        segments[end]["end"]
        ))
    start = end
    end = start
    


scored_segments.sort(key = lambda x: x[0], reverse=True)

top_segments = scored_segments[:3]

#for seg in top_segments:
#    print(f"{seg[1]}s - {seg[2]}s:", seg[0])


for i,(density, text, ts_start, ts_end) in enumerate(top_segments,start=1):
    print(f"[{ts_start:.2f}s - {ts_end:.2f}s] ({density:.2f} w/s): {text}")

    output_file = f"{i}.mp3"
    utils.extract_clip(filename,ts_start,ts_end,output_file)
    print(f" Saved {output_file}")



