#!/usr/bin/env python3
"""Turn a logo/emblem into a COLOURED ascii-portrait.svg.

Each glyph keeps the source pixel's own colour, so a crest on a plain
background reads in full colour while the background stays blank. Best for
flat, high-contrast art (emblems, logos) rather than photos.

    pip install pillow
    python scripts/make_ascii_color.py emblem.jfif --cols 100

The white field maps to blank space; coloured/dark ink maps to glyphs whose
density grows with how far the pixel is from white. Near-black outlines are
lifted to a readable grey so they survive on GitHub's dark theme.
"""
import argparse
import pathlib
import sys

from PIL import Image, ImageEnhance

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from palette import MAJORELLE, MONO  # noqa: E402

RAMP = " .:-=+*#%@"
CHAR_ASPECT = 0.52


def lift(r, g, b):
    """Keep the hue but guarantee enough brightness to read on a dark ground."""
    m = max(r, g, b)
    if m < 40:
        return (122, 122, 130)          # near-black outline -> readable grey
    if m < 170:
        s = 170 / m
        return (min(255, int(r * s)), min(255, int(g * s)), min(255, int(b * s)))
    return (r, g, b)


def quant(v, step=32):
    return min(255, (v + step // 2) // step * step)


def grid(path, cols, contrast, saturation):
    rgb = Image.open(path).convert("RGB")
    if saturation != 1.0:
        rgb = ImageEnhance.Color(rgb).enhance(saturation)
    rows = max(1, int(cols * rgb.height / rgb.width * CHAR_ASPECT))
    rgb = rgb.resize((cols, rows), Image.LANCZOS)
    px = rgb.load()

    g = []
    for y in range(rows):
        line = []
        for x in range(cols):
            r, gr, b = px[x, y]
            ink = 1 - min(r, gr, b) / 255          # white -> 0, colour/ink -> high
            ink = max(0.0, min(1.0, (ink - 0.5) * contrast + 0.5))
            ch = RAMP[min(len(RAMP) - 1, int(ink * len(RAMP)))]
            if ch == " ":
                line.append((" ", None))
            else:
                col = lift(quant(r), quant(gr), quant(b))
                line.append((ch, "#{:02X}{:02X}{:02X}".format(*col)))
        g.append(line)
    return g


def crop(g):
    """Trim fully-blank edge rows and columns so the emblem sits tight."""
    def blank_row(row):
        return all(c is None for _, c in row)
    while g and blank_row(g[0]):
        g.pop(0)
    while g and blank_row(g[-1]):
        g.pop()
    if not g:
        return [[(" ", None)]]
    cols = len(g[0])
    left = 0
    while left < cols and all(row[left][1] is None for row in g):
        left += 1
    right = cols - 1
    while right > left and all(row[right][1] is None for row in g):
        right -= 1
    return [row[left:right + 1] for row in g]


def build(g, font_size=7.4):
    lh = font_size * 1.06
    adv = font_size * 0.6
    cols = max(len(r) for r in g)
    w = int(cols * adv) + 24
    h = int(len(g) * lh) + 24

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" font-family="{MONO}" role="img" '
        'aria-label="Coloured ASCII emblem">',
        f"<style>text{{font-size:{font_size}px;white-space:pre;letter-spacing:0}}"
        ".l{opacity:0;animation:type .01s linear both}"
        "@keyframes type{to{opacity:1}}"
        "@media(prefers-reduced-motion:reduce){.l{opacity:1;animation:none}}"
        "</style>",
    ]

    for y, row in enumerate(g):
        segs, run_col, run_txt = [], "init", ""
        for ch, col in row:
            if col == run_col:
                run_txt += ch
            else:
                if run_txt:
                    segs.append(run_txt if run_col is None
                                else f'<tspan fill="{run_col}">{run_txt}</tspan>')
                run_col, run_txt = col, ch
        if run_txt:
            segs.append(run_txt if run_col is None
                        else f'<tspan fill="{run_col}">{run_txt}</tspan>')
        yy = 14 + y * lh
        out.append(f'<text class="l" x="12" y="{yy:.1f}" '
                   f'style="animation-delay:{y * 0.022:.3f}s">{"".join(segs)}</text>')

    out.append(
        f'<rect x="0" y="0" width="{w}" height="2" fill="{MAJORELLE}" opacity="0">'
        f'<animate attributeName="y" from="0" to="{h}" dur="{len(g)*0.022:.2f}s" fill="freeze"/>'
        f'<animate attributeName="opacity" values="0;.55;.55;0" '
        f'dur="{len(g)*0.022:.2f}s" fill="freeze"/></rect>'
    )
    out.append("</svg>")
    return "\n".join(out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("photo")
    ap.add_argument("--cols", type=int, default=100)
    ap.add_argument("--contrast", type=float, default=1.35)
    ap.add_argument("--saturation", type=float, default=1.2)
    a = ap.parse_args()

    g = crop(grid(a.photo, a.cols, a.contrast, a.saturation))
    dest = pathlib.Path(__file__).resolve().parents[1] / "assets" / "ascii-portrait.svg"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(build(g), encoding="utf-8")
    print(f"wrote {dest} ({max(len(r) for r in g)}x{len(g)} cells)")
