# DAOS — Sistem Alokasi Kantong Darah (Kelompok 2, UAS Praktikum
# Struktur Data dan Algoritma B)
#
#   make          — kompilasi binary ./daos (gcc, -Wall -Wextra)
#   make test     — smoke test nyata: binary dijalankan dengan input
#                   contoh, output di-assert (bukan echo sukses)
#   make demo     — jalankan sesi contoh, tampilkan output ke terminal
#   make clean    — hapus binary + artefak build
#
# Standar: C11, tanpa dependensi eksternal, tanpa Makefile sub-direktori.

CC      := gcc
CFLAGS  := -Wall -Wextra -std=c11 -O2
TARGET  := daos
SRCS    := src/main.c src/uas.c

.PHONY: all test demo clean

all: $(TARGET)

$(TARGET): $(SRCS) src/uas.h
	$(CC) $(CFLAGS) -o $@ $(SRCS)

test: $(TARGET)
	@sh scripts/smoke-test.sh

demo: $(TARGET)
	@./$(TARGET) < scripts/demo-input.txt

clean:
	rm -f $(TARGET) *.o src/*.o
