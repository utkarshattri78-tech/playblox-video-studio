import json
import subprocess
import sys
from pathlib import Path

WIDTH, HEIGHT, FPS, DURATION = 1920, 1080, 30, 30

def run(command):
    subprocess.run(command, check=True)

def create_video(topic):
    output = Path("output")
    output.mkdir(exist_ok=True)

    script = [
        "Welcome back to PlayBlox Gaming!",
        f"Today, we're exploring {topic}.",
        "Get ready, because this adventure is about to begin!",
        "Let's jump in and see what happens next.",
        "Thanks for watching. Subscribe for more gaming videos!"
    ]

    script_file = output / "script.txt"
    script_file.write_text("\n\n".join(script), encoding="utf-8")

    narration_text = " ".join(script)
    narration_file = output / "narration.wav"

    run([
        "espeak-ng", "-v", "en-us", "-s", "155",
        "-w", str(narration_file), narration_text
    ])

    video_file = output / "playblox_video.mp4"

    visual_filter = (
        "drawbox=x=0:y=ih/2-6:w=iw:h=12:color=0x00d9ff@0.8:t=fill,"
        "drawtext=text='PLAYBLOX GAMING':fontcolor=white:fontsize=90:"
        "x=(w-text_w)/2:y=h*0.25,"
        "drawtext=text='AI GAMING ADVENTURE':fontcolor=0x00d9ff:fontsize=48:"
        "x=(w-text_w)/2:y=h*0.43,"
        "drawtext=text='LET THE ADVENTURE BEGIN!':fontcolor=yellow:fontsize=40:"
        "x=(w-text_w)/2:y=h*0.72"
    )

    run([
        "ffmpeg", "-y",
        "-f", "lavfi", "-i",
        f"color=c=0x10152b:s={WIDTH}x{HEIGHT}:r={FPS}:d={DURATION}",
        "-i", str(narration_file),
        "-vf", visual_filter,
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "128k",
        "-shortest", "-movflags", "+faststart",
        str(video_file)
    ])

    print(f"Video: {video_file}")
    print(f"Narration: {narration_file}")
    print(f"Script: {script_file}")

if __name__ == "__main__":
    with open("config.json", encoding="utf-8") as file:
        config = json.load(file)

    topic = sys.argv[1] if len(sys.argv) > 1 else "Minecraft survival adventure"
    create_video(topic)
