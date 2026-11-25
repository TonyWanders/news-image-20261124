#!/usr/bin/env python3
"""Build the news front page for Tuesday 24 November 2026.

Draws a newspaper front page with PIL (standard library + Pillow) and
writes the image to the path it is given. Fully deterministic: no network,
no clock, no random numbers, fixed fonts, fixed layout.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (20, 20, 20)
RED = (178, 34, 34)
BLUE = (24, 58, 110)
GREY = (90, 90, 90)
LIGHT = (232, 226, 210)
ORANGE = (230, 110, 20)
GREEN = (30, 130, 60)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, width, fill=INK, leading=None):
    if leading is None:
        leading = fnt.size + 6
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def headline(draw, x, y, text, fnt, width, fill=INK, leading=None):
    return para(draw, x, y, text, fnt, width, fill=fill, leading=leading)


def rule(draw, x, y, w, fill=INK, width=2):
    draw.line([(x, y), (x + w, y)], fill=fill, width=width)


def draw_factory_fire(draw, x, y, w, h):
    # Night sky, factory block, layered flames and rising smoke.
    draw.rectangle([x, y, x + w, y + h], fill=(52, 58, 72))
    draw.rectangle([x, y + h - 44, x + w, y + h], fill=(30, 30, 30))
    # factory block
    draw.rectangle([x + 30, y + h - 150, x + w - 30, y + h - 44], fill=(96, 92, 84))
    draw.rectangle([x + 30, y + h - 150, x + w - 30, y + h - 138], fill=(70, 66, 60))
    # chimney
    draw.rectangle([x + w - 90, y + 60, x + w - 60, y + h - 140], fill=(80, 76, 70))
    # windows, lit from inside
    for i in range(5):
        wx = x + 55 + i * 62
        draw.rectangle([wx, y + h - 130, wx + 34, y + h - 100], fill=(255, 190, 60))
    # flames: outer orange tongues, inner yellow core
    flame = [(x + 60, y + h - 140), (x + 78, y + h - 205), (x + 100, y + h - 155),
             (x + 122, y + h - 220), (x + 148, y + h - 160), (x + 172, y + h - 210),
             (x + 198, y + h - 150), (x + 226, y + h - 200), (x + 252, y + h - 150),
             (x + 282, y + h - 190), (x + 310, y + h - 140)]
    draw.polygon(flame, fill=ORANGE)
    flame2 = [(x + 100, y + h - 140), (x + 118, y + h - 180), (x + 142, y + h - 148),
              (x + 168, y + h - 190), (x + 196, y + h - 150), (x + 224, y + h - 178),
              (x + 252, y + h - 140)]
    draw.polygon(flame2, fill=(255, 200, 40))
    # smoke: small dark puffs rising above the chimney, clear of the flames
    for cx, cy, r in [(x + 330, y + 26, 13), (x + 360, y + 16, 16),
                      (x + 388, y + 28, 11)]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(90, 90, 96))


def draw_kyiv(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(38, 48, 70))
    # city skyline
    heights = [60, 85, 50, 105, 70, 90, 55]
    bx = x + 10
    for hh in heights:
        draw.rectangle([bx, y + h - 40 - hh, bx + 46, y + h - 40], fill=(18, 20, 28))
        bx += 56
    draw.rectangle([x, y + h - 40, x + w, y + h], fill=(14, 14, 18))
    # explosion burst with rays, not a plain disc
    cx, cy = x + w - 110, y + 70
    for r, col in [(46, (255, 200, 60)), (34, (255, 140, 30)), (20, (255, 220, 120))]:
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    for dx, dy in [(-58, -18), (58, -22), (-44, 34), (52, 30), (0, -62),
                   (-70, 6), (70, 4)]:
        draw.line([(cx, cy), (cx + dx, cy + dy)], fill=(255, 170, 40),
                  width=5)
    # sparks
    for sx, sy in [(cx - 60, cy + 20), (cx + 55, cy - 30), (cx - 40, cy - 45),
                   (cx + 70, cy + 35), (cx, cy - 60)]:
        draw.ellipse([sx - 5, sy - 5, sx + 5, sy + 5], fill=(255, 200, 60))
    # sea strip with a sinking ship (Libya coast)
    draw.rectangle([x, y + h - 34, x + w, y + h], fill=(24, 90, 130))
    draw.polygon([(x + 30, y + h - 34), (x + 90, y + h - 34), (x + 78, y + h - 12),
                  (x + 42, y + h - 12)], fill=(60, 60, 60))
    draw.rectangle([x + 58, y + h - 52, x + 64, y + h - 34], fill=(60, 60, 60))


def draw_climate(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(178, 214, 235))
    cx, cy, r = x + w // 2, y + h // 2 - 8, 62
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(46, 130, 200))
    draw.ellipse([cx - r + 14, cy - r + 24, cx - r + 62, cy - r + 50], fill=GREEN)
    draw.ellipse([cx + 6, cy + 18, cx + 50, cy + 54], fill=GREEN)
    draw.ellipse([cx - r + 24, cy - r + 6, cx - r + 46, cy - r + 20], fill=GREEN)
    # crack across the globe
    draw.line([(cx - 48, cy - 44), (cx - 16, cy - 8), (cx - 36, cy + 20),
               (cx + 8, cy + 48), (cx + 32, cy + 62)], fill=(20, 20, 20), width=5)
    draw.text((x + 18, y + h - 34), "NO DEAL", font=font(SANS_B, 26), fill=RED)


def draw_handshake(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(250, 244, 224))
    # India: saffron, white, green with the chakra
    draw.rectangle([x + 20, y + 8, x + 168, y + 28], fill=(255, 153, 51))
    draw.rectangle([x + 20, y + 28, x + 168, y + 48], fill=(255, 255, 255))
    draw.rectangle([x + 20, y + 48, x + 168, y + 68], fill=(19, 136, 8))
    draw.ellipse([x + 80, y + 28, x + 108, y + 50], outline=(0, 0, 128),
                 width=3)
    # Nepal: two stacked crimson pennants with a blue border
    draw.polygon([(x + 268, y + 8), (x + 268, y + 40), (x + 388, y + 24)],
                 fill=(220, 20, 60), outline=(0, 0, 128))
    draw.polygon([(x + 268, y + 44), (x + 268, y + 76), (x + 398, y + 60)],
                 fill=(220, 20, 60), outline=(0, 0, 128))
    draw.ellipse([x + 292, y + 18, x + 306, y + 32], fill=(255, 255, 255))
    draw.ellipse([x + 292, y + 54, x + 306, y + 68], fill=(255, 255, 255))
    # gold seal between the flags: the 8 deals
    draw.ellipse([x + 196, y + 22, x + 240, y + 66], fill=(176, 124, 12))
    draw.text((x + 206, y + 34), "8", font=font(SANS_B, 26),
              fill=(255, 255, 255))
    draw.text((x + 176, y + 82), "8 DEALS SIGNED", font=font(SANS_B, 18),
              fill=(176, 124, 12))


def draw_chip(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(12, 40, 20))
    # rising graph
    pts = [(x + 20, y + h - 50), (x + 90, y + h - 90), (x + 150, y + h - 70),
           (x + 220, y + h - 120), (x + 300, y + h - 90), (x + w - 30, y + 45)]
    draw.line(pts, fill=(120, 220, 120), width=6)
    draw.polygon(pts + [(x + w - 30, y + h - 30), (x + 20, y + h - 30)],
                 fill=(30, 130, 60))
    # chip
    cx, cy = x + w - 110, y + h - 55
    draw.rectangle([cx - 50, cy - 34, cx + 50, cy + 34], fill=(20, 20, 20),
                   outline=(120, 220, 120), width=3)
    draw.text((cx - 34, cy - 14), "AI", font=font(SANS_B, 30), fill=(120, 220, 120))
    for i in range(4):
        draw.line([(cx - 36 + i * 24, cy - 44), (cx - 36 + i * 24, cy - 34)],
                  fill=(120, 220, 120), width=3)
        draw.line([(cx - 36 + i * 24, cy + 34), (cx - 36 + i * 24, cy + 44)],
                  fill=(120, 220, 120), width=3)
    draw.text((x + 18, y + 12), "+$1 TRILLION", font=font(SANS_B, 26), fill=(255, 255, 255))


def build(target):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    d.text((512, 18), "THE WORLD TODAY", font=font(SERIF, 64),
           fill=INK, anchor="ma")
    rule(d, 40, 96, 944, fill=INK, width=3)
    d.text((40, 106), "TUESDAY 24 NOVEMBER 2026", font=font(SANS_B, 26), fill=RED)
    d.text((984, 106), "WORLD NEWS IN ONE IMAGE", font=font(SANS_B, 22),
           fill=GREY, anchor="ra")
    rule(d, 40, 142, 944, fill=INK, width=2)

    # Lead story: Indonesia factory fire
    y = 158
    y = headline(d, 40, y, "FACTORY FIRE KILLS 24 IN INDONESIA",
                 font(SERIF, 34), 520, leading=42)
    y += 8
    y = para(d, 40, y, "Candy factory blaze leaves about 30 workers missing",
             font(SANS_B, 22), 520, fill=RED, leading=28)
    y += 8
    para(d, 40, y,
         "At least 24 people are dead after a huge fire tore through a "
         "candy factory in Cikande, Indonesia. Rescuers are still "
         "searching for around 30 missing workers.",
         font(SANS, 21), 500, leading=28)
    draw_factory_fire(d, 580, 158, 404, 230)
    d.text((580, 392), "Firefighters search the burned-out factory.",
           font=font(SANS, 18), fill=GREY)
    rule(d, 40, 436, 944, fill=INK, width=2)

    # Row 2: Ukraine and COP31
    y = 448
    d.text((40, y), "UKRAINE WAR SPREADS", font=font(SERIF, 30), fill=INK)
    d.text((532, y), "COP31 TALKS COLLAPSE", font=font(SERIF, 30), fill=INK)
    y += 40
    draw_kyiv(d, 40, y, 452, 150)
    draw_climate(d, 532, y, 452, 150)
    y += 158
    para(d, 40, y,
         "A Russian strike on Dymer, north of Kyiv, kills 11. A boy "
         "of 7 is pulled alive from the rubble after 14 hours, and a "
         "79-year-old woman after 22 hours.",
         font(SANS, 20), 452, leading=27)
    para(d, 532, y,
         "The UN climate summit ends with no deal after the row over "
         "fossil fuels, the first failure since 2009.",
         font(SANS, 20), 452, leading=27)
    rule(d, 40, 750, 944, fill=INK, width=2)

    # Row 3: India-Nepal and Nvidia
    y = 766
    d.text((40, y), "INDIA, NEPAL SIGN 8 DEALS", font=font(SERIF, 24), fill=INK)
    d.text((532, y), "HUANG BACK, NVIDIA SOARS", font=font(SERIF, 24), fill=INK)
    y += 34
    draw_handshake(d, 40, y, 452, 120)
    draw_chip(d, 532, y, 452, 120)
    y += 126
    para(d, 40, y,
         "PM Modi and Nepal PM Balendra Shah agree a Rs 15,000 crore "
         "package for energy and trade.",
         font(SANS, 18), 452, leading=24)
    para(d, 532, y,
         "Nvidia brings back Jensen Huang as chief. Shares surge by "
         "a third, adding about $1 trillion.",
         font(SANS, 18), 452, leading=24)
    rule(d, 40, 986, 944, fill=INK, width=2)

    # Also today strip
    y = 996
    d.text((40, y), "ALSO TODAY:", font=font(SANS_B, 16), fill=RED)
    d.text((168, y),
           "Democrats take the US House  |  South Korea scrambles jets over Russian planes  |  CrowdStrike to buy Zscaler for $44bn",
           font=font(SANS, 14), fill=INK)

    img.save(target, format="PNG", optimize=True)
    print(f"wrote {target}")


if __name__ == "__main__":
    import sys
    from pathlib import Path

    build(Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/output/entry.png"))
