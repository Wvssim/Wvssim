#!/usr/bin/env python3
"""Turn a photo into assets/ascii-portrait.svg, revealed line by line.

    pip install pillow
    python scripts/make_ascii.py photo.jpg
    python scripts/make_ascii.py photo.jpg --cols 78 --invert

Use a high-contrast headshot with a plain background — ASCII has about ten
levels of tone to work with, so a busy background turns to noise. Crop it
square-ish first; the script does not try to find your face.
"""
import argparse
import pathlib
import sys

from PIL import Image, ImageEnhance, ImageOps

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from palette import MAJORELLE, MONO, theme_css  # noqa: E402

RAMP = " .:-=+*#%@"
CHAR_ASPECT = 0.52  # monospace glyphs are about twice as tall as wide


def to_rows(path, cols, invert, contrast):
    img = Image.open(path).convert("L")
    img = ImageOps.autocontrast(img, cutoff=2)
    if contrast != 1.0:
        img = ImageEnhance.Contrast(img).enhance(contrast)
    rows = max(1, int(cols * img.height / img.width * CHAR_ASPECT))
    img = img.resize((cols, rows), Image.LANCZOS)
    px = img.load()

    out = []
    for y in range(rows):
        line = []
        for x in range(cols):
            v = px[x, y] / 255
            if invert:
                v = 1 - v
            line.append(RAMP[min(len(RAMP) - 1, int(v * len(RAMP)))])
        out.append("".join(line).rstrip())
    return [r for r in out if r.strip()] or [""]


def build(rows, font_size=7.4):
    lh = font_size * 1.06
    adv = font_size * 0.6
    w = int(max(len(r) for r in rows) * adv) + 24
    h = int(len(rows) * lh) + 24

    css = theme_css({"ink": ("#EDE7DC", "#1C1814")})
    esc = lambda s: s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" font-family="{MONO}" role="img" '
        'aria-label="ASCII portrait">',
        f"<style>{css}"
        f"text{{fill:var(--ink);font-size:{font_size}px;"
        "white-space:pre;letter-spacing:0}"
        ".l{opacity:0;animation:type .01s linear both}"
        "@keyframes type{to{opacity:1}}"
        "@media(prefers-reduced-motion:reduce){.l{opacity:1;animation:none}}"
        "</style>",
    ]
    for i, row in enumerate(rows):
        y = 14 + i * lh
        out.append(f'<text class="l" x="12" y="{y:.1f}" '
                   f'style="animation-delay:{i * 0.028:.3f}s">{esc(row)}</text>')
    # a single accented scanline that sweeps once, then rests
    out.append(
        f'<rect x="0" y="0" width="{w}" height="2" fill="{MAJORELLE}" opacity="0">'
        f'<animate attributeName="y" from="0" to="{h}" dur="{len(rows)*0.028:.2f}s" '
        'fill="freeze"/>'
        f'<animate attributeName="opacity" values="0;.55;.55;0" '
        f'dur="{len(rows)*0.028:.2f}s" fill="freeze"/></rect>'
    )
    out.append("</svg>")
    return "\n".join(out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("photo")
    ap.add_argument("--cols", type=int, default=74)
    ap.add_argument("--contrast", type=float, default=1.25)
    ap.add_argument("--invert", action="store_true",
                    help="use for light-background photos")
    a = ap.parse_args()

    rows = to_rows(a.photo, a.cols, a.invert, a.contrast)
    dest = pathlib.Path(__file__).resolve().parents[1] / "assets" / "ascii-portrait.svg"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(build(rows), encoding="utf-8")
    print(f"wrote {dest} ({a.cols}x{len(rows)} chars)")
