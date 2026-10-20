"""Builds the roxx990 profile README and its custom SVGs from one palette.

Run: python3 -I scripts/build.py            (README.md and every assets/*.svg)
     python3 -I scripts/build.py activity   (only assets/activity.svg; run daily by CI)
The activity graph needs the GitHub CLI (`gh`) logged in, or GH_TOKEN set.
"""
import json
import re
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

USER = "roxx990"
SCRIPTS = Path(__file__).resolve().parent
OUT = SCRIPTS.parent
ASSETS = OUT / "assets"
ICONS = SCRIPTS / "icons"

# ---- Palette: change these to re-theme everything ----------------------------
A1 = "#6366F1"       # indigo
A2 = "#A855F7"       # violet
A_MID = "#8B5CF6"    # accent used on light backgrounds (typing text, badges)
A_SOFT = "#C4B5FD"   # accent used on dark cards
RAMP = ["#312E81", "#4338CA", "#6366F1", "#818CF8", "#8B5CF6", "#A855F7", "#C084FC", "#E9D5FF"]
CARD = "#11131C"
BORDER = "#262A38"
TEXT = "#E8EAF2"
BODY = "#C3C7D6"
MUTED = "#8C92A6"
WALL_1, WALL_2 = "#1E1B4B", "#3B0764"   # toolbox "desktop" wallpaper
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"

hexs = lambda c: c.lstrip("#")


def icon_path(slug):
    svg = (ICONS / f"{slug}.svg").read_text()
    return re.search(r'<path d="([^"]+)"', svg).group(1)


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ---- Toolbox: a macOS desktop with a fastfetch-style terminal ----------------
FETCH = [
    ("OS", "iOS, iPadOS, macOS"),
    ("Role", "Software Engineer @ CoderZone"),
    ("Languages", "Swift, Dart"),
    ("Frameworks", "SwiftUI, UIKit, AppKit, Flutter"),
    ("Tools", "Xcode, SwiftPM, Git, GitHub"),
    ("Focus", "Apps, Swift packages, dev tools"),
]
DOCK = ["swift", "xcode", "apple", "flutter", "dart", "git", "github"]


def toolbox_svg():
    W, H = 840, 462
    win_x, win_y, win_w, win_h = 70, 50, 700, 318
    body_y = win_y + 30

    # fastfetch output, revealed line by line
    info_x, y0, step = 292, body_y + 58, 21
    lines = [f'<tspan fill="{A_SOFT}" font-weight="700">zuraiz</tspan><tspan fill="{TEXT}">@</tspan>'
             f'<tspan fill="{A_SOFT}" font-weight="700">roxx990</tspan>',
             f'<tspan fill="{MUTED}">{"─" * 14}</tspan>']
    lines += [f'<tspan fill="{A_SOFT}" font-weight="700">{esc(k)}</tspan><tspan fill="{MUTED}">:</tspan> {esc(v)}'
              for k, v in FETCH]
    info = "".join(f'<text x="{info_x}" y="{y0 + i * step}" class="t l" style="animation-delay:{.35 + i * .12:.2f}s">{l}</text>'
                   for i, l in enumerate(lines))
    sw_y = y0 + len(lines) * step - 4
    swatches = "".join(f'<rect x="{info_x + i * 26}" y="{sw_y}" width="22" height="14" rx="3" fill="{c}"/>' for i, c in enumerate(RAMP))
    swatch_delay = .35 + len(lines) * .12

    # dock
    tile, gap, pad = 46, 16, 14
    dock_w = len(DOCK) * tile + (len(DOCK) - 1) * gap + pad * 2
    dock_x, dock_y = (W - dock_w) / 2, win_y + win_h + 14
    tiles = []
    for i, slug in enumerate(DOCK):
        x, y = dock_x + pad + i * (tile + gap), dock_y + 9
        s = 26 / 24
        cls = ' class="bounce"' if slug == "xcode" else ""
        tiles.append(f'<g{cls}><rect x="{x}" y="{y}" width="{tile}" height="{tile}" rx="11" fill="url(#tile)" stroke="#fff" stroke-opacity=".12"/>'
                     f'<path transform="translate({x + 10} {y + 10}) scale({s:.4f})" d="{icon_path(slug)}" fill="#fff"/></g>')
        if slug in ("swift", "xcode"):
            tiles.append(f'<circle cx="{x + tile / 2}" cy="{y + tile + 6}" r="2" fill="#fff" fill-opacity=".8"/>')

    # menu bar status glyphs
    status = f"""
    <g fill="none" stroke="#fff" stroke-width="1.6" stroke-linecap="round" opacity=".9">
      <path d="M{W - 112} 13.5a8 8 0 0 1 11 0M{W - 109.5} 16.5a4.4 4.4 0 0 1 6 0"/>
      <rect x="{W - 90}" y="9" width="20" height="10" rx="3"/>
    </g>
    <circle cx="{W - 106.5}" cy="19.5" r="1.4" fill="#fff"/>
    <rect x="{W - 88}" y="11" width="13" height="6" rx="1.5" fill="#fff"/>
    <rect x="{W - 68.5}" y="12" width="1.8" height="4" rx=".9" fill="#fff" opacity=".9"/>
    <text x="{W - 18}" y="19" class="menu" text-anchor="end">9:41</text>"""

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Toolbox. Languages: Swift, Dart. Frameworks: SwiftUI, UIKit, AppKit, Flutter. Tools: Xcode, SwiftPM, Git, GitHub.">
  <style>
    .menu {{ font: 13px {SANS}; fill: #fff }}
    .t {{ font: 13.5px {MONO}; fill: {BODY} }}
    .wt {{ font: 12px {SANS}; fill: {MUTED} }}
    .l {{ animation: in .45s ease-out both }}
    @keyframes in {{ from {{ opacity: 0; transform: translateX(-8px) }} to {{ opacity: 1; transform: none }} }}
    .logo {{ animation: pop .7s cubic-bezier(.2,.9,.3,1.2) .15s both; transform-origin: 181px 203px }}
    @keyframes pop {{ from {{ opacity: 0; transform: scale(.85) }} to {{ opacity: 1; transform: none }} }}
    .cursor {{ animation: blink 1.1s steps(1) infinite }}
    @keyframes blink {{ 50% {{ opacity: 0 }} }}
    .bounce {{ animation: bounce 6s ease-in-out 2s infinite }}
    @keyframes bounce {{ 0%,70%,100% {{ transform: translateY(0) }} 76% {{ transform: translateY(-14px) }} 82% {{ transform: translateY(0) }} 88% {{ transform: translateY(-6px) }} 94% {{ transform: translateY(0) }} }}
    .blob1 {{ animation: drift1 16s ease-in-out infinite alternate }}
    .blob2 {{ animation: drift2 20s ease-in-out infinite alternate }}
    @keyframes drift1 {{ to {{ transform: translate(140px, -40px) }} }}
    @keyframes drift2 {{ to {{ transform: translate(-160px, 50px) }} }}
  </style>
  <defs>
    <linearGradient id="wall" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{WALL_1}"/><stop offset="1" stop-color="{WALL_2}"/></linearGradient>
    <linearGradient id="logo" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{A1}"/><stop offset="1" stop-color="{A2}"/></linearGradient>
    <linearGradient id="tile" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2C2F45"/><stop offset="1" stop-color="#181A28"/></linearGradient>
    <filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="45"/></filter>
    <filter id="shadow" x="-10%" y="-10%" width="120%" height="130%"><feDropShadow dx="0" dy="14" stdDeviation="16" flood-color="#000" flood-opacity=".45"/></filter>
    <clipPath id="screen"><rect width="{W}" height="{H}" rx="16"/></clipPath>
  </defs>
  <g clip-path="url(#screen)">
    <rect width="{W}" height="{H}" fill="url(#wall)"/>
    <circle class="blob1" cx="140" cy="330" r="150" fill="{A1}" opacity=".55" filter="url(#blur)"/>
    <circle class="blob2" cx="700" cy="120" r="150" fill="{A2}" opacity=".45" filter="url(#blur)"/>

    <!-- menu bar -->
    <rect width="{W}" height="28" fill="#000" fill-opacity=".3"/>
    <path transform="translate(18 7) scale(.58)" d="{icon_path('apple')}" fill="#fff"/>
    <text x="44" y="19" class="menu" font-weight="700">Terminal</text>
    <text x="118" y="19" class="menu" fill-opacity=".85">Shell</text>
    <text x="162" y="19" class="menu" fill-opacity=".85">Edit</text>
    <text x="200" y="19" class="menu" fill-opacity=".85">View</text>
    <text x="244" y="19" class="menu" fill-opacity=".85">Window</text>
    {status}

    <!-- terminal window -->
    <g filter="url(#shadow)">
      <rect x="{win_x}" y="{win_y}" width="{win_w}" height="{win_h}" rx="12" fill="#0C0D15" fill-opacity=".92" stroke="#fff" stroke-opacity=".14"/>
    </g>
    <path d="M{win_x} {body_y}H{win_x + win_w}" stroke="#fff" stroke-opacity=".08"/>
    <circle cx="{win_x + 20}" cy="{win_y + 15}" r="6" fill="#fff" fill-opacity=".22"/>
    <circle cx="{win_x + 40}" cy="{win_y + 15}" r="6" fill="#fff" fill-opacity=".22"/>
    <circle cx="{win_x + 60}" cy="{win_y + 15}" r="6" fill="#fff" fill-opacity=".22"/>
    <text x="{win_x + win_w / 2}" y="{win_y + 19}" text-anchor="middle" class="wt">zuraiz — zsh — 80×24</text>

    <text x="{win_x + 24}" y="{body_y + 28}" class="t"><tspan fill="{A_SOFT}">~</tspan> <tspan fill="{MUTED}">$</tspan> fastfetch</text>
    <g class="logo"><path transform="translate(106 128) scale(6.25)" d="{icon_path('swift')}" fill="url(#logo)"/></g>
    {info}
    <g class="l" style="animation-delay:{swatch_delay:.2f}s">{swatches}</g>
    <text x="{win_x + 24}" y="{win_y + win_h - 20}" class="t"><tspan fill="{A_SOFT}">~</tspan> <tspan fill="{MUTED}">$</tspan></text>
    <rect class="cursor" x="{win_x + 60}" y="{win_y + win_h - 31}" width="8" height="15" fill="{A_SOFT}"/>

    <!-- dock -->
    <rect x="{dock_x}" y="{dock_y}" width="{dock_w}" height="{tile + 24}" rx="20" fill="#fff" fill-opacity=".10" stroke="#fff" stroke-opacity=".18"/>
    {''.join(tiles)}
  </g>
</svg>
"""


# ---- Project cards: a bento grid of macOS windows ----------------------------
GUTTER = 8   # transparent margin baked into each card's sides; gaps are always 2x this
ROW_GAP = 10 # extra transparent space under the featured card (inline images add ~4px)

GLYPHS = {
    # 44x44 line glyphs, drawn white on the gradient app tile
    "phone": '<rect x="15" y="9" width="14" height="26" rx="3.5"/><path d="M20 12.5h4"/><circle cx="22" cy="30.5" r="1" fill="#fff"/>',
    "cloud": '<path d="M14.5 31h15.5a6 6 0 0 0 .6-11.97A8.5 8.5 0 0 0 14.2 21.4 4.8 4.8 0 0 0 14.5 31z"/>',
    "box": '<rect x="10" y="11" width="24" height="7" rx="1.8"/><path d="M12 18v13a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V18"/><path d="M19 23h6"/>',
}

CARD_STYLE = f"""
    .wt {{ font: 11.5px {MONO}; fill: {MUTED} }}
    .name {{ font: 700 22px {SANS}; fill: {TEXT} }}
    .kind {{ font: 13px {SANS}; fill: {MUTED} }}
    .desc {{ font: 14.5px {SANS}; fill: {BODY} }}
    .tag {{ font: 600 11.5px {SANS}; fill: {A_SOFT} }}
    .go {{ font: 600 13px {SANS}; fill: {A_SOFT} }}
    .lang {{ font: 12.5px {SANS}; fill: {MUTED} }}
    .mono {{ font: 11px {MONO}; fill: {MUTED} }}
    .glow {{ animation: glow 3.2s ease-in-out infinite }}
    @keyframes glow {{ 50% {{ opacity: .35 }} }}"""

CARD_DEFS = f"""
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{A1}"/><stop offset="1" stop-color="{A2}"/></linearGradient>
    <linearGradient id="edge" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{A1}" stop-opacity="0"/><stop offset=".5" stop-color="{A2}"/><stop offset="1" stop-color="{A1}" stop-opacity="0"/></linearGradient>
    <filter id="soft" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="9"/></filter>
    <pattern id="dots" width="16" height="16" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1" fill="#fff" fill-opacity=".07"/></pattern>"""


def window(w, h, title):
    return (f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="16" fill="{CARD}" stroke="{BORDER}"/>'
            f'<circle cx="20" cy="18" r="5" fill="#363B4D"/><circle cx="36" cy="18" r="5" fill="#363B4D"/><circle cx="52" cy="18" r="5" fill="#363B4D"/>'
            f'<text x="{w / 2}" y="22" text-anchor="middle" class="wt">{esc(title)}</text>'
            f'<path d="M1 36.5H{w - 1}" stroke="{BORDER}"/><path d="M60 36.5H{w - 60}" stroke="url(#edge)"/>')


def app_tile(x, y, glyph, size=48):
    s = size / 44
    return (f'<rect class="glow" x="{x}" y="{y}" width="{size}" height="{size}" rx="{size * .27}" fill="url(#g)" filter="url(#soft)" opacity=".7"/>'
            f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="{size * .27}" fill="url(#g)"/>'
            f'<g transform="translate({x} {y}) scale({s:.3f})" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">{GLYPHS[glyph]}</g>')


def tags_row(x, y, tags):
    out = []
    for t in tags:
        w = 18 + len(t) * 6.9
        out.append(f'<rect x="{x}" y="{y}" width="{w}" height="24" rx="12" fill="{A2}" fill-opacity=".12" stroke="{A_SOFT}" stroke-opacity=".35"/>'
                   f'<text x="{x + w / 2}" y="{y + 16}" text-anchor="middle" class="tag">{esc(t)}</text>')
        x += w + 7
    return "".join(out)


def svg_wrap(w, h, label, body, extra_style="", bottom=0):
    G = GUTTER
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w + 2 * G} {h + bottom}" width="{w + 2 * G}" height="{h + bottom}" role="img" aria-label="{esc(label)}">
  <style>{CARD_STYLE}{extra_style}
  </style>
  <defs>{CARD_DEFS}
    <filter id="shadow" x="-20%" y="-20%" width="140%" height="160%"><feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#000" flood-opacity=".5"/></filter>
  </defs>
  <g transform="translate({G} 0)">{body}</g>
</svg>
"""


def devsim_svg():
    W, H = 840, 316
    desc = ["Jump straight into iOS Simulator app", "containers: open, inspect, reset and",
            "uninstall apps, or erase a simulator."]
    left = (app_tile(28, 60, "phone", 52)
            + f'<text x="96" y="84" class="name">devsim</text><text x="96" y="105" class="kind">macOS menu bar app</text>'
            + "".join(f'<text x="28" y="{152 + i * 25}" class="desc">{esc(l)}</text>' for i, l in enumerate(desc))
            + tags_row(28, 236, ["macOS", "Menu bar", "Simulator"])
            + f'<circle cx="34" cy="{H - 30}" r="5" fill="{A_MID}"/><text x="46" y="{H - 26}" class="lang">Swift</text>'
            + f'<text x="396" y="{H - 26}" text-anchor="end" class="go">View on GitHub →</text>')

    # right: a slice of desktop with devsim's menu open
    rx, ry, rw, rh = 432, 52, 384, 316 - 52 - 24
    mx, my, mw = 588, ry + 32, 214
    items = ["Open App Container", "Inspect Data", "Reset App", "Uninstall App"]
    rows = "".join(f'<text x="{mx + 16}" y="{my + 63 + i * 26}" class="mi">{t}</text>' for i, t in enumerate(items))
    menu = f"""
      <g filter="url(#shadow)"><rect x="{mx}" y="{my}" width="{mw}" height="190" rx="10" fill="#1A1C29" fill-opacity=".96" stroke="#fff" stroke-opacity=".12"/></g>
      <circle cx="{mx + 18}" cy="{my + 21}" r="4" fill="{A_SOFT}"/>
      <text x="{mx + 30}" y="{my + 25}" class="mh">iPhone 16 Pro</text>
      <text x="{mx + mw - 14}" y="{my + 25}" text-anchor="end" class="mm">Booted</text>
      <path d="M{mx + 10} {my + 38.5}H{mx + mw - 10}" stroke="#fff" stroke-opacity=".1"/>
      <rect class="hl" x="{mx + 6}" y="{my + 46}" width="{mw - 12}" height="24" rx="6" fill="url(#g)"/>
      {rows}
      <path d="M{mx + 10} {my + 156.5}H{mx + mw - 10}" stroke="#fff" stroke-opacity=".1"/>
      <text x="{mx + 16}" y="{my + 178}" class="mi" fill-opacity=".6">Erase Simulator…</text>"""
    right = f"""
    <clipPath id="desk"><rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="12"/></clipPath>
    <g clip-path="url(#desk)">
      <rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" fill="url(#wall)"/>
      <circle cx="{rx + 60}" cy="{ry + 200}" r="90" fill="{A1}" opacity=".5" filter="url(#blur)"/>
      <circle cx="{rx + 330}" cy="{ry + 40}" r="90" fill="{A2}" opacity=".45" filter="url(#blur)"/>
      <rect x="{rx}" y="{ry}" width="{rw}" height="26" fill="#000" fill-opacity=".3"/>
      <rect x="{mx + 4}" y="{ry + 3}" width="24" height="20" rx="5" fill="#fff" fill-opacity=".22"/>
      <g transform="translate({mx + 4} {ry + 1}) scale(.55)" fill="none" stroke="#fff" stroke-width="3.4" stroke-linecap="round">{GLYPHS['phone']}</g>
      <g fill="none" stroke="#fff" stroke-width="1.5" stroke-linecap="round" opacity=".9">
        <path d="M{rx + rw - 96} {ry + 12.5}a7 7 0 0 1 9.6 0M{rx + rw - 93.8} {ry + 15.2}a3.8 3.8 0 0 1 5.2 0"/>
        <rect x="{rx + rw - 78}" y="{ry + 8.5}" width="18" height="9" rx="2.6"/>
      </g>
      <rect x="{rx + rw - 76}" y="{ry + 10.5}" width="12" height="5" rx="1.3" fill="#fff"/>
      <text x="{rx + rw - 14}" y="{ry + 17.5}" text-anchor="end" class="mb">9:41</text>
      {menu}
    </g>"""
    style = f"""
    .mi {{ font: 13px {SANS}; fill: #fff }}
    .mh {{ font: 600 13px {SANS}; fill: #fff }}
    .mm {{ font: 11.5px {SANS}; fill: {MUTED} }}
    .mb {{ font: 12px {SANS}; fill: #fff }}
    .hl {{ animation: hl 6s ease-in-out infinite }}
    @keyframes hl {{ 0%,20% {{ transform: translateY(0) }} 25%,45% {{ transform: translateY(26px) }} 50%,70% {{ transform: translateY(52px) }} 75%,95% {{ transform: translateY(78px) }} 100% {{ transform: translateY(0) }} }}"""
    defs = (f'<linearGradient id="wall" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{WALL_1}"/><stop offset="1" stop-color="{WALL_2}"/></linearGradient>'
            '<filter id="blur" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="35"/></filter>')
    body = f"<defs>{defs}</defs>{window(W, H, 'devsim.app')}{left}{right}"
    return svg_wrap(W, H, "devsim: macOS menu bar app. " + " ".join(desc), body, style, bottom=ROW_GAP)


def package_svg(name, kind, glyph, desc, tags, art, art_style, label):
    W, H = 412, 384   # two of these (with gutters) are exactly as wide as the featured card
    body = (window(W, H, "Package.swift")
            + f'<rect x="16" y="50" width="{W - 32}" height="132" rx="12" fill="#0C0E16"/>'
            + f'<rect x="16" y="50" width="{W - 32}" height="132" rx="12" fill="url(#dots)" stroke="{BORDER}"/>'
            + f'<g transform="translate({(W - 404) / 2} 0)">{art}</g>'
            + app_tile(24, 202, glyph, 44)
            + f'<text x="80" y="222" class="name" style="font-size:19px">{esc(name)}</text><text x="80" y="242" class="kind">{esc(kind)}</text>'
            + "".join(f'<text x="24" y="{284 + i * 23}" class="desc" style="font-size:14px">{esc(l)}</text>' for i, l in enumerate(desc))
            + tags_row(24, H - 52, tags)
            + f'<text x="{W - 24}" y="{H - 35}" text-anchor="end" class="go">View →</text>')
    return svg_wrap(W, H, label, body, art_style)


def doc(cx, cy, ext, extra=""):
    return (f'<g {extra}><path d="M{cx - 20} {cy - 26}h28l12 12v40a3 3 0 0 1-3 3h-34a3 3 0 0 1-3-3v-49a3 3 0 0 1 3-3z" fill="#1C1F2E" stroke="#fff" stroke-opacity=".22"/>'
            f'<path d="M{cx + 8} {cy - 26}v9a3 3 0 0 0 3 3h9" fill="none" stroke="#fff" stroke-opacity=".22"/>'
            f'<rect x="{cx - 17}" y="{cy + 6}" width="34" height="15" rx="4" fill="url(#g)"/>'
            f'<text x="{cx}" y="{cy + 17}" text-anchor="middle" class="ext">{ext}</text></g>')


def cloudconvert_svg():
    cy = 108
    art = f"""
    {doc(76, cy, "MOV")}
    <path class="flow" d="M110 {cy}H160" stroke="{A_SOFT}" stroke-width="2" stroke-dasharray="4 6" stroke-linecap="round"/>
    <circle class="ring" cx="202" cy="{cy}" r="38" fill="none" stroke="{A_SOFT}" stroke-opacity=".5"/>
    <circle cx="202" cy="{cy}" r="30" fill="url(#g)"/>
    <g transform="translate(180 {cy - 22})" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">{GLYPHS['cloud']}<path class="spin" d="M17 24.5a5 5 0 0 1 9-2.5m1 4.5a5 5 0 0 1-9 2.5"/></g>
    <path class="flow" d="M244 {cy}H294" stroke="{A_SOFT}" stroke-width="2" stroke-dasharray="4 6" stroke-linecap="round"/>
    {doc(328, cy, "MP4", 'class="out"')}
    <text x="76" y="{cy + 58}" text-anchor="middle" class="mono">stage</text>
    <text x="202" y="{cy + 58}" text-anchor="middle" class="mono">convert</text>
    <text x="328" y="{cy + 58}" text-anchor="middle" class="mono">save</text>"""
    style = f"""
    .ext {{ font: 700 9.5px {SANS}; fill: #fff; letter-spacing: .5px }}
    .flow {{ animation: flow 1s linear infinite }}
    @keyframes flow {{ to {{ stroke-dashoffset: -20 }} }}
    .ring {{ animation: ring 2.4s ease-out infinite; transform-box: fill-box; transform-origin: center }}
    @keyframes ring {{ from {{ transform: scale(.8); opacity: 1 }} to {{ transform: scale(1.25); opacity: 0 }} }}
    .out {{ animation: out 2.4s ease-in-out infinite }}
    @keyframes out {{ 0%,40% {{ opacity: .35 }} 60%,100% {{ opacity: 1 }} }}"""
    return package_svg("CloudConvertKit", "Swift package", "cloud",
                       ["The whole CloudConvert lifecycle, from staging", "the input to saving the output. Zero deps."],
                       ["SwiftPM", "async/await", "URLSession"], art, style,
                       "CloudConvertKit: the whole CloudConvert lifecycle, from staging the input to saving the output.")


def targzip_svg():
    cy = 116
    files = [("folder", "release/", 0), ("file", "README.md", 1), ("file", "Package.swift", 1), ("folder", "Sources/", 1), ("file", "LICENSE", 1)]
    rows = []
    for i, (kind, label, indent) in enumerate(files):
        x, y = 222 + indent * 16, 70 + i * 21
        if kind == "folder":
            ic = f'<path d="M{x} {y - 9}h5l2 2h7v8h-14z" fill="{A_SOFT}" fill-opacity=".85"/>'
        else:
            ic = f'<path d="M{x + 2} {y - 10}h7l3 3v9h-10z" fill="none" stroke="#fff" stroke-opacity=".55"/>'
        rows.append(f'<g class="row" style="animation-delay:{i * .25:.2f}s">{ic}<text x="{x + 20}" y="{y}" class="file">{label}</text></g>')
    art = f"""
    <rect class="glow" x="62" y="{cy - 34}" width="68" height="68" rx="18" fill="url(#g)" filter="url(#soft)" opacity=".7"/>
    <g class="pack"><rect x="62" y="{cy - 34}" width="68" height="68" rx="18" fill="url(#g)"/>
    <g transform="translate(74 {cy - 22}) scale(1)" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">{GLYPHS['box']}</g></g>
    <text x="96" y="{cy + 54}" text-anchor="middle" class="mono">release.tar.gz</text>
    <path class="flow" d="M148 {cy - 12}H196" stroke="{A_SOFT}" stroke-width="2" stroke-dasharray="4 6" stroke-linecap="round"/>
    <path d="M190 {cy - 17}l6 5-6 5" fill="none" stroke="{A_SOFT}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    <rect x="208" y="54" width="164" height="114" rx="8" fill="#151826" stroke="#fff" stroke-opacity=".08"/>
    {''.join(rows)}"""
    style = f"""
    .file {{ font: 12px {MONO}; fill: {BODY} }}
    .flow {{ animation: flow 1s linear infinite }}
    @keyframes flow {{ to {{ stroke-dashoffset: -20 }} }}
    .row {{ animation: row 5s ease-out infinite both }}
    @keyframes row {{ 0% {{ opacity: 0; transform: translateX(-6px) }} 10%,85% {{ opacity: 1; transform: none }} 95%,100% {{ opacity: 0 }} }}
    .pack {{ animation: pack 5s ease-in-out infinite; transform-box: fill-box; transform-origin: center }}
    @keyframes pack {{ 0%,100% {{ transform: scale(1) }} 6% {{ transform: scale(.92) }} 12% {{ transform: scale(1) }} }}"""
    return package_svg("NVHTarGzip-Swift", "Swift library", "box",
                       ["Handle .tar.gz and .tgz archives on", "iOS and macOS, in plain Swift."],
                       ["SwiftPM", "iOS", "macOS"], art, style,
                       "NVHTarGzip-Swift: handle .tar.gz and .tgz archives on iOS and macOS.")


PROJECT_CARDS = {
    "devsim": devsim_svg,
    "CloudConvertKit": cloudconvert_svg,
    "NVHTarGzip-Swift": targzip_svg,
}


# ---- Activity: an "Activity Monitor" window over the last year ---------------
HEAT = ["#1B1E2B", "#3B3A8F", "#5B54D6", "#8B5CF6", "#C4B5FD"]
LEVELS = ["NONE", "FIRST_QUARTILE", "SECOND_QUARTILE", "THIRD_QUARTILE", "FOURTH_QUARTILE"]
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()
QUERY = """query($login: String!) { user(login: $login) { contributionsCollection { contributionCalendar {
  totalContributions weeks { contributionDays { date contributionCount contributionLevel } } } } } }"""


def fetch_calendar():
    raw = subprocess.run(["gh", "api", "graphql", "-f", f"query={QUERY}", "-f", f"login={USER}"],
                         check=True, capture_output=True, text=True).stdout
    cal = json.loads(raw)["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    return cal["totalContributions"], [w["contributionDays"] for w in cal["weeks"]]


def streaks(days):
    longest = run = 0
    for d in days:
        run = run + 1 if d["contributionCount"] else 0
        longest = max(longest, run)
    # like GitHub, today not having a contribution yet doesn't break the current streak
    tail = days[:-1] if not days[-1]["contributionCount"] else days
    current = 0
    for d in reversed(tail):
        if not d["contributionCount"]:
            break
        current += 1
    return current, longest


def pretty(iso, year=True):
    d = date.fromisoformat(iso)
    return f"{MONTHS[d.month - 1]} {d.day}" + (f", {d.year}" if year else "")


def activity_svg(total, weeks):
    W, H = 840, 318
    CELL, STEP = 11, 14
    days = [d for w in weeks for d in w]
    best = max(days, key=lambda d: d["contributionCount"])
    active = sum(1 for d in days if d["contributionCount"])
    current, longest = streaks(days)

    grid_w = len(weeks) * STEP - (STEP - CELL)
    gx, gy = (W - (grid_w + 30)) / 2 + 30, 86

    months, last_month, last_x = [], None, -99
    cols = []
    for wi, week in enumerate(weeks):
        x = gx + wi * STEP
        m = date.fromisoformat(week[0]["date"]).month
        # label a month where it starts; the partial first column gets none, like GitHub
        if last_month is not None and m != last_month and x - last_x > 30:
            months.append(f'<text x="{x}" y="{gy - 10}" class="ax">{MONTHS[m - 1]}</text>')
            last_x = x
        last_month = m
        cells = []
        for d in week:
            row = (date.fromisoformat(d["date"]).weekday() + 1) % 7   # Sunday-first, like GitHub
            fill = HEAT[LEVELS.index(d["contributionLevel"])]
            cells.append(f'<rect x="{x}" y="{gy + row * STEP}" width="{CELL}" height="{CELL}" rx="2.5" fill="{fill}"/>')
            if d is best and best["contributionCount"]:
                cells.append(f'<rect class="ring" x="{x - 2.5}" y="{gy + row * STEP - 2.5}" width="{CELL + 5}" height="{CELL + 5}" rx="4" fill="none" stroke="{A_SOFT}" stroke-width="1.5"/>')
        cols.append(f'<g class="wk" style="animation-delay:{wi * .018:.3f}s">{"".join(cells)}</g>')

    day_labels = "".join(f'<text x="{gx - 8}" y="{gy + r * STEP + 9}" text-anchor="end" class="ax">{n}</text>'
                         for r, n in ((1, "Mon"), (3, "Wed"), (5, "Fri")))

    ly = gy + 7 * STEP + 12
    legend_x = gx + grid_w - len(HEAT) * STEP - 30
    legend = (f'<text x="{legend_x - 6}" y="{ly + 9}" text-anchor="end" class="ax">Less</text>'
              + "".join(f'<rect x="{legend_x + i * STEP}" y="{ly}" width="{CELL}" height="{CELL}" rx="2.5" fill="{c}"/>' for i, c in enumerate(HEAT))
              + f'<text x="{legend_x + len(HEAT) * STEP + 2}" y="{ly + 9}" class="ax">More</text>')
    best_note = ""
    if best["contributionCount"]:
        best_note = (f'<rect x="{gx}" y="{ly - 1}" width="{CELL + 2}" height="{CELL + 2}" rx="3.5" fill="none" stroke="{A_SOFT}" stroke-width="1.5"/>'
                     f'<text x="{gx + 20}" y="{ly + 9}" class="ax">Best day</text>')

    tiles_data = [
        ("CONTRIBUTIONS", str(total), "in the last year"),
        ("ACTIVE DAYS", str(active), f"of {len(days)} days"),
        ("BEST DAY", str(best["contributionCount"]), pretty(best["date"]) if best["contributionCount"] else "-"),
        ("LONGEST STREAK", str(longest), f"days · current {current}"),
    ]
    ty, th, pad, gap = ly + 30, 70, 24, 12
    tw = (W - 2 * pad - 3 * gap) / 4
    tiles = []
    for i, (label, value, sub) in enumerate(tiles_data):
        x = pad + i * (tw + gap)
        tiles.append(f'<rect x="{x}" y="{ty}" width="{tw}" height="{th}" rx="10" fill="#161927" stroke="{BORDER}"/>'
                     f'<text x="{x + 16}" y="{ty + 24}" class="tl">{label}</text>'
                     f'<text x="{x + 16}" y="{ty + 54}" class="tv">{value}</text>'
                     f'<text x="{x + 24 + len(value) * 15}" y="{ty + 54}" class="ts">{esc(sub)}</text>')

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{total} contributions in the last year across {active} active days. Best day: {best['contributionCount']}. Longest streak: {longest} days.">
  <style>
    .ttl {{ font: 600 13px {SANS}; fill: {TEXT} }}
    .sub {{ font: 12px {SANS}; fill: {MUTED} }}
    .ax {{ font: 10.5px {SANS}; fill: {MUTED} }}
    .tl {{ font: 600 10.5px {SANS}; fill: {MUTED}; letter-spacing: 1.1px }}
    .tv {{ font: 700 26px {SANS}; fill: {TEXT} }}
    .ts {{ font: 12px {SANS}; fill: {MUTED} }}
    .wk {{ animation: in .5s ease-out both }}
    @keyframes in {{ from {{ opacity: 0 }} to {{ opacity: 1 }} }}
    .ring {{ animation: pulse 2.4s ease-in-out infinite }}
    @keyframes pulse {{ 50% {{ opacity: .25 }} }}
  </style>
  <defs>
    <linearGradient id="edge" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{A1}" stop-opacity="0"/><stop offset=".5" stop-color="{A2}"/><stop offset="1" stop-color="{A1}" stop-opacity="0"/></linearGradient>
  </defs>
  <rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="14" fill="{CARD}" stroke="{BORDER}"/>
  <circle cx="20" cy="20" r="6" fill="#363B4D"/><circle cx="40" cy="20" r="6" fill="#363B4D"/><circle cx="60" cy="20" r="6" fill="#363B4D"/>
  <text x="84" y="25" class="ttl">Activity Monitor</text>
  <text x="{W - 20}" y="25" text-anchor="end" class="sub">@{USER} · last 12 months</text>
  <path d="M1 40.5H{W - 1}" stroke="{BORDER}"/>
  <path d="M120 40.5H{W - 120}" stroke="url(#edge)"/>
  {''.join(months)}
  {day_labels}
  {''.join(cols)}
  {best_note}
  {legend}
  {''.join(tiles)}
</svg>
"""


def build_activity():
    (ASSETS / "activity.svg").write_text(activity_svg(*fetch_calendar()))


def readme():
    header = (f"https://capsule-render.vercel.app/api?type=waving&color=0:{hexs(A1)},100:{hexs(A2)}&height=180&section=header"
              "&text=Zuraiz%20Ahmad&fontSize=48&fontColor=ffffff&animation=fadeIn&fontAlignY=36"
              "&desc=Software%20Engineer%20-%20iOS%20%26amp%3B%20macOS&descAlignY=58&descSize=18")
    footer = f"https://capsule-render.vercel.app/api?type=waving&color=0:{hexs(A2)},100:{hexs(A1)}&height=100&section=footer"
    typing = (f"https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=600&size=22&pause=1000&color={hexs(A_MID)}"
              "&center=true&vCenter=true&width=560&lines=Building+apps+for+iPhone%2C+iPad+%26+Mac;"
              "Swift+%E2%80%A2+SwiftUI+%E2%80%A2+UIKit+%E2%80%A2+AppKit;Writing+dependency-free+Swift+packages;"
              "Making+developer+tools+I+actually+use")
    # no whitespace between links: the gutters baked into each SVG are the only gaps
    link = lambda name, width: (f'<a href="https://github.com/{USER}/{name}"><img width="{width}" '
                                f'src="assets/project-{name.lower()}.svg" alt="{name}" /></a>')
    cards = link("devsim", "100%") + "<br/>" + link("CloudConvertKit", "50%") + link("NVHTarGzip-Swift", "50%")
    return f"""<div align="center">

<img src="{header}" width="100%" />

<a href="https://github.com/roxx990">
  <img src="{typing}" alt="Typing SVG" />
</a>

<br/>

<img src="https://komarev.com/ghpvc/?username=roxx990&style=flat-square&color={hexs(A_MID)}&label=Profile+views" alt="Profile views" />
<a href="https://github.com/CoderZone"><img src="https://img.shields.io/badge/Working%20at-CoderZone-{hexs(A_MID)}?style=flat-square&labelColor=555" alt="CoderZone" /></a>
<a href="https://www.linkedin.com/in/zuraiz-ahmad/"><img src="https://img.shields.io/badge/LinkedIn-zuraiz--ahmad-{hexs(A_MID)}?style=flat-square&labelColor=555&logo=linkedin&logoColor=white" alt="LinkedIn" /></a>

</div>

## About me

- I build native apps for **iPhone, iPad and Mac** at [@CoderZone](https://github.com/CoderZone)
- I turn everyday Xcode chores into small tools, like **devsim**
- I write Swift packages that stay **dependency-free** whenever they can
- Most at home in **SwiftUI**, dropping into UIKit and AppKit when it matters
- Some **Flutter & Dart** on the side

## Toolbox

<img src="assets/toolbox.svg" width="100%" alt="Toolbox. Languages: Swift, Dart. Frameworks: SwiftUI, UIKit, AppKit, Flutter. Tools: Xcode, SwiftPM, Git, GitHub." />

## Featured projects

<p align="center">{cards}</p>

## Activity

<img src="assets/activity.svg" width="100%" alt="Contribution activity over the last 12 months" />

<img src="{footer}" width="100%" />
"""


if __name__ == "__main__":
    ASSETS.mkdir(parents=True, exist_ok=True)
    build_activity()
    if sys.argv[1:] == ["activity"]:
        sys.exit()
    (ASSETS / "toolbox.svg").write_text(toolbox_svg())
    for name, make in PROJECT_CARDS.items():
        (ASSETS / f"project-{name.lower()}.svg").write_text(make())
    (OUT / "README.md").write_text(readme())
    print("built", sorted(x.name for x in ASSETS.iterdir()))
