
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

WIDTH, HEIGHT, FPS = 1920, 1080, 30
OUTPUT = Path("output")
HF_MODEL = "stabilityai/stable-diffusion-3-medium-diffusers"
HF_URL = f"https://router.huggingface.co/hf-inference/models/{HF_MODEL}"


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


def generate_image(prompt, destination, token):
    payload = json.dumps({
        "inputs": prompt,
        "parameters": {
            "width": 1024,
            "height": 1024
        }
    }).encode("utf-8")

    request = urllib.request.Request(
        HF_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "image/png",
        },
        method="POST",
    )

    for attempt in range(3):
        try:
            with urllib.request.urlopen(request, timeout=180) as response:
                image_data = response.read()

            if not image_data.startswith(b"\x89PNG\r\n\x1a\n"):
                raise RuntimeError(
                    "The image service did not return a PNG image."
                )

            destination.write_bytes(image_data)
            print(f"Created AI image: {destination.name}")
            return

        except urllib.error.HTTPError as error:
            details = error.read().decode("utf-8", errors="replace")

            if error.code == 503 and attempt < 2:
                print("The image model is loading. Retrying shortly...")
                time.sleep(20)
                continue

            raise RuntimeError(
                f"Hugging Face image generation failed (HTTP {error.code}): "
                f"{details[:500]}"
            ) from None

        except urllib.error.URLError as error:
            raise RuntimeError(
                f"Could not connect to the image service: {error.reason}"
            ) from None


def create_fallback_image(destination, scene_number, topic):
    """Create a colourful scene locally without using paid image services."""
    colours = [
        ("#182848", "#4b6cb7"),
        ("#42275a", "#734b6d"),
        ("#134e5e", "#71b280"),
        ("#642b73", "#c6426e"),
    ]

    start, end = colours[(scene_number - 1) % len(colours)]

    # Use FFmpeg to create a gradient background and simple decorative shapes.
    # Escape colour values for FFmpeg's filter syntax.
    filter_text = (
        f"gradients=s={WIDTH}x{HEIGHT}:"
        f"c0={start}:c1={end}:"
        "x0=0:y0=0:x1=1920:y1=1080"
    )

    run([
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", filter_text,
        "-frames:v", "1",
        str(destination),
    ])

    print(
        f"Created fallback background for scene {scene_number}. "
        "This is a gradient, not an AI cartoon image."
    )


def create_video(topic):
    token = os.environ.get("HF_TOKEN")
    OUTPUT.mkdir(exist_ok=True)

    story = [
        (
            f"Imagine a world where {topic}. At first, everything seems "
            "ordinary, but one surprising discovery changes the day. "
            "Our story begins in a colourful world full of curious "
            "characters, strange places, and unexpected possibilities."
        ),
        (
            "As the adventure continues, our hero discovers something "
            "nobody expected. A mysterious clue points toward a bigger "
            "secret. There are questions everywhere, and every new "
            "discovery makes the mystery more exciting."
        ),
        (
            "Suddenly, a difficult problem appears. The easy option "
            "doesn't work, so our hero has to think differently. "
            "With a little creativity, courage, and help from an "
            "unexpected friend, a clever new plan begins to take shape."
        ),
        (
            "At last, the pieces come together. The journey reveals "
            "a surprising lesson: curiosity can lead us to amazing "
            "places. But this story might not be over. What do you "
            "think should happen next? Share your idea, and join us "
            "for another colourful adventure."
        ),
    ]

    prompts = [
        (
            f"A beautiful original 3D animated family-friendly cartoon "
            f"scene about {topic}, a curious young cartoon explorer "
            "discovering a magical colourful world, expressive character, "
            "cinematic lighting, vibrant colours, polished animated movie "
            "look, detailed environment, wide establishing shot, "
            "no text, no letters, landscape composition"
        ),
        (
            f"An original family-friendly 3D cartoon scene about {topic}, "
            "the same young cartoon explorer finding a mysterious glowing "
            "clue in a whimsical colourful landscape, expressive face, "
            "cinematic lighting, vibrant animated movie style, detailed "
            "background, no text, no letters, landscape composition"
        ),
        (
            f"An original family-friendly 3D animated cartoon scene about "
            f"{topic}, the same young explorer solving a surprising "
            "challenge with a friendly unusual creature, dynamic poses, "
            "colourful imaginative environment, cinematic animated movie "
            "style, no text, no letters, landscape composition"
        ),
        (
            f"An original family-friendly 3D cartoon finale about {topic}, "
            "the same young explorer celebrating a wonderful discovery "
            "in a magical colourful world at sunset, joyful expression, "
            "beautiful cinematic lighting, polished animated movie look, "
            "no text, no letters, landscape composition"
        ),
    ]

    script_file = OUTPUT / "script.txt"
    script_file.write_text("\n\n".join(story), encoding="utf-8")

    narration = OUTPUT / "narration.wav"
    make_narration(script_file, narration)

    images = []

    for index, prompt in enumerate(prompts, start=1):
        destination = OUTPUT / f"scene_{index}.png"

        if token:
            try:
                generate_image(prompt, destination, token)
            except (RuntimeError, urllib.error.URLError) as error:
                print(f"AI image unavailable: {error}")
                print("Switching to the local no-credit fallback.")
                create_fallback_image(destination, index, topic)
        else:
            print("HF_TOKEN is missing. Using local fallback.")
            create_fallback_image(destination, index, topic)

        images.append(destination)

    # Animate the still images with a gentle zoom effect.
    # These are animated stills, not AI-generated moving footage.
    scene_seconds = 40
    frames = scene_seconds * FPS
    filters = []

    for index in range(4):
        filters.append(
            f"[{index}:v]"
            f"scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=increase,"
            f"crop={WIDTH}:{HEIGHT},"
            f"zoompan=z='min(zoom+0.0003,1.12)':"
            f"x='iw/2-(iw/zoom/2)':"
            f"y='ih/2-(ih/zoom/2)':"
            f"d={frames}:s={WIDTH}x{HEIGHT}:fps={FPS},"
            f"setsar=1,format=yuv420p[v{index}]"
        )

    inputs = []

    for image_path in images:
        inputs.extend([
            "-loop", "1",
            "-framerate", str(FPS),
            "-i", str(image_path),
        ])

    filters.append(
        "".join(f"[v{i}]" for i in range(4))
        + "concat=n=4:v=1:a=0[vout]"
    )

    video = OUTPUT / "playblox_video.mp4"

    run([
        "ffmpeg", "-y",
        *inputs,
        "-i", str(narration),
        "-filter_complex", ";".join(filters),
        "-map", "[vout]",
        "-map", "4:a:0",
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "160k",
        "-shortest",
        "-movflags", "+faststart",
        str(video),
    ])

    print(f"Video created: {video}")


if __name__ == "__main__":
    topic = (
        " ".join(sys.argv[1:]).strip()
        if len(sys.argv) > 1
        else "a tiny dragon who discovers a hidden candy kingdom"
    )
    create_video(topic)
