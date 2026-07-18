"""Design tokens shared by every generated SVG.

Palette is an electric-violet "cyber" scheme: a cool violet-black field,
vivid violet as the primary accent, and a lighter lilac reserved for peaks.
Edit here and every asset follows.
"""

# Surfaces
INK = "#0F0B18"        # violet-black (dark mode)
BONE = "#F4F1FB"       # cool off-white (light mode)
PANEL_D = "#17121F"    # raised panel, dark
PANEL_L = "#EAE4F5"    # raised panel, light

# Text
TEXT_D = "#EDE9F7"
TEXT_L = "#1A1626"
MUTED_D = "#8B84A0"
MUTED_L = "#6A6280"

# Accents
MAJORELLE = "#8B5CF6"   # primary — electric violet
SAFFRON = "#A78BFA"     # secondary — light violet (peaks, @)
TERRA = "#C084FC"       # tertiary — orchid

# Contribution ramp, empty -> busiest.
# Violet field brightening to lilac: the heaviest days glow.
RAMP_D = ["#1C1630", "#6249AD", "#8261E4", "#A588F6", "#CBB8FF"]
RAMP_L = ["#ECE6F6", "#B4A0EA", "#9376E6", "#7856D4", "#5B3FB0"]

MONO = "ui-monospace,SFMono-Regular,'SF Mono',Menlo,Consolas,'Liberation Mono',monospace"


def theme_css(pairs):
    """Emit CSS custom properties that flip with the reader's colour scheme.

    `pairs` maps a variable name to (dark_value, light_value). GitHub renders
    README images inside <img>, where prefers-color-scheme still applies, so
    this is what keeps the assets legible on both themes.
    """
    dark = "".join(f"--{k}:{d};" for k, (d, _) in pairs.items())
    light = "".join(f"--{k}:{l};" for k, (_, l) in pairs.items())
    return (
        f":root{{{dark}}}"
        f"@media(prefers-color-scheme:light){{:root{{{light}}}}}"
    )
