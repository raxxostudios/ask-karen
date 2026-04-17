#!/usr/bin/env python3
"""
Render the ask-karen demo as a terminal-style GIF.
No external tool required beyond ffmpeg. Produces demo.gif in the repo root.
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import subprocess, shutil, sys, os

REPO = Path(__file__).resolve().parent.parent
FRAMES = REPO / "scripts" / "_frames"
OUT_GIF = REPO / "demo.gif"

WIDTH, HEIGHT = 900, 520
BG = (31, 31, 33)           # #1f1f21
FG = (245, 245, 247)        # #F5F5F7
ACCENT = (227, 252, 2)      # #e3fc02 lime
DIM = (120, 120, 126)
PADDING = 28
LINE_HEIGHT = 28
FONT_SIZE = 18

FONT_CANDIDATES = [
    "/System/Library/Fonts/Menlo.ttc",
    "/System/Library/Fonts/Monaco.ttf",
    "/Library/Fonts/SF-Mono-Regular.otf",
    "/System/Library/Fonts/Courier.ttc",
]

def load_font(size):
    for path in FONT_CANDIDATES:
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()

FONT = load_font(FONT_SIZE)
FONT_BOLD = load_font(FONT_SIZE)

PROMPT_LINE = "> /karen what is 1+1"

KAREN = (
    "First of all, I would like to speak to whoever is in CHARGE "
    "here. The WiFi has been acting up since Tuesday and nobody "
    "has called me back. Back in MY day we said hello before we "
    "asked strangers for favors, but I GUESS that's too much to "
    "ask in 2026. Not that anyone asked me, but Greg used to do "
    "this exact same thing, he would just BARGE into a conversation "
    "with no greeting, and look where that marriage ended up, "
    "speaking of which, the woman from the gym was named Brittany, "
    "THIRTY-TWO, and I read on Facebook that...\n\n"
    "   (continues for 5,847 more words)"
)

def wrap_text(text, font, max_width):
    """Wrap text to fit max_width pixels, preserving explicit newlines."""
    lines = []
    for paragraph in text.split("\n"):
        if paragraph == "":
            lines.append("")
            continue
        words = paragraph.split(" ")
        line = ""
        for w in words:
            trial = (line + " " + w).strip() if line else w
            bbox = font.getbbox(trial)
            if bbox[2] - bbox[0] <= max_width:
                line = trial
            else:
                lines.append(line)
                line = w
        if line:
            lines.append(line)
    return lines

def render_frame(chars_shown, show_cursor=True):
    img = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(img)

    # Prompt line in lime
    draw.text((PADDING, PADDING), PROMPT_LINE, fill=ACCENT, font=FONT_BOLD)

    # Visible Karen text so far
    visible = KAREN[:chars_shown]
    wrapped = wrap_text(visible, FONT, WIDTH - PADDING * 2)
    y = PADDING + LINE_HEIGHT + 10
    for line in wrapped:
        color = DIM if line.strip().startswith("(continues") else FG
        draw.text((PADDING, y), line, fill=color, font=FONT)
        y += LINE_HEIGHT
        if y > HEIGHT - PADDING - LINE_HEIGHT:
            break

    # Cursor block at end of visible text
    if show_cursor and chars_shown < len(KAREN):
        if wrapped:
            last = wrapped[-1]
            bbox = FONT.getbbox(last)
            cursor_x = PADDING + (bbox[2] - bbox[0])
            cursor_y = y - LINE_HEIGHT
            draw.rectangle(
                [cursor_x + 2, cursor_y + 4, cursor_x + 12, cursor_y + LINE_HEIGHT - 2],
                fill=FG,
            )

    return img

def main():
    if FRAMES.exists():
        shutil.rmtree(FRAMES)
    FRAMES.mkdir(parents=True)

    CHARS_PER_FRAME = 6
    END_HOLD_FRAMES = 20
    total_chars = len(KAREN)

    i = 0
    idx = 0
    while idx < total_chars:
        idx = min(idx + CHARS_PER_FRAME, total_chars)
        frame = render_frame(idx, show_cursor=(i % 2 == 0))
        frame.save(FRAMES / f"frame_{i:04d}.png")
        i += 1

    # Hold final frame
    for j in range(END_HOLD_FRAMES):
        frame = render_frame(total_chars, show_cursor=(j % 4 < 2))
        frame.save(FRAMES / f"frame_{i:04d}.png")
        i += 1

    print(f"rendered {i} frames", file=sys.stderr)

    ffmpeg = os.environ.get("FFMPEG", "/Users/norman/bin/ffmpeg")
    # Two-pass palette for decent GIF colors
    palette = FRAMES / "palette.png"
    subprocess.run([
        ffmpeg, "-y", "-framerate", "18",
        "-i", str(FRAMES / "frame_%04d.png"),
        "-vf", "palettegen=max_colors=64",
        str(palette),
    ], check=True)
    subprocess.run([
        ffmpeg, "-y", "-framerate", "18",
        "-i", str(FRAMES / "frame_%04d.png"),
        "-i", str(palette),
        "-lavfi", "paletteuse=dither=bayer:bayer_scale=5",
        "-loop", "0",
        str(OUT_GIF),
    ], check=True)

    size_kb = OUT_GIF.stat().st_size / 1024
    print(f"demo.gif: {size_kb:.0f} KB", file=sys.stderr)

if __name__ == "__main__":
    main()
