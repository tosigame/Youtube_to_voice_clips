import subprocess

def extract_clip(input_file, start, end , output_file):
    duration = end - start
    subprocess.run([
        "ffmpeg", "-y", "-i",input_file,
        "-ss", str(start), "-t", str(duration),
        output_file
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
