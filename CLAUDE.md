# Praskripsi Ferdi — Prediksi Harga BTC/IDR dengan Model Boosting (v3.0)

Repo LaTeX praskripsi (proposal) Informatika UPN "Veteran" Jawa Timur, kelas `upnjatim-skripsi.cls`. Penulis: Ferdi Endahas Ahmad. Komunikasi dengan Ferdi: bahasa Indonesia santai (gw/lu), langsung, ringkas.

> **Topik lama (v2.x: LightGBM vs HAR-RV, realized variance, Binance BTC/USDT) sudah tidak dipakai.** Isinya hanya ada di `context/arsip/` dan `chapters/arsip-v2.9/`. Jangan dijadikan acuan.

## Status
- **Praskripsi.** Bab I–III saja.
- Eksperimen 14–20 Okt 2026 (satu minggu) hanya **uji coba awal**. Eksperimen final dijalankan Februari 2027 dengan data Oktober 2026 – Februari 2027.
- **Hasil eksperimen tidak boleh muncul di Bab I–III**, termasuk angka MAE, persentase vs Naive, model/metode/horizon terbaik. Yang boleh: desain, deskripsi data, alasan pemilihan metode, literatur, dan angka dari paper orang lain yang tercatat di kartu.

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
- Notasi pasar: **BTC/IDR** = harga Bitcoin dalam rupiah. Sumber datanya API publik Indodax. Pasar spot selalu ditulis dengan garis miring.
- **Objek penelitian = harga BTC/IDR, bukan "pasar Indodax".** Indodax hanya disebut sebagai sumber data (API, *collector*, kelipatan harga Rp1.000, *candle* yang tersedia). Jangan menulis "pasar spot Indodax", "harga Bitcoin di Indodax", "prediksi untuk Indodax", atau istilah "oracle". Penelitian tidak membuat sistem prediksi untuk platform tertentu. Keterbatasan yang wajib tetap ada: data berasal dari satu sumber, sehingga hasil berlaku untuk data harga dari sumber tersebut.
- **Istilah baku (23 Nov 2026), jangan dicampur:**
  - **horizon prediksi** ($h$) = berapa menit ke depan harga diprediksi (1, 5, 15, 30, 60 menit). Cukup "horizon" setelah disebut lengkap. Di bagian tipe *trader*, lama pegang posisi ditulis "horizon waktu".
  - ***time frame*** = lama satu *candle* (1 menit, 5 menit), sesuai istilah trader. **Jangan** memakai *time frame* untuk jarak prediksi, dan jangan memakai "resolusi *candle*".
  - **data latih** (bukan "periode pengembangan"), **data uji** (bukan "blok uji final"), **data validasi** pada *fold* (bukan "blok validasi").
  - **metode optimasi** (*hyperparameter*), bukan "strategi *tuning*"; **MAE validasi**, bukan "skor validasi"; "kombinasi dataset dan horizon", bukan "pasangan".
  - **prediksi**/**memprediksi** untuk keluaran model (bukan "ramalan"); "peramalan" hanya untuk nama bidang (*forecasting*).
  - ***trial*** untuk satu percobaan *tuning* (bukan "percobaan"/"anggaran percobaan"); ***default*** (pengaturan bawaan pustaka).
  - ***candle*** di narasi (bukan "bar"); "*candle* tanpa transaksi (volume nol)"; "ditetapkan" (bukan "dikunci") di narasi.
  - Kode `prediksi_btc` tetap memakai nama lama (`horizon_menit`, `t_u`, `hasil_uji_final.csv`); jangan ubah kode hanya karena istilah.
- Notasi: $P_t$ harga, $h$ horizon prediksi (menit), $r_{t,h}=\ln(P_{t+h}/P_t)$, $\hat{P}_{t+h}=P_t\exp(\hat{r}_{t,h})$. Simbol baru ditambahkan ke `frontmatter/daftar-notasi.tex`. Simbol v2.9 yang tidak dipakai lagi boleh dihapus hanya bila brief menyuruh.
- Rujuk persamaan, tabel, dan gambar dengan `\ref`/`\eqref`, jangan disalin ulang.
- **Contoh perhitungan manual** (`chapters/bab3-contoh-perhitungan.tex`) memakai **angka permisalan** yang ditulis manual (24 Nov 2026): 6 baris latih, 3 baris uji, fitur $x_1$/$x_2$, $\nu = 0{,}5$, 1 bp ≈ Rp100.000. Bila angka diubah, hitung ulang semua langkah dan cocokkan XGBoost/LightGBM/CatBoost (mode Plain) dengan pustaka aslinya. Ilustrasi *ordered boosting* di contoh hanya menjelaskan ide; eksperimen memakai CatBoost mode Plain (`boosting_type="Plain"` di kode, 27 Nov 2026). Contoh dengan data asli ada di `chapters/lampiran-contoh-data-asli.tex` (keluaran `scripts/contoh_manual.py`, belum di-`\input`).
- **Tata letak (panduan format, 27 Nov 2026):**
  - **Prinsip gambar (keputusan Ferdi 27 Nov 2026):** (1) sebelum gambar, perkenalkan konteks dan rujuk nomornya ("ditunjukkan pada Gambar~\ref{...}"); (2) letakkan `figure` sesudah paragraf yang pertama kali merujuknya; (3) sesudah gambar, jelaskan isi, ciri, atau tafsirannya. Pembuka penjelasan boleh bervariasi ("Pada Gambar ...", "Berdasarkan Gambar ...", "Gambar ... menunjukkan ..."). `flafter` dipakai agar gambar tidak muncul di atas rujukannya.
  - Tidak ada ruang kosong > 3 cm, kecuali halaman terakhir bab. Jangan pakai `[H]`; gambar memakai `[!htbp]`.
  - Setelah compile, jalankan `python scripts/cek_tata_letak.py build/praskripsi.pdf`. Hasil harus 0 pelanggaran gambar (gambar muncul sebelum dirujuk). Ruang kosong hanya boleh di akhir bab atau daftar.
  - Tabel daftar diberi kolom No, dan judul kolom ditulis tebal. Hindari kode RM1/RQ1 di naskah; tulis "rumusan masalah pertama".
  - Grafik data Bab III (`fig:statdata`) dibuat dari `scripts/grafik_data.py`, yang memakai `btcpred.data.load`. Datanya ada di `assets/data/`, dan grafik memakai pgfplots hitam-putih.
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
- Judul sementara: "Prediksi Harga BTC/IDR Jangka Pendek dengan Model Boosting dan Optimasi Hyperparameter" (23 Nov 2026); final diputuskan bersama dosen. Dosen pembimbing: Dr. Rizky Parlika, S.Kom, M.Kom.
- **Rumusan masalah:**
  1. Bagaimana membangun model XGBoost, LightGBM, CatBoost, dan AdaBoost untuk memprediksi harga BTC/IDR pada berbagai horizon prediksi?
  2. Bagaimana pengaruh optimasi *hyperparameter* terhadap akurasi keempat model tersebut?
  3. Model mana yang memiliki performa terbaik berdasarkan nilai MAE, RMSE, dan MAPE dibandingkan dengan Naive?
- **Data:** API publik Indodax; *collector* Python dijalankan cron tiap 1 menit di VPS (UTC) dan disimpan di SQLite. *Candle* 1 menit dari `tradingview/history_v2` (`tf=1`). **Indodax tidak menyediakan candle 5 menit**, jadi *candle* 5 menit dibentuk dari agregasi *candle* 1 menit. Snapshot ticker ikut disimpan, tetapi tidak dipakai dalam eksperimen.
- **Desain:**
  - horizon prediksi 1, 5, 15, 30, 60 menit (1 menit hanya untuk *candle* 1 menit); *time frame* *candle* 1 dan 5 menit;
  - harga *typical* (high+low+close)/3; target *log return*, dikonversi ke rupiah;
  - fitur dari harga dan volume *candle* saja;
  - model XGBoost, LightGBM, CatBoost, AdaBoost (AdaBoost.R2) + Naive;
  - optimasi: default, Grid (27), Random, TPE, CMA-ES, GA (NSGA-II), QMC (30 *trial*); teknik tambahan *early stopping*, top-15 fitur, *loss* L1, *pruner* median;
  - data latih ±80% + data uji 20% (*purging* berbasis waktu); validasi *walk-forward* 5 fold dengan *purging* berbasis waktu; Tahap 3 = panjang data latih 100/75/50%;
  - metrik MAE, RMSE, MAPE, akurasi arah; uji Diebold-Mariano dengan koreksi HLN; koreksi Holm untuk uji berganda;
  - Tahap 1 dan 2 memilih dari median MAE validasi vs Naive 4 model (rata-rata dua nilai tengah); RM2 diuji dengan DM metode optimasi terpilih vs default (keluarga Holm sendiri).
- **Menunggu keputusan dosen:** tanggal pasti periode data, ada/tidaknya aplikasi web, dan aturan menentukan "model terbaik" (dikunci sebelum eksperimen final).
