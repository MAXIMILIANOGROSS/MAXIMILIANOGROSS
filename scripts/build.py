#!/usr/bin/env python3
import re
"""Generates every SVG asset + README.md from data/*.json. No external services needed for assets."""
import json, math, pathlib, textwrap, datetime, random
from xml.sax.saxutils import escape as esc
ROOT = pathlib.Path(__file__).resolve().parent.parent
import sys; sys.path.insert(0, str(ROOT / "scripts")); import anim, i18n, i18n_art
P = json.loads((ROOT / "data/projects.json").read_text())
try: R = json.loads((ROOT / "data/repos.json").read_text())
except FileNotFoundError: R = {"generated": "", "public_repos": [], "languages": {}}
MONO = "'JetBrains Mono','SFMono-Regular',Menlo,Consolas,'DejaVu Sans Mono',monospace"
SANS = "'Segoe UI',Helvetica,Arial,sans-serif"
C = dict(bg="#070b12", panel="#0c1420", line="#1b2a3d", cyan="#00d4ff", vio="#7c3aed", green="#34d399", amber="#fbbf24", txt="#eaf6ff", mute="#8aa4bd")
STATUS_COLOR = {"PUBLISHED": C["green"], "FINISHED": C["green"], "BUILDING": C["cyan"], "IN TESTING": C["amber"], "OPEN SOURCE": C["vio"], "EXPERIMENT": C["vio"]}
DEFS = f'''<defs>
<linearGradient id="ac" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{C['cyan']}"/><stop offset="1" stop-color="{C['vio']}"/></linearGradient>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#070b12"/><stop offset=".55" stop-color="#0c1726"/><stop offset="1" stop-color="#070b12"/></linearGradient>
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="{C['line']}" stroke-width="1" opacity=".5"/></pattern>
</defs>'''
def svg(w, h, body, label):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{esc(label)}">{DEFS}{body}</svg>'
def write(rel, content):
    p = ROOT / rel; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(content, encoding="utf-8")
def hexpts(cx, cy, r): return " ".join(f"{cx + r*math.cos(math.radians(60*k-30)):.1f},{cy + r*math.sin(math.radians(60*k-30)):.1f}" for k in range(6))
def pill(x, y, t, c, h=30):
    w = int(len(t) * 9.4 + 40)
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h//2}" fill="{C["bg"]}" stroke="{c}" stroke-opacity=".65"/>'
            f'<circle cx="{x+16}" cy="{y+h//2}" r="4.5" fill="{c}"><animate attributeName="opacity" values="1;.3;1" dur="2s" repeatCount="indefinite"/></circle>'
            f'<text x="{x+30}" y="{y+h//2+5}" font-family="{MONO}" font-size="13" fill="#cfe6f7">{esc(t)}</text>'), w

# ---------- logo ----------
def logo(animated):
    rot = f'<animateTransform attributeName="transform" type="rotate" from="0 100 100" to="360 100 100" dur="40s" repeatCount="indefinite"/>' if animated else ""
    b = (f'<polygon points="{hexpts(100,100,86)}" fill="#0b1220" stroke="url(#ac)" stroke-width="4"/>'
         f'<polygon points="{hexpts(100,100,72)}" fill="none" stroke="{C["cyan"]}" stroke-opacity=".35" stroke-dasharray="6 8">{rot}</polygon>'
         f'<text x="100" y="118" text-anchor="middle" font-family="{SANS}" font-weight="800" font-size="58" fill="{C["txt"]}" letter-spacing="-2">M<tspan fill="{C["cyan"]}">O</tspan></text>'
         f'<text x="100" y="148" text-anchor="middle" font-family="{MONO}" font-size="12" fill="#65d9ff" letter-spacing="3">&lt;/BUILD&gt;</text>')
    return svg(200, 200, b, "MO monogram")

# ---------- hero ----------
LG = 'en'
def Xt(): return i18n_art.X[LG]
def hero():
    W, H = 1600, 540; random.seed(7); o = []
    cx, cy = 430, 270
    o.append(f'<defs><filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
             f'<radialGradient id="g1" cx="{cx/W:.3f}" cy=".5" r=".45"><stop offset="0" stop-color="{C["cyan"]}" stop-opacity=".30"/><stop offset="1" stop-color="{C["cyan"]}" stop-opacity="0"/></radialGradient>'
             f'<linearGradient id="sc" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C["cyan"]}" stop-opacity="0"/><stop offset="1" stop-color="{C["cyan"]}" stop-opacity=".18"/></linearGradient>'
             f'<linearGradient id="sw" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{C["cyan"]}" stop-opacity="0"/><stop offset="1" stop-color="{C["cyan"]}" stop-opacity=".55"/></linearGradient></defs>')
    o.append(f'<rect width="{W}" height="{H}" fill="url(#bg)"/><rect width="{W}" height="{H}" fill="url(#grid)"/><rect width="{W}" height="{H}" fill="url(#g1)"><animate attributeName="opacity" values=".7;1;.7" dur="5s" repeatCount="indefinite"/></rect>')
    # data rain
    for i in range(16):
        x = 30 + i * 52 + random.randint(-8, 8); n = 9
        ts = "".join(f'<tspan x="{x}" dy="19">{random.choice("01")}</tspan>' for _ in range(n))
        o.append(f'<g opacity="{random.choice([.10,.14,.18,.22])}"><text font-family="{MONO}" font-size="15" fill="{C["cyan"]}">{ts}<animateTransform attributeName="transform" type="translate" from="0 -200" to="0 {H}" dur="{7+i%5*2}s" begin="-{i*1.3:.1f}s" repeatCount="indefinite"/></text></g>')
    # background network (right side, faint)
    pts = [(random.randint(820, 1580), random.randint(30, 510)) for _ in range(30)]
    k = 0
    for i, (x, y) in enumerate(pts):
        for (x2, y2) in pts[i+1:]:
            if (x-x2)**2 + (y-y2)**2 < 160**2:
                o.append(f'<line x1="{x}" y1="{y}" x2="{x2}" y2="{y2}" stroke="{C["cyan"]}" stroke-opacity=".12"/>')
                if k < 18: o.append(f'<circle r="2.4" fill="#7cecff"><animateMotion path="M{x} {y} L{x2} {y2}" dur="{2+k%4}s" begin="{k*.4:.1f}s" repeatCount="indefinite"/></circle>'); k += 1
    for i, (x, y) in enumerate(pts):
        o.append(f'<circle cx="{x}" cy="{y}" r="2.6" fill="{C["cyan"]}"><animate attributeName="opacity" values=".2;1;.2" dur="{3+i%4}s" begin="{i*.3:.1f}s" repeatCount="indefinite"/></circle>')
    # scan line
    o.append(f'<rect x="0" y="-70" width="{W}" height="70" fill="url(#sc)"><animate attributeName="y" from="-70" to="{H}" dur="6s" repeatCount="indefinite"/></rect>')
    # central tech core
    def rot(r, dur, rev=False): return f'<animateTransform attributeName="transform" type="rotate" from="{360 if rev else 0} {cx} {cy}" to="{0 if rev else 360} {cx} {cy}" dur="{dur}s" repeatCount="indefinite"/>'
    o.append(f'<circle cx="{cx}" cy="{cy}" r="215" fill="none" stroke="{C["line"]}" stroke-width="2"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="200" fill="none" stroke="{C["cyan"]}" stroke-opacity=".5" stroke-width="2" stroke-dasharray="3 14">{rot(200, 60)}</circle>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="160" fill="none" stroke="url(#ac)" stroke-width="3" stroke-dasharray="90 40 20 40">{rot(160, 14, True)}</circle>')
    o.append(f'<polygon points="{hexpts(cx,cy,125)}" fill="none" stroke="{C["cyan"]}" stroke-opacity=".6" stroke-width="2" stroke-dasharray="10 10">{rot(125, 26)}</polygon>')
    o.append(f'<polygon points="{hexpts(cx,cy,92)}" fill="#0b1220" stroke="url(#ac)" stroke-width="4" filter="url(#glow)"><animate attributeName="stroke-opacity" values="1;.55;1" dur="2.4s" repeatCount="indefinite"/></polygon>')
    o.append(f'<text x="{cx}" y="{cy+16}" text-anchor="middle" font-family="{MONO}" font-weight="800" font-size="50" fill="{C["cyan"]}" filter="url(#glow)">&lt;/&gt;</text>')
    # radar sweep
    o.append(f'<g>{rot(0, 5)}<path d="M{cx} {cy} L{cx+200} {cy-34} A203 203 0 0 1 {cx+200} {cy+34} Z" fill="url(#sw)"/></g>')
    # orbiting nodes
    for j, (r, d, rev, col) in enumerate([(200, 18, False, "#7cecff"), (160, 11, True, C["green"]), (125, 8, False, "#a78bfa"), (200, 25, True, C["amber"]), (160, 15, False, "#7cecff")]):
        a = j * 72
        o.append(f'<g transform="rotate({a} {cx} {cy})"><g>{rot(r, d, rev)}<circle cx="{cx+r}" cy="{cy}" r="6" fill="{col}" filter="url(#glow)"/><circle cx="{cx+r}" cy="{cy}" r="12" fill="none" stroke="{col}" stroke-opacity=".5"><animate attributeName="r" values="7;16;7" dur="2.2s" begin="{j*.4}s" repeatCount="indefinite"/><animate attributeName="stroke-opacity" values=".7;0;.7" dur="2.2s" begin="{j*.4}s" repeatCount="indefinite"/></circle></g></g>')
    # labels around the core
    for t, a in [("iOS", -90), ("ANDROID", -18), ("macOS", 54), ("WINDOWS", 126), ("AI", 198)]:
        import math as _m
        lx = cx + 232 * _m.cos(_m.radians(a)); ly = cy + 232 * _m.sin(_m.radians(a)) + 4
        o.append(f'<text x="{lx:.0f}" y="{ly:.0f}" text-anchor="middle" font-family="{MONO}" font-size="13" fill="#65d9ff" letter-spacing="2">{t}<animate attributeName="opacity" values=".4;1;.4" dur="3.5s" begin="{a%7}s" repeatCount="indefinite"/></text>')
    # text block (right)
    x0 = 900
    o.append(f'<text x="{x0}" y="95" font-family="{MONO}" font-size="20" fill="{C["green"]}">{P["owner"].lower()}@lab:~$ <tspan fill="{C["mute"]}">whoami</tspan><tspan fill="{C["cyan"]}">█<animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></tspan></text>')
    o.append(f'<text x="{x0}" y="190" font-family="{SANS}" font-weight="800" font-size="86" fill="{C["txt"]}" letter-spacing="-1" filter="url(#glow)">MAXIMILIANO</text>')
    o.append(f'<text x="{x0}" y="278" font-family="{SANS}" font-weight="800" font-size="86" fill="url(#ac)" letter-spacing="-1">OLMOS</text>')
    o.append(f'<text x="{x0}" y="366" font-family="{SANS}" font-weight="800" font-size="86" fill="url(#ac)" letter-spacing="-1">SÁNCHEZ</text>')
    o.append(f'<rect x="{x0}" y="384" width="120" height="4" fill="{C["cyan"]}"><animate attributeName="width" values="40;420;40" dur="4s" repeatCount="indefinite"/></rect>')
    o.append(f'<text x="{x0+2}" y="424" font-family="{MONO}" font-size="{min(20, (600/len(Xt()["sub"]) - 3) / 0.62):.1f}" fill="#9fb6cc" letter-spacing="3" textLength="{min(len(Xt()["sub"]) * (0.62 * 20 + 3), 600):.0f}" lengthAdjust="spacingAndGlyphs">{esc(Xt()["sub"])}</text>')
    lines = Xt()["tags"]
    for i, t in enumerate(lines):
        op = "1" if i == 0 else "0"
        o.append(f'<text x="{x0+2}" y="458" font-family="{MONO}" font-size="22" fill="{C["cyan"]}" opacity="{op}">&gt; {esc(t)}<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;{i/3:.3f};{i/3+.03:.3f};{i/3+.30:.3f};{i/3+.33:.3f};1" dur="9s" repeatCount="indefinite"/></text>')
    x = x0 + 2
    for t, c in zip(Xt()["pills"], [C["cyan"], C["green"], "#a78bfa"]):
        s, w = pill(x, 482, t, c, 34); o.append(s); x += w + 14
    o.append(f'<rect width="{W}" height="6" fill="url(#ac)"/><rect y="{H-3}" width="{W}" height="3" fill="url(#ac)" opacity=".6"/>')
    o.append(f'<rect y="{H-3}" width="260" height="3" fill="#fff" opacity=".9"><animate attributeName="x" from="-260" to="{W}" dur="3.5s" repeatCount="indefinite"/></rect>')
    return svg(W, H, "".join(o), "Maximiliano Olmos Sánchez — Software Developer, Product Builder")

# ---------- section headers ----------
def section(num, title, right):
    W, H = 1200, 64
    b = (f'<rect width="{W}" height="{H}" rx="10" fill="{C["bg"]}"/><rect x="14" y="22" width="14" height="14" fill="{C["cyan"]}"/>'
         f'<text x="44" y="36" font-family="{MONO}" font-size="20" fill="{C["cyan"]}" letter-spacing="3">{num}</text>'
         f'<text x="96" y="36" font-family="{SANS}" font-weight="800" font-size="24" fill="{C["txt"]}" letter-spacing="2">{esc(title)}</text>'
         f'<text x="{W-16}" y="36" text-anchor="end" font-family="{MONO}" font-size="13" fill="{C["mute"]}" letter-spacing="2">{esc(right)}</text>'
         f'<line x1="14" y1="54" x2="{W-14}" y2="54" stroke="{C["line"]}" stroke-width="2"/><rect x="14" y="52" width="220" height="4" fill="url(#ac)"/><rect x="14" y="51" width="90" height="6" rx="3" fill="#7cecff" opacity=".95"><animate attributeName="x" from="14" to="{W-104}" dur="4s" repeatCount="indefinite"/></rect><rect x="14" y="22" width="14" height="14" fill="#00d4ff"><animate attributeName="opacity" values="1;.25;1" dur="1.6s" repeatCount="indefinite"/></rect>')
    return svg(W, H, b, f"{num} {title}")

# ---------- project cards ----------
def card(p):
    W, H = 600, 270; col = STATUS_COLOR.get(p["status"], C["cyan"])
    o = [f'<rect width="{W}" height="{H}" rx="14" fill="{C["panel"]}" stroke="{C["line"]}" stroke-width="2"/><rect width="{W}" height="{H}" rx="14" fill="url(#grid)" opacity=".6"/>',
         f'<rect x="0" y="0" width="7" height="{H}" rx="3" fill="{col}"/>']
    import base64
    ic = ROOT / f"assets/icons/{p['id']}.png"
    if ic.exists():
        uri = "data:image/png;base64," + base64.b64encode(ic.read_bytes()).decode()
        o.append(f'<clipPath id="ic"><rect x="26" y="28" width="70" height="70" rx="16"/></clipPath><image href="{uri}" x="26" y="28" width="70" height="70" clip-path="url(#ic)"/><rect x="26" y="28" width="70" height="70" rx="16" fill="none" stroke="{col}" stroke-opacity=".8" stroke-width="2"/>')
    else:
        o.append(f'<polygon points="{hexpts(60,62,32)}" fill="#0b1220" stroke="{col}" stroke-width="3"/><text x="60" y="71" text-anchor="middle" font-family="{SANS}" font-weight="800" font-size="24" fill="{C["txt"]}">{esc(p["name"][0])}</text>')
    nm = p["name"]; fs = 30 if len(nm) <= 16 else 21
    o.append(f'<text x="116" y="62" font-family="{SANS}" font-weight="800" font-size="{fs}" fill="{C["txt"]}">{esc(nm)}</text>')
    o.append(f'<text x="116" y="86" font-family="{MONO}" font-size="12" fill="{C["mute"]}" letter-spacing="2">{esc(p["category"])}</text>')
    s, w = pill(W - 24 - int(len(p["status"])*9.4+40), 22, p["status"], col, 26); o.append(s)
    for i, line in enumerate(textwrap.wrap(p["tagline"], 56)[:4]):
        o.append(f'<text x="32" y="{132+i*24}" font-family="{SANS}" font-size="16" fill="#c6d6e6">{esc(line)}</text>')
    x = 32
    for t in p["tech"]:
        w = int(len(t) * 8.2 + 22)
        o.append(f'<rect x="{x}" y="{H-62}" width="{w}" height="26" rx="6" fill="#0b1220" stroke="{C["line"]}"/><text x="{x+w/2}" y="{H-44}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="#9fd8ee">{esc(t)}</text>')
        x += w + 8
    o.append(f'<text x="32" y="{H-18}" font-family="{MONO}" font-size="12" fill="{C["mute"]}">{esc(p["access"])}</text>')
    o.append(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="none" stroke="{col}" stroke-width="3" stroke-dasharray="70 1700" pathLength="1770"><animate attributeName="stroke-dashoffset" from="0" to="-1770" dur="{5+len(p["id"])%4}s" repeatCount="indefinite"/></rect>')
    o.append(f'<rect x="8" y="-40" width="{W-16}" height="40" fill="{col}" opacity=".07"><animate attributeName="y" from="-40" to="{H}" dur="5s" repeatCount="indefinite"/></rect>')
    return svg(W, H, "".join(o), f'{p["name"]} — {p["status"]}')

# ---------- radar ----------
def radar():
    W, H = 1000, 560; cx, cy = 345, 280
    rings = [(k, Xt()["rings"][i], r, c) for i, (k, r, c) in enumerate([("building", 70, C["cyan"]), ("published", 135, C["green"]), ("open", 200, C["vio"]), ("next", 255, C["mute"])])]
    items = {k: [] for k, *_ in rings}
    for p in P["projects"]: items[p["ring"]].append(p["name"].split(" ·")[0])
    for p in P["radar_extra"]: items[p["ring"]].append(p["name"])
    o = [f'<rect width="{W}" height="{H}" rx="14" fill="{C["panel"]}" stroke="{C["line"]}" stroke-width="2"/><rect width="{W}" height="{H}" rx="14" fill="url(#grid)" opacity=".5"/>']
    for k, lab, r, c in rings: o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{c}" stroke-opacity=".35" stroke-dasharray="3 6"/>')
    o.append(f'<line x1="{cx-262}" y1="{cy}" x2="{cx+262}" y2="{cy}" stroke="{C["line"]}"/><line x1="{cx}" y1="{cy-262}" x2="{cx}" y2="{cy+262}" stroke="{C["line"]}"/>')
    o.append(f'<linearGradient id="sw" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{C["cyan"]}" stop-opacity="0"/><stop offset="1" stop-color="{C["cyan"]}" stop-opacity=".35"/></linearGradient>'
             f'<g><path d="M{cx} {cy} L{cx+255} {cy} A255 255 0 0 0 {cx+255*math.cos(math.radians(-35)):.1f} {cy+255*math.sin(math.radians(-35)):.1f} Z" fill="url(#sw)"/><animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="12s" repeatCount="indefinite"/></g>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="5" fill="{C["cyan"]}"/>')
    ang0 = {"building": -90, "published": -80, "open": -60, "next": -45}
    for k, lab, r, c in rings:
        n = len(items[k]); 
        for i, name in enumerate(items[k]):
            a = math.radians(ang0[k] + i * (360 / max(n, 1)))
            x, y = cx + r * math.cos(a), cy + r * math.sin(a)
            o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="{c}"><animate attributeName="opacity" values="1;.4;1" dur="{2+i%3}s" repeatCount="indefinite"/></circle>')
            anchor, dx = ("start", 12) if math.cos(a) >= -0.05 else ("end", -12)
            o.append(f'<text x="{x+dx:.1f}" y="{y+4:.1f}" text-anchor="{anchor}" font-family="{MONO}" font-size="11.5" fill="#cfe6f7">{esc(name)}</text>')
    lx = 690; o.append(f'<text x="{lx}" y="60" font-family="{MONO}" font-size="14" fill="{C["cyan"]}" letter-spacing="3">{esc(Xt()["r_title"])}</text>')
    for i, (k, lab, r, c) in enumerate(rings):
        y = 110 + i * 70
        o.append(f'<circle cx="{lx+8}" cy="{y}" r="7" fill="{c}"/><text x="{lx+28}" y="{y+5}" font-family="{SANS}" font-weight="700" font-size="17" fill="{C["txt"]}">{esc(lab)}</text><text x="{lx+28}" y="{y+26}" font-family="{MONO}" font-size="12" fill="{C["mute"]}">{len(items[k])} {Xt()["item"] if len(items[k])==1 else Xt()["items"]}</text>')
    o.append(f'<text x="{lx}" y="{H-70}" font-family="{MONO}" font-size="11.5" fill="{C["mute"]}">{esc(Xt()["r_s1"])}</text><text x="{lx}" y="{H-50}" font-family="{MONO}" font-size="11.5" fill="{C["mute"]}">{esc(Xt()["r_s2"])}</text>')
    return svg(W, H, "".join(o), "Project radar")

# ---------- terminal ----------
def terminal():
    pub = sum(1 for p in P["projects"] if p["ring"] == "published"); bld = sum(1 for p in P["projects"] if p["ring"] == "building") + sum(1 for p in P["radar_extra"] if p["ring"] == "building")
    npub = len(R["public_repos"]); upd = R.get("generated", "n/a")
    lines = [(C["green"], f"{P['owner'].lower()}@lab:~$ system.status"), (C["txt"], f"[OK]     {Xt()['t_pub']}: {pub}"),
             (C["txt"], f"[ACTIVE] {Xt()['t_dev']}: {bld}"), (C["txt"], f"[OK]     {Xt()['t_repos']}: {npub}"),
             (C["txt"], f"[OK]     {Xt()['t_plat']}: {Xt()['t_plat_v']}"),
             (C["mute"], f"# {Xt()['t_data']} {upd}"), (C["green"], f"{P['owner'].lower()}@lab:~$ ")]
    W, H = 1000, 64 + len(lines) * 30 + 24
    o = [f'<rect width="{W}" height="{H}" rx="12" fill="#05080e" stroke="{C["line"]}" stroke-width="2"/><rect width="{W}" height="38" rx="12" fill="#0c1420"/><rect y="26" width="{W}" height="12" fill="#0c1420"/>',
         '<circle cx="24" cy="19" r="6" fill="#ff5f56"/><circle cx="46" cy="19" r="6" fill="#ffbd2e"/><circle cx="68" cy="19" r="6" fill="#27c93f"/>',
         f'<text x="{W/2}" y="24" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{C["mute"]}">{esc(Xt()["t_title"])}</text>']
    for i, (c, t) in enumerate(lines):
        y = 74 + i * 30
        o.append(f'<text x="24" y="{y}" font-family="{MONO}" font-size="15" fill="{c}" xml:space="preserve">{esc(t)}<animate attributeName="opacity" from="0" to="1" begin="{i*.7:.1f}s" dur=".3s" fill="freeze"/></text>')
    o.append(f'<rect x="{24+len(lines[-1][1])*9}" y="{74+(len(lines)-1)*30-15}" width="9" height="18" fill="{C["cyan"]}"><animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></rect>')
    return svg(W, H, "".join(o), "System status terminal")

# ---------- stats (from real API data) ----------
def stats():
    W, H = 1000, 250; repos = R["public_repos"]; langs = R["languages"]; tot = sum(langs.values()) or 1
    rel = sum(1 for r in repos if r["release"])
    o = [f'<rect width="{W}" height="{H}" rx="14" fill="{C["panel"]}" stroke="{C["line"]}" stroke-width="2"/>']
    kp = list(zip(Xt()["s_keys"], [len(repos), rel, len(langs), len(P["projects"])]))
    for i, (k, v) in enumerate(kp):
        x = 40 + i * 235
        o.append(f'<text x="{x}" y="70" font-family="{SANS}" font-weight="800" font-size="44" fill="{C["cyan"]}">{v}</text><text x="{x}" y="96" font-family="{MONO}" font-size="12" fill="{C["mute"]}" letter-spacing="2">{k}</text>')
    x = 40; cols = [C["cyan"], C["green"], C["vio"], C["amber"], "#fb7185", "#60a5fa"]
    top = list(langs.items())[:6]
    for i, (k, v) in enumerate(top):
        w = max(6, (W - 80) * v / tot)
        o.append(f'<rect x="{x:.1f}" y="130" width="{w:.1f}" height="14" fill="{cols[i%6]}" rx="3"/>'); x += w
    for i, (k, v) in enumerate(top):
        o.append(f'<circle cx="{46+(i%3)*300}" cy="{176+(i//3)*28}" r="6" fill="{cols[i%6]}"/><text x="{60+(i%3)*300}" y="{181+(i//3)*28}" font-family="{MONO}" font-size="13" fill="#cfe6f7">{esc(k)} {100*v/tot:.1f}%</text>')
    o.append(f'<text x="40" y="{H-14}" font-family="{MONO}" font-size="11" fill="{C["mute"]}">{esc(Xt()["s_note"])} {esc(R.get("generated",""))}</text>')
    return svg(W, H, "".join(o), "Verified GitHub metrics")

def footer():
    W, H = 1600, 120
    b = (f'<rect width="{W}" height="{H}" fill="url(#bg)"/><rect width="{W}" height="{H}" fill="url(#grid)"/><rect width="{W}" height="4" fill="url(#ac)"/><rect y="0" width="260" height="4" fill="#7cecff"><animate attributeName="x" from="-260" to="{W}" dur="5s" repeatCount="indefinite"/></rect>'
         f'<text x="{W/2}" y="62" text-anchor="middle" font-family="{SANS}" font-weight="800" font-size="30" fill="url(#ac)" letter-spacing="8">THINK · BUILD · SHIP · EVOLVE</text>'
         f'<text x="{W/2}" y="92" text-anchor="middle" font-family="{MONO}" font-size="14" fill="{C["mute"]}" letter-spacing="3">MAXIMILIANO OLMOS SÁNCHEZ — INDEPENDENT SOFTWARE DEVELOPER</text>')
    return svg(W, H, b, "footer")

def repo_table():
    if not R["public_repos"]: return "_Repository data is generated by GitHub Actions._"
    rows = ["| Repository | What it is | Language | Latest release | Updated |", "|---|---|---|---|---|"]
    for r in R["public_repos"]:
        rel = f"[{r['release']['tag']}]({r['release']['url']})" if r["release"] else "—"
        rows.append(f"| [`{r['name']}`]({r['url']}) | {r['description'] or '—'} | {r['language'] or '—'} | {rel} | {r['pushed_at'][:10]} |")
    return "\n".join(rows)


def career(lg):
    import textwrap as tw
    title, roles, lines = i18n.CAREER[lg]
    W, H = 1200, 330
    def wr(t, n):
        if " " not in t.strip() and any("\u4e00" <= c <= "\u9fff" for c in t): return [t[i:i+n//2] for i in range(0, len(t), n//2)]
        return tw.wrap(t, n)
    cards = [("SR TECHNICS · ZÜRICH", ["PT", "MT", "VT"], C["cyan"]), ("PLD SPACE", ["RT", "NDT"], "#a78bfa"), ("BUREAU VERITAS", ["ISO 9001", "QA"], C["green"]), ({"en":"NOW","es":"AHORA","de":"HEUTE","it":"OGGI","fr":"AUJOURD'HUI","zh":"现在","ar":"الآن"}[lg], ["iOS", "macOS", "AI"], C["amber"])]
    o = [f'<defs><filter id="cg" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>',
         f'<rect width="{W}" height="{H}" rx="14" fill="{C["panel"]}" stroke="{C["line"]}" stroke-width="2"/><rect width="{W}" height="{H}" rx="14" fill="url(#grid)" opacity=".55"/>',
         f'<text x="30" y="40" font-family="{MONO}" font-size="15" fill="{C["cyan"]}" letter-spacing="4">{esc(title)}</text>',
         f'<rect x="30" y="52" width="140" height="3" fill="url(#ac)"><animate attributeName="width" values="60;420;60" dur="5s" repeatCount="indefinite"/></rect>']
    cw, gap = 262, 40
    for i, ((org, chips, col), role, line) in enumerate(zip(cards, roles, lines)):
        x = 30 + i * (cw + gap); y = 76
        o.append(f'<rect x="{x}" y="{y}" width="{cw}" height="226" rx="14" fill="#0b1220" stroke="{col}" stroke-opacity="{".95" if i == 3 else ".55"}" stroke-width="2"{" stroke-dasharray=" + chr(34) + "10 6" + chr(34) if i == 3 else ""}>' + (f'<animate attributeName="stroke-dashoffset" from="0" to="-32" dur="1.6s" repeatCount="indefinite"/>' if i == 3 else "") + '</rect>')
        o.append(f'<rect x="{x}" y="{y}" width="{cw}" height="5" rx="2" fill="{col}"/>')
        o.append(f'<g transform="translate({x+cw-34} {y+34})"><polygon points="{hexpts(0,0,17)}" fill="none" stroke="{col}" stroke-width="2"><animateTransform attributeName="transform" type="rotate" from="0" to="{360 if i%2==0 else -360}" dur="{12+i*3}s" repeatCount="indefinite"/></polygon><circle r="4" fill="{col}" filter="url(#cg)"><animate attributeName="opacity" values="1;.3;1" dur="{2+i*.4:.1f}s" repeatCount="indefinite"/></circle></g>')
        o.append(f'<text x="{x+18}" y="{y+36}" font-family="{MONO}" font-size="11.5" fill="{col}" letter-spacing="2">{esc(org)}</text>')
        for k, ln in enumerate(wr(role, 21)[:3]): o.append(f'<text x="{x+18}" y="{y+68+k*24}" font-family="{SANS}" font-weight="800" font-size="19" fill="{C["txt"]}">{esc(ln)}</text>')
        cx_ = x + 18
        for ch in chips:
            w = int(len(ch) * 9 + 22)
            o.append(f'<rect x="{cx_}" y="{y+134}" width="{w}" height="24" rx="12" fill="{col}" fill-opacity=".12" stroke="{col}"><animate attributeName="fill-opacity" values=".1;.3;.1" dur="{2.4+i*.3:.1f}s" begin="{cx_%5*.2:.1f}s" repeatCount="indefinite"/></rect><text x="{cx_+w/2}" y="{y+151}" text-anchor="middle" font-family="{MONO}" font-size="12" font-weight="700" fill="#e6f6ff">{esc(ch)}</text>')
            cx_ += w + 8
        for k, ln in enumerate(wr(line, 30)[:3]): o.append(f'<text x="{x+18}" y="{y+184+k*19}" font-family="{SANS}" font-size="13.5" fill="#9fb6cc">{esc(ln)}</text>')
        if i < 3:
            ax = x + cw + 6
            o.append(f'<line x1="{ax}" y1="{y+113}" x2="{ax+gap-12}" y2="{y+113}" stroke="{C["line"]}" stroke-width="3"/><path d="M{ax+gap-22} {y+105} l10 8 l-10 8" fill="none" stroke="{C["cyan"]}" stroke-width="3"><animate attributeName="opacity" values=".2;1;.2" dur="1.4s" begin="{i*.4}s" repeatCount="indefinite"/></path><circle r="3.5" fill="#7cecff" filter="url(#cg)"><animateMotion path="M{ax} {y+113} L{ax+gap-12} {y+113}" dur="1.4s" begin="{i*.4}s" repeatCount="indefinite"/></circle>')
    o.append(f'<rect x="0" y="{H-4}" width="{W}" height="4" fill="url(#ac)" opacity=".5"/><rect y="{H-4}" width="240" height="4" fill="#fff" opacity=".85"><animate attributeName="x" from="-240" to="{W}" dur="4s" repeatCount="indefinite"/></rect>')
    return svg(W, H, "".join(o), title)
def pulse():
    W, H = 1200, 40
    d = "M0 20 H300 l10 -14 l12 28 l10 -24 l8 10 H700 l10 -14 l12 28 l10 -24 l8 10 H1200"
    b = (f'<path d="{d}" fill="none" stroke="{C["line"]}" stroke-width="2"/>'
         f'<path d="{d}" fill="none" stroke="{C["cyan"]}" stroke-width="3" stroke-dasharray="120 1400" stroke-linecap="round"><animate attributeName="stroke-dashoffset" from="1520" to="0" dur="4s" repeatCount="indefinite"/></path>'
         f'<circle r="5" fill="#7cecff"><animateMotion path="{d}" dur="4s" repeatCount="indefinite"/></circle>')
    return svg(W, H, b, "pulse divider")
def main():
    from urllib.parse import quote
    write("assets/branding/logo.svg", logo(False)); write("assets/branding/logo-animated.svg", logo(True))
    write("assets/branding/footer.svg", footer())
    order = [("01", "about"), ("02", "products"), ("03", "radar"), ("04", "building"), ("05", "pipeline"), ("06", "stack"), ("07", "metrics"), ("08", "lab"), ("09", "connect")]
    for lg, _, _ in i18n.LANGS:
        for n, k in order:
            t, r = i18n.SEC[k][lg]
            write(("assets/sections/" if lg == "en" else f"assets/sections/{lg}/") + f"{k}.svg", section(n, t, r))
    base_p = [dict(p) for p in P["projects"]]
    for lg, _, _ in i18n.LANGS:
        for p in base_p:
            q = dict(p)
            if lg != "en" and p["id"] in i18n.PROJ: q["tagline"], q["access"] = i18n.PROJ[p["id"]][lg]
            write(("assets/projects/" if lg == "en" else f"assets/projects/{lg}/") + f"{p['id']}.svg", card(q))
        write("assets/generated/pulse.svg", pulse())
    global LG
    HERO, ORB, CAR = {}, {}, {}
    for lg, _, _ in i18n.LANGS:
        LG = lg; bd = "assets/branding/" + ("" if lg == "en" else lg + "/"); gd = "assets/generated/" + ("" if lg == "en" else lg + "/")
        import hashlib, glob
        def hashed(d, base, content):
            for f in glob.glob(str(ROOT / d / (base + "*.svg"))): pathlib.Path(f).unlink()
            name = f"{base}-{hashlib.md5(content.encode()).hexdigest()[:8]}.svg"; write(d + name, content); return d + name
        HERO[lg] = hashed(bd, "hero", hero())
        CAR[lg] = hashed(gd, "career", career(lg))
        npub = sum(1 for q in P['projects'] if q['ring'] == 'published')
        write(gd + "ticker.svg", anim.ticker([t.format(n=npub) for t in Xt()["ticker"]]))
        ORB[lg] = hashed(gd, "orbit", anim.orbit(Xt()["o_sub"], Xt()["o_cap"]))
        write(gd + "pipeline.svg", anim.pipeline(Xt()["p_subs"]))
        write(gd + "radar.svg", radar()); write(gd + "terminal.svg", terminal()); write(gd + "stats.svg", stats())
    snake = ""
    if (ROOT / "assets/generated/snake.svg").exists() and (ROOT / "assets/generated/snake-dark.svg").exists():
        snake = '<picture><source media="(prefers-color-scheme: dark)" srcset="assets/generated/snake-dark.svg"><img alt="Contribution snake" src="assets/generated/snake.svg" width="100%"></picture>'
    tpl0 = (ROOT / "templates/README.tpl.md").read_text(encoding="utf-8")
    for lg, short, fname in i18n.LANGS:
        T = i18n.T[lg]; pd = "" if lg == "en" else lg + "/"
        cards = [P["projects"][i:i+2] for i in range(0, len(P["projects"]), 2)]
        def cell(p):
            link = (f'<a href="{p["url"]}"><b>{T["open"].format(p["name"].split(" ·")[0].title())}</b></a>') if p["url"] else f'<sub>{T["private"]}</sub>'
            return f'<td width="50%" valign="top"><img src="assets/projects/{pd}{p["id"]}.svg" alt="{esc(p["name"])} — {p["status"]}" width="100%"><br>{link}</td>\n'
        grid = "<table>\n" + "".join("<tr>\n" + "".join(cell(p) for p in row) + "</tr>\n" for row in cards) + "</table>"
        lab = "\n".join(f"| **{l['name']}** | `{l['status']}` | {i18n.LABT.get(l['name'], {}).get(lg, l['text'])} | [{T['site'] if l.get('url') else T['repo']}]({l.get('url') or 'https://github.com/' + P['owner'] + '/' + l['repo']}) |" for l in P["lab"])
        navk = [("about", "n_about", "161B22", "githubsponsors", "00D4FF"), ("products", "n_products", "00D4FF", "github", "black"), ("radar", "n_radar", "161B22", "target", "00D4FF"), ("building", "n_building", "161B22", "rocket", "00D4FF"), ("metrics", "n_metrics", "161B22", "graphql", "00D4FF"), ("connect", "n_connect", "161B22", "linkedin", "00D4FF")]
        nav = "\n".join(f'<a href="#{a}"><img src="https://img.shields.io/badge/{quote(T[k].replace("-", "--").replace("_", "__"))}-{bg}?style=for-the-badge&logo={lo}&logoColor={lc}" alt="{T[k]}"></a>' for a, k, bg, lo, lc in navk)
        bar = ["<p>🌐"]
        for l2, sh, f2 in i18n.LANGS:
            nm = i18n.NAMES[l2]; col = "00D4FF" if l2 == lg else "161B22"; fc = "black" if l2 == lg else "00D4FF"
            bar.append(f'<a href="{f2}"><img src="https://img.shields.io/badge/{quote(nm)}-{col}?style=flat-square&labelColor=0D1117&logoColor={fc}" alt="{nm}"></a>')
        bar.append("</p>")
        rtl = lg == "ar"
        out = tpl0
        for k, v in {"{{LANGBAR}}": " ".join(bar), "{{NAV}}": nav, "{{DIR_OPEN}}": '<div dir="rtl">' if rtl else "", "{{DIR_CLOSE}}": "</div>" if rtl else "", "{{SD}}": "" if lg == "en" else lg + "/", "{{HERO}}": HERO[lg], "{{CAREER}}": CAR[lg], "{{ORBIT}}": ORB[lg], "{{BD}}": "assets/branding/" + ("" if lg == "en" else lg + "/"), "{{GD}}": "assets/generated/" + ("" if lg == "en" else lg + "/"),
                     "{{GRID}}": grid, "{{LAB}}": lab, "{{REPOS}}": repo_table(), "{{SNAKE}}": snake, "{{UPDATED}}": R.get("generated", "pending first workflow run"), "{{OWNER}}": P["owner"],
                     "{{LINKEDIN}}": P["contact"]["linkedin"], "{{SITE}}": P["contact"]["site"]}.items(): out = out.replace(k, v)
        out = re.sub(r"\{\{t\.(\w+)\}\}", lambda m: T[m.group(1)], out)
        write(fname, out)
    print("built", len(i18n.LANGS), "languages")
main()
