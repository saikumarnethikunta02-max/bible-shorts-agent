
from pathlib import Path
import subprocess
from PIL import Image, ImageOps, ImageDraw, ImageFont

IMAGE = Path("Golden Path to the Sunrise.png")
POSTER = Path("poster.jpg")
OUTPUT = Path("bible_short.mp4")

if not IMAGE.exists():
    raise FileNotFoundError(f"Sunrise image not found: {IMAGE}")

# Prepare a vertical 9:16 background.
image = Image.open(IMAGE).convert("RGB")
image = ImageOps.fit(image, (1080, 1920))
draw = ImageDraw.Draw(image, "RGBA")

# Add a subtle dark panel behind the title.
draw.rounded_rectangle(
    (70, 1330, 1010, 1690),
    radius=35,
    fill=(0, 0, 0, 145)
)

font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
font = ImageFont.truetype(font_path, 66)

title = ["GOD IS ALREADY", "IN TOMORROW"]
y = 1410

for line in title:
    box = draw.textbbox((0, 0), line, font=font)
    x = (1080 - (box[2] - box[0])) // 2
    draw.text((x, y), line, font=font, fill="white")
    y += 90

small_font = ImageFont.truetype(font_path, 38)
verse = "MATTHEW 6:34"
box = draw.textbbox((0, 0), verse, font=small_font)
x = (1080 - (box[2] - box[0])) // 2
draw.text((x, 1600), verse, font=small_font, fill=(255, 220, 150))

image.save(POSTER, quality=95)

# Create a 43-second vertical MP4 with a gentle zoom.
subprocess.run([
    "ffmpeg", "-y",
    "-loop", "1",
    "-framerate", "30",
    "-i", str(POSTER),
    "-vf",
    "zoompan=z='min(zoom+0.00004,1.05)':d=1290:s=1080x1920:fps=30,format=yuv420p",
    "-t", "43",
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-movflags", "+faststart",
    str(OUTPUT)
], check=True)

print(f"Video created: {OUTPUT}")
