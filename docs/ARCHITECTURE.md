# ARCHITECTURE — DAOS

> C11 murni, in-memory, tanpa dependensi eksternal. Tiga file sumber.

## 1. Peta modul

```
src/main.c   — entry point + loop menu CLI (0–5), sanitasi input menu
src/uas.c    — semua logika: heap, alokasi, menu input/tampil
src/uas.h    — konstanta, struct, variabel global, prototipe
```

## 2. Struktur data

| Struct | Isi |
|---|---|
| `Pasien` | `id`, `nama[64]`, `gol_darah[4]`, `triage` (1–5), `is_emergency` (0/1) |
| `Darah` | `id`, `gol_darah[4]`, `sisa_hari` (1–365) |
| `RiwayatTransaksi` | `nomor`, salinan `Pasien`, salinan `Darah`, `timestamp[32]` |

Kapasitas statis: `MAX_PASIEN = MAX_DARAH = MAX_RIWAYAT = 100`.
ID dihitung dari counter global (`id_pasien_counter`,
`id_darah_counter`, mulai dari 1). `timestamp` riwayat bukan jam
nyata — berisi label `Transaksi #NNN`.

## 3. Algoritma

### Antrean pasien — Max-Heap (prioritas = triage terkecil)

- `prioritas_pasien_lebih_tinggi(a, b)`: triage lebih kecil menang;
  seri diputus `is_emergency` lebih besar.
- `enqueue_pasien`: pasien biasa → `heapify_up_pasien`;
  pasien darurat → digeser ke root (indeks 0) lalu
  `heapify_down_pasien(0)`.
- `dequeue_pasien`: ambil root, pindah elemen terakhir ke root,
  `heapify_down_pasien(0)`.

### Stok darah — Min-Heap (prioritas = sisa hari terkecil)

- `enqueue_darah` → `heapify_up_darah` (sisa hari kecil naik).
- `dequeue_darah_by_index(idx)` → ganti posisi `idx` dengan elemen
  terakhir, lalu `heapify_up` + `heapify_down` (indeks sembarang
  butuh perbaikan dua arah).

### Alokasi — Linear Search + Greedy (`cari_dan_alokasi_darah`)

1. Guard: antrean atau stok kosong → tolak.
2. Peek pasien root (tanpa dequeue dulu).
3. Linear Search seluruh stok: hitung kantong kompatibel
   (`is_kompatibel`, aturan ABO) dan simpan indeks dengan sisa hari
   terkecil (Greedy).
4. Tidak ada yang kompatibel → `[GAGAL]`, pasien tetap di antrean.
5. Ada → `dequeue_pasien` + `dequeue_darah_by_index`, catat riwayat,
   cetak `[SUKSES] Kantong D… dialokasikan ke Pasien P…`.

Kompleksitas: enqueue/dequeue heap O(log n); satu alokasi O(n)
karena Linear Search atas stok.

## 4. Perilaku yang perlu diketahui

- **Darurat vs triage:** pasien darurat langsung ke root saat
  enqueue, tetapi `heapify_down_pasien` membandingkan dengan
  `prioritas_pasien_lebih_tinggi` — triage tetap dominan. Pasien
  darurat triage 5 bisa turun lagi di bawah pasien triage 1 saat
  heap dirapikan. Ini perilaku asli kode, didokumentasikan bukan
  diperbaiki diam-diam.
- **Tampilan antrean** menunjukkan urutan array heap, bukan urutan
  terurut penuh — itu wajar untuk heap dan memang tujuan menunya
  ("membuktikan struktur heap berjalan").
- **Tidak ada persistensi:** keluar program = semua data hilang.
- **Input EOF:** `scanf` yang gagal membaca (EOF) meninggalkan nilai
  lama; menu utama sudah menangani `scanf` gagal untuk pilihan menu
  (pilihan = −1 → pesan tidak valid).

## 5. Perbaikan yang dilakukan PR proper (19 Nov 2026)

1. `heapify_down_pasien` **tidak pernah didefinisikan** di kode asli
   — dipanggil dari `enqueue_pasien` dan `dequeue_pasien`, sehingga
   program tidak bisa di-link. Ditambahkan implementasinya (cermin
   `heapify_down_darah`, memakai `prioritas_pasien_lebih_tinggi`).
2. Baris 128 `uas.c` asli: `/ Menambah kantong darah…` — kurang satu
   `/`, error sintaks. Diperbaiki jadi `// …`.
3. Enam `scanf` tanpa cek return memicu `-Wunused-result` di `-O2`.
   Return value kini ditampung ke variabel lalu `(void)` — perilaku
   sama, build bebas warning.
