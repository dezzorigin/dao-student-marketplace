# DEPLOY — DAOS

## 1. Yang di-deploy

Landing statis di root repo (`index.html`, `styles.css`, `app.js`,
`og-image.png`, `favicon.svg`) — etalase program C, bukan app web.
Binary C tidak di-deploy (program CLI dijalankan lokal via `make`).

Target: Cloudflare Pages, proyek `dao-student-marketplace`
(fallback: `dao-marketplace`, `pasar-mahasiswa-dao`).

Deploy memakai `~/workspace/github-actions/cf_pages.py` (API token
via vault, pola rantai P1):

```sh
python3 ~/workspace/github-actions/cf_pages.py create-project dao-student-marketplace
python3 ~/workspace/github-actions/cf_pages.py deploy dao-student-marketplace .
```

## 2. Verifikasi live (sebelum merge)

- Root `https://dao-student-marketplace.pages.dev/` HTTP 200 +
  marker landing (`DAOS - SISTEM ALOKASI KANTONG DARAH`).
- Semua tag `og:`/`twitter:` ada dan absolut ke URL Pages.
- `og-image.png` HTTP 200 dengan `content-type: image/*`
  (bukan `text/html` — fallback Pages menipu).
- Cek live memakai Python `urllib` dengan User-Agent browser
  (UA default Python kena 403 Cloudflare).

## 3. Batasan sandbox VM (19 Nov 2026)

- Screenshot dan video demo **tidak bisa** dari VM ini (Chrome lokal
  tidak bisa start; `mmap` memfd ditolak EPERM). Keduanya follow-up
  via browser live — BUKAN gate merge.
- `curl -o` menulis file 0 byte walau melapor size N; pipe
  `curl | grep` tidak bisa dipercaya. Pakai `urllib` + UA browser.
- Tulis file sesudah I/O jaringan dalam satu sesi exec = EPERM:
  file ditulis lewat muse.write atau proses tanpa jaringan.
