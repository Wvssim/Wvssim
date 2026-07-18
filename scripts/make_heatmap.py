#!/usr/bin/env python3
"""Render assets/contrib-heatmap.svg from real GitHub contribution data.

    GITHUB_TOKEN=ghp_xxx python scripts/make_heatmap.py --login Wvssim
    python scripts/make_heatmap.py --demo        # styling preview, fake data

The contribution calendar is only exposed through the GraphQL API, which
always requires a token — even for public profiles. In CI the workflow's
built-in GITHUB_TOKEN is enough; no secret to create.
"""
import argparse
import datetime as dt
import json
import os
import pathlib
import random
import sys
import urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from palette import RAMP_D, RAMP_L, MUTED_D, MUTED_L, TEXT_D, TEXT_L, MONO, theme_css  # noqa: E402

QUERY = """
query($login:String!){
  user(login:$login){
    contributionsCollection{
      contributionCalendar{
        totalContributions
        weeks{ contributionDays{ date contributionCount weekday } }
      }
    }
  }
}
"""

CELL, PITCH = 13, 16
LEFT, TOP = 34, 24
BOTTOM = 36


def fetch(login, token):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": login}}).encode(),
        headers={"Authorization": f"bearer {token}",
                 "Content-Type": "application/json",
                 "User-Agent": "profile-art"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        payload = json.load(r)
    if "errors" in payload:
        raise SystemExit(f"GitHub API error: {payload['errors']}")
    cal = payload["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    weeks = [[(d["date"], d["contributionCount"], d["weekday"])
              for d in w["contributionDays"]] for w in cal["weeks"]]
    return weeks, cal["totalContributions"]


def demo():
    """Synthetic calendar so the styling can be checked without a token."""
    rng = random.Random(7)
    end = dt.date.today()
    start = end - dt.timedelta(days=364)
    start -= dt.timedelta(days=(start.weekday() + 1) % 7)
    weeks, cur, total = [], start, 0
    while cur <= end:
        week = []
        for _ in range(7):
            if cur > end:
                break
            n = 0 if rng.random() < 0.12 else rng.randint(1, 14)
            total += n
            week.append((cur.isoformat(), n, (cur.weekday() + 1) % 7))
            cur += dt.timedelta(days=1)
        weeks.append(week)
    return weeks, total


def level(n, peak):
    if n <= 0:
        return 0
    for i, frac in enumerate((0.15, 0.35, 0.65), start=1):
        if n <= max(1, round(peak * frac)):
            return i
    return 4


def build(weeks, total):
    w = LEFT + len(weeks) * PITCH + 8
    h = TOP + 7 * PITCH + BOTTOM
    peak = max((c for wk in weeks for _, c, _ in wk), default=1)

    css = theme_css({
        "muted": (MUTED_D, MUTED_L),
        "text": (TEXT_D, TEXT_L),
        **{f"l{i}": (RAMP_D[i], RAMP_L[i]) for i in range(5)},
    })

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" font-family="{MONO}" role="img" '
        f'aria-label="{total} contributions in the last year">',
        f"<style>{css}"
        ".lbl{fill:var(--muted);font-size:11px;font-weight:600}"
        ".total{fill:var(--text);font-size:13px;font-weight:700}"
        f".tot-n{{fill:{RAMP_D[4]};font-size:13px;font-weight:700}}"
        ".c{transform-box:fill-box;transform-origin:center;opacity:0;"
        "animation:pop .5s ease-out both}"
        "@keyframes pop{0%{opacity:0;transform:scale(.2)}"
        "60%{opacity:1;transform:scale(1.12)}100%{opacity:1;transform:scale(1)}}"
        "@media(prefers-reduced-motion:reduce){.c{opacity:1;animation:none}}"
        "</style>",
    ]

    # month labels, placed on the first week of each new month
    seen = set()
    for wi, wk in enumerate(weeks):
        if not wk:
            continue
        d = dt.date.fromisoformat(wk[0][0])
        if (d.year, d.month) not in seen:
            seen.add((d.year, d.month))
            out.append(f'<text class="lbl" x="{LEFT + wi * PITCH}" y="16">'
                       f'{d.strftime("%b")}</text>')
    for wd, name in ((1, "Mon"), (3, "Wed"), (5, "Fri")):
        out.append(f'<text class="lbl" x="0" y="{TOP + wd * PITCH + 11}">{name}</text>')

    n = 0
    for wi, wk in enumerate(weeks):
        for date, count, wd in wk:
            x, y = LEFT + wi * PITCH, TOP + wd * PITCH
            delay = n * 0.0022
            out.append(
                f'<rect class="c" x="{x}" y="{y}" width="{CELL}" height="{CELL}" '
                f'rx="2.5" fill="var(--l{level(count, peak)})" '
                f'style="animation-delay:{delay:.3f}s">'
                f"<title>{date}: {count}</title></rect>"
            )
            n += 1

    out.append(f'<text class="total" x="{LEFT}" y="{h - 12}">'
               f'<tspan class="tot-n">{total:,}</tspan> contributions '
               "in the last year</text>")
    out.append("</svg>")
    return "\n".join(out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--login", default=os.environ.get("GH_LOGIN", "Wvssim"))
    ap.add_argument("--demo", action="store_true")
    a = ap.parse_args()

    if a.demo:
        weeks, total = demo()
    else:
        tok = os.environ.get("GITHUB_TOKEN")
        if not tok:
            raise SystemExit("set GITHUB_TOKEN, or pass --demo for a preview")
        weeks, total = fetch(a.login, tok)

    dest = pathlib.Path(__file__).resolve().parents[1] / "assets" / "contrib-heatmap.svg"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(build(weeks, total), encoding="utf-8")
    print(f"wrote {dest} ({total:,} contributions)")
