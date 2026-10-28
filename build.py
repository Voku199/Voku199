"""Vygeneruje animovaná SVG (světlá + tmavá varianta) a README.md z data.py.

    python build.py            # spočítá kód v nadřazené složce (monorepu)
    python build.py --root X   # jiná složka ke spočítání

Když složka nic neobsahuje (např. na GitHubu), vezmou se čísla ze stats.json.
"""
import argparse
import json
import os
import textwrap
from datetime import date
from html import escape

import data

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")
STATS_FILE = os.path.join(HERE, "stats.json")

THEMES = {
    "dark": {"fg": "#e6edf3", "muted": "#8b949e", "faint": "#30363d", "card": "#161b22", "accent": "#ff5a36"},
    "light": {"fg": "#1f2328", "muted": "#59636e", "faint": "#d0d7de", "card": "#f6f8fa", "accent": "#e5482a"},
}
LANG_COLORS = {"Python": "#3572A5", "HTML": "#e34c26", "JavaScript": "#f1e05a", "CSS": "#663399",
               "Java": "#b07219", "TypeScript": "#3178c6", "Kotlin": "#A97BFF", "Shell": "#89e051"}

# ---------------------------------------------------------------- stats

CODE_EXT = {".py": "Python", ".js": "JavaScript", ".ts": "TypeScript", ".java": "Java", ".html": "HTML",
            ".css": "CSS", ".kt": "Kotlin", ".sh": "Shell"}
SKIP_DIRS = {"venv", ".venv", "env", "node_modules", ".git", "__pycache__", "site-packages", "Lib", "lib",
             "dist", "build", ".gradle", "graphify-out"}


def scan(root):
    """Neprázdné řádky kódu podle jazyka + počet projektů (složek s kódem)."""
    lines, projects = {}, 0
    me = os.path.basename(HERE)
    for top in sorted(os.listdir(root)):
        path = os.path.join(root, top)
        if not os.path.isdir(path) or top == me or "-src-" in top or top in data.EXCLUDE:
            continue
        found = False
        for cur, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS and "vendor" not in d]
            for f in files:
                lang = CODE_EXT.get(os.path.splitext(f)[1])
                p = os.path.join(cur, f)
                if not lang or f.endswith(".min.js") or os.path.getsize(p) > 400_000:
                    continue
                with open(p, encoding="utf-8", errors="ignore") as fh:
                    n = sum(1 for line in fh if line.strip())
                lines[lang] = lines.get(lang, 0) + n
                found = True
        projects += found
    return {"lines": lines, "projects": projects}


def load_stats(root):
    stats = scan(root) if root and os.path.isdir(root) else {"projects": 0}
    if stats["projects"]:
        with open(STATS_FILE, "w", encoding="utf-8") as fh:
            json.dump(stats, fh, indent=2)
        return stats
    with open(STATS_FILE, encoding="utf-8") as fh:
        return json.load(fh)


def round_down(n, step):
    return f"{n // step * step // 1000}k+" if n >= 1000 else str(n)

# ---------------------------------------------------------------- svg helpers


def svg(w, h, theme, css, body, title):
    t = THEMES[theme]
    base = f"""
    .sans{{font-family:'Segoe UI',-apple-system,BlinkMacSystemFont,'Helvetica Neue',Arial,sans-serif}}
    .mono{{font-family:'JetBrains Mono','Cascadia Code',Consolas,'SF Mono',Menlo,monospace}}
    .fg{{fill:{t['fg']}}} .muted{{fill:{t['muted']}}} .accent{{fill:{t['accent']}}}
    .up{{opacity:0;animation:up .8s cubic-bezier(.2,.7,.2,1) forwards}}
    @keyframes up{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:none}}}}
    .draw{{animation:draw 1.4s cubic-bezier(.6,0,.2,1) forwards}}
    @keyframes draw{{to{{stroke-dashoffset:0}}}}
    .pulse{{animation:pulse 2s ease-in-out infinite}}
    @keyframes pulse{{50%{{opacity:.25}}}}
    {css}
    @media (prefers-reduced-motion:reduce){{*{{animation:none!important}}.up{{opacity:1}}.draw{{stroke-dashoffset:0}}}}
    """
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'role="img"><title>{escape(title)}</title><style>{textwrap.dedent(base)}</style>{body}</svg>')


def delay(sec):
    return f'style="animation-delay:{sec:.2f}s"'


def hero(theme):
    t = THEMES[theme]
    n = len(data.ROTATING)
    slot = 100 / n
    css = (f".rot{{opacity:0;animation:rot {n * 3}s infinite}}"
           f"@keyframes rot{{0%{{opacity:0;transform:translateY(10px)}}"
           f"{slot * .12:.1f}%{{opacity:1;transform:none}}{slot * .88:.1f}%{{opacity:1;transform:none}}"
           f"{slot:.1f}%{{opacity:0;transform:translateY(-10px)}}100%{{opacity:0}}}}"
           "@media (prefers-reduced-motion:reduce){.rot0{opacity:1}}")
    words = "".join(
        f'<text class="sans rot rot{i}" x="0" y="214" font-size="26" style="animation-delay:{i * 3}s">'
        f'<tspan class="muted">I build </tspan><tspan class="fg" font-weight="600">{escape(w)}</tspan></text>'
        for i, w in enumerate(data.ROTATING))
    body = f"""
    <text class="mono muted up" x="0" y="36" font-size="14" letter-spacing="3">{escape(data.USER.upper())} · {escape(data.LOCATION.upper())}</text>
    <text class="sans fg up" x="-3" y="118" font-size="68" font-weight="700" letter-spacing="-1.5" {delay(.15)}>{escape(data.NAME)}</text>
    <line x1="0" y1="150" x2="1000" y2="150" stroke="{t['faint']}" stroke-width="1"/>
    <line class="draw" x1="0" y1="150" x2="1000" y2="150" stroke="{t['accent']}" stroke-width="2"
          stroke-dasharray="1000" stroke-dashoffset="1000" style="animation-delay:.3s"/>
    <circle cy="150" r="3.5" fill="{t['accent']}">
      <animate attributeName="cx" values="0;1000" dur="4s" begin="1.7s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.1;.9;1" dur="4s" begin="1.7s" repeatCount="indefinite"/>
    </circle>
    {words}
    <g class="up" {delay(.6)}>
      <circle class="pulse" cx="6" cy="255" r="5" fill="{t['accent']}"/>
      <text class="mono muted" x="22" y="260" font-size="15">now building: <tspan class="fg">{escape(data.NOW)}</tspan></text>
    </g>"""
    return svg(1000, 280, theme, css, body, f"{data.NAME}: I build {', '.join(data.ROTATING)}")


def stats_svg(theme, stats):
    t = THEMES[theme]
    lines = stats["lines"]
    total = sum(lines.values())
    langs = sorted(lines.items(), key=lambda kv: -kv[1])
    numbers = [(f"{stats['projects']}", "projects & experiments"),
               (round_down(total, 10_000), "lines of code"),
               (str(sum(1 for _, v in langs if v > 1000)), "languages I ship in")] + data.FACTS[:1]
    cols = ""
    for i, (big, small) in enumerate(numbers):
        x = i * 250
        cols += (f'<g class="up" {delay(.1 + i * .12)}>'
                 f'<text class="sans fg" x="{x}" y="52" font-size="44" font-weight="700" letter-spacing="-1">{escape(big)}</text>'
                 f'<text class="sans muted" x="{x}" y="80" font-size="15">{escape(small)}</text></g>')
    bar, legend, x = "", [], 0.0
    for lang, v in langs:
        w = 1000 * v / total
        bar += f'<rect x="{x:.1f}" y="112" width="{w:.1f}" height="8" fill="{LANG_COLORS.get(lang, t["muted"])}"/>'
        x += w
        if v / total >= .01:
            legend.append(f"{lang} {100 * v / total:.0f}%")
    body = f"""{cols}
    <clipPath id="reveal"><rect x="0" y="108" width="1000" height="16" rx="4">
      <animate attributeName="width" from="0" to="1000" dur="1.6s" begin="0s" fill="freeze" calcMode="spline" keySplines=".6 0 .2 1" keyTimes="0;1"/>
    </rect></clipPath>
    <rect x="0" y="112" width="1000" height="8" rx="4" fill="{t['faint']}"/>
    <g clip-path="url(#reveal)">{bar}</g>
    <text class="mono muted up" x="0" y="150" font-size="13" {delay(1.4)}>{escape('  ·  '.join(legend))}</text>"""
    alt = ", ".join(f"{b} {s}" for b, s in numbers)
    return svg(1000, 160, theme, "", body, alt)


def header(theme, num, title):
    t = THEMES[theme]
    start = 70 + len(title) * 12
    body = f"""
    <text class="mono accent" x="0" y="27" font-size="15">{num:02d}</text>
    <text class="sans fg" x="36" y="28" font-size="22" font-weight="600">{escape(title)}</text>
    <line class="draw" x1="{start}" y1="21" x2="1000" y2="21" stroke="{t['faint']}" stroke-width="1"
          stroke-dasharray="{1000 - start}" stroke-dashoffset="{1000 - start}"/>"""
    return svg(1000, 40, theme, "", body, title)


def card(theme, i, p):
    t = THEMES[theme]
    w, h = 490, 170
    desc = "".join(f'<text class="sans muted" x="28" y="{86 + k * 22}" font-size="15">{escape(line)}</text>'
                   for k, line in enumerate(textwrap.wrap(p["line"], 56)[:2]))
    tags, x = "", 28
    for tag in p["tags"]:
        tw = len(tag) * 7.6 + 20
        tags += (f'<rect x="{x}" y="128" width="{tw:.0f}" height="22" rx="11" fill="none" stroke="{t["faint"]}"/>'
                 f'<text class="mono muted" x="{x + tw / 2:.0f}" y="143" font-size="12" text-anchor="middle">{escape(tag)}</text>')
        x += tw + 8
    arrow = f'<text class="sans accent" x="{w - 28}" y="50" font-size="20" text-anchor="end">↗</text>' if p["link"] else ""
    css = f".sweep{{animation:sweep 7s linear infinite}}@keyframes sweep{{from{{transform:translateX(-120px)}}to{{transform:translateX({w + 20}px)}}}}"
    body = f"""
    <clipPath id="c"><rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="14"/></clipPath>
    <rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="14" fill="{t['card']}" stroke="{t['faint']}"/>
    <g clip-path="url(#c)"><rect class="sweep" x="0" y="0" width="100" height="2" fill="{t['accent']}" style="animation-delay:-{i * 1.3:.1f}s"/></g>
    <g class="up" {delay(.1 + i * .08)}>
      <text class="sans fg" x="28" y="50" font-size="22" font-weight="700">{escape(p['name'])}</text>{arrow}
      {desc}{tags}
    </g>"""
    return svg(w, h, theme, css, body, f"{p['name']}: {p['line']}")


def footer(theme):
    body = f"""<text class="mono muted" x="500" y="30" font-size="13" text-anchor="middle">built by build.py · updated {date.today().isoformat()}<tspan class="accent"> _<animate attributeName="fill-opacity" values="1;0;1" dur="1.1s" calcMode="discrete" repeatCount="indefinite"/></tspan></text>"""
    return svg(1000, 44, theme, "", body, "footer")

# ---------------------------------------------------------------- readme


def picture(name, alt, width="100%"):
    return (f'<picture><source media="(prefers-color-scheme: dark)" srcset="assets/{name}-dark.svg">'
            f'<img src="assets/{name}-light.svg" alt="{escape(alt)}" width="{width}"></picture>')


def write_asset(name, make):
    for theme in THEMES:
        with open(os.path.join(ASSETS, f"{name}-{theme}.svg"), "w", encoding="utf-8") as fh:
            fh.write(make(theme))


def build(root):
    os.makedirs(ASSETS, exist_ok=True)
    stats = load_stats(root)
    sections = ["selected projects", "what I've done", "elsewhere"]

    write_asset("hero", hero)
    write_asset("stats", lambda th: stats_svg(th, stats))
    write_asset("footer", footer)
    for n, title in enumerate(sections, 1):
        write_asset(f"h{n}", lambda th, n=n, title=title: header(th, n, title))
    for i, p in enumerate(data.PROJECTS):
        write_asset(f"card{i}", lambda th, i=i, p=p: card(th, i, p))

    cards = []
    for i, p in enumerate(data.PROJECTS):
        img = picture(f"card{i}", f"{p['name']}: {p['line']}", "49%")
        cards.append(f'<a href="{p["link"]}">{img}</a>' if p["link"] else img)
    links = " · ".join(f"[{label}]({url})" for label, url in data.LINKS)

    readme = f"""<div align="center">

{picture("hero", f"{data.NAME}: I build " + ", ".join(data.ROTATING))}

</div>

{data.ABOUT}

{links}

<br>

{picture("stats", "Stats from my monorepo")}

<br><br>

{picture("h1", sections[0])}

<div align="center">

{chr(10).join(cards)}

</div>

<br>

{picture("h2", sections[1])}

{chr(10).join("- " + a for a in data.ACHIEVEMENTS)}

<br>

{picture("h3", sections[2])}

Most of my projects live in a private monorepo. The finished, public ones are on my **[portfolio]({data.PORTFOLIO})**.

<br>

{picture("footer", "")}
"""
    with open(os.path.join(HERE, "README.md"), "w", encoding="utf-8") as fh:
        fh.write(readme)
    print(f"{stats['projects']} projects, {sum(stats['lines'].values())} lines -> README.md + {len(os.listdir(ASSETS))} svg")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=os.path.dirname(HERE))
    build(ap.parse_args().root)
