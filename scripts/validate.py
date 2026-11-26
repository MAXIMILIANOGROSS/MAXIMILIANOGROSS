#!/usr/bin/env python3
"""Integrity checks: README asset refs exist, SVG/JSON parse, no placeholders, no links to private repos."""
import json, pathlib, re, sys, xml.etree.ElementTree as ET
ROOT = pathlib.Path(__file__).resolve().parent.parent
errs = []
FILES = ["README.md"] + [f"README.{c}.md" for c in ("es","de","it","fr","zh","ar")]
readme = "\n".join((ROOT / f).read_text(encoding="utf-8") for f in FILES)
for ref in re.findall(r'(?:src|srcset)="(assets/[^"]+)"', readme):
    if not (ROOT / ref).exists(): errs.append(f"missing asset: {ref}")
for f in ROOT.glob("assets/**/*.svg"):
    try: ET.parse(f)
    except ET.ParseError as e: errs.append(f"bad svg {f.relative_to(ROOT)}: {e}")
    if "<script" in f.read_text(encoding="utf-8").lower(): errs.append(f"script in svg: {f.name}")
for f in ROOT.glob("data/*.json"):
    try: json.loads(f.read_text(encoding="utf-8"))
    except Exception as e: errs.append(f"bad json {f.name}: {e}")
if re.search(r"TODO|lorem|placeholder|\{\{", readme, re.I): errs.append("placeholder text in README")
if "<script" in readme.lower() or "<iframe" in readme.lower(): errs.append("script/iframe in README")
public = {r["name"] for r in json.loads((ROOT / "data/repos.json").read_text())["public_repos"]} if (ROOT / "data/repos.json").exists() else None
owner = json.loads((ROOT / "data/projects.json").read_text())["owner"]
if public is not None:
    for name in re.findall(rf"github\.com/{owner}/([\w.\-]+)", readme):
        if name != owner and name not in public: errs.append(f"README links to non-public/unknown repo: {name}")
try:
    import yaml
    for f in (ROOT / ".github/workflows").glob("*.yml"): yaml.safe_load(f.read_text())
except ImportError: print("pyyaml missing: workflow YAML not checked")
except Exception as e: errs.append(f"bad yaml: {e}")
print("\n".join(errs) if errs else "VALIDATION OK"); sys.exit(1 if errs else 0)
