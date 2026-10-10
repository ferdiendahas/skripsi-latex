# Praskripsi Ferdi — LightGBM vs HAR-RV, Realized Variance Bitcoin

Repo LaTeX praskripsi (proposal) Informatika UPN "Veteran" Jawa Timur, kelas `upnjatim-skripsi.cls`. Penulis: Ferdi Endahas Ahmad. Komunikasi dengan Ferdi: bahasa Indonesia santai (gw/lu), langsung, ringkas.

## Status
- **Praskripsi.** Bab I–III saja. Eksperimen sebenarnya sudah selesai, tetapi **hasil out-of-sample tidak boleh muncul di Bab I–III** (QLIKE rata-rata, ΔL, UDmax, p-value hipotesis, kurva window). Yang boleh: desain, deskripsi data, hasil di window awal (VIF, hyperparameter terkunci), dan perhitungan manual Subbab 3.3.
- Uji konfirmatori sudah dijalankan, jadi **RQ, hipotesis, judul, dan uji konfirmatori tidak boleh diubah** mengikuti hasil (anti-HARKing).

## Sumber konteks (`context/`)
Baca hanya bagian yang relevan dengan tugas; jangan memuat semuanya.
- `KOREKSI.md` — **baca lebih dulu.** Daftar bagian dokumen riset yang salah atau usang.
- `hasil_riset_bitcoin_v2_5.md` — desain riset, literatur, RQ/hipotesis. Sebagian sudah usang (lihat KOREKSI).
- `hasil_eksperimen_bitcoin_v2_5.md` — kronologi, hasil, deviasi implementasi, dan **source code final** (`rvlib/`).
- `perhitungan_manual.md` — angka Subbab 3.3 (window awal, terverifikasi terhadap kode).
- `briefs/` — instruksi kerja per tugas. Bila Ferdi bilang "kerjakan brief X", ikuti brief itu persis dan kirim laporan balik sesuai format di bagian akhirnya.

**Urutan otoritas bila bertentangan:** brief terbaru > `KOREKSI.md` > source code di `hasil_eksperimen` > `hasil_riset`.

## Aturan menulis
- **Jangan mengarang** angka, metadata referensi, klaim isi paper, atau parameter. Bila tidak bisa dipastikan, tulis komentar `% CEK: <alasan>` dan biarkan.
- Pertahankan semua `% CEK:` yang sudah ada kecuali brief menyuruh menghapus.
- Klaim isi paper harus sesuai status bacaan di dokumen riset (✅F full text, ✅A abstrak, ✅M metadata, ⚠ belum dicek). Paper ✅A/✅M hanya boleh dikutip untuk klaim umum, dengan `% CEK:`.
- Notasi pasar: **BTC/USDT** = spot (yang dipakai). BTCUSDT tanpa garis miring = perpetual; hanya untuk nama berkas arsip Binance.
- Istilah asing `\textit{}` pada kemunculan pertama per bab; nama model (LightGBM, HAR-RV) tidak miring.
- Notasi wajib konsisten dengan `frontmatter/daftar-notasi.tex`. Simbol baru ditambahkan ke sana. Simbol yang sudah terpakai tidak boleh diberi makna kedua (mis. $m$ = jumlah titik patah; $D^{\text{KS}}$ vs $D_t$; $P^H_t, P^L_t$ untuk harga, $L$ untuk loss).
- Sitasi IEEE via biblatex: `\cite{key}`. Rujuk persamaan/tabel/gambar dengan `\ref`/`\eqref`, jangan menyalin ulang.
- Gambar data hanya dari keluaran pipeline `skripsi_rv`; diagram konsep dengan TikZ; jangan menempel gambar dari paper (gambar ulang + "diadaptasi dari").

## `references.bib`
- Metadata diambil dari `https://api.crossref.org/works/<DOI>`. Jangan menimpa field yang sudah lebih lengkap (rentang halaman, nama depan, "The" di nama jurnal, tipe `@incollection`/`@inproceedings`). Entitas HTML (`&amp;`) dan karakter di luar Times New Roman (mis. U+2010) dinormalkan.
- Judul yang berbeda substansi dari dokumen riset → laporkan ke Ferdi dan tandai kalimat pengutipnya dengan `% CEK:`; jangan menulis ulang kalimat sendiri.

## Build
- `make` → `build/praskripsi.pdf` (XeLaTeX + Biber via latexmk). `make check` → validasi format pedoman.
- Setiap tugas selesai: jalankan `make check` dan laporkan jumlah halaman, overfull box, rujukan menggantung, missing character.
- Jangan commit/push kecuali Ferdi minta.

## Fakta kunci (ringkas)
- Judul sementara: Analisis Stabilitas Kinerja Relatif LightGBM terhadap HAR-RV dalam Peramalan *Realized Variance* Bitcoin (final menunggu pembimbing).
- Data: BTC/USDT spot Binance, 5 menit, 17 Agu 2017 – 30 Sep 2026. OOS mulai 1 Sep 2018. Batas era transition|institutional: 1 Jan 2021 (Do, 2026).
- Desain 2×2: HAR, HAR-X, LGBM-HAR, LGBM-X (+ naive). HAR-X tanpa log Amihud (VIF).
- Skema: S0 static, S1 expanding, S2 rolling (W 365/730; eksploratori 180/1095/tertunda). Retrain bulanan.
- Loss utama QLIKE, pelengkap MSE. ΔL = L(ML) − L(HAR). Pasangan konfirmatori LGBM-X vs HAR, skema S2-365.
- Uji konfirmatori per hipotesis: H1 UDmax (lalu DM); H2a uji-F HAC regresi ΔL bulanan; H2b dua uji-t HAC + Holm; H3 uji-t HAC dua sisi pada $D_t = \Delta L_t(\text{S2-365}) - \Delta L_t(\text{S1})$ di era institutional.
