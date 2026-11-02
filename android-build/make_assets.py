"""Draw the Pitch Smart icon: a little pitch with the centre circle and an orange ball.

Usage:
  python android-build/make_assets.py web docs/icons                    # icons for the web app
  python android-build/make_assets.py android android/app/src/main/res  # Android launcher icons + splash

For Android, every image keeps the size of the file it replaces, so this keeps working
if the Capacitor template changes its densities or adds splash variants.
"""
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw

INK = (21, 33, 59)
GRASS = (61, 154, 77)
GRASS2 = (68, 165, 84)
ORANGE = (255, 107, 53)
WHITE = (255, 255, 255)
PAPER = (244, 241, 232)


def art(size: int, scale: float, bg) -> Image.Image:
    """Pitch art inside a square of `size`; `scale` = share of the square the pitch uses."""
    S = size * 4
    im = Image.new("RGBA", (S, S), bg)
    d = ImageDraw.Draw(im)
    w = S * scale
    x0 = y0 = (S - w) / 2
    x1 = y1 = x0 + w
    r = w * 0.16
    d.rounded_rectangle([x0, y0, x1, y1], radius=r, fill=GRASS)
    # stripes
    band = w / 6
    for i in range(6):
        if i % 2:
            top = y0 + i * band
            stripe = Image.new("L", (S, S), 0)
            ImageDraw.Draw(stripe).rectangle([x0, top, x1, top + band], fill=255)
            clip = Image.new("L", (S, S), 0)
            ImageDraw.Draw(clip).rounded_rectangle([x0, y0, x1, y1], radius=r, fill=255)
            from PIL import ImageChops
            m = ImageChops.multiply(stripe, clip)
            im.paste(Image.new("RGBA", (S, S), GRASS2), (0, 0), m)
    lw = max(2, int(w * 0.035))
    cx = cy = S / 2
    d.line([x0 + lw, cy, x1 - lw, cy], fill=WHITE, width=lw)
    cr = w * 0.22
    d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], outline=WHITE, width=lw)
    br = w * 0.11
    d.ellipse([cx - br - lw * .6, cy - br - lw * .6, cx + br + lw * .6, cy + br + lw * .6], fill=WHITE)
    d.ellipse([cx - br, cy - br, cx + br, cy + br], fill=ORANGE)
    # goal boxes
    bw = w * 0.42
    bh = w * 0.13
    d.rectangle([cx - bw / 2, y0 + lw * .5, cx + bw / 2, y0 + bh], outline=WHITE, width=lw)
    d.rectangle([cx - bw / 2, y1 - bh, cx + bw / 2, y1 - lw * .5], outline=WHITE, width=lw)
    return im.resize((size, size), Image.LANCZOS)


def flat(size: int, scale: float, bg) -> Image.Image:
    return art(size, scale, bg).convert("RGB") if len(bg) == 3 else art(size, scale, bg)


def legacy_icon(w: int, round_: bool) -> Image.Image:
    im = art(w, 0.86, INK + (255,))
    mask = Image.new("L", (w * 4, w * 4), 0)
    md = ImageDraw.Draw(mask)
    if round_:
        md.ellipse([0, 0, w * 4, w * 4], fill=255)
    else:
        md.rounded_rectangle([0, 0, w * 4, w * 4], radius=w * 4 * 0.18, fill=255)
    im.putalpha(mask.resize((w, w), Image.LANCZOS))
    return im


def splash(w: int, h: int) -> Image.Image:
    im = Image.new("RGB", (w, h), PAPER)
    s = int(min(w, h) * 0.34)
    a = art(s, 0.95, (0, 0, 0, 0))
    im.paste(a, ((w - s) // 2, (h - s) // 2), a)
    return im


def web(out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    for name, size in (("icon-192.png", 192), ("icon-512.png", 512)):
        art(size, 0.92, (0, 0, 0, 0)).save(out / name)
    art(512, 0.66, GRASS + (255,)).convert("RGB").save(out / "maskable-512.png")
    art(180, 0.84, PAPER + (255,)).convert("RGB").save(out / "apple-touch-icon.png")
    art(32, 0.98, (0, 0, 0, 0)).save(out / "favicon-32.png")
    print("web icons written to", out)


def android(res: Path) -> None:
    done = 0
    for f in sorted(res.rglob("*.png")):
        w, h = Image.open(f).size
        name = f.name
        if name == "ic_launcher_foreground.png":
            # adaptive icon: 108dp canvas, only the middle ~66% is always visible
            art(w, 0.6, (0, 0, 0, 0)).save(f)
        elif name == "ic_launcher.png":
            legacy_icon(w, round_=False).save(f)
        elif name == "ic_launcher_round.png":
            legacy_icon(w, round_=True).save(f)
        elif name.startswith("splash"):
            splash(w, h).save(f)
        else:
            continue
        done += 1
    bg = res / "values" / "ic_launcher_background.xml"
    if bg.exists():
        bg.write_text(re.sub(r"#[0-9A-Fa-f]{6,8}", "#15213B", bg.read_text()))
        done += 1
    if done == 0:
        sys.exit(f"no launcher icons or splash images found under {res}")
    print(f"{done} Android images updated")


if __name__ == "__main__":
    mode, target = sys.argv[1], Path(sys.argv[2])
    {"web": web, "android": android}[mode](target)
