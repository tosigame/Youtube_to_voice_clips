#utils.py

import subprocess
import argparse
import os

def valid_dir(path: str) -> str:
    """Validate that a path is a directory (or can be created as one)."""
    if os.path.exists(path) and not os.path.isdir(path):
        raise argparse.ArgumentTypeError(f"{path} exists but is not a directory")
    return path


def extract_clip(input_file, start, end , output_file):
    duration = end - start
    subprocess.run([
        "ffmpeg", "-y", "-i",input_file,
        "-ss", str(start), "-t", str(duration),
        output_file
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
