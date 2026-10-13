import subprocess
import sys
from pathlib import Path

WIDTH, HEIGHT, FPS = 1920, 1080, 30


def run(command):
    subprocess.run(command, check=True)


def make_narration(script_file, output_file):
    run([
        "kokoro-tts",
        str(script_file),
        str(output_file),
        "--voice", "am_adam",
        "--lang", "en-us",
        "--speed", "1.05",
    ])


def create_video(topic):
    output = Path("output")
    output.mkdir(exist_ok=True)

    assets = Path("assets")
    gameplay = assets / "gameplay.mp4"

    script = [
        "Yo, what's up, PlayBlox squad! Welcome back!",
        f"Today, we're jumping into {topic}. And honestly, "
        "I'm excited to see what happens.",
        "We've got a big adventure ahead, so stick around.",
        "Alright, enough talking. Let's get into the gameplay!",
        "If you're enjoying the video, hit subscribe "
        "and join the PlayBlox squad!"
    ]

    script_file = output / "script.txt"
    script_file.write_text(
        "\n\n".join(script), encoding="utf-8"
    )

    narration = output / "narration.wav"
    make_narration(script_file, narration)

    video = output / "playblox_video.mp4"

    if gameplay.exists():
        video_input = ["-stream_loop", "-1", "-i", str(gameplay)]
        visual_filter = (
            "scale=1920:1080:force_original_aspect_ratio=increase,"
            "crop=1920:1080,"
            "drawtext=text='PLAYBLOX GAMING':"
            "fontcolor=white:fontsize=54:"
            "x=40:y=40:box=1:boxcolor=black@0.5"
        )
    else:
        print("No gameplay footage found; using title-screen fallback.")
        video_input = [
            "-f", "lavfi", "-i",
            "color=c=0x10152b:s=1920x1080:r=30:d=60"
        ]
        visual_filter = (
            "drawtext=text='PLAYBLOX GAMING':"
            "fontcolor=white:fontsize=90:"
            "x=(w-text_w)/2:y=h*0.25,"
            "drawtext=text='GAMING ADVENTURE':"
            "fontcolor=0x00d9ff:fontsize=48:"
            "x=(w-text_w)/2:y=h*0.43,"
            "drawtext=text='LETS GO!':"
            "fontcolor=yellow:fontsize=60:"
            "x=(w-text_w)/2:y=h*0.72"
        )

    run([
        "ffmpeg", "-y",
        *video_input,
        "-i", str(narration),
        "-vf", visual_filter,
        "-map", "0:v:0",
        "-map", "1:a:0",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        "-movflags", "+faststart",
        str(video)
    ])

    print(f"Video created: {video}")


if __name__ == "__main__":
    topic = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "Minecraft survival adventure"
    )
    create_video(topic)
