import json
import subprocess
import sys
from pathlib import Path

WIDTH = 1920
HEIGHT = 1080
FPS = 30
DURATION = 30

def load_config():
    with open("config.json", "r", encoding="utf-8") as file:
        return json.load(file)

def create_script(topic):
    return [
        "Welcome back to PlayBlox Gaming!",
        f"Today, we're exploring {topic}.",
        "Let's jump into the adventure!",
        "Stay tuned to see what happens next.",
        "Thanks for watching PlayBlox Gaming!",
        "Subscribe for more gaming videos!"
    ]

def create_video(topic):
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    script = create_script(topic)
    (output_dir / "script.txt").write_text(
        "\n\n".join(script), encoding="utf-8"
    )

    video_path = output_dir / "playblox_video.mp4"

    command = [
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", f"color=c=0x10152b:s={WIDTH}x{HEIGHT}:r={FPS}:d={DURATION}",
        "-vf",
        "drawbox=x=0:y=ih/2-8:w=iw:h=16:color=0x00d9ff@0.7:t=fill,"
        "drawtext=text='PLAYBLOX GAMING':fontcolor=white:fontsize=100:"
        "x=(w-text_w)/2:y=(h-text_h)/2,"
        "drawtext=text='AI GAMING VIDEO':fontcolor=0x00d9ff:fontsize=48:"
        "x=(w-text_w)/2:y=h*0.72",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-t", str(DURATION),
        str(video_path)
    ]

    subprocess.run(command, check=True)
    print(f"Video created: {video_path}")
    print(f"Script saved: {output_dir / 'script.txt'}")

if __name__ == "__main__":
    config = load_config()
    topic = sys.argv[1] if len(sys.argv) > 1 else "Minecraft survival adventure"
    create_video(topic)
