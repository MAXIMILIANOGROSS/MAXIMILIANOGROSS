"""Animated SVG components (SMIL, GitHub-compatible, static fallback = fully visible)."""
import math
from xml.sax.saxutils import escape as esc
MONO = "'JetBrains Mono','SFMono-Regular',Menlo,Consolas,'DejaVu Sans Mono',monospace"
SANS = "'Segoe UI',Helvetica,Arial,sans-serif"
CY, VIO, GRN, AMB, TXT, MUTE, BG, PANEL, LINE = "#00d4ff", "#7c3aed", "#34d399", "#fbbf24", "#eaf6ff", "#8aa4bd", "#070b12", "#0c1420", "#1b2a3d"
DEFS = f'''<defs><linearGradient id="ac" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CY}"/><stop offset="1" stop-color="{VIO}"/></linearGradient>
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="{LINE}" stroke-width="1" opacity=".5"/></pattern></defs>'''
def wrap(w, h, body, label): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{esc(label)}">{DEFS}{body}</svg>'

def ticker(items):
    W, H = 1200, 44; text = "   ◆   ".join(items) + "   ◆   "; cw = 8.6; L = len(text) * cw
    g = "".join(f'<text x="{k*L:.0f}" y="28" font-family="{MONO}" font-size="14" fill="#9fd8ee" xml:space="preserve">{esc(text)}</text>' for k in range(3))
    b = (f'<clipPath id="tk"><rect width="{W}" height="{H}" rx="8"/></clipPath><rect width="{W}" height="{H}" rx="8" fill="{PANEL}" stroke="{LINE}" stroke-width="2"/>'
         f'<g clip-path="url(#tk)"><g>{g}<animateTransform attributeName="transform" type="translate" from="0 0" to="-{L:.0f} 0" dur="{max(20, L/45):.0f}s" repeatCount="indefinite"/></g>'
         f'<rect width="90" height="{H}" fill="url(#fl)"/><rect x="{W-90}" width="90" height="{H}" fill="url(#fr)"/></g>'
         f'<linearGradient id="fl" x1="0" x2="1"><stop offset="0" stop-color="{PANEL}"/><stop offset="1" stop-color="{PANEL}" stop-opacity="0"/></linearGradient>'
         f'<linearGradient id="fr" x1="0" x2="1"><stop offset="0" stop-color="{PANEL}" stop-opacity="0"/><stop offset="1" stop-color="{PANEL}"/></linearGradient>'
         f'<circle cx="18" cy="22" r="5" fill="{GRN}"><animate attributeName="opacity" values="1;.2;1" dur="1.4s" repeatCount="indefinite"/></circle>')
    return wrap(W, H, b, "Live status ticker")

def pipeline(subs=None):
    W, H = 1200, 270; st = list(zip(["IDEA", "RESEARCH", "DESIGN", "ARCHITECTURE", "DEVELOP", "TEST / QA", "DEPLOY", "ITERATE"], subs or ["problem", "market", "UX", "stack", "build", "verify", "ship", "improve"]))
    o = [f'<rect width="{W}" height="{H}" rx="14" fill="{PANEL}" stroke="{LINE}" stroke-width="2"/><rect width="{W}" height="{H}" rx="14" fill="url(#grid)" opacity=".6"/>']
    y = 105; x0, x1 = 75, 1125
    o.append(f'<line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="{LINE}" stroke-width="3"/><line x1="{x0}" y1="{y}" x2="{x1}" y2="{y}" stroke="url(#ac)" stroke-width="3" stroke-dasharray="10 12"><animate attributeName="stroke-dashoffset" from="0" to="-44" dur="1.2s" repeatCount="indefinite"/></line>')
    for i, (n, sub) in enumerate(st):
        cx = x0 + i * 150; f = i * 150 / 1050
        a, c = max(f - .035, 0), min(f + .09, .999)
        o.append(f'<rect x="{cx-62}" y="{y-32}" width="124" height="64" rx="12" fill="#0b1220" stroke="{LINE}" stroke-width="2"/>'
                 f'<rect x="{cx-62}" y="{y-32}" width="124" height="64" rx="12" fill="{CY}" opacity="0"><animate attributeName="opacity" values="0;0;.28;0;0" keyTimes="0;{a:.3f};{f:.3f};{c:.3f};1" dur="8s" repeatCount="indefinite"/></rect>'
                 f'<rect x="{cx-62}" y="{y-32}" width="124" height="64" rx="12" fill="none" stroke="{CY}" stroke-width="2" opacity="0"><animate attributeName="opacity" values="0;0;1;0;0" keyTimes="0;{a:.3f};{f:.3f};{c:.3f};1" dur="8s" repeatCount="indefinite"/></rect>'
                 f'<text x="{cx}" y="{y+5}" text-anchor="middle" font-family="{SANS}" font-weight="800" font-size="{14 if len(n)>9 else 16}" fill="{TXT}">{esc(n)}</text>'
                 f'<text x="{cx}" y="{y+56}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{MUTE}" letter-spacing="2">{esc(sub)}</text>'
                 f'<text x="{cx-52}" y="{y-40}" font-family="{MONO}" font-size="11" fill="{CY}">0{i+1}</text>')
    o.append(f'<circle r="7" fill="{CY}"><animateMotion path="M{x0} {y} L{x1} {y}" dur="8s" repeatCount="indefinite"/></circle>'
             f'<circle r="16" fill="{CY}" opacity=".25"><animateMotion path="M{x0} {y} L{x1} {y}" dur="8s" repeatCount="indefinite"/></circle>')
    fb = f"M{x1} {y+90} C{x1} {y+150} {x0} {y+150} {x0} {y+90}"
    o.append(f'<path d="{fb}" fill="none" stroke="{VIO}" stroke-width="2" stroke-dasharray="6 8"><animate attributeName="stroke-dashoffset" from="0" to="28" dur="1.5s" repeatCount="indefinite"/></path>'
             f'<text x="{W/2}" y="{y+160}" text-anchor="middle" font-family="{MONO}" font-size="13" fill="#a78bfa" letter-spacing="3">FEEDBACK LOOP · USERS · DATA · NEXT VERSION</text>')
    return wrap(W, H, "".join(o), "Engineering pipeline: idea, research, design, architecture, develop, test, deploy, iterate")

def orbit(sub="ONLY WHAT SHIPS", cap="Technologies that appear in my actual repositories — inner ring: languages · middle: frameworks · outer: services & tools"):
    import random
    random.seed(11)
    W, H = 900, 600; cx, cy = 450, 292
    rings = [(100, ["Swift", "Kotlin", "Python"], 34, 1, -90), (172, ["TypeScript", "JavaScript", "HTML", "FastAPI", "Next.js"], 52, -1, -54), (240, ["Firebase", "Supabase", "SQLite", "Vercel", "Git", "GitHub", "Xcode", "Android Studio"], 80, 1, -68)]
    cols = [CY, GRN, VIO]
    o = [f'<defs><filter id="gl" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
         f'<radialGradient id="cg" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{CY}" stop-opacity=".28"/><stop offset="1" stop-color="{CY}" stop-opacity="0"/></radialGradient>'
         f'<linearGradient id="sw2" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CY}" stop-opacity="0"/><stop offset="1" stop-color="{CY}" stop-opacity=".45"/></linearGradient>'
         f'<linearGradient id="sc2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CY}" stop-opacity="0"/><stop offset="1" stop-color="{CY}" stop-opacity=".16"/></linearGradient></defs>']
    o.append(f'<rect width="{W}" height="{H}" rx="14" fill="{PANEL}" stroke="{LINE}" stroke-width="2"/><rect width="{W}" height="{H}" rx="14" fill="url(#grid)" opacity=".5"/><circle cx="{cx}" cy="{cy}" r="300" fill="url(#cg)"><animate attributeName="opacity" values=".6;1;.6" dur="5s" repeatCount="indefinite"/></circle>')
    # data rain
    for i in range(14):
        x = 24 + i * 64 + random.randint(-10, 10)
        ts = "".join(f'<tspan x="{x}" dy="17">{random.choice("01")}</tspan>' for _ in range(8))
        o.append(f'<g opacity="{random.choice([.08,.12,.16])}"><text font-family="{MONO}" font-size="13" fill="{CY}">{ts}<animateTransform attributeName="transform" type="translate" from="0 -160" to="0 {H}" dur="{9+i%5*2}s" begin="-{i*1.7:.1f}s" repeatCount="indefinite"/></text></g>')
    # floating geometric shapes
    shapes = []
    for i in range(16):
        x, y = random.choice([random.randint(20, 150), random.randint(W-150, W-20)]), random.randint(30, H-60)
        s = random.randint(8, 16); col = random.choice([CY, GRN, VIO, AMB]); kind = i % 4
        if kind == 0: sh = f'<polygon points="0,{-s} {s},{s} {-s},{s}" fill="none" stroke="{col}" stroke-width="1.6"/>'
        elif kind == 1: sh = f'<rect x="{-s/2}" y="{-s/2}" width="{s}" height="{s}" fill="none" stroke="{col}" stroke-width="1.6"/>'
        elif kind == 2: sh = f'<polygon points="0,{-s} {s},0 0,{s} {-s},0" fill="none" stroke="{col}" stroke-width="1.6"/>'
        else: sh = f'<circle r="{s/2}" fill="none" stroke="{col}" stroke-width="1.6"/><circle r="2" fill="{col}"/>'
        shapes.append(f'<g transform="translate({x} {y})" opacity=".55"><g><animateTransform attributeName="transform" type="rotate" from="0" to="{random.choice([360,-360])}" dur="{14+i*2}s" repeatCount="indefinite"/>{sh}</g><animateTransform attributeName="transform" additive="sum" type="translate" values="0 0;0 -14;0 0" dur="{5+i%4}s" repeatCount="indefinite"/></g>')
    o += shapes
    # outer ticks + HUD brackets
    o.append(f'<g transform="translate({cx} {cy})"><circle r="262" fill="none" stroke="{CY}" stroke-opacity=".5" stroke-width="10" stroke-dasharray="1.5 11"><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="120s" repeatCount="indefinite"/></circle></g>')
    for (x, y, dx, dy) in [(14, 14, 1, 1), (W-14, 14, -1, 1), (14, H-14, 1, -1), (W-14, H-14, -1, -1)]:
        o.append(f'<path d="M{x} {y+dy*26} V{y} H{x+dx*26}" fill="none" stroke="{CY}" stroke-width="2.5" opacity=".8"><animate attributeName="opacity" values=".4;1;.4" dur="3s" repeatCount="indefinite"/></path>')
    # radar sweep
    o.append(f'<g transform="translate({cx} {cy})"><g><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="7s" repeatCount="indefinite"/><path d="M0 0 L250 -42 A254 254 0 0 1 250 42 Z" fill="url(#sw2)"/></g></g>')
    # core ripples
    for j in range(3):
        o.append(f'<circle cx="{cx}" cy="{cy}" r="50" fill="none" stroke="{CY}" stroke-width="2"><animate attributeName="r" values="50;140" dur="4.5s" begin="{j*1.5}s" repeatCount="indefinite"/><animate attributeName="opacity" values=".7;0" dur="4.5s" begin="{j*1.5}s" repeatCount="indefinite"/></circle>')
    # rings with nodes, links, packets, satellites
    for (r, names, dur, d, a0), c in zip(rings, cols):
        o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{c}" stroke-opacity=".4" stroke-dasharray="3 7"/>')
        o.append(f'<g transform="translate({cx} {cy})"><circle r="{r}" fill="none" stroke="{c}" stroke-width="3" stroke-dasharray="70 {2*math.pi*r/2-70:.0f}" stroke-linecap="round" opacity=".85"><animateTransform attributeName="transform" type="rotate" from="0" to="{-360*d}" dur="{dur*.35:.1f}s" repeatCount="indefinite"/></circle></g>')
        g = []
        for k, n in enumerate(names):
            a = math.radians(a0 + 360 * k / len(names)); x, y = r * math.cos(a), r * math.sin(a); w = len(n) * 8.4 + 26
            g.append(f'<line x1="0" y1="0" x2="{x:.1f}" y2="{y:.1f}" stroke="{c}" stroke-opacity=".22"/>'
                     f'<circle r="3" fill="#7cecff" filter="url(#gl)"><animateMotion path="M0 0 L{x:.1f} {y:.1f}" dur="{2.4+k%3*.8:.1f}s" begin="{k*.5:.1f}s" repeatCount="indefinite"/></circle>')
            g.append(f'<g transform="translate({x:.1f} {y:.1f})"><g><animateTransform attributeName="transform" type="rotate" from="0" to="{-360*d}" dur="{dur}s" repeatCount="indefinite"/>'
                     f'<rect x="{-w/2:.1f}" y="-14" width="{w:.1f}" height="28" rx="14" fill="#0b1220" stroke="{c}" stroke-opacity=".9" filter="url(#gl)"/>'
                     f'<circle cx="{-w/2+11:.1f}" cy="0" r="3" fill="{c}"><animate attributeName="opacity" values="1;.2;1" dur="{1.6+k*.3:.1f}s" repeatCount="indefinite"/></circle>'
                     f'<text x="6" y="5" text-anchor="middle" font-family="{MONO}" font-size="13" fill="#e2f3ff">{esc(n)}</text></g></g>')
        o.append(f'<g transform="translate({cx} {cy})"><g><animateTransform attributeName="transform" type="rotate" from="0" to="{360*d}" dur="{dur}s" repeatCount="indefinite"/>{"".join(g)}</g></g>')
        # satellites on counter-rotating orbit
        o.append(f'<g transform="translate({cx} {cy})"><g><animateTransform attributeName="transform" type="rotate" from="{random.randint(0,300)}" to="{random.randint(0,300)+(-360*d)}" dur="{dur*.5:.0f}s" repeatCount="indefinite"/><circle cx="{r}" r="4.5" fill="{c}" filter="url(#gl)"/><circle cx="{r}" r="9" fill="none" stroke="{c}" stroke-opacity=".5"><animate attributeName="r" values="5;14;5" dur="2.4s" repeatCount="indefinite"/></circle></g></g>')
    # core
    hx = lambda R: " ".join(f"{cx+R*math.cos(math.radians(60*k-30)):.1f},{cy+R*math.sin(math.radians(60*k-30)):.1f}" for k in range(6))
    o.append(f'<g transform="translate({cx} {cy})"><polygon points="{" ".join(f"{70*math.cos(math.radians(60*k-30)):.1f},{70*math.sin(math.radians(60*k-30)):.1f}" for k in range(6))}" fill="none" stroke="{CY}" stroke-opacity=".6" stroke-dasharray="8 8"><animateTransform attributeName="transform" type="rotate" from="0" to="-360" dur="22s" repeatCount="indefinite"/></polygon></g>')
    o.append(f'<polygon points="{hx(52)}" fill="#0b1220" stroke="url(#ac)" stroke-width="3" filter="url(#gl)"><animate attributeName="stroke-width" values="3;6;3" dur="3s" repeatCount="indefinite"/></polygon>'
             f'<text x="{cx}" y="{cy+4}" text-anchor="middle" font-family="{SANS}" font-weight="800" font-size="20" fill="{TXT}" letter-spacing="2">STACK</text>'
             f'<text x="{cx}" y="{cy+22}" text-anchor="middle" font-family="{MONO}" font-size="8" fill="{MUTE}">{esc(sub)}</text>')
    o.append(f'<rect x="0" y="-60" width="{W}" height="60" fill="url(#sc2)"><animate attributeName="y" from="-60" to="{H}" dur="6s" repeatCount="indefinite"/></rect>')
    o.append(f'<text x="{W/2}" y="{H-16}" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{MUTE}">{esc(cap)}</text>')
    return wrap(W, H, "".join(o), "Technology orbit: Swift, Kotlin, Python, TypeScript, JavaScript, HTML, FastAPI, Next.js, Firebase, Supabase, SQLite, Vercel, Git, GitHub, Xcode, Android Studio")
