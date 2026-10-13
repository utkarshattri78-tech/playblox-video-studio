
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

    # Original gaming-adventure narration.
    script = [
        "Yo, what's up, PlayBlox squad! Welcome back! "
        "Today, we're starting a brand-new gaming adventure. "
        "Our mission is simple: explore, improve, overcome "
        "challenges, and see how far we can go. Stick around, "
        "because things are about to get interesting.",

        f"Today's adventure is all about {topic}. "
        "Every great gaming journey starts somewhere. "
        "At first, everything looks easy. You have time to "
        "explore, learn the controls, and figure out your plan. "
        "But the real challenge begins when you start setting "
        "bigger goals. We aren't here just to stand around. "
        "We're here to make progress and create an adventure "
        "worth watching.",

        "First, we need a plan. Every second matters when "
        "you're trying to build something impressive. We need "
        "to look around, choose our next objective, and avoid "
        "wasting time. Sometimes the smartest move is to take "
        "things slowly. Other times, you need to take a risk "
        "and see what happens. That's what makes gaming fun. "
        "You never know exactly how the next moment will turn out.",

        "Now the mission is getting serious. Imagine finding "
        "something rare just when you thought the adventure "
        "couldn't get any better. Suddenly, the plan changes. "
        "Do you keep exploring, or do you protect what you've "
        "already achieved? This is where patience and quick "
        "decisions make a difference. One mistake can cost time, "
        "but one smart decision can completely change the run.",

        "Here comes another challenge. Things don't always go "
        "according to plan, and that's completely normal. "
        "Sometimes you have to start again, try a different "
        "strategy, or learn from a mistake. The important thing "
        "is not giving up after the first problem. Every attempt "
        "teaches you something new. That's how you improve, "
        "and that's how an ordinary gaming session can turn "
        "into an amazing story.",

        "Let's raise the difficulty. Our next goal is to make "
        "real progress instead of repeating the same easy steps. "
        "We need to think ahead, use our resources carefully, "
        "and decide which objective matters most. If everything "
        "works out, we'll be in a much stronger position by the "
        "end. But if something goes wrong, we'll have to adapt. "
        "Either way, we're keeping the adventure moving.",

        "We're getting closer to the final challenge. Think about "
        "how much we've learned since the beginning. We started "
        "with a simple idea, made a plan, faced obstacles, and "
        "kept moving forward. Now it's time to put that progress "
        "to the test. This is the moment to stay focused and "
        "finish strong. The goal isn't just to play; it's to "
        "make every part of the journey count.",

        "And that's the spirit of PlayBlox Gaming! Every adventure "
        "gives us another chance to explore, improve, and try "
        "something new. Tell me in the comments what game we "
        "should tackle next and what challenge you'd like to see. "
        "If you enjoyed this adventure, subscribe to PlayBlox "
        "Gaming and join the squad. Thanks for watching, and "
        "I'll see you in the next video. Peace!"
    ]

    script_file = output / "script.txt"
    script_file.write_text(
        "\n\n".join(script), encoding="utf-8"
    )

    narration = output / "narration.wav"
    make_narration(script_file, narration)

    video = output / "playblox_video.mp4"

    # Moving shapes create an animated gaming-style background.
    visual_filter = (
        "drawbox=x='100+100*sin(t*0.7)':y=220:"
        "w=420:h=8:color=0x00d9ff@0.9:t=fill,"
        "drawbox=x='1100+150*sin(t*0.5)':y=720:"
        "w=500:h=8:color=0xff00aa@0.8:t=fill,"
        "drawbox=x='700+200*cos(t*0.4)':y=470:"
        "w=260:h=260:color=0x263d70@0.5:t=5,"
        "drawtext=text='PLAYBLOX GAMING':"
        "fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
        "fontcolor=white:fontsize=72:"
        "x=(w-text_w)/2:y=100:"
        "shadowcolor=black:shadowx=3:shadowy=3,"
        "drawtext=text='YOUR NEXT GAMING ADVENTURE':"
        "fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
        "fontcolor=0x00d9ff:fontsize=38:"
        "x=(w-text_w)/2:y=205:"
        "enable='between(t\\,0\\,15)',"
        "drawtext=text='MISSION STARTED':"
        "fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
        "fontcolor=yellow:fontsize=60:"
        "x=(w-text_w)/2:y=480:"
        "enable='between(t\\,0\\,10)',"
        "drawtext=text='TIME TO LEVEL UP!':"
        "fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
        "fontcolor=white:fontsize=56:"
        "x=(w-text_w)/2:y=480:"
        "enable='between(t\\,45\\,55)',"
        "drawtext=text='NEW CHALLENGE UNLOCKED':"
        "fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
        "fontcolor=0x00d9ff:fontsize=52:"
        "x=(w-text_w)/2:y=480:"
        "enable='between(t\\,100\\,112)',"
        "drawtext=text='NEVER GIVE UP!':"
        "fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
        "fontcolor=yellow:fontsize=64:"
        "x=(w-text_w)/2:y=480:"
        "enable='between(t\\,170\\,182)',"
        "drawtext=text='SUBSCRIBE FOR MORE!':"
        "fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
        "fontcolor=white:fontsize=52:"
        "x=(w-text_w)/2:y=h-150:"
        "enable='between(t\\,240\\,255)'"
    )

    # The background runs until the narration finishes.
    run([
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", "color=c=0x10152b:s=1920x1080:r=30:d=900",
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
        " ".join(sys.argv[1:])
        if len(sys.argv) > 1
        else "Minecraft survival adventure"
    )
    create_video(topic)
