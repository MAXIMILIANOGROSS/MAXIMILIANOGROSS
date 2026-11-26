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
import json as _json, datetime as _dt
METRICS = _json.loads((ROOT / "data/metrics.json").read_text(encoding="utf-8"))

def svg(w, h, body, label):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{esc(label)}">{DEFS}{body}</svg>'
def write(rel, content):
    if "/ar/" in rel and rel.endswith(".svg"): content = re.sub(r' letter-spacing="[^"]*"', '', content)
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
    o.append(f'<text x="116" y="86" font-family="{MONO}" font-size="12" fill="{C["mute"]}" letter-spacing="2">{esc(i18n.CAT.get(p["category"],{}).get(LG,p["category"]))}</text>')
    _st = i18n.ST.get(p["status"],{}).get(LG,p["status"]); s, w = pill(W - 24 - int(len(_st)*9.4+40), 22, _st, col, 26); o.append(s)
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
    W, H = 1200, 640; cx, cy = 368, 322; DUR = 10
    X_ = Xt()
    rings = [(k, X_["rings"][i], r, c) for i, (k, r, c) in enumerate([("building", 82, C["cyan"]), ("published", 150, C["green"]), ("open", 218, C["vio"]), ("next", 282, C["mute"])])]
    items = {k: [] for k, *_ in rings}
    for p in P["projects"]: items[p["ring"]].append(p["name"].split(" ·")[0])
    for p in P["radar_extra"]: items[p["ring"]].append(p["name"])
    total = sum(len(v) for v in items.values()) or 1
    o = [f'<defs><clipPath id="rc"><rect width="{W}" height="{H}" rx="14"/></clipPath><filter id="rg" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
         f'<radialGradient id="rbg" cx="{cx/W:.3f}" cy="{cy/H:.3f}" r=".5"><stop offset="0" stop-color="#0d2236"/><stop offset="1" stop-color="{C["panel"]}"/></radialGradient>'
         f'<linearGradient id="sw" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{C["cyan"]}" stop-opacity="0"/><stop offset="1" stop-color="{C["cyan"]}" stop-opacity=".45"/></linearGradient></defs><g clip-path="url(#rc)">',
         f'<rect width="{W}" height="{H}" fill="url(#rbg)"/><rect width="{W}" height="{H}" fill="url(#grid)" opacity=".5"/>']
    # outer tick ring (rotating slowly)
    R0 = 305
    ticks = "".join(f'<line x1="{cx+R0*math.cos(math.radians(a)):.1f}" y1="{cy+R0*math.sin(math.radians(a)):.1f}" x2="{cx+(R0+(12 if a%30==0 else 6))*math.cos(math.radians(a)):.1f}" y2="{cy+(R0+(12 if a%30==0 else 6))*math.sin(math.radians(a)):.1f}" stroke="{C["cyan"]}" stroke-opacity="{.8 if a%30==0 else .35}"/>' for a in range(0, 360, 5))
    o.append(f'<g>{ticks}<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="-360 {cx} {cy}" dur="90s" repeatCount="indefinite"/></g>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{R0}" fill="none" stroke="{C["cyan"]}" stroke-opacity=".25"/>')
    for k, lab, r, c in rings:
        o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{c}" fill-opacity=".035" stroke="{c}" stroke-opacity=".55" stroke-dasharray="2 7"/>')
    o.append(f'<line x1="{cx-R0}" y1="{cy}" x2="{cx+R0}" y2="{cy}" stroke="{C["line"]}"/><line x1="{cx}" y1="{cy-R0}" x2="{cx}" y2="{cy+R0}" stroke="{C["line"]}"/>')
    for d in (45, 135):
        a = math.radians(d); o.append(f'<line x1="{cx-R0*math.cos(a):.1f}" y1="{cy-R0*math.sin(a):.1f}" x2="{cx+R0*math.cos(a):.1f}" y2="{cy+R0*math.sin(a):.1f}" stroke="{C["line"]}" stroke-opacity=".5" stroke-dasharray="2 8"/>')
    # sweep (wedge + leading beam)
    sw = 290; a2 = math.radians(-50)
    o.append(f'<g><path d="M{cx} {cy} L{cx+sw} {cy} A{sw} {sw} 0 0 0 {cx+sw*math.cos(a2):.1f} {cy+sw*math.sin(a2):.1f} Z" fill="url(#sw)"/><line x1="{cx}" y1="{cy}" x2="{cx+sw}" y2="{cy}" stroke="#7cecff" stroke-width="2" filter="url(#rg)"/><animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="{DUR}s" repeatCount="indefinite"/></g>')
    ang0 = {"building": -100, "published": -72, "open": -35, "next": -20}
    blips = []
    for k, lab, r, c in rings:
        n = len(items[k])
        for i, name in enumerate(items[k]):
            deg = ang0[k] + i * (360 / max(n, 1)); a = math.radians(deg)
            x, y = cx + r * math.cos(a), cy + r * math.sin(a)
            t = ((deg % 360) / 360) * DUR
            o.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="{c}" stroke-opacity=".10"/>')
            o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="none" stroke="{c}" stroke-width="2" opacity="0"><animate attributeName="r" values="7;26" dur="{DUR}s" begin="{t:.2f}s" repeatCount="indefinite" keyTimes="0;1" calcMode="linear"/><animate attributeName="opacity" values="0.9;0;0" keyTimes="0;.18;1" dur="{DUR}s" begin="{t:.2f}s" repeatCount="indefinite"/></circle>')
            o.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6.5" fill="{c}" filter="url(#rg)"><animate attributeName="opacity" values="1;.55;1" dur="{2+i%3}s" repeatCount="indefinite"/></circle><circle cx="{x:.1f}" cy="{y:.1f}" r="2.5" fill="#fff"/>')
            w = int(len(name) * 6.9 + 16); right = math.cos(a) >= -0.05
            bx = x + 13 if right else x - 13 - w
            blips.append(f'<g><rect x="{bx:.1f}" y="{y-10:.1f}" width="{w}" height="20" rx="6" fill="#07111d" fill-opacity=".92" stroke="{c}" stroke-opacity=".55"/><text x="{bx+w/2:.1f}" y="{y+4:.1f}" text-anchor="middle" font-family="{MONO}" font-size="11" font-weight="700" fill="#e6f6ff">{esc(name)}</text></g>')
    o += blips
    o.append(f'<circle cx="{cx}" cy="{cy}" r="9" fill="{C["cyan"]}" filter="url(#rg)"/><circle cx="{cx}" cy="{cy}" r="16" fill="none" stroke="{C["cyan"]}" stroke-opacity=".6"><animate attributeName="r" values="9;30;9" dur="3s" repeatCount="indefinite"/><animate attributeName="opacity" values=".7;0;.7" dur="3s" repeatCount="indefinite"/></circle>')
    # HUD brackets
    for bx, by, sx_, sy_ in ((14, 14, 1, 1), (W-14, 14, -1, 1), (14, H-14, 1, -1), (W-14, H-14, -1, -1)):
        o.append(f'<path d="M{bx} {by+sy_*26} L{bx} {by} L{bx+sx_*26} {by}" fill="none" stroke="{C["cyan"]}" stroke-width="2.5" opacity=".8"/>')
    # right dashboard
    lx = 735
    o.append(f'<line x1="{lx-34}" y1="40" x2="{lx-34}" y2="{H-40}" stroke="{C["line"]}"/>')
    o.append(f'<text x="{lx}" y="62" font-family="{MONO}" font-size="15" fill="{C["cyan"]}" letter-spacing="4">{esc(X_["r_title"])}</text><circle cx="{W-52}" cy="57" r="5" fill="{C["green"]}" filter="url(#rg)"><animate attributeName="opacity" values="1;.2;1" dur="1.4s" repeatCount="indefinite"/></circle><text x="{W-62}" y="62" text-anchor="end" font-family="{MONO}" font-size="11" fill="{C["green"]}" letter-spacing="3">LIVE</text>')
    o.append(f'<text x="{lx}" y="118" font-family="{SANS}" font-weight="800" font-size="54" fill="{C["txt"]}">{total}</text><text x="{lx+92}" y="118" font-family="{MONO}" font-size="12" fill="{C["mute"]}" letter-spacing="3">{esc(X_["items"]).upper()}</text>')
    bw = 380
    for i, (k, lab, r, c) in enumerate(rings):
        y = 168 + i * 88; n = len(items[k]); pct = round(100 * n / total)
        o.append(f'<rect x="{lx}" y="{y-24}" width="{bw+40}" height="72" rx="12" fill="#0b1220" stroke="{c}" stroke-opacity=".45"/><rect x="{lx}" y="{y-24}" width="5" height="72" rx="2" fill="{c}"/>')
        o.append(f'<circle cx="{lx+26}" cy="{y}" r="7" fill="{c}" filter="url(#rg)"/><text x="{lx+44}" y="{y+5}" font-family="{SANS}" font-weight="800" font-size="17" fill="{C["txt"]}">{esc(lab)}</text>')
        o.append(f'<text x="{lx+bw+22}" y="{y+5}" text-anchor="end" font-family="{MONO}" font-weight="700" font-size="16" fill="{c}">{n} · {pct}%</text>')
        o.append(f'<rect x="{lx+26}" y="{y+20}" width="{bw-10}" height="8" rx="4" fill="{C["line"]}"/><rect x="{lx+26}" y="{y+20}" width="0" height="8" rx="4" fill="{c}" filter="url(#rg)"><animate attributeName="width" from="0" to="{(bw-10)*n/total:.0f}" dur="1.4s" begin="{i*.2:.1f}s" fill="freeze"/></rect>')
    o.append(f'<text x="{lx}" y="{H-54}" font-family="{MONO}" font-size="11.5" fill="{C["mute"]}">{esc(X_["r_s1"])}</text><text x="{lx}" y="{H-36}" font-family="{MONO}" font-size="11.5" fill="{C["mute"]}">{esc(X_["r_s2"])}</text>')
    o.append(f'<rect y="{H-5}" width="{W}" height="5" fill="url(#ac)" opacity=".55"/><rect y="{H-5}" width="260" height="5" fill="#fff" opacity=".85"><animate attributeName="x" from="-260" to="{W}" dur="4s" repeatCount="indefinite"/></rect></g><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="none" stroke="{C["line"]}" stroke-width="2"/>')
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

def footer(lg="en"):
    W, H = 1600, 120; ft = i18n.FT[lg]
    b = (f'<rect width="{W}" height="{H}" fill="url(#bg)"/><rect width="{W}" height="{H}" fill="url(#grid)"/><rect width="{W}" height="4" fill="url(#ac)"/><rect y="0" width="260" height="4" fill="#7cecff"><animate attributeName="x" from="-260" to="{W}" dur="5s" repeatCount="indefinite"/></rect>'
         f'<text x="{W/2}" y="62" text-anchor="middle" font-family="{SANS}" font-weight="800" font-size="30" fill="url(#ac)" letter-spacing="{8 if lg in ("en","es","it","fr","de") and len(ft[0])<36 else 4}" textLength="{min(1200, max(520, len(ft[0])*22))}" lengthAdjust="spacingAndGlyphs">{esc(ft[0])}</text>'
         f'<text x="{W/2}" y="92" text-anchor="middle" font-family="{MONO}" font-size="14" fill="{C["mute"]}" letter-spacing="3">MAXIMILIANO OLMOS SÁNCHEZ — {esc(ft[1])}</text>')
    return svg(W, H, b, "footer")

def repo_table():
    if not R["public_repos"]: return "_Repository data is generated by GitHub Actions._"
    rows = ["| Repository | What it is | Language | Latest release | Updated |", "|---|---|---|---|---|"]
    for r in R["public_repos"]:
        rel = f"[{r['release']['tag']}]({r['release']['url']})" if r["release"] else "—"
        rows.append(f"| [`{r['name']}`]({r['url']}) | {r['description'] or '—'} | {r['language'] or '—'} | {rel} | {r['pushed_at'][:10]} |")
    return "\n".join(rows)


def career(lg):
    import textwrap as tw, base64, io
    title, roles, lines = i18n.CAREER[lg]
    W, H = 1200, 476
    def wr(t, n):
        if " " not in t.strip() and any("一" <= c <= "鿿" for c in t): return [t[i:i+n//2] for i in range(0, len(t), n//2)]
        return tw.wrap(t, n)
    def thumb(name, w=420):
        f = ROOT / "assets/screenshots" / name
        if not f.exists(): return None
        try:
            from PIL import Image
            im = Image.open(f).convert("RGB"); im.thumbnail((w, 700)); b = io.BytesIO(); im.save(b, "JPEG", quality=72); data = b.getvalue()
        except Exception: data = f.read_bytes()
        return "data:image/jpeg;base64," + base64.b64encode(data).decode()
    cards = [("SR TECHNICS · ZÜRICH", ["PT", "MT", "VT"], C["cyan"], thumb("sr-1-t.jpg"), "YMid"),
             ("PLD SPACE", ["RT", "NDT"], "#a78bfa", thumb("pld-1-t.jpg"), "YMid"),
             ("BUREAU VERITAS", ["ISO 9001", "QA"], C["green"], None, ""),
             ({"en": "NOW", "es": "AHORA", "de": "HEUTE", "it": "OGGI", "fr": "AUJOURD'HUI", "zh": "现在", "ar": "الآن"}[lg], ["iOS", "macOS", "AI"], C["amber"], None, "")]
    o = [f'<defs><clipPath id="pc"><rect width="{W}" height="{H}" rx="14"/></clipPath><filter id="cg" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
         f'<linearGradient id="ov" x1="0" y1="0" x2="0" y2="1"><stop offset=".35" stop-color="#0b1220" stop-opacity="0"/><stop offset="1" stop-color="#0b1220" stop-opacity=".95"/></linearGradient>'
         f'<linearGradient id="scn" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#7cecff" stop-opacity=".35"/></linearGradient></defs><g clip-path="url(#pc)">',
         f'<rect width="{W}" height="{H}" fill="{C["panel"]}"/><rect width="{W}" height="{H}" fill="url(#grid)" opacity=".55"/>']
    # data rain background
    import random as _r; _r.seed(5)
    for i in range(12):
        x = 40 + i * 98 + _r.randint(-12, 12); ts = "".join(f'<tspan x="{x}" dy="17">{_r.choice("01")}</tspan>' for _ in range(8))
        o.append(f'<g opacity=".07"><text font-family="{MONO}" font-size="13" fill="{C["cyan"]}">{ts}<animateTransform attributeName="transform" type="translate" from="0 -150" to="0 {H}" dur="{10+i%4*3}s" begin="-{i*1.6:.1f}s" repeatCount="indefinite"/></text></g>')
    o.append(f'<text x="30" y="38" font-family="{MONO}" font-size="16" fill="{C["cyan"]}" letter-spacing="4">{esc(title)}</text><rect x="30" y="50" width="160" height="3" fill="url(#ac)"><animate attributeName="width" values="60;460;60" dur="5s" repeatCount="indefinite"/></rect>')
    cw, gap = 262, 40
    # rail
    o.append(f'<line x1="30" y1="78" x2="{W-30}" y2="78" stroke="{C["line"]}" stroke-width="2"/><circle r="5" cy="78" fill="#7cecff" filter="url(#cg)"><animate attributeName="cx" from="30" to="{W-30}" dur="6s" repeatCount="indefinite"/></circle>')
    for i, ((org, chips, col, img, pos), role, line) in enumerate(zip(cards, roles, lines)):
        x = 30 + i * (cw + gap); y = 98; ch = 360
        o.append(f'<circle cx="{x+cw/2}" cy="78" r="6" fill="{C["panel"]}" stroke="{col}" stroke-width="2.5"/><text x="{x+cw/2}" y="66" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{col}" letter-spacing="2">0{i+1}</text>')
        o.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="14" fill="#0b1220" stroke="{col}" stroke-opacity="{".95" if i == 3 else ".6"}" stroke-width="2"{" stroke-dasharray=" + chr(34) + "10 6" + chr(34) if i == 3 else ""}>' + ('<animate attributeName="stroke-dashoffset" from="0" to="-32" dur="1.6s" repeatCount="indefinite"/>' if i == 3 else "") + '</rect>')
        # visual area
        vx, vy, vw, vh = x + 12, y + 12, cw - 24, 128
        o.append(f'<clipPath id="v{i}"><rect x="{vx}" y="{vy}" width="{vw}" height="{vh}" rx="10"/></clipPath>')
        if img:
            o.append(f'<g clip-path="url(#v{i})"><image href="{img}" x="{vx}" y="{vy-20}" width="{vw}" height="{vh+60}" preserveAspectRatio="xMid{pos} slice"/><rect x="{vx}" y="{vy}" width="{vw}" height="{vh}" fill="url(#ov)"/><rect x="{vx}" y="{vy-40}" width="{vw}" height="40" fill="url(#scn)"><animate attributeName="y" from="{vy-40}" to="{vy+vh}" dur="{3+i}s" repeatCount="indefinite"/></rect></g>')
        else:
            o.append(f'<rect x="{vx}" y="{vy}" width="{vw}" height="{vh}" rx="10" fill="{col}" fill-opacity=".06"/>')
            cx0, cy0 = vx + vw / 2, vy + vh / 2
            if i == 2:  # audit checklist
                for k in range(3):
                    yy = vy + 24 + k * 32
                    o.append(f'<rect x="{vx+28}" y="{yy}" width="{vw-56}" height="22" rx="6" fill="#0b1220" stroke="{col}" stroke-opacity=".5"/><rect x="{vx+36}" y="{yy+6}" width="{[110,140,90][k]}" height="10" rx="3" fill="{col}" fill-opacity=".35"/>'
                             f'<path d="M{vx+vw-58} {yy+11} l5 5 l10 -11" fill="none" stroke="{col}" stroke-width="3" stroke-linecap="round" stroke-dasharray="30" stroke-dashoffset="30"><animate attributeName="stroke-dashoffset" values="30;0;0;30" keyTimes="0;.2;.8;1" dur="4s" begin="{k*.7}s" repeatCount="indefinite"/></path>')
            else:  # code core
                for r_, d_ in [(52, 18), (36, -12)]:
                    o.append(f'<circle cx="{cx0}" cy="{cy0}" r="{r_}" fill="none" stroke="{col}" stroke-opacity=".6" stroke-dasharray="4 8"><animateTransform attributeName="transform" type="rotate" from="0 {cx0} {cy0}" to="{360 if d_>0 else -360} {cx0} {cy0}" dur="{abs(d_)}s" repeatCount="indefinite"/></circle>')
                o.append(f'<polygon points="{hexpts(cx0,cy0,30)}" fill="#0b1220" stroke="{col}" stroke-width="3" filter="url(#cg)"/><text x="{cx0}" y="{cy0+7}" text-anchor="middle" font-family="{MONO}" font-weight="800" font-size="20" fill="{col}">&lt;/&gt;</text><g><animateTransform attributeName="transform" type="rotate" from="0 {cx0} {cy0}" to="360 {cx0} {cy0}" dur="6s" repeatCount="indefinite"/><circle cx="{cx0+52}" cy="{cy0}" r="5" fill="#7cecff" filter="url(#cg)"/></g>')
        o.append(f'<rect x="{vx}" y="{vy}" width="{vw}" height="{vh}" rx="10" fill="none" stroke="{col}" stroke-opacity=".5"/>')
        o.append(f'<text x="{x+18}" y="{y+166}" font-family="{MONO}" font-size="12" fill="{col}" letter-spacing="2.5">{esc(org)}</text>')
        for k, ln in enumerate(wr(role, 20)[:3]): o.append(f'<text x="{x+18}" y="{y+192+k*25}" font-family="{SANS}" font-weight="800" font-size="20" fill="{C["txt"]}">{esc(ln)}</text>')
        cx_ = x + 18
        for chp in chips:
            w = int(len(chp) * 9.5 + 24)
            o.append(f'<rect x="{cx_}" y="{y+266}" width="{w}" height="26" rx="13" fill="{col}" fill-opacity=".14" stroke="{col}"><animate attributeName="fill-opacity" values=".1;.34;.1" dur="{2.4+i*.3:.1f}s" begin="{(cx_ % 5) * .2:.1f}s" repeatCount="indefinite"/></rect><text x="{cx_+w/2}" y="{y+284}" text-anchor="middle" font-family="{MONO}" font-size="12.5" font-weight="700" fill="#e6f6ff">{esc(chp)}</text>')
            cx_ += w + 8
        for k, ln in enumerate(wr(line, 29)[:3]): o.append(f'<text x="{x+18}" y="{y+316+k*18}" font-family="{SANS}" font-size="13.5" fill="#a9bfd4">{esc(ln)}</text>')
        if i < 3:
            ax = x + cw + 5
            o.append(f'<line x1="{ax}" y1="{y+170}" x2="{ax+gap-10}" y2="{y+170}" stroke="{C["line"]}" stroke-width="3"/><path d="M{ax+gap-20} {y+162} l10 8 l-10 8" fill="none" stroke="{C["cyan"]}" stroke-width="3"><animate attributeName="opacity" values=".2;1;.2" dur="1.4s" begin="{i*.4}s" repeatCount="indefinite"/></path><circle r="3.5" fill="#7cecff" filter="url(#cg)"><animateMotion path="M{ax} {y+170} L{ax+gap-10} {y+170}" dur="1.4s" begin="{i*.4}s" repeatCount="indefinite"/></circle>')
    o.append(f'<rect y="{H-5}" width="{W}" height="5" fill="url(#ac)" opacity=".55"/><rect y="{H-5}" width="260" height="5" fill="#fff" opacity=".85"><animate attributeName="x" from="-260" to="{W}" dur="4s" repeatCount="indefinite"/></rect></g>')
    o.append(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="none" stroke="{C["line"]}" stroke-width="2"/>')
    return svg(W, H, "".join(o), title)


def journey(lg):
    title, nt, st, roles, places, sw1, sw2, miura, srx = i18n.J[lg]; st = i18n.IND[lg]
    W, H = 1200, 450
    X = lambda y: 70 + (y - 2007) / 19.95 * 1060
    segs = [("ENOD SRL", 2007.0, 2010.1, places[0], "VT·PT·MT·UT·RT", roles[0], C["amber"], "A", None),
            ("MOTOMECÁNICA", 2010.1, 2016.2, places[0], "VT·MT", roles[1], C["green"], "B", None),
            ("CONUAR", 2016.2, 2019.2, places[0], "PT·MT", roles[2], "#60a5fa", "A", None),
            ("PLD SPACE", 2019.2, 2023.1, places[1], "RT·PT·VT", roles[3], "#a78bfa", "B", miura),
            ("BUREAU VERITAS", 2023.1, 2024.9, places[1], "QA·AUDIT", roles[4], "#fb7185", "B", None),
            ("SR TECHNICS", 2024.9, 2026.4, places[2], "PT·MT·VT", roles[5], C["cyan"], "A", srx)]
    o = [f'<defs><filter id="jg" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs><defs><clipPath id="jc"><rect width="{W}" height="{H}" rx="14"/></clipPath></defs><g clip-path="url(#jc)">',
         f'<rect width="{W}" height="{H}" fill="{C["panel"]}"/><rect width="{W}" height="{H}" fill="url(#grid)" opacity=".55"/>',
         f'<text x="30" y="38" font-family="{MONO}" font-size="16" fill="{C["cyan"]}" letter-spacing="4">{esc(title)}</text><rect x="30" y="48" width="160" height="3" fill="url(#ac)"><animate attributeName="width" values="60;460;60" dur="5s" repeatCount="indefinite"/></rect>']
    for yr in [2007, 2010, 2013, 2016, 2019, 2022, 2025]:
        x = X(yr); o.append(f'<line x1="{x:.0f}" y1="72" x2="{x:.0f}" y2="193" stroke="{C["line"]}" stroke-dasharray="2 6"/><text x="{x:.0f}" y="68" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{C["mute"]}">{yr}</text>')
    yb = 205
    o.append(f'<text x="30" y="{yb-22}" font-family="{MONO}" font-size="11" fill="{C["mute"]}" letter-spacing="3">{esc(nt)}</text>')
    o.append(f'<rect x="{X(2007)-4:.0f}" y="{yb+10}" width="{X(2026.5)-X(2007)+8:.0f}" height="4" rx="2" fill="{C["line"]}"/>')
    for k, (name, a, b, place, meth, role, col, row, extra) in enumerate(segs):
        x1, x2 = X(a), X(b); w = x2 - x1
        o.append(f'<rect x="{x1+1:.0f}" y="{yb-12}" width="{w-2:.0f}" height="24" rx="8" fill="{col}" fill-opacity=".22" stroke="{col}" stroke-width="2"/>'
                 f'<rect x="{x1+1:.0f}" y="{yb-12}" width="{w-2:.0f}" height="24" rx="8" fill="{col}" opacity="0"><animate attributeName="opacity" values="0;0;.45;0;0" keyTimes="0;{max(a-2007,0)/20-.02:.3f};{(a+b)/2-2007:.0f};{min((b-2007)/20+.03,.999):.3f};1" dur="12s" repeatCount="indefinite"/></rect>')
        cx = (x1 + x2) / 2
        if row == "U":
            o.append(f'<line x1="{cx:.0f}" y1="{yb-12}" x2="{cx:.0f}" y2="170" stroke="{col}" stroke-opacity=".6"/>')
            tx, anc, ty = 1048, "end", 108
            o += [f'<text x="{tx}" y="{ty+60}" text-anchor="{anc}" font-family="{SANS}" font-weight="800" font-size="15" fill="{C["txt"]}">{esc(name)}</text>',
                  f'<text x="{tx}" y="{ty+77}" text-anchor="{anc}" font-family="{MONO}" font-size="11" fill="{col}" letter-spacing="1">{esc(place)} · {meth}</text>',
                  f'<text x="{tx}" y="{ty+93}" text-anchor="{anc}" font-family="{SANS}" font-size="12.5" fill="#9fb6cc">{esc(role)}</text>']
            # nudge: place BV block between bar and software label
            continue
        base = 262 if row == "A" else 350
        anc = "start"; tx = x1
        if name == "SR TECHNICS": anc = "end"; tx = 1142
        o.append(f'<line x1="{cx:.0f}" y1="{yb+12}" x2="{cx:.0f}" y2="{base-16}" stroke="{col}" stroke-opacity=".55" stroke-dasharray="3 4"/><circle cx="{cx:.0f}" cy="{base-16}" r="3.5" fill="{col}" filter="url(#jg)"/>')
        o += [f'<text x="{tx:.0f}" y="{base}" text-anchor="{anc}" font-family="{SANS}" font-weight="800" font-size="16" fill="{C["txt"]}">{esc(name)}</text>',
              f'<text x="{tx:.0f}" y="{base+18}" text-anchor="{anc}" font-family="{MONO}" font-size="11.5" fill="{col}" letter-spacing="1">{esc(place)} · {meth}</text>',
              f'<text x="{tx:.0f}" y="{base+35}" text-anchor="{anc}" font-family="{SANS}" font-size="13" fill="#9fb6cc">{esc(role)}</text>']
        if extra: o.append(f'<text x="{tx:.0f}" y="{base+54}" text-anchor="{anc}" font-family="{SANS}" font-weight="700" font-size="13" fill="{C["amber"]}">{esc(extra)}</text>')
    # scanner + packet
    o.append(f'<line y1="72" y2="{yb+14}" stroke="{C["cyan"]}" stroke-width="2" opacity=".8" filter="url(#jg)"><animate attributeName="x1" from="{X(2007):.0f}" to="{X(2026.5):.0f}" dur="12s" repeatCount="indefinite"/><animate attributeName="x2" from="{X(2007):.0f}" to="{X(2026.5):.0f}" dur="12s" repeatCount="indefinite"/></line>')
    o.append(f'<circle r="5" cy="{yb}" fill="#fff" filter="url(#jg)"><animate attributeName="cx" from="{X(2007):.0f}" to="{X(2026.5):.0f}" dur="12s" repeatCount="indefinite"/></circle>')
    # software track (top right)
    sx = X(2025.8); yt = 130
    o.append(f'<line x1="{sx:.0f}" y1="{yb-12}" x2="{sx:.0f}" y2="{yt+12}" stroke="{C["amber"]}" stroke-width="2" stroke-dasharray="4 4"><animate attributeName="stroke-dashoffset" from="0" to="-16" dur="1s" repeatCount="indefinite"/></line><circle r="4" fill="#fff" filter="url(#jg)"><animateMotion path="M{sx:.0f} {yb-12} L{sx:.0f} {yt+12}" dur="1.6s" repeatCount="indefinite"/></circle>')
    o.append(f'<rect x="{sx:.0f}" y="{yt-12}" width="{X(2026.95)-sx:.0f}" height="24" rx="8" fill="{C["amber"]}" fill-opacity=".25" stroke="{C["amber"]}" stroke-width="2" filter="url(#jg)"><animate attributeName="fill-opacity" values=".15;.5;.15" dur="2.4s" repeatCount="indefinite"/></rect>')
    o.append(f'<path d="M{sx+10:.0f} {yt-6} l8 6 l-8 6 M{sx+26:.0f} {yt-6} l8 6 l-8 6" fill="none" stroke="#fff" stroke-width="2.5"><animate attributeName="opacity" values=".3;1;.3" dur="1.2s" repeatCount="indefinite"/></path>')
    o += [f'<text x="{sx-14:.0f}" y="{yt-20}" text-anchor="end" font-family="{MONO}" font-size="11" fill="{C["amber"]}" letter-spacing="3">{esc(st)}</text>',
          f'<text x="{sx-14:.0f}" y="{yt-2}" text-anchor="end" font-family="{SANS}" font-weight="800" font-size="15" fill="{C["txt"]}">{esc(sw1)}</text>',
          f'<text x="{sx-14:.0f}" y="{yt+16}" text-anchor="end" font-family="{MONO}" font-size="11.5" fill="#9fb6cc">{esc(sw2)}</text>']
    o.append(f'<rect y="{H-5}" width="{W}" height="5" fill="url(#ac)" opacity=".55"/><rect y="{H-5}" width="260" height="5" fill="#fff" opacity=".85"><animate attributeName="x" from="-260" to="{W}" dur="4s" repeatCount="indefinite"/></rect></g><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="none" stroke="{C["line"]}" stroke-width="2"/>')
    return svg(W, H, "".join(o), title)

def mapping(lg):
    title, hl, hr, L, R = i18n.M[lg]
    W, H = 1200, 520; cols = [C["cyan"], C["green"], "#a78bfa", C["amber"], "#fb7185", "#60a5fa", C["cyan"]]
    o = [f'<defs><clipPath id="mc"><rect width="{W}" height="{H}" rx="14"/></clipPath><filter id="mg" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs><g clip-path="url(#mc)">',
         f'<rect width="{W}" height="{H}" fill="{C["panel"]}"/><rect width="{W}" height="{H}" fill="url(#grid)" opacity=".55"/>',
         f'<text x="30" y="38" font-family="{MONO}" font-size="16" fill="{C["cyan"]}" letter-spacing="4">{esc(title)}</text><rect x="30" y="48" width="160" height="3" fill="url(#ac)"><animate attributeName="width" values="60;460;60" dur="5s" repeatCount="indefinite"/></rect>',
         f'<text x="60" y="88" font-family="{MONO}" font-size="12" fill="{C["mute"]}" letter-spacing="3">{esc(hl)}</text><text x="{W-60}" y="88" text-anchor="end" font-family="{MONO}" font-size="12" fill="{C["mute"]}" letter-spacing="3">{esc(hr)}</text>']
    n = len(L); y0 = 104; rh = 58
    for i in range(n):
        y = y0 + i * rh; col = cols[i]; mid = y + 23
        o.append(f'<rect x="40" y="{y}" width="{W-80}" height="46" rx="12" fill="#0b1220" stroke="{col}" stroke-opacity=".35"/>'
                 f'<rect x="40" y="{y}" width="{W-80}" height="46" rx="12" fill="{col}" opacity="0"><animate attributeName="opacity" values="0;0;.22;0;0" keyTimes="0;{i/n:.3f};{(i+.5)/n:.3f};{(i+1)/n:.3f};1" dur="14s" repeatCount="indefinite"/></rect>')
        o.append(f'<circle cx="64" cy="{mid}" r="5" fill="{col}" filter="url(#mg)"/><text x="82" y="{mid+6}" font-family="{MONO}" font-weight="700" font-size="17" fill="#e6f6ff">{esc(L[i])}</text>')
        x1, x2 = 470, 730
        o.append(f'<line x1="{x1}" y1="{mid}" x2="{x2}" y2="{mid}" stroke="{col}" stroke-opacity=".5" stroke-dasharray="6 6"><animate attributeName="stroke-dashoffset" from="0" to="-24" dur="1.2s" repeatCount="indefinite"/></line>'
                 f'<path d="M{x2-12} {mid-7} l12 7 l-12 7" fill="none" stroke="{col}" stroke-width="3"/><circle r="4" fill="#fff" filter="url(#mg)"><animateMotion path="M{x1} {mid} L{x2} {mid}" dur="1.8s" begin="{i*.25:.2f}s" repeatCount="indefinite"/></circle>')
        o.append(f'<text x="{W-64}" y="{mid+6}" text-anchor="end" font-family="{SANS}" font-weight="800" font-size="19" fill="{col}">{esc(R[i])}</text>')
    o.append(f'<rect x="40" y="{y0-6}" width="{W-80}" height="4" fill="{C["cyan"]}" opacity=".7" filter="url(#mg)"><animate attributeName="y" values="{y0-6};{y0+n*rh-8};{y0-6}" dur="14s" repeatCount="indefinite"/></rect>')
    o.append(f'<rect y="{H-5}" width="{W}" height="5" fill="url(#ac)" opacity=".55"/><rect y="{H-5}" width="260" height="5" fill="#fff" opacity=".85"><animate attributeName="x" from="-260" to="{W}" dur="4s" repeatCount="indefinite"/></rect></g><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="none" stroke="{C["line"]}" stroke-width="2"/>')
    return svg(W, H, "".join(o), title)

def cstats(lg):
    W, H = 1200, 190; tiles = list(i18n.S[lg]); tiles[0] = (f"{_dt.date.today().year - METRICS['ndt_since']}+", tiles[0][1]); tiles[1] = (METRICS["aircraft_inspections"], tiles[1][1]); tiles[2] = (str(METRICS["countries_ndt"]), tiles[2][1]); tiles[4] = (str(METRICS["appstore_apps"]), tiles[4][1]); cols = [C["cyan"], C["green"], "#a78bfa", C["amber"], "#fb7185"]
    o = [f'<defs><clipPath id="sc5"><rect width="{W}" height="{H}" rx="14"/></clipPath><filter id="sg" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs><g clip-path="url(#sc5)">',
         f'<rect width="{W}" height="{H}" fill="{C["panel"]}"/><rect width="{W}" height="{H}" fill="url(#grid)" opacity=".55"/>']
    tw = (W - 60 - 4 * 16) / 5
    import textwrap as tw_
    for i, (v, lab) in enumerate(tiles):
        x = 30 + i * (tw + 16); col = cols[i]
        o.append(f'<rect x="{x:.0f}" y="22" width="{tw:.0f}" height="146" rx="14" fill="#0b1220" stroke="{col}" stroke-opacity=".6" stroke-width="2"/><rect x="{x:.0f}" y="22" width="{tw:.0f}" height="4" fill="{col}"/>')
        r = 14; cx_, cy_ = x + tw - 30, 44
        o.append(f'<circle cx="{cx_:.0f}" cy="{cy_}" r="{r}" fill="none" stroke="{C["line"]}" stroke-width="4"/><circle cx="{cx_:.0f}" cy="{cy_}" r="{r}" fill="none" stroke="{col}" stroke-width="4" stroke-linecap="round" stroke-dasharray="{2*3.1416*r*.28:.0f} {2*3.1416*r:.0f}"><animateTransform attributeName="transform" type="rotate" from="0 {cx_:.0f} {cy_}" to="360 {cx_:.0f} {cy_}" dur="{4+i}s" repeatCount="indefinite"/></circle><circle cx="{cx_:.0f}" cy="{cy_}" r="4" fill="{col}" filter="url(#sg)"><animate attributeName="opacity" values="1;.3;1" dur="2s" repeatCount="indefinite"/></circle>')
        fs = 44 if len(v) <= 3 else 34
        o.append(f'<text x="{x+20:.0f}" y="78" font-family="{SANS}" font-weight="800" font-size="{fs}" fill="{col}" filter="url(#sg)">{esc(v)}</text>')
        ls = [lab[k:k+13] for k in range(0, len(lab), 13)] if " " not in lab else tw_.wrap(lab, 19)
        for k, ln in enumerate(ls[:3]): o.append(f'<text x="{x+20:.0f}" y="{110+k*16}" font-family="{MONO}" font-size="11.5" fill="#9fb6cc" letter-spacing="1.2">{esc(ln)}</text>')
    o.append(f'<rect y="{H-4}" width="{W}" height="4" fill="url(#ac)" opacity=".55"/><rect y="{H-4}" width="240" height="4" fill="#fff" opacity=".85"><animate attributeName="x" from="-240" to="{W}" dur="4s" repeatCount="indefinite"/></rect></g><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="none" stroke="{C["line"]}" stroke-width="2"/>')
    return svg(W, H, "".join(o), "career stats")
def standards(lg):
    W, H = 1200, 150
    QL = {"en": "QUALIFICATIONS", "es": "CUALIFICACIONES", "de": "QUALIFIKATIONEN", "it": "QUALIFICHE", "fr": "QUALIFICATIONS", "zh": "资质", "ar": "المؤهلات"}
    rows = [(i18n.T[lg]["std_h"].upper(), ["EASA", "EN 4179", "EN 9100", "ISO 9001", "ASME", "VCA"], C["mute"]),
            (QL[lg], ["PT · LEVEL 2", "MT · LEVEL 1+2", "CSN · RADIATION OPERATOR · 2023–2028"], C["cyan"])]
    o = [f'<rect width="{W}" height="{H}" rx="12" fill="{C["panel"]}" stroke="{C["line"]}" stroke-width="2"/><rect width="{W}" height="{H}" rx="12" fill="url(#grid)" opacity=".5"/>']
    for r, (lab, chips, col) in enumerate(rows):
        y = 40 + r * 56
        o.append(f'<text x="28" y="{y-14}" font-family="{MONO}" font-size="11" fill="{col}" letter-spacing="3">{esc(lab)}</text>')
        x = 28
        for k, ch in enumerate(chips):
            w = int(len(ch) * 8.6 + 28)
            o.append(f'<rect x="{x}" y="{y-4}" width="{w}" height="30" rx="8" fill="#0b1220" stroke="{col}" stroke-opacity=".7"/><text x="{x+w/2}" y="{y+16}" text-anchor="middle" font-family="{MONO}" font-weight="700" font-size="13" fill="#e6f6ff">{esc(ch)}</text>')
            x += w + 10
    o.append(f'<rect x="0" y="{H-3}" width="{W}" height="3" fill="url(#ac)" opacity=".5"/>')
    return svg(W, H, "".join(o), i18n.T[lg]["std_h"])

def navchip(label, num, col):
    w = max(120, int(len(label) * 10.5 + 70)) if all(ord(c) < 0x2e80 for c in label) else max(120, len(label) * 20 + 70)
    h = 44
    body = (f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="10" fill="#0b1220" stroke="{col}" stroke-opacity=".6" stroke-width="1.5"/>'
            f'<text x="14" y="{h/2+4}" font-family="{MONO}" font-size="11" fill="{col}">{num}</text>'
            f'<text x="{w/2+8}" y="{h/2+5}" text-anchor="middle" font-family="{SANS}" font-weight="800" font-size="14" fill="#e6f6ff">{esc(label)}</text>'
            f'<rect x="12" y="{h-5}" width="22" height="2" rx="1" fill="{col}"><animate attributeName="width" values="22;{w-24};22" dur="6s" repeatCount="indefinite"/></rect>')
    return svg(w, h, body, label), w

def pulse():
    W, H = 1200, 40
    d = "M0 20 H300 l10 -14 l12 28 l10 -24 l8 10 H700 l10 -14 l12 28 l10 -24 l8 10 H1200"
    b = (f'<path d="{d}" fill="none" stroke="{C["line"]}" stroke-width="2"/>'
         f'<path d="{d}" fill="none" stroke="{C["cyan"]}" stroke-width="3" stroke-dasharray="120 1400" stroke-linecap="round"><animate attributeName="stroke-dashoffset" from="1520" to="0" dur="4s" repeatCount="indefinite"/></path>'
         f'<circle r="5" fill="#7cecff"><animateMotion path="{d}" dur="4s" repeatCount="indefinite"/></circle>')
    return svg(W, H, b, "pulse divider")
def prune_assets():
    import re as _re
    refs = "".join((ROOT / f).read_text(encoding="utf-8") for _, _, f in i18n.LANGS)
    for d in ("assets/generated", "assets/sections", "assets/branding", "assets/projects"):
        for f in (ROOT / d).rglob("*.svg"):
            if _re.search(r"-[0-9a-f]{8}\.svg$", f.name) and f.name not in refs: f.unlink()
    for f in (ROOT / "assets/generated").rglob("career-*.svg"): f.unlink()

def main():
    global LG
    from urllib.parse import quote
    write("assets/branding/logo.svg", logo(False)); write("assets/branding/logo-animated.svg", logo(True))
    write("assets/branding/footer.svg", footer())
    for _lg, _, _ in i18n.LANGS: write(f"assets/branding/{_lg}/footer.svg", footer(_lg))
    order = [("01", "about"), ("02", "products"), ("03", "radar"), ("04", "building"), ("05", "pipeline"), ("06", "stack"), ("07", "metrics"), ("08", "lab"), ("09", "connect")]
    for lg, _, _ in i18n.LANGS:
        for n, k in order:
            t, r = i18n.SEC[k][lg]
            write(("assets/sections/" if lg == "en" else f"assets/sections/{lg}/") + f"{k}.svg", section(n, t, r))
    base_p = [dict(p) for p in P["projects"]]
    for lg, _, _ in i18n.LANGS:
        for p in base_p:
            q = dict(p); LG = lg
            if lg != "en" and p["id"] in i18n.PROJ: q["tagline"], q["access"] = i18n.PROJ[p["id"]][lg]
            write(("assets/projects/" if lg == "en" else f"assets/projects/{lg}/") + f"{p['id']}.svg", card(q))
        write("assets/generated/pulse.svg", pulse())
    HERO, ORB, CAR, MAP, CST, RAD, STD = {}, {}, {}, {}, {}, {}, {}
    for lg, _, _ in i18n.LANGS:
        LG = lg; bd = "assets/branding/" + ("" if lg == "en" else lg + "/"); gd = "assets/generated/" + ("" if lg == "en" else lg + "/")
        import hashlib, glob
        def hashed(d, base, content):
            for f in glob.glob(str(ROOT / d / (base + "*.svg"))): pathlib.Path(f).unlink()
            name = f"{base}-{hashlib.md5(content.encode()).hexdigest()[:8]}.svg"; write(d + name, content); return d + name
        HERO[lg] = hashed(bd, "hero", hero())
        CAR[lg] = hashed(gd, "journey", journey(lg)); MAP[lg] = hashed(gd, "mapping", mapping(lg)); STD[lg] = hashed(gd, "standards", standards(lg)); CST[lg] = hashed(gd, "cstats", cstats(lg))
        npub = sum(1 for q in P['projects'] if q['ring'] == 'published')
        write(gd + "ticker.svg", anim.ticker([t.format(n=METRICS["appstore_apps"]) for t in Xt()["ticker"]]))
        ORB[lg] = hashed(gd, "orbit", anim.orbit(Xt()["o_sub"], Xt()["o_cap"]))
        write(gd + "pipeline.svg", anim.pipeline(Xt()["p_subs"]))
        RAD[lg] = hashed(gd, "radar", radar()); write(gd + "terminal.svg", terminal()); write(gd + "stats.svg", stats())
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
        lab = "\n".join(f"| **{l['name']}** | `{i18n.ST.get(l['status'],{}).get(lg,l['status'])}` | {i18n.LABT.get(l['name'], {}).get(lg, l['text'])} | [{T['site'] if l.get('url') else T['repo']}]({l.get('url') or 'https://github.com/' + P['owner'] + '/' + l['repo']}) |" for l in P["lab"])
        navk = [("about", "n_about", "161B22", "githubsponsors", "00D4FF"), ("products", "n_products", "00D4FF", "github", "black"), ("radar", "n_radar", "161B22", "target", "00D4FF"), ("building", "n_building", "161B22", "rocket", "00D4FF"), ("metrics", "n_metrics", "161B22", "graphql", "00D4FF"), ("connect", "n_connect", "161B22", "linkedin", "00D4FF")]
        _nk = [("about", "n_about"), ("products", "n_products"), ("radar", "n_radar"), ("building", "n_building"), ("career", "n_career"), ("metrics", "n_metrics"), ("connect", "n_connect")]
        _nv = []
        for _i, (_a, _k) in enumerate(_nk):
            _s, _w = navchip(T[_k], f"{_i+1:02d}", C["cyan"])
            _p = hashed("assets/generated/" + ("" if lg == "en" else lg + "/"), f"nav-{_a}", _s)
            _nv.append(f'<a href="#{_a}"><img src="{_p}" alt="{T[_k]}" height="44"></a>')
        nav = "&nbsp;".join(_nv)
        bar = ["<p>🌐"]
        for l2, sh, f2 in i18n.LANGS:
            nm = i18n.NAMES[l2]; col = "00D4FF" if l2 == lg else "161B22"; fc = "black" if l2 == lg else "00D4FF"
            bar.append(f'<a href="{f2}"><img src="https://img.shields.io/badge/{quote(nm)}-{col}?style=flat-square&labelColor=0D1117&logoColor={fc}" alt="{nm}"></a>')
        bar.append("</p>")
        rtl = lg == "ar"
        out = tpl0
        for k, v in {"{{LANGBAR}}": " ".join(bar), "{{NAV}}": nav, "{{DIR_OPEN}}": '<div dir="rtl">' if rtl else "", "{{DIR_CLOSE}}": "</div>" if rtl else "", "{{SD}}": "" if lg == "en" else lg + "/", "{{HERO}}": HERO[lg], "{{CAREER}}": CAR[lg], "{{RADAR}}": RAD[lg], "{{STANDARDS}}": STD[lg], "{{MAPPING}}": MAP[lg], "{{CSTATS}}": CST[lg], "{{ORBIT}}": ORB[lg], "{{BD}}": "assets/branding/" + ("" if lg == "en" else lg + "/"), "{{GD}}": "assets/generated/" + ("" if lg == "en" else lg + "/"),
                     "{{GRID}}": grid, "{{LAB}}": lab, "{{REPOS}}": repo_table(), "{{SNAKE}}": snake, "{{UPDATED}}": R.get("generated", "pending first workflow run"), "{{OWNER}}": P["owner"],
                     "{{LINKEDIN}}": P["contact"]["linkedin"], "{{SITE}}": P["contact"]["site"]}.items(): out = out.replace(k, v)
        out = re.sub(r"\{\{t\.(\w+)\}\}", lambda m: T[m.group(1)], out)
        write(fname, out)
    print("built", len(i18n.LANGS), "languages")
main(); prune_assets()
