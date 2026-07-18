#!/usr/bin/env python3
"""Render assets/info-card.svg — a neofetch-style identity panel.

Everything you'd want to change lives in HOST and ROWS below.

    python scripts/make_info_card.py
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from palette import (  # noqa: E402
    INK, BONE, PANEL_D, PANEL_L, TEXT_D, TEXT_L, MUTED_D, MUTED_L,
    MAJORELLE, SAFFRON, TERRA, RAMP_D, MONO, theme_css,
)

HOST = "wassim@casablanca"

ROWS = [
    ("os",       "Morocco · Casablanca (GMT+1)"),
    ("host",     "EMSI — Génie Logiciel, 5e année"),
    ("kernel",   "full-stack → data engineering"),
    ("shell",    "français · العربية · english"),
    ("wm",       "Claude Code + VS Code"),
    ("packages", "next.js · spring-boot · tauri · kafka"),
    ("uptime",   "4 yrs building, 2 yrs shipping to clients"),
    ("disk",     "swhnegoce.ma · SwhOffice · CDC pipeline"),
]

SWATCHES = [RAMP_D[1], RAMP_D[2], RAMP_D[3], RAMP_D[4],
            MAJORELLE, SAFFRON, TERRA, TEXT_D]

W = 490
PAD = 26
ROW_H = 26
HEAD_H = 62
FOOT_H = 44


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def build():
    h = HEAD_H + len(ROWS) * ROW_H + FOOT_H
    key_w = max(len(k) for k, _ in ROWS)

    css = theme_css({
        "bg":    (PANEL_D, PANEL_L),
        "edge":  ("#241B33", "#D6CBEA"),
        "text":  (TEXT_D, TEXT_L),
        "muted": (MUTED_D, MUTED_L),
    })

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" '
        f'viewBox="0 0 {W} {h}" font-family="{MONO}" role="img" '
        f'aria-label="Identity card for {esc(HOST)}">',
        f"<style>{css}"
        ".k{fill:var(--muted);font-size:12.5px}"
        ".v{fill:var(--text);font-size:12.5px}"
        f".host{{fill:{MAJORELLE};font-size:14px;font-weight:700}}"
        f".at{{fill:{SAFFRON};font-size:14px;font-weight:700}}"
        ".row{opacity:0;animation:in .4s ease-out both}"
        "@keyframes in{from{opacity:0;transform:translateX(-6px)}"
        "to{opacity:1;transform:translateX(0)}}"
        "@media(prefers-reduced-motion:reduce){.row{opacity:1;animation:none}}"
        "</style>",
        f'<rect x="0.5" y="0.5" width="{W-1}" height="{h-1}" rx="10" '
        'fill="var(--bg)" stroke="var(--edge)"/>',
    ]

    # header: user@host, then a rule the width of the string
    user, host = HOST.split("@")
    out.append(f'<text class="host" x="{PAD}" y="34">{esc(user)}'
               f'<tspan class="at">@</tspan>{esc(host)}</text>')
    out.append(f'<line x1="{PAD}" y1="45" x2="{W-PAD}" y2="45" '
               'stroke="var(--edge)"/>')

    y = HEAD_H + 12
    for i, (k, v) in enumerate(ROWS):
        d = i * 0.055
        out.append(
            f'<g class="row" style="animation-delay:{d:.3f}s">'
            f'<text class="k" x="{PAD}" y="{y}">{esc(k.ljust(key_w))}</text>'
            f'<text class="v" x="{PAD + key_w * 8 + 14}" y="{y}">{esc(v)}</text>'
            "</g>"
        )
        y += ROW_H

    # neofetch-style colour blocks
    sw_y = h - 30
    for i, c in enumerate(SWATCHES):
        out.append(f'<rect x="{PAD + i * 22}" y="{sw_y}" width="16" height="10" '
                   f'rx="2" fill="{c}"/>')

    out.append("</svg>")
    return "\n".join(out)


if __name__ == "__main__":
    dest = pathlib.Path(__file__).resolve().parents[1] / "assets" / "info-card.svg"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(build(), encoding="utf-8")
    print(f"wrote {dest}")
