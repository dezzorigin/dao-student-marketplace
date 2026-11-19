# CHANGELOG — DAOS

## 1.0.0 — 19 Nov 2026 (PR proper #42)

### Perbaikan kode (bug asli yang membuat program tidak bisa jalan)

- `src/uas.c`: menambahkan `heapify_down_pasien` yang tidak pernah
  didefinisikan di kode asli (dipanggil `enqueue_pasien` dan
  `dequeue_pasien`) — sebelumnya program gagal link.
- `src/uas.c`: memperbaiki typo komentar baris 128 (`/ Menambah…`
  menjadi `// Menambah…`) — sebelumnya error sintaks, program tidak
  bisa dikompilasi sama sekali.
- `src/uas.c`: enam `scanf` tanpa cek return kini menampung return
  value (`-Wunused-result` di `-O2` hilang); perilaku tidak berubah.
  Build kini bersih tanpa warning di `gcc -Wall -Wextra -std=c11 -O2`.

### Proper repo

- `LICENSE` MIT (Kelompok 2), `.gitignore` (binary, objek, node_modules).
- `Makefile`: `all` / `test` / `demo` / `clean`.
- `scripts/demo-input.txt` + `scripts/smoke-test.sh`: smoke test nyata
  (6 kelompok assert atas output program).
- `README.md` ditulis ulang (standar repo): penjelasan sistem, build,
  sesi contoh asli, pembagian tugas tim.
- `docs/`: PRD, ARCHITECTURE, USAGE, TESTING, DEPLOY, DESIGN
  (kontrak arah), `diagrams.html` (diagram arsitektur HTML+SVG),
  `contoh-sesi.txt` (output demo verbatim), slide UAS asli
  (`Kelompok2_PPTUTS_B.pdf`, tidak diubah).
- Landing statis (`index.html`, `styles.css`, `app.js`, `favicon.svg`,
  `og-image.png` 1200×630 via PIL) — etalase, deploy Cloudflare Pages.
- CI (`.github/workflows/ci.yml`, 5 job): build-test gcc/make,
  static-checks (html-validate + gate P0/OG), advisory-sweep OSV,
  playwright-e2e, smoke.
- `package.json` + `scripts/check-static.mjs` + `scripts/smoke.mjs`
  (dev-only: html-validate + Playwright).
