# Brief Agen — Bab I v4 (16 Okt 2026)

> Menggantikan `brief_agen_bab1_v3.md`. Dasar: audit Bab I commit `c0e7b1b`. Revisi 16 Okt malam: P1-P3 lama dipadatkan menjadi P1-P2 (total 12 paragraf).
> Sumber klaim: `context/kartu_paper.md` (kode kartu ada di komentar setiap paragraf). **Jangan menambah paragraf atau klaim yang tidak ada di brief ini.** Kalau ada usulan, tulis sebagai komentar `% USUL:` dan laporkan ke Ferdi.

## 0. Tugas (urut)
1. **Housekeeping repo** (Bagian 5) dikerjakan dulu, supaya kartu bisa dibaca saat menulis.
2. Ganti **seluruh** isi `\section{Latar Belakang}` di `chapters/bab1-pendahuluan.tex` dengan teks Bagian 3. P0 lama dihapus.
3. Ganti isi `\section{Tujuan Penelitian}` dengan Bagian 4.1, lalu lakukan perbaikan kecil di Bagian 4.2.
4. Ganti komentar kepala file (baris 1-5) dengan komentar dua baris versi v4.
5. Jalankan pemeriksaan Bagian 6 dan `make check`. **Jangan commit/push.** Laporkan hasilnya ke Ferdi.

## 1. Aturan gaya
- **Bahasa S1 sederhana:** kalimat pendek, satu ide per kalimat, istilah dijelaskan saat pertama muncul.
- **Istilah asing dicetak miring hanya pada kemunculan pertama di Bab I.** Nama model (HAR-RV, LightGBM, LSTM, GARCH) tidak dimiringkan.
- **Pakai "merupakan" untuk definisi** ("X merupakan Y"), tetapi **jangan sebelum kata kerja**. "Cara lainnya merupakan melatih" itu salah; tulis "Cara lainnya yaitu melatih".
- **Aturan sitasi (diperbarui):**
  - Usahakan satu key hanya dikutip sekali di Bab I.
  - Kalau terpaksa mengutip ulang, **jangan sebut nama penulisnya** di kalimat. Tulis langsung klaimnya lalu `\cite{}`, atau pakai "penelitian terdahulu `\cite{}`".
  - **Sitasi kelompok** seperti `\cite{a,b,c}` boleh dipakai bila **setiap** paper di dalamnya mendukung isi kalimat itu menurut kartu. Jangan menggabungkan paper hanya karena topiknya mirip.
  - Kutipan ulang yang diizinkan di brief ini: `mokni2024` (P1, P2), `andersen1998` (P2, P3), `chassot2026` (P2, P10), `dudek2024` (P6, P12). Selain itu, tidak boleh ada kutipan ulang.
- **Tidak boleh ada hasil *out-of-sample*.** Tidak boleh ada kata "membuktikan", "terbukti", "selalu", atau "sangat ideal".

## 2. Peta paragraf

| P | Isi | Key (kartu) |
|---|---|---|
| P1 | **Hook:** Bitcoin berubah dari pasar *niche* ke institusional, lalu pertanyaan apakah model terbaik tetap terbaik | `nakamoto2008` (C1), `do2026` (C2) |
| P2 | Likuiditas makin tahan guncangan, tetapi perubahan tidak mulus (efisiensi berganti-ganti) | `do2026` (ulang), `mokni2024` (C3) |
| P3 | Efisiensi bentuk lemah != volatilitas tidak bisa diramal; kegunaan ramalan volatilitas | `yi2023` (C4), `andersen1998` (A1) |
| P4 | Definisi RV; RV 5 menit | `andersen1998` (ulang), `liu2015` (A2) |
| P5 | HAR-RV | `corsi2009` (A3), `qiu2025` (D7) |
| P6 | ML dan tiga alasan memilih LightGBM | `wang2023` (D4), `ke2017` (I1), `grinsztajn2022` (I4), `makridakis2022` (I5) |
| P7 | ML vs HAR-RV | `christensen2023` (D1), `huang2024` (D2), `dudek2024` (D3) |
| P8 | LightGBM/pohon vs HAR-RV | `dudek2025lgbm` (D8), `brauneis2026` (D9), `kilic2025` (D10), `pyrlik2021` (D11) |
| P9 | Masalah 1: satu periode uji | `tashman2000` (F5), `gama2014` (J1), `giacomini2010` (G2), `martins2016` (G4), `trucios2023` (E3) |
| P10 | Masalah 2: rolling vs expanding | `rossi2013` (G3), `feng2024window` (F1), `akgun2025` (F2), `feng2024ml` (D5) |
| P11 | Perlakuan pembaruan yang adil | `chassot2026` (D6) |
| P12 | QLIKE dan MSE | `patton2011` (H1) |
| P13 | Yang dilakukan penelitian ini | `dudek2024` (ulang), `suarez2023` (J5) |

## 3. Teks Latar Belakang
Teks lengkap ada di `chapters/bab1-pendahuluan.tex` hasil penerapan brief ini
(P1-P13, lihat komentar penanda paragraf dan kode kartu di tiap paragraf).

## 4. Subbab lain

### 4.1 Tujuan Penelitian
Diganti seluruhnya, sejajar satu-satu dengan RQ. Lihat berkas Bab I.

### 4.2 Perbaikan kecil
| Lokasi | Lama | Baru |
|---|---|---|
| Manfaat Praktis | "baik ML terbukti lebih unggul, setara, maupun lebih buruk" | "baik ML lebih unggul, setara, maupun lebih buruk" |
| Batasan no. 2 | "Yang diramalkan merupakan ..." | "Variabel yang diramalkan yaitu ..." |
| Batasan no. 3 | "Model yang dibandingkan merupakan ..." | "Model yang dibandingkan yaitu ..." |

**Rumusan Masalah tidak boleh diubah.**

## 5. Housekeeping repo
1. Salin `kartu_paper.md` (dari Ferdi) ke `context/kartu_paper.md`.
2. Salin brief ini ke `context/briefs/brief_agen_bab1_v4.md`. Pindahkan `brief_agen_bab1_bab2_v2.md` ke `context/arsip/`.
3. Di `CLAUDE.md`, ganti bagian **Sumber konteks** dan **Urutan otoritas**.
4. Di bagian **Aturan menulis** CLAUDE.md, ganti baris "Klaim isi paper harus sesuai status bacaan ..." menjadi rujukan ke `kartu_paper.md`.

## 6. Pemeriksaan sebelum lapor
1. Hitung `\cite` per key di Bab I. Yang boleh muncul 2 kali hanya `mokni2024`, `andersen1998`, `chassot2026`, `dudek2024`; selain itu semua 1.
2. Di kalimat yang memuat kutipan ulang, nama penulis tidak disebut.
3. Tidak ada kata "GOSS" atau "EFB" di Bab I.
4. Tidak ada kata "merupakan" yang langsung diikuti kata kerja (cari pola `merupakan me`).
5. Semua key ada di `references.bib`. Tidak ada angka hasil *out-of-sample*.
6. Di Latar Belakang hanya tersisa dua `% CEK`: P2 (ditulis ulang Ferdi) dan P5 (Makridakis).
7. `make check` lolos. Laporkan jumlah halaman, overfull box, rujukan menggantung.

---

## Catatan penerapan (diisi agen, 16 Okt 2026)
- Butir 5.1 **tidak dapat dikerjakan**: `kartu_paper.md` tidak ditemukan di
  mesin maupun repo. CLAUDE.md sudah dirujukkan ke berkas itu, tetapi
  berkasnya sendiri masih harus ditaruh Ferdi ke `context/kartu_paper.md`.
- Butir 5.2-5.4, Bagian 2-4, dan Bagian 6 selesai. `make check` LULUS.
