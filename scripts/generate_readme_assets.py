#!/usr/bin/env python3
"""Buat aset GIF beranimasi untuk README GitHub."""

from pathlib import Path
import math

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "assets"
OUT.mkdir(parents=True, exist_ok=True)

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
LOGO = ROOT / "assets" / "logo-grup-mbr-tjkt.jpeg"

INK = (12, 11, 13)
DARK = (17, 17, 16)
YELLOW = (235, 202, 50)
PAPER = (244, 241, 233)
MUTED = (170, 166, 156)
LINE = (52, 50, 46)
AMBER_DARK = (58, 50, 20)


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT_DIR / name), size)


def save_gif(frames, filename: str, duration: int) -> None:
    quantized = [frame.quantize(colors=64, method=Image.Quantize.MEDIANCUT) for frame in frames]
    target = OUT / filename
    quantized[0].save(
        target,
        save_all=True,
        append_images=quantized[1:],
        duration=duration,
        loop=0,
        optimize=True,
        disposal=2,
    )
    print(f"{target.name}: {target.stat().st_size / 1024:.1f} KB")


def hero_frame(index: int, total: int) -> Image.Image:
    width, height = 960, 240
    image = Image.new("RGB", (width, height), DARK)
    draw = ImageDraw.Draw(image)

    offset = int((index / total) * width)
    for x in range(-width + offset, width * 2, 96):
        draw.rectangle((x, 0, x + 38, 6), fill=YELLOW)
        draw.rectangle((x + 48, height - 6, x + 86, height), fill=AMBER_DARK)

    for x in range(0, width, 80):
        draw.line((x, 16, x, height - 16), fill=LINE, width=1)

    draw.text((48, 50), "GRUP MBR TJKT", font=font("DejaVuSans-Bold.ttf", 62), fill=PAPER)
    draw.text((50, 124), "RANDOM, TAPI NYAMBUNG", font=font("DejaVuSerif-Bold.ttf", 28), fill=YELLOW)
    draw.text(
        (70, 176),
        "11 RODA  •  10 ANGGOTA  •  2 KANAL",
        font=font("DejaVuSansMono.ttf", 20),
        fill=MUTED,
    )

    pulse = (1 + math.sin(2 * math.pi * index / total)) / 2
    dot_radius = int(5 + 3 * pulse)
    draw.ellipse(
        (50 - dot_radius, 185 - dot_radius, 50 + dot_radius, 185 + dot_radius),
        fill=YELLOW,
    )

    draw.rectangle((48, height - 30, 460, height - 26), fill=LINE)
    progress = 48 + int((index / total) * 412)
    draw.rectangle((48, height - 30, progress, height - 26), fill=YELLOW)

    logo = Image.open(LOGO).convert("RGB")
    logo = logo.resize((132, 132), Image.Resampling.LANCZOS)
    mask = Image.new("L", (132, 132), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, 131, 131), fill=255)
    image.paste(logo, (780, 54), mask)

    draw = ImageDraw.Draw(image)
    draw.ellipse((780, 54, 912, 186), outline=YELLOW, width=3)
    angle = int((index / total) * 360)
    draw.arc((770, 44, 922, 196), start=angle, end=angle + 70, fill=YELLOW, width=4)
    return image


def wheel_frame(index: int, total: int) -> Image.Image:
    size = 320
    image = Image.new("RGB", (size, size), DARK)
    draw = ImageDraw.Draw(image)

    center_x, center_y, radius = 160, 166, 108
    colors = [YELLOW, INK, PAPER, AMBER_DARK, YELLOW, INK]
    start = -90 + (index / total) * 360

    for slice_index in range(6):
        first = start + slice_index * 60
        last = first + 60
        draw.pieslice(
            (center_x - radius, center_y - radius, center_x + radius, center_y + radius),
            start=first,
            end=last,
            fill=colors[slice_index],
            outline=DARK,
            width=2,
        )

    draw.ellipse(
        (center_x - 27, center_y - 27, center_x + 27, center_y + 27),
        fill=PAPER,
        outline=INK,
        width=3,
    )
    draw.text(
        (center_x, center_y),
        "?",
        font=font("DejaVuSans-Bold.ttf", 34),
        fill=INK,
        anchor="mm",
    )

    draw.polygon([(center_x - 12, 16), (center_x + 12, 16), (center_x, 44)], fill=YELLOW)
    draw.text(
        (center_x, 292),
        "PUTAR RODA",
        font=font("DejaVuSansMono.ttf", 19),
        fill=PAPER,
        anchor="mm",
    )

    arc_start = int((index / total) * 360)
    draw.arc(
        (center_x - radius - 10, center_y - radius - 10, center_x + radius + 10, center_y + radius + 10),
        start=arc_start,
        end=arc_start + 90,
        fill=YELLOW,
        width=3,
    )
    return image


def pulse_frame(index: int, total: int) -> Image.Image:
    width, height = 600, 80
    image = Image.new("RGB", (width, height), DARK)
    draw = ImageDraw.Draw(image)

    draw.line((40, 58, width - 40, 58), fill=LINE, width=3)
    x = 40 + int((index / total) * (width - 80))
    pulse = (1 + math.sin(2 * math.pi * index / total)) / 2
    radius = int(7 + 4 * pulse)

    draw.ellipse((x - radius, 58 - radius, x + radius, 58 + radius), fill=YELLOW)
    draw.text(
        (width // 2, 25),
        "SCROLL  •  KLIK  •  PUTAR",
        font=font("DejaVuSansMono.ttf", 21),
        fill=PAPER,
        anchor="mm",
    )
    return image


def main() -> None:
    hero = [hero_frame(i, 36) for i in range(36)]
    wheel = [wheel_frame(i, 36) for i in range(36)]
    pulse = [pulse_frame(i, 30) for i in range(30)]

    save_gif(hero, "readme-hero.gif", 80)
    save_gif(wheel, "readme-wheel.gif", 70)
    save_gif(pulse, "readme-pulse.gif", 80)


if __name__ == "__main__":
    main()
