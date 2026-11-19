#!/usr/bin/env python3
"""Generate og-image.png 1200x630 for DAOS (PIL, local only, no network).

Design follows the landing's own language (docs/DESIGN.md): paper
#F4F1ED, life-pulse red #C0392B, ink #23211E, slate #5B6770, stable
green #2F6B4F, quiet blush #E8C4C4. No gradients, no emoji, no stock
imagery — a plain editorial card with one blood-bag tag motif.
Not a screenshot of anything.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
PAPER = (244, 241, 237)  # #F4F1ED
INK = (35, 33, 30)       # #23211E
RED = (192, 57, 43)      # #C0392B
RED_SOFT = (246, 227, 224)
SLATE = (91, 103, 112)   # #5B6770
GREEN = (47, 107, 79)    # #2F6B4F
BLUSH = (232, 196, 196)  # #E8C4C4
LINE = (216, 210, 200)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
MONO_B = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# red rule at top + faint inner frame
d.rectangle([0, 0, W, 10], fill=RED)
d.rectangle([28, 28, W - 28, H - 28], outline=LINE, width=2)

# droplet mark (simple polygon-ish drop via pieslice + triangle)
cx, cy = 96, 128
d.pieslice([cx - 26, cy - 26, cx + 26, cy + 26], start=0, end=180, fill=RED)
d.polygon([(cx - 26, cy), (cx + 26, cy), (cx, cy - 44)], fill=RED)

# kicker (dipendekkan supaya tidak menabrak kartu kantong di kanan)
f_kick = ImageFont.truetype(MONO_B, 28)
d.text((140, 108), "UAS  ·  STRUKTUR DATA & ALGORITMA B", font=f_kick, fill=RED)

# title
f_title = ImageFont.truetype(SERIF_B, 150)
d.text((68, 168), "DAOS", font=f_title, fill=INK)

# subtitle
f_sub = ImageFont.truetype(SANS, 38)
d.text((72, 348), "Sistem Alokasi Kantong Darah", font=f_sub, fill=INK)
d.text((72, 398), "Pasien paling kritis dilayani dulu.", font=f_sub, fill=SLATE)
d.text((72, 446), "Kantong hampir basi dipakai dulu.", font=f_sub, fill=SLATE)

# chips row
f_chip = ImageFont.truetype(MONO_B, 25)
chips = [("MAX-HEAP PASIEN · TRIAGE", RED, (255, 247, 245)),
         ("MIN-HEAP DARAH · SISA HARI", GREEN, (255, 255, 255))]
x, y = 72, 514
for label, bg, fg in chips:
    tw = d.textlength(label, font=f_chip)
    pad_x, pad_y = 20, 12
    d.rounded_rectangle([x, y, x + tw + pad_x * 2, y + 50], radius=25, fill=bg)
    d.text((x + pad_x, y + 11), label, font=f_chip, fill=fg)
    x += tw + pad_x * 2 + 18

# ── blood-bag tag card, right side (by0 digeser ke bawah supaya
#     tidak menutupi kicker; teks di tengah kartu, bukan offset tetap) ──
bx0, by0, bx1, by1 = 830, 150, 1130, 495
d.rounded_rectangle([bx0, by0, bx1, by1], radius=18, fill=(255, 255, 255),
                    outline=LINE, width=2)
# hanging hole
d.ellipse([bx0 + 135, by0 + 18, bx0 + 165, by0 + 48], outline=SLATE, width=3)
# droplet
dx, dy = bx0 + 150, by0 + 108
d.pieslice([dx - 20, dy - 20, dx + 20, dy + 20], start=0, end=180, fill=RED)
d.polygon([(dx - 20, dy), (dx + 20, dy), (dx, dy - 34)], fill=RED)
# bag id + blood group (rata tengah di dalam kartu)
f_id = ImageFont.truetype(MONO, 26)
t = "D001"
d.text((bx0 + (300 - d.textlength(t, font=f_id)) / 2, by0 + 150), t, font=f_id, fill=SLATE)
f_blood = ImageFont.truetype(SERIF_B, 72)
t = "Gol O"
d.text((bx0 + (300 - d.textlength(t, font=f_blood)) / 2, by0 + 182), t, font=f_blood, fill=INK)
# expiry bar (3 of 365 days -> thin red sliver, labelled)
d.rounded_rectangle([bx0 + 36, by0 + 288, bx1 - 36, by0 + 302], radius=7, fill=RED_SOFT)
d.rounded_rectangle([bx0 + 36, by0 + 288, bx0 + 60, by0 + 302], radius=7, fill=RED)
f_days = ImageFont.truetype(MONO_B, 26)
d.text((bx0 + 36, by0 + 312), "3 HARI TERSISA", font=f_days, fill=RED)

# footer url
f_meta = ImageFont.truetype(MONO, 26)
d.text((72, 570), "dao-student-marketplace.pages.dev  ·  C murni  ·  aturan ABO",
       font=f_meta, fill=SLATE)

img.save("og-image.png")
print("og-image.png written")
