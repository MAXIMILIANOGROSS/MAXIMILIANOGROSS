#!/usr/bin/env python3
"""Fetch REAL public repository data from the GitHub API -> data/repos.json (no invented numbers)."""
import json, os, subprocess, sys, urllib.request, datetime, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
OWNER = json.loads((ROOT / "data/projects.json").read_text())["owner"]

def token():
    t = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if t: return t
    try: return subprocess.check_output(["gh", "auth", "token"], text=True).strip()
    except Exception: return ""

def api(path):
    h = {"Accept": "application/vnd.github+json", "User-Agent": "profile-dashboard"}
    t = token()
    if t: h["Authorization"] = "Bearer " + t
    try:
        with urllib.request.urlopen(urllib.request.Request("https://api.github.com" + path, headers=h), timeout=30) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        if e.code == 404: return None
        raise

def main():
    repos = api(f"/users/{OWNER}/repos?type=owner&per_page=100&sort=pushed") or []
    out, langs = [], {}
    for r in repos:
        if r["fork"] or r["name"] == OWNER or r["private"]: continue
        l = api(f"/repos/{OWNER}/{r['name']}/languages") or {}
        for k, v in l.items(): langs[k] = langs.get(k, 0) + v
        rel = api(f"/repos/{OWNER}/{r['name']}/releases/latest")
        out.append({"name": r["name"], "description": r["description"] or "", "language": r["language"] or "",
                    "stars": r["stargazers_count"], "forks": r["forks_count"], "pushed_at": r["pushed_at"],
                    "url": r["html_url"], "license": (r.get("license") or {}).get("spdx_id") or "",
                    "release": ({"tag": rel["tag_name"], "name": rel["name"], "url": rel["html_url"], "date": rel["published_at"]} if rel else None)})
    data = {"generated": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
            "public_repos": out, "languages": dict(sorted(langs.items(), key=lambda kv: -kv[1]))}
    (ROOT / "data/repos.json").write_text(json.dumps(data, indent=1, ensure_ascii=False))
    print(f"{len(out)} public repos, {len(langs)} languages")
main()
