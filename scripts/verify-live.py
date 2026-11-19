#!/usr/bin/env python3
"""Verifikasi live dao-student-marketplace.pages.dev (UA browser)."""
import sys
import urllib.request
import urllib.error

BASE = "https://dao-student-marketplace.pages.dev"
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

def get(path):
    req = urllib.request.Request(BASE + path, headers={"User-Agent": UA})
    try:
        with urllib.request.build_opener().open(req, timeout=60) as r:
            return r.status, r.headers.get("Content-Type", ""), r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.headers.get("Content-Type", ""), e.read()

fails = []
st, ct, body = get("/")
print(f"root: {st} {ct} {len(body)} bytes")
if st != 200:
    fails.append(f"root HTTP {st}")
html = body.decode("utf-8", "replace")
for marker in ["DAOS - SISTEM ALOKASI KANTONG DARAH", "Budi Santoso",
               "Papan triase", "Kantong di rak"]:
    ok = marker in html
    print(f"marker {marker!r}: {'ADA' if ok else 'HILANG'}")
    if not ok:
        fails.append(f"marker hilang: {marker}")
for tag in ['property="og:title"', 'property="og:description"',
            'property="og:type"', 'property="og:url"',
            'property="og:image" content="https://dao-student-marketplace.pages.dev/og-image.png"',
            'name="twitter:card" content="summary_large_image"',
            'name="twitter:title"', 'name="twitter:description"',
            'name="twitter:image" content="https://dao-student-marketplace.pages.dev/og-image.png"']:
    ok = tag in html
    print(f"tag {tag[:40]}...: {'ADA' if ok else 'HILANG'}")
    if not ok:
        fails.append(f"tag hilang: {tag}")

st, ct, body = get("/og-image.png")
print(f"og-image.png: {st} {ct} {len(body)} bytes")
if st != 200:
    fails.append(f"og-image HTTP {st}")
if "image/" not in ct:
    fails.append(f"og-image content-type bukan image/*: {ct}")
if len(body) < 10 * 1024:
    fails.append(f"og-image < 10 KB: {len(body)}")

st, ct, body = get("/favicon.svg")
print(f"favicon.svg: {st} {ct} {len(body)} bytes")
if st != 200:
    fails.append(f"favicon HTTP {st}")

st, ct, body = get("/docs/PRD.md")
print(f"docs/PRD.md: {st} {ct} {len(body)} bytes")
if st != 200:
    fails.append(f"PRD HTTP {st}")

if fails:
    print("VERIFIKASI GAGAL:")
    for f in fails:
        print(" -", f)
    sys.exit(1)
print("VERIFIKASI LIVE OK")
