# TESTING — DAOS

## 1. Smoke test (`make test`)

`make test` menjalankan `scripts/smoke-test.sh`: binary dijalankan
dengan input contoh, outputnya di-assert dengan `grep`. Bukan echo
sukses — assert yang gagal menghentikan skrip (`set -e`).

Enam kelompok assert:

| # | Uji | Input | Harapan |
|---|---|---|---|
| 1 | Sesi demo penuh | `scripts/demo-input.txt` (3 pasien, 3 kantong, 2 alokasi) | D001 → P002 (Budi), D002 → P001 (Ayu), sisa P003 + D003, riwayat #001/#002, total transaksi 2 |
| 2 | Alokasi kosong | `3`, `0` | `Antrean pasien atau stok darah kosong` |
| 3 | ABO | pasien O + stok A saja | `[GAGAL] Tidak ada darah kompatibel` |
| 4 | Validasi golongan | golongan `X` lalu `A` | `X` ditolak, `A` diterima, pasien tersimpan |
| 5 | Menu tidak valid | `9`, `0` | `Pilihan tidak valid` |
| 6 | Greedy | pasien AB + stok O 40 hari & O 5 hari | kantong 5 hari (D002) yang dipilih, bukan 40 hari |

Jalankan lokal:

```sh
make test
```

## 2. CI

Workflow `.github/workflows/ci.yml` (5 job):

- **build-test** — `make` (gcc, `-Wall -Wextra`, warning = bukti
  build tidak bersih, tapi job gagal hanya bila kompilasi/test gagal)
  lalu `make test`.
- **static-checks** — Node 24, `npm install` (repo belum punya
  lockfile — JANGAN `npm ci`, JANGAN `cache: npm`), `html-validate`
  untuk landing, lalu `npm run validate` (gate P0 anti-slop + tag
  OG/Twitter, `scripts/check-static.mjs`).
- **advisory-sweep** — `scripts/advisory-sweep.py` (OSV batch, pola
  repo #24–#41). Repo ini 0 dependensi produksi — sweep tetap jalan
  sebagai bukti.
- **playwright-e2e** — landing statis di server lokal (desktop +
  mobile 390px), HANYA di CI.
- **smoke** — semua file yang di-deploy ada dan tidak kosong,
  `og-image.png` ≥ 10 KB, semua href/src lokal di `index.html`
  mengarah ke file yang ada.

## 3. Yang belum diuji otomatis

- Screenshot desktop + mobile dan video demo: follow-up (butuh
  browser live; tidak bisa dari VM sandbox — lihat DEPLOY.md).
- Interaksi ketik manual di terminal (sesi demo memakai stdin
  ter-redirect; perilaku interaktifnya sama, hanya echo ketikan
  yang tidak tampil).
