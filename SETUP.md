# Setup

Five minutes, once.

## 1. Put the files in the repo

Everything goes at the root of `Wvssim/Wvssim`:

```
README.md
SETUP.md
assets/            ascii-portrait.svg, info-card.svg, contrib-heatmap.svg
scripts/           palette.py, make_ascii.py, make_info_card.py, make_heatmap.py
.github/workflows/ update-profile-art.yml
```

```bash
git clone https://github.com/Wvssim/Wvssim.git
cd Wvssim
# copy the files in, then:
git add .
git commit -m "feat: profile README with generated art"
git branch -M main
git push -u origin main
```

## 2. Swap the placeholder portrait for your photo

`assets/ascii-portrait.svg` currently holds a zellige star, so the layout is
not broken on day one. Replace it:

```bash
pip install pillow
python scripts/make_ascii.py ~/Pictures/moi.jpg --cols 74
```

Crop the photo square-ish first and pick one with a plain background — ASCII
has about ten levels of tone, so a busy background turns into noise. If the
result looks like a negative, add `--invert`. `--cols` is the resolution knob;
above ~90 it stops reading as a face at README scale.

## 3. Give the workflow a token

The contribution calendar is only available through GitHub's GraphQL API, and
that endpoint requires a token even for public profiles. The workflow's
built-in `GITHUB_TOKEN` is repo-scoped and does not reliably cover it, so:

1. **Settings → Developer settings → Personal access tokens → Tokens (classic)**
2. Generate one with the **`read:user`** scope only. Nothing else.
3. In `Wvssim/Wvssim`: **Settings → Secrets and variables → Actions → New
   repository secret**, named `PROFILE_TOKEN`.

Then run it once by hand: **Actions → update profile art → Run workflow**.

Until that first run, `assets/contrib-heatmap.svg` holds **generated sample
data** — the totals are not yours. The workflow overwrites it.

## 4. Editing later

| Want to change | Edit |
|---|---|
| Colours, anywhere | `scripts/palette.py` |
| The info card rows | `HOST` and `ROWS` in `scripts/make_info_card.py` |
| Projects, links, badges | `README.md` directly |
| How often art refreshes | the `cron` in the workflow |

After editing a script, re-run it and commit the changed SVG — the workflow
only regenerates on its schedule.

## Notes

- Every SVG carries a `prefers-color-scheme` block, so it stays legible for
  readers on GitHub's light theme. Most profile READMEs hardcode dark-theme
  colours and disappear on light.
- Animations are CSS, which browsers run inside `<img>`-referenced SVGs.
  `<script>` would not run — don't reach for it.
- `prefers-reduced-motion` is respected throughout.
- Don't create another repo named `Wvssim`; the rename you did already
  redirects the old name, and reusing it breaks the redirect.
