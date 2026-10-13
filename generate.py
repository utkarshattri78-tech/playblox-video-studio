```python
import asyncio
import subprocess
import sys
from pathlib import Path
import edge_tts

WIDTH, HEIGHT, FPS, DURATION = 1920, 1080, 30, 30
VOICE = "en-US-GuyNeural"

def run(command):
    subprocess.run(command, check=True)

async def make_narration(text, output_file):
    speech = edge_tts.Communicate(
        text,
        VOICE,
        rate="+5%",
        pitch="+0Hz"
    )
    await speech.save(str(output_file))

def create_video(topic):
    output = Path("output")
    output.mkdir(exist_ok=True)

    script = [
        "Yo, what's up, everyone? Welcome back to PlayBlox Gaming!",
        f"Today, we're jumping into {topic}. Let's see how far we can go!",
        "Stick around, because things could get pretty interesting.",
        "Let's jump straight into the adventure!",
        "If you enjoy the video, subscribe and join the PlayBlox Gaming squad!"
    ]

    (output / "script.txt").write_text(
        "\n\n".join(script), encoding="utf-8"
    )

    narration = output / "narration.mp3"
    asyncio.run(make_narration(" ".join(script), narration))

    video = output / "playblox_video.mp4"

    visual_filter = (
        "drawbox=x=0:y=ih/2-6:w=iw:h=12:color=0x00d9ff@0.8:t=fill,"
        "drawtext=text='PLAYBLOX GAMING':fontcolor=white:fontsize=90:"
        "x=(w-text_w)/2:y=h*0.25,"
        "drawtext=text='GAMING ADVENTURE':fontcolor=0x00d9ff:fontsize=48:"
        "x=(w-text_w)/2:y=h*0.43,"
        "drawtext=text='LETS GO!':fontcolor=yellow:fontsize=60:"
        "x=(w-text_w)/2:y=h*0.72"
    )

    run([
        "ffmpeg", "-y",
        "-f", "lavfi", "-i",
        f"color=c=0x10152b:s={WIDTH}x{HEIGHT}:r={FPS}:d={DURATION}",
        "-i", str(narration),
        "-vf", visual_filter,
        "-map", "0:v:0", "-map", "1:a:0",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest", "-movflags", "+faststart",
        str(video)
    ])

    print(f"Video created: {video}")

if __name__ == "__main__":
    topic = sys.argv[1] if len(sys.argv) > 1 else "Minecraft survival adventure"
    create_video(topic)
```
