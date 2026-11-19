# DESIGN.md — Kontrak Arah Desain dao-student-marketplace

> Ditulis SEBELUM coding landing (standar anti-slop P1). Referensi dulu,
> baru bangun. Produk: **bukan app web** — ini program CLI C (UAS Praktikum
> Struktur Data dan Algoritma B) yang mengalokasikan kantong darah ke pasien
> dengan Double Priority Queue. Landing di repo ini adalah **etalase**:
> menjelaskan sistem, menampilkan sesi asli, dan cara build. Produknya
> tetap binary C `./daos`.

## Kejujuran isi (penting)

Nama repo `dao-student-marketplace` menyesatkan: isi repo aslinya adalah
**Sistem Alokasi Kantong Darah (DAOS, SDG 3)** — antrean pasien Max-Heap
berdasarkan triage, stok darah Min-Heap berdasarkan sisa hari, alokasi
dengan Linear Search + Greedy dan aturan kompatibilitas ABO. **Bukan**
marketplace mahasiswa, bukan jual-beli kampus. Tidak ada fitur marketplace
yang di-invent di sini — landing menjelaskan sistem apa adanya, dengan nama
tim asli (Muhammad Rizki, Siti Fildzahra Revani, Nabil Aulia Dika, Irvan
Almidar) dan angka dari **satu kali jalan nyata** di VM (gcc 13.3.0),
dilabeli "contoh". Tidak ada statistik vanity, tidak ada klaim "10x lebih
cepat". Semua nama pasien/kantong di contoh sesi adalah data fiktif.

## Referensi

**Pemenang: Bloodbridge — Blood Drive Landing Page Template**
https://www.rocket.new/templates/bloodbridge-lifesaving-blooddrive-landing-page-template

Kenapa menang: satu halaman blood drive untuk bank darah komunitas —
hero yang dipimpin testimoni/misi, layout rantai orang bergantian, dan
finder drive inline. Sistem desainnya: klinik bersih saat fajar, tenang
tapi mendesak. Paletnya: putih kabut pagi `#F4F1ED`, blush tenang
`#E8C4C4`, slate mantap `#5B6770`, dan merah denyut hidup `#C0392B`
yang **hanya** dipakai untuk CTA dan data kritis. Itu persis nada yang
dibutuhkan DAOS: kertas rekam medis + satu warna darurat yang tidak
diboroskan. Strukturnya yang di-clone: hero misi satu kolom dengan kartu
status stok di samping, deretan kartu "kantong" sebagai etalase, dan
bagian cara kerja sebagai alur berurutan.
Yang diubah: finder kode pos diganti **papan triase** (tangga triase 1–5
+ antrean pasien), kartu orang diganti **kartu kantong darah** berlabel
gantung dengan bar sisa hari, dan isinya disesuaikan ke algoritma DAOS
(Double Priority Queue, Linear Search + Greedy, ABO) + sesi terminal asli.

Kandidat yang kalah:

- **Blood Donation App — Sebastian Dydo**
  https://sebastian.dydo.com.pl/portfolio/donation/
  Kalah: ini UI aplikasi iOS donor (gamifikasi, dashboard donor), bukan
  landing etalase sistem alokasi. Nada "motivating without pressuring"
  bagus, tapi strukturnya aplikasi, bukan halaman penjelasan.
- **RedHope — How It Works**
  https://redhope.thefreelanzer.com/how-it-works
  Kalah: alur langkah 01–07 rapi dan dekat dengan cara kerja DAOS, tapi
  visualnya generik aplikasi donor (kartu langkah seragam) dan tidak
  punya bahasa "papan klinik" yang dicari.

## Kontrak arah

**Palet (6 warna bernama, tiap warna punya tugas):**

| Nama | Hex | Peran |
|---|---|---|
| Kertas Kabut | `#F4F1ED` | Latar halaman — kertas rekam medis pagi hari |
| Merah Denyut | `#C0392B` | HANYA aksi kritis & data darurat: CTA utama, triase 1, kantong hampir kedaluwarsa |
| Blush Tenang | `#E8C4C4` | Kartu lembut / latar aksen sekunder, tidak berteriak |
| Slate Mantap | `#5B6770` | Teks sekunder, label, garis pemisah |
| Tinta Rekam | `#23211E` | Teks utama — hitam hangat, bukan slate gelap |
| Hijau Stabil | `#2F6B4F` | Status sukses: alokasi berhasil, kantong aman |

**Tipografi (2 keluarga):** Fraunces (display serif — headline editorial
klinik, bukan sans generik) + IBM Plex Mono (body/data — mesin ketik rekam
medis, angka tabular bawaan). Tidak ada Inter/Roboto.

**Layout (satu kalimat):** Papan triase klinik — kolom kiri papan antrean
pasien bertingkat (tangga triase 1–5), kolom kanan aliran alokasi +
sesi terminal asli.

**Satu detail khas:** kartu kantong darah bergaya **label gantung**
(lubang gantung + tetesan darah SVG + bar sisa hari kedaluwarsa) —
benda fisik yang dialokasikan sistem, bukan kartu generik.

**Beda dari repo sebelumnya (#41 umkm-analytics) — 5 dari 5 sumbu:**

| Sumbu | #41 | #42 ini |
|---|---|---|
| Palet | arang gelap + amber fosfor | kertas kabut terang + merah denyut |
| Tipografi | JetBrains Mono saja | Fraunces serif + IBM Plex Mono |
| Layout | satu kolom sesi terminal | papan triase dua kolom asimetris |
| Radius/spacing | tajam 2px, rapat | kartu 14px, napas lega 8pt |
| Detail khas | kursor blok berkedip | label gantung kantong darah + bar sisa hari |

## Larangan yang dipatuhi

P0: tanpa gradient apa pun; tanpa headline gradient; tanpa emoji sebagai
ikon (ikon SVG stroke 1.5px); tanpa statistik vanity; tanpa hero tengah +
3 kartu identik; tanpa `rounded-2xl shadow-lg` di semua permukaan; tanpa
copy generik. Orde-kedua: bukan krim+terracotta (blush dipakai sebagai
aksen lembut, bukan terracotta), bukan near-black+lime, bukan label mono
all-caps di mana-mana, bukan hiasan 01/02/03, bukan satu hue, bukan
dark blue/slate, bukan espresso+oranye.

## Gate 7 sumbu (target ≥4 tiap sumbu, dinilai sebelum merge)

1. anti-slop purity — nol P0 + nol orde-kedua (gate otomatis
   `scripts/check-static.mjs`)
2. UX speed & 1-to-3 — satu aksi utama per viewport (CTA "jalankan demo"),
   maks 3 sekunder
3. tipografi — 2 font, angka tabular, body ≤75ch
4. spacing & geometri — grid 8pt, radius dalam = radius luar − padding,
   padding kartu ≥16px
5. motion — <200ms ease-out, active scale 0.97, hormati
   `prefers-reduced-motion`
6. a11y — focus ring terlihat, aria-label di tombol ikon, tag semantik
7. mobile 390px — stack vertikal, tanpa scroll horizontal

## Tes siluet

Kecilkan landing ke thumbnail hitam-putih: yang harus tetap ketahuan
adalah **papan triase + kantong darah berlabel** — bukan halaman produk
generik. Kalau siluetnya bisa jadi landing SaaS mana pun, desain gagal.
