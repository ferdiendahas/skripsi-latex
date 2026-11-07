# Praskripsi Ferdi — Prediksi Harga BTC/IDR dengan Model Boosting (v3.0)

Repo LaTeX praskripsi (proposal) Informatika UPN "Veteran" Jawa Timur, kelas `upnjatim-skripsi.cls`. Penulis: Ferdi Endahas Ahmad. Komunikasi dengan Ferdi: bahasa Indonesia santai (gw/lu), langsung, ringkas.

> **Topik lama (v2.x: LightGBM vs HAR-RV, realized variance, Binance BTC/USDT) sudah tidak dipakai.** Isinya hanya ada di `context/arsip/` dan `chapters/arsip-v2.9/`. Jangan dijadikan acuan.

## Status
- **Praskripsi.** Bab I–III saja.
- Eksperimen 14–20 Okt 2026 (satu minggu) hanya **uji coba awal**. Eksperimen final dijalankan Februari 2027 dengan data Oktober 2026 – Februari 2027.
- **Hasil eksperimen tidak boleh muncul di Bab I–III**, termasuk angka MAE, persentase vs Naive, model/metode/*time frame* terbaik. Yang boleh: desain, deskripsi data, alasan pemilihan metode, literatur, dan angka dari paper orang lain yang tercatat di kartu.

## Sumber konteks (`context/`) — selalu pakai nomor versi tertinggi
- `kartu_paper_v3*.md` — **satu-satunya sumber klaim isi paper.** Ikuti baris "Boleh dikutip untuk" dan "Jangan". Tidak semua kartu wajib dipakai.
- `hasil_riset_v3*.md` — posisi riset, penelitian terdahulu, research gap, desain ringkas.
- `konteks_collector_data_v3*.md` — sistem pengumpulan data (API, cron, SQLite, candle/ticker).
- `hasil_eksperimen_v3*.md` — desain terkunci, hasil uji coba awal (bukan hasil skripsi), dan source code `prediksi_btc`.
- `konteks_skripsi_v3*.md` — arah penelitian dan aturan penulisan.
- `briefs/` — instruksi kerja per tugas.
- `arsip/` — dokumen v2.x. **Jangan dipakai.**

**Urutan otoritas:** brief terbaru > `kartu_paper_v3*` (isi paper) > `hasil_riset_v3*` > `konteks_collector_data_v3*` dan source code di `hasil_eksperimen_v3*` > `konteks_skripsi_v3*` > arsip.

## Aturan menulis
- **Jangan mengarang** angka, metadata referensi, klaim isi paper, atau parameter. Bila tidak bisa dipastikan, tulis komentar `% CEK: <alasan>` dan biarkan.
- Pertahankan semua `% CEK:` yang sudah ada kecuali brief menyuruh menghapus.
- Bahasa sederhana khas mahasiswa S1. Satu kalimat berisi satu gagasan. Tidak melebih-lebihkan klaim ("menunjukkan" atau "menemukan", bukan "membuktikan").
- Definisi memakai "merupakan". Tidak memakai titik dua di tengah kalimat.
- Sitasi IEEE via biblatex (`\cite{key}`), **tanpa nama penulis** di narasi. Hindari mengulang sitasi yang sama.
- Istilah asing `\textit{}` pada kemunculan pertama per bab, termasuk *trader*, *scalper*, *time frame*, *candle*, *hyperparameter*. Nama model dan metode (XGBoost, LightGBM, Grid Search, TPE) ditulis tegak.
- Singkatan ditulis kepanjangannya saat pertama kali muncul di setiap bab.
- "Naive" (kapital) = pembanding di penelitian ini. "model naive" = model naive di penelitian orang lain.
- Notasi pasar: **BTC/IDR** = spot Indodax (yang dipakai). Pasar spot selalu ditulis dengan garis miring.
- *Time frame* = jarak waktu prediksi (berapa menit ke depan harga diprediksi), bukan resolusi *candle*.
- Notasi: $P_t$ harga, $h$ *time frame*/horizon (menit), $r_{t,h}=\ln(P_{t+h}/P_t)$, $\hat{P}_{t+h}=P_t\exp(\hat{r}_{t,h})$. Simbol baru ditambahkan ke `frontmatter/daftar-notasi.tex`. Simbol v2.9 yang tidak dipakai lagi boleh dihapus hanya bila brief menyuruh.
- Rujuk persamaan, tabel, dan gambar dengan `\ref`/`\eqref`, jangan disalin ulang.
- Diagram konsep memakai TikZ di `assets/tikz-v3/`. Gambar data hanya dari keluaran pipeline `prediksi_btc`. Jangan menempel gambar dari paper; gambar ulang dan tulis "diadaptasi dari".

## `references.bib`
- Metadata diambil dari `https://api.crossref.org/works/<DOI>` atau doi.org. Jangan menimpa field yang sudah lebih lengkap (rentang halaman, nama depan, "The" di nama jurnal, tipe `@incollection`/`@inproceedings`). Entitas HTML (`&amp;`) dan karakter di luar Times New Roman (mis. U+2010) dinormalkan.
- Nomor artikel memakai `eid`, bukan `pages`.
- Entri di bawah komentar `ARSIP v2.9` hanya dipertahankan sampai Bab I–III v3.0 selesai.
- Judul yang berbeda substansi dari dokumen riset → laporkan ke Ferdi dan tandai kalimat pengutipnya dengan `% CEK:`; jangan menulis ulang kalimat sendiri.

## Build
- `make` → `build/praskripsi.pdf` (XeLaTeX + Biber via latexmk). `make check` → validasi format pedoman.
- Opsi `ketat` butuh font Times New Roman/Arial. Di mesin tanpa font itu, compile salinan dengan opsi `ketat` dihapus; jangan ubah `praskripsi.tex` asli.
- Setiap tugas selesai: jalankan `make check` dan laporkan jumlah halaman, overfull box, rujukan menggantung, missing character.
- Jangan commit/push kecuali Ferdi minta.

## Fakta kunci (ringkas)
- Judul final belum ditetapkan. Dosen pembimbing: Dr. Rizky Parlika, S.Kom, M.Kom.
- **Rumusan masalah:**
  1. Bagaimana membangun model XGBoost, LightGBM, CatBoost, dan AdaBoost untuk memprediksi harga BTC/IDR pada berbagai *time frame*?
  2. Bagaimana pengaruh optimasi *hyperparameter* terhadap akurasi keempat model tersebut?
  3. Model mana yang memiliki performa terbaik berdasarkan nilai MAE, RMSE, dan MAPE dibandingkan dengan Naive?
- **Data:** API publik Indodax; *collector* Python dijalankan cron tiap 1 menit di VPS (UTC) dan disimpan di SQLite. *Candle* 1 menit dari `tradingview/history_v2` (`tf=1`). **Indodax tidak menyediakan candle 5 menit**, jadi *candle* 5 menit dibentuk dari agregasi *candle* 1 menit. Snapshot ticker ikut disimpan, tetapi tidak dipakai dalam eksperimen.
- **Desain:**
  - *time frame* 1, 5, 15, 30, 60 menit (utama 5 menit; 1 menit hanya untuk *candle* 1 menit);
  - harga *typical* (high+low+close)/3; target *log return*, dikonversi ke rupiah;
  - fitur dari harga dan volume *candle* saja;
  - model XGBoost, LightGBM, CatBoost, AdaBoost (AdaBoost.R2) + Naive;
  - optimasi: default, Grid (27), Random, TPE, CMA-ES, GA (NSGA-II), QMC (30 *trial*); teknik tambahan *early stopping*, top-15 fitur, *loss* L1, *pruner* median;
  - validasi *walk-forward* 5 fold dengan jeda = *time frame*; *split* 80:20, 70:30, 60:40 berurutan waktu + *purging*;
  - metrik MAE, RMSE, MAPE, akurasi arah; uji Diebold-Mariano dengan koreksi HLN; koreksi Holm untuk uji berganda.
- **Menunggu keputusan dosen:** tanggal pasti periode data, ada/tidaknya aplikasi web, dan aturan menentukan "model terbaik" (dikunci sebelum eksperimen final).
