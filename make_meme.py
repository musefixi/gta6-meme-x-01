#!/usr/bin/env python3
"""Build meme.png for the make.fun gta6-meme-x-01 entry.

The joke: GTA fans have waited 13 years since GTA V (2013) for GTA 6.
The picture shows one of them, now an old man with a waist-length beard,
still waiting on a neon Vice City boardwalk -- while the make.fun ghost,
his AI agent, stands next to him holding its star coin, having paid for
the game with bounty money earned on make.fun.

Inputs (all in this directory):
  scene.webp  -- original AI-generated Vice City boardwalk scene
                 (neon art-deco hotels, palms, sunset, old gamer).
  ghost.png   -- make.fun's official logo mark (mark-1024.png from
                 https://make.fun/press/), the ghost mascot badge.

Steps:
  1. Cut the ghost (with its magenta star coin) out of the badge: the
     badge background is a flat magenta disc, so flood-fill from inside
     the ghost's white body over every solid non-magenta pixel, then
     fill the holes the fill cannot reach (the coin's magenta middle).
  2. Paste the ghost onto the boardwalk at character size, with a soft
     magenta neon glow behind it and a contact shadow under it.
  3. Draw the classic black meme caption bars, top and bottom, in a
     heavy bold font, sized to stay readable when the whole picture is
     shrunk to 480x480 (the size the judge sees).

Output: meme.png (plus ghost-cutout.png, the extracted mascot).
"""

from collections import deque
from PIL import Image, ImageDraw, ImageFilter, ImageFont

CANVAS = 1440
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

TOP_TEXT = "WAITED 13 YEARS FOR GTA 6"
BOTTOM_TEXT = "MY AI AGENT PAID FOR IT\nWITH MAKE.FUN BOUNTIES"


def is_magenta(r, g, b):
    """The badge disc's flat magenta (and the coin's fill)."""
    return r > 110 and g < 120 and b > 60 and r - g > 60


def extract_ghost(mark_path):
    """Cut the ghost + star coin out of the circular logo badge."""
    img = Image.open(mark_path).convert("RGBA")
    w, h = img.size
    px = img.load()

    def solid_non_magenta(x, y):
        r, g, b, a = px[x, y]
        return a > 128 and not is_magenta(r, g, b)

    # Flood fill from a seed inside the ghost's white body.
    seed = (450, 580)
    region = bytearray(w * h)
    q = deque([seed])
    region[seed[1] * w + seed[0]] = 1
    while q:
        x, y = q.popleft()
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= nx < w and 0 <= ny < h and not region[ny * w + nx]:
                if solid_non_magenta(nx, ny):
                    region[ny * w + nx] = 1
                    q.append((nx, ny))

    # Fill holes: anything not reachable from the border without crossing
    # the region is inside the mascot (e.g. the coin's magenta middle).
    outside = bytearray(w * h)
    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if not region[y * w + x] and not outside[y * w + x]:
                outside[y * w + x] = 1
                q.append((x, y))
    for y in range(h):
        for x in (0, w - 1):
            if not region[y * w + x] and not outside[y * w + x]:
                outside[y * w + x] = 1
                q.append((x, y))
    while q:
        x, y = q.popleft()
        for nx, ny in ((x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)):
            if 0 <= nx < w and 0 <= ny < h:
                i = ny * w + nx
                if not region[i] and not outside[i]:
                    outside[i] = 1
                    q.append((nx, ny))
    for i in range(w * h):
        if not outside[i]:
            region[i] = 1

    mask = Image.frombytes("L", (w, h), bytes(255 * v for v in region))
    bbox = mask.getbbox()
    cut = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    cut.paste(img, (0, 0), mask)
    return cut.crop(bbox)


def fit_font(draw, lines, max_width, start_size):
    """Largest bold font (<= start_size) whose widest line fits."""
    size = start_size
    while size > 10:
        font = ImageFont.truetype(FONT_PATH, size)
        widest = max(draw.textlength(line, font=font) for line in lines)
        if widest <= max_width:
            return font
        size -= 4
    return ImageFont.truetype(FONT_PATH, size)


def caption_bar(base, lines, font, at_top):
    """Draw one black caption bar with centred white bold text."""
    draw = ImageDraw.Draw(base)
    asc, desc = font.getmetrics()
    line_h = int((asc + desc) * 1.12)
    pad = int(font.size * 0.34)
    bar_h = line_h * len(lines) + pad * 2
    y0 = 0 if at_top else base.height - bar_h
    draw.rectangle([0, y0, base.width, y0 + bar_h], fill=(0, 0, 0))
    for i, line in enumerate(lines):
        tw = draw.textlength(line, font=font)
        x = (base.width - tw) / 2
        y = y0 + pad + i * line_h
        draw.text((x, y), line, font=font, fill=(255, 255, 255))
    return bar_h


def main():
    scene = Image.open("scene.webp").convert("RGB")
    scene = scene.resize((CANVAS, CANVAS), Image.LANCZOS)
    canvas = scene.convert("RGBA")

    ghost = extract_ghost("ghost.png")
    ghost.save("ghost-cutout.png")

    # Character size: about a third of the picture tall, so the ghost is
    # unmistakable even after the judge shrinks the meme to 480x480.
    target_h = int(CANVAS * 0.335)
    scale = target_h / ghost.height
    ghost = ghost.resize(
        (int(ghost.width * scale), target_h), Image.LANCZOS
    )

    # Stand the ghost on the boardwalk to the right of the old gamer,
    # fully inside the scene: its feet rest above the bottom caption bar
    # (the two-line bar starts at about 77% of the height).
    base_y = int(CANVAS * 0.755)
    gx = int(CANVAS * 0.70 - ghost.width / 2)
    gy = base_y - ghost.height

    # Soft magenta neon glow behind the ghost, in make.fun's colour.
    glow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    glow.paste((214, 38, 138, 150), (gx, gy), ghost)
    glow = glow.filter(ImageFilter.GaussianBlur(28))
    canvas.alpha_composite(glow)

    # Contact shadow so the ghost stands on the boardwalk, not floats.
    shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.ellipse(
        [gx + ghost.width * 0.08, base_y - 16,
         gx + ghost.width * 0.92, base_y + 30],
        fill=(10, 0, 20, 130),
    )
    canvas.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(10)))
    canvas.alpha_composite(ghost, (gx, gy))

    # Caption bars last, so nothing in the scene fights the words.
    probe = ImageDraw.Draw(canvas)
    top_font = fit_font(probe, TOP_TEXT.split("\n"), CANVAS * 0.94, 118)
    bottom_font = fit_font(probe, BOTTOM_TEXT.split("\n"), CANVAS * 0.94, 104)
    caption_bar(canvas, TOP_TEXT.split("\n"), top_font, at_top=True)
    caption_bar(canvas, BOTTOM_TEXT.split("\n"), bottom_font, at_top=False)

    canvas.convert("RGB").save("meme.png")
    print("wrote meme.png", canvas.size)


if __name__ == "__main__":
    main()
