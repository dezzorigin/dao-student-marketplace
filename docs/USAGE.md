# USAGE — Cara Pakai DAOS

## 1. Build

Persyaratan: `gcc` (diuji 13.3.0) dan `make`. Tanpa dependensi lain.

```sh
make            # menghasilkan binary ./daos
```

atau tanpa make:

```sh
gcc -Wall -Wextra -std=c11 -O2 -o daos src/main.c src/uas.c
```

## 2. Menjalankan

```sh
./daos
```

Menu utama:

```
[1] Input Data Pasien
[2] Input Kantong Darah
[3] Eksekusi Alokasi Darah
[4] Tampilkan Antrean Pasien & Stok Darah
[5] Tampilkan Riwayat Transaksi
[0] Keluar
```

### Menu 1 — Input pasien

- Nama pasien (bebas, maks 63 karakter)
- Golongan darah: hanya `A`, `B`, `AB`, `O` — selain itu ditolak dan
  diminta ulang
- Triage 1–5: 1 KRITIS EKSTREM, 2 KRITIS, 3 MENDESAK, 4 KURANG
  MENDESAK, 5 TIDAK MENDESAK
- Darurat: `1` ya, `0` tidak

### Menu 2 — Input kantong darah

- Golongan darah (A/B/AB/O, divalidasi)
- Sisa hari 1–365 (hari menuju kedaluwarsa)

### Menu 3 — Eksekusi alokasi

Satu kali tekan = satu alokasi: pasien prioritas tertinggi mendapat
satu kantong yang kompatibel dengan sisa hari terkecil. Kalau tidak
ada kantong kompatibel, program mencetak `[GAGAL]` dan pasien tetap
menunggu.

### Menu 4 & 5 — Lihat antrean, stok, dan riwayat

Menu 4 menampilkan isi kedua heap; menu 5 menampilkan daftar alokasi
yang sudah terjadi.

## 3. Sesi contoh (data fiktif)

Jalankan sesi demo yang sama dengan yang dipakai smoke test:

```sh
make demo
# sama dengan: ./daos < scripts/demo-input.txt
```

Skenario: 3 pasien (Budi Santoso O triage 1 darurat; Ayu Lestari B
triage 2; Citra Dewi A triage 4) dan 3 kantong (O 3 hari; B 30 hari;
A 12 hari). Hasilnya: Budi mendapat D001, Ayu mendapat D002, Citra
dan D003 tersisa, total transaksi 2. Output lengkap yang asli ada di
`docs/contoh-sesi.txt` (162 baris, verbatim dari satu kali jalan).

## 4. Aturan kompatibilitas ABO

| Pasien | Bisa terima |
|---|---|
| AB | A, B, AB, O (semua) |
| A | A, O |
| B | B, O |
| O | O saja |

Rhesus (+/−) tidak dimodelkan — golongan hanya A/B/AB/O.
