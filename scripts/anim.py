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

def orbit():
    W, H = 800, 500; cx, cy = 400, 235
    rings = [(80, ["Swift", "Kotlin", "Python"], 28, 1), (150, ["TypeScript", "JavaScript", "HTML", "FastAPI", "Next.js"], 46, -1), (212, ["Firebase", "Supabase", "SQLite", "Vercel", "Git", "GitHub", "Xcode", "Android Studio"], 70, 1)]
    cols = [CY, GRN, VIO]
    o = [f'<rect width="{W}" height="{H}" rx="14" fill="{PANEL}" stroke="{LINE}" stroke-width="2"/><rect width="{W}" height="{H}" rx="14" fill="url(#grid)" opacity=".5"/>']
    for (r, names, dur, d), c in zip(rings, cols):
        o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{c}" stroke-opacity=".35" stroke-dasharray="3 7"/>')
        g = []
        for k, n in enumerate(names):
            a = math.radians(360 * k / len(names) - 90); x, y = r * math.cos(a), r * math.sin(a); w = len(n) * 8.4 + 26
            g.append(f'<g transform="translate({x:.1f} {y:.1f})"><g><animateTransform attributeName="transform" type="rotate" from="0" to="{-360*d}" dur="{dur}s" repeatCount="indefinite"/>'
                     f'<rect x="{-w/2:.1f}" y="-14" width="{w:.1f}" height="28" rx="14" fill="#0b1220" stroke="{c}" stroke-opacity=".8"/>'
                     f'<text y="5" text-anchor="middle" font-family="{MONO}" font-size="13" fill="#e2f3ff">{esc(n)}</text></g></g>')
        o.append(f'<g transform="translate({cx} {cy})"><g><animateTransform attributeName="transform" type="rotate" from="0" to="{360*d}" dur="{dur}s" repeatCount="indefinite"/>{"".join(g)}</g></g>')
    hx = " ".join(f"{cx+52*math.cos(math.radians(60*k-30)):.1f},{cy+52*math.sin(math.radians(60*k-30)):.1f}" for k in range(6))
    o.append(f'<polygon points="{hx}" fill="#0b1220" stroke="url(#ac)" stroke-width="3"><animate attributeName="stroke-width" values="3;5;3" dur="3s" repeatCount="indefinite"/></polygon>'
             f'<text x="{cx}" y="{cy+5}" text-anchor="middle" font-family="{SANS}" font-weight="800" font-size="20" fill="{TXT}" letter-spacing="2">STACK</text>'
             f'<text x="{cx}" y="{cy+24}" text-anchor="middle" font-family="{MONO}" font-size="9" fill="{MUTE}">ONLY WHAT SHIPS</text>')
    o.append(f'<text x="20" y="{H-14}" font-family="{MONO}" font-size="10.5" fill="{MUTE}">Technologies that appear in my actual repositories — inner ring: languages · middle: frameworks · outer: services &amp; tools</text>')
    return wrap(W, H, "".join(o), "Technology orbit: Swift, Kotlin, Python, TypeScript, JavaScript, HTML, FastAPI, Next.js, Firebase, Supabase, SQLite, Vercel, Git, GitHub, Xcode, Android Studio")
