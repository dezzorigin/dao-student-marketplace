# PRD — DAOS: Sistem Alokasi Kantong Darah

> Versi 1.0.0 — 19 Nov 2026. Dokumen ini menjelaskan produk **apa adanya**:
> program CLI C untuk UAS Praktikum Struktur Data dan Algoritma B.
> Nama repo (`dao-student-marketplace`) tidak mencerminkan isinya — ini
> **bukan** marketplace mahasiswa. Tidak ada fitur jual-beli yang di-invent
> di sini, dan PRD ini tidak mengarangnya.

## 1. Ringkasan

Program CLI bahasa C murni (in-memory, tanpa database, tanpa jaringan)
yang mengoptimalkan distribusi kantong darah berdasarkan tingkat kritis
pasien darurat, sekaligus meminimalkan pemborosan stok darah yang
mendekati masa kedaluwarsa (SDG 3 — Kehidupan Sehat dan Sejahtera).

Dua antrean prioritas bekerja berpasangan (Double Priority Queue):

| Antrean | Struktur | Kunci prioritas |
|---|---|---|
| Pasien | Max-Heap | triage terkecil dulu (1 = KRITIS EKSTREM), darurat jadi penentu seri |
| Kantong darah | Min-Heap | sisa hari terkecil dulu (paling cepat kedaluwarsa dipakai dulu) |

Satu eksekusi alokasi: ambil pasien prioritas tertinggi (peek root) →
Linear Search seluruh stok untuk kantong yang kompatibel (aturan ABO) →
Greedy pilih sisa hari terkecil → dequeue keduanya → catat riwayat.

## 2. Pengguna & konteks

- **Pengguna:** petugas bank darah / simulasi ruang gawat darurat, dan
  mahasiswa Praktikum Struktur Data dan Algoritma B (USK).
- **Tim pembuat (Kelompok 2):** Muhammad Rizki (250810701100049),
  Siti Fildzahra Revani (250810701100107), Nabil Aulia Dika
  (250810701100090), Irvan Almidar (250810701100085).
- **Konteks:** tugas kelompok UAS — kode ditulis kolaboratif, tiap anggota
  menyumbang modul (lihat README untuk pembagian tugas).

## 3. Fitur (yang benar-benar ada di kode)

1. **Input pasien** — nama, golongan darah (A/B/AB/O, divalidasi),
   triage 1–5, status darurat (1/0). Kapasitas 100 pasien.
2. **Input kantong darah** — golongan darah (divalidasi), sisa hari
   1–365. Kapasitas 100 kantong.
3. **Eksekusi alokasi** — satu pasien + satu kantong per eksekusi, dengan
   aturan kompatibilitas ABO: AB terima semua; A terima A/O; B terima
   B/O; O hanya terima O.
4. **Tampilkan antrean & stok** — isi kedua heap apa adanya (urutan heap,
   bukan urutan terurut penuh).
5. **Riwayat transaksi** — daftar alokasi yang sudah terjadi
   (`#001 | Pasien: … -> Darah: D…`), kapasitas 100.
6. **Keluar** — menampilkan total transaksi sesi itu.

Yang **tidak** ada (jangan diklaim): penyimpanan permanen (semua data
hilang saat program keluar), login/pengguna, jaringan/API, golongan
Rhesus (+/−), tanggal kedaluwarsa kalender (hanya hitung hari), dan
fitur marketplace apa pun.

## 4. Aturan bisnis

- Triage 1 paling kritis; triage 5 paling tidak mendesak. Label:
  1 KRITIS EKSTREM, 2 KRITIS, 3 MENDESAK, 4 KURANG MENDESAK,
  5 TIDAK MENDESAK.
- Pasien darurat (`is_emergency = 1`) langsung ke root antrean saat
  enqueue, tapi triage tetap dominan saat heapify-down (lihat
  ARCHITECTURE.md § "Perilaku yang perlu diketahui").
- Kantong yang dipilih selalu yang kompatibel dengan sisa hari
  **terkecil** — darah yang hampir kedaluwarsa tidak dibiarkan basi.
- Alokasi gagal (tidak ada kantong kompatibel) tidak mengeluarkan
  pasien dari antrean; pasien tetap menunggu.

## 5. Kriteria selesai

- `make` bersih tanpa warning (`-Wall -Wextra -std=c11 -O2`).
- `make test` lolos: 6 kelompok assert (sesi demo, alokasi kosong,
  ABO, validasi golongan, menu tidak valid, greedy sisa-hari).
- Landing menjelaskan sistem + menampilkan sesi asli + cara build.
- CI hijau, deploy live di Cloudflare Pages.
