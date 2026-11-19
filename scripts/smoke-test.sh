#!/bin/sh
# Smoke test nyata DAOS — dijalankan `make test` (lokal + CI).
# Binary dijalankan dengan input contoh, lalu outputnya di-assert.
# BUKAN echo sukses: setiap assert yang gagal menghentikan skrip (set -e).
set -eu

BIN="./daos"
OUT="$(mktemp)"
trap 'rm -f "$OUT"' EXIT INT TERM

fail() { echo "FAIL: $1" >&2; exit 1; }
ok()   { echo "ok: $1"; }

# ── 1. Sesi demo penuh (3 pasien, 3 kantong, 2 alokasi) ───────────────
"$BIN" < scripts/demo-input.txt > "$OUT" 2>&1

grep -q "DAOS - SISTEM ALOKASI KANTONG DARAH" "$OUT" \
  || fail "banner tidak tampil"
grep -q "Pasien Prioritas Tertinggi: Budi Santoso (Gol: O)" "$OUT" \
  || fail "pasien triage 1 + darurat bukan prioritas tertinggi"
grep -q "\[SUKSES\] Kantong D001 dialokasikan ke Pasien P002" "$OUT" \
  || fail "alokasi 1: D001 (O, 3 hari) harus ke Budi Santoso P002"
grep -q "Pasien Prioritas Tertinggi: Ayu Lestari (Gol: B)" "$OUT" \
  || fail "pasien prioritas ke-2 harus Ayu Lestari"
grep -q "\[SUKSES\] Kantong D002 dialokasikan ke Pasien P001" "$OUT" \
  || fail "alokasi 2: D002 (B, 30 hari) harus ke Ayu Lestari P001"
grep -q "1. P003 | Citra Dewi | Gol: A | Triage: 4 | Darurat: Tidak" "$OUT" \
  || fail "sisa antrean harus Citra Dewi P003"
grep -q "1. D003 | Gol: A | Sisa: 12 hari" "$OUT" \
  || fail "sisa stok harus D003 (A, 12 hari)"
grep -q "#001 | Pasien: Budi Santoso -> Darah: D001" "$OUT" \
  || fail "riwayat #001 hilang"
grep -q "#002 | Pasien: Ayu Lestari -> Darah: D002" "$OUT" \
  || fail "riwayat #002 hilang"
grep -q "Program dihentikan. Total transaksi: 2." "$OUT" \
  || fail "total transaksi harus 2"
ok "sesi demo: 2 alokasi sukses, antrean + stok sisa benar, riwayat benar"

# ── 2. Alokasi saat antrean/stok kosong ────────────────────────────────
printf '3\n0\n' | "$BIN" > "$OUT" 2>&1
grep -q "Antrean pasien atau stok darah kosong" "$OUT" \
  || fail "alokasi kosong harus ditolak dengan pesan kosong"
ok "alokasi kosong ditolak"

# ── 3. Tidak ada darah kompatibel (pasien O, stok hanya A) ─────────────
printf '1\nDoni\nO\n3\n0\n2\nA\n10\n3\n0\n' | "$BIN" > "$OUT" 2>&1
grep -q "\[GAGAL\] Tidak ada darah kompatibel" "$OUT" \
  || fail "pasien O + stok A harus GAGAL (aturan ABO)"
ok "aturan kompatibilitas ABO ditegakkan (O hanya terima O)"

# ── 4. Golongan darah tidak valid ditolak, lalu diterima yang valid ────
printf '1\nEka\nX\nA\n3\n0\n0\n' | "$BIN" > "$OUT" 2>&1
grep -q "\[OK\] Pasien berhasil ditambahkan" "$OUT" \
  || fail "golongan X harus ditolak lalu A diterima"
ok "validasi golongan darah (hanya A/B/AB/O)"

# ── 5. Menu tidak valid ────────────────────────────────────────────────
printf '9\n0\n' | "$BIN" > "$OUT" 2>&1
grep -q "Pilihan tidak valid" "$OUT" \
  || fail "menu 9 harus ditolak"
ok "menu tidak valid ditolak"

# ── 6. Greedy: kantong paling cepat kedaluwarsa dipilih dulu ───────────
#    Pasien AB (terima semua) + stok O 40 hari & O 5 hari -> harus D002.
printf '1\nFajar\nAB\n2\n0\n2\nO\n40\n2\nO\n5\n3\n0\n' | "$BIN" > "$OUT" 2>&1
grep -q "\[SUKSES\] Kantong D002 dialokasikan ke Pasien P001" "$OUT" \
  || fail "greedy harus memilih kantong 5 hari (D002), bukan 40 hari (D001)"
ok "greedy sisa-hari-terkecil: kantong hampir kedaluwarsa dipakai dulu"

echo "SMOKE OK: semua assert lolos"
