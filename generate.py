import json
import os
import random
import subprocess
from pathlib import Path

WIDTH = 1920
HEIGHT = 1080
FPS = 30

def load_config():
    with open("config.json", "r", encoding="utf-8") as f:
        return json.load(f)

def create_script(topic):
    return [
        f"Welcome back to PlayBlox Gaming!",
        f"Today, we're exploring {topic}.",
        "Things are about to get interesting.",
        "Let's see what happens next.",
        "Thanks for watching PlayBlox Gaming!",
        "Subscribe for more gaming videos!"
    ]

def create_video(topic):
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    script = create_script(topic)
    script_path = output_dir / "script.txt"
    script_path.write_text("\n\n".join(script), encoding="utf-8")

    # Create a colourful animated background using FFmpeg.
    video_path = output_dir / "playblox_video.mp4"

    command = [
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", f"color=c=0x10152b:s={WIDTH}x{HEIGHT}:r={FPS}:d=30",
        "-vf",
        "drawbox=x=0:y=ih/2-8:w=iw:h=16:color=0x00d9ff@0.7:t=fill,"
        "drawtext=text='PLAYBLOX GAMING':fontcolor=white:fontsize=100:"
        "x=(w-text_w)/2:y=(h-text_h)/2,"
        "drawtext=text='AI GAMING VIDEO':fontcolor=0x00d9ff:fontsize=48:"
        "x=(w-text_w)/2:y=h*0.72",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-t", "30",
        str(video_path)
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Video created: {video_path}")
        print(f"Script saved: {script_path}")
    except FileNotFoundError:
        print("FFmpeg is not installed. Install it before generating videos.")
    except subprocess.CalledProcessError:
        print("Video creation failed. Check your FFmpeg installation.")

if __name__ == "__main__":
    config = load_config()
    topic = input("Enter your gaming video topic: ").strip()
    if topic:
        create_video(topic)
    else:
        print("Please enter a topic.")
