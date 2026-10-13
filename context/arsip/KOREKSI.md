# Koreksi terhadap Dokumen Konteks

Daftar bagian `hasil_riset_bitcoin_v2_5.md` dan `hasil_eksperimen_bitcoin_v2_5.md` yang salah atau usang. **Bila dokumen konteks bertentangan dengan file ini, ikuti file ini.** Diperbarui 10 Oktober 2026.

## A. Desain dan implementasi (`hasil_riset`, Bagian V)

| No | Dokumen menulis | Yang benar | Dasar |
|---|---|---|---|
| A1 | Status "Belum ada eksperimen"; Roadmap ⏳ | Eksperimen penuh selesai 6 Okt 2026 (config hash `0af5b5b98c60`) | `hasil_eksperimen` |
| A2 | Timestamp "milidetik → mikrodetik" | **Mikrodetik → milidetik.** Arsip Binance sejak 1 Jan 2025 memakai mikrodetik | `rvlib/data.py` |
| A3 | "Scaler di-fit per window latih" (V.7) | **Tidak ada scaler/standarisasi.** Jangan ditulis | kode |
| A4 | Hari tidak lengkap "drop/interpolasi" | Hari dengan bar < 95% (< 274/288) ditandai; pasangan (t, t+1) dibuang bila t **atau** t+1 tidak lengkap atau RV = 0. 27 hari ditandai | `rvlib/data.py` |
| A5 | Periode "~Agustus 2017" | 17 Agu 2017 – 30 Sep 2026; OOS mulai 1 Sep 2018 | `hasil_eksperimen` §3 |
| A6 | Era institutional "2021–2025" tanpa tanggal | Batas era **1 Januari 2021** | `config.py` |
| A7 | Penanda peristiwa: Mar 2020, Terra, FTX | **Lima**: + flash crash 17 Agu 2023 dan "10/10" (10 Okt 2025) | patch v1.2 |
| A8 | Fitur X dipakai HAR-X dan LGBM-X | Log Amihud **dibuang dari HAR-X** (VIF 19,6); hanya LGBM-X | `hasil_eksperimen` §6 |
| A9 | Tools R (`strucchange`, `sandwich`) | Semua uji di Python. HAC diverifikasi identik dengan `sandwich::kernHAC`. R hanya untuk CI tanggal break (opsional, tidak relevan karena 0 break) | kode |
| A10 | Nilai kritis dari tabel Bai–Perron | **Disimulasikan** (CV 5% UDmax 9,01; tabel ~8,88 sebagai pembanding) | `rvlib/stats.py` |
| A11 | Tuning "forward-chaining" saja | Grid + perluasan tepi maks. 2 kali; batas bawah min_child_samples 5. LGBM-X terkunci di 5 (batas bawah) | `config.py` |
| A12 | Sensitivitas RV 5 menit subsampled dan retuning tahunan | **Belum dijalankan.** Jangan ditulis sebagai sudah/akan dilakukan kecuali Ferdi memutuskan | `hasil_eksperimen` §3.3 |

## B. Uji statistik

| No | Dokumen menulis | Yang benar |
|---|---|---|
| B1 | "Satu uji konfirmatori per RQ" (II, VI, VIII, X) | **Per hipotesis.** RQ2 punya H2a dan H2b; H2b = dua uji-t HAC (HAR-X−HAR, LGBM-X−LGBM-HAR) + koreksi Holm |
| B2 | RQ3 "uji-t HAC" | Uji-t HAC **dua sisi** pada $D_t$ (S2-365 vs S1), era institutional |
| B3 | `hasil_eksperimen` §3.1: "H3 ditolak" | **"H3 tidak didukung; arah sebaliknya signifikan (hipotesis tandingan)."** Hipotesis penelitian tidak "ditolak"; yang ditolak H0. (Hanya relevan untuk Bab IV) |

## C. Referensi (`hasil_riset`, Bagian III)

| No | Dokumen menulis | Yang benar |
|---|---|---|
| C1 | Akgun & Gulay (2025): "rolling vs expanding pada BTC (hanya GARCH)" | 11 model GARCH + ANN/LSTM/CNN; BTC, ETH, BNB s.d. akhir 2021. Perbandingan rolling vs expanding **dilaporkan rinci hanya untuk GARCH**; rolling umumnya lebih akurat. Tanpa HAR, tanpa uji signifikansi. (Diverifikasi dari full text) |
| C2 | Feng (2024), penulis tunggal, judul "Rolling window, expanding window, or both?" | Feng, Zhang & Wang (2024), "Out-of-sample volatility prediction: Rolling window, expanding window, or both?" |
| C3 | Liu, Patton & Sheppard (2015) 187(2) | **187(1)**, 293–311 |
| C4 | Zhang dkk. (2024): "proxy likuiditas harian di kripto" | Judul: "Relationships among return and liquidity of cryptocurrencies" |
| C5 | Qiu dkk. (2025): "spesifikasi tetap tidak universal" | Judul: "Predicting cryptocurrency volatility: The power of model clustering" (isi belum dibaca) |
| C6 | Nama depan penulis di beberapa entri | Ikuti `bibliography/references.bib` (sudah diverifikasi Crossref) |
| C7 | Paper Parlika dkk. (dosen pembimbing) | **Dikeluarkan dari pertimbangan** atas permintaan Ferdi; jangan dipakai sebagai argumen |

## D. Masih terbuka (jangan diisi tebakan)
- Full text belum dibaca: Chassot & Audrino (2026), Feng, Qi & Lucey (2024) — penentu kebaruan RQ3; Giacomini & Rossi (2010), Trucíos & Taylor (2023), Christensen dkk. (2023), Qiu dkk. (2025).
- Judul final, pembimbing II, dan jadwal penelitian: dari Ferdi/prodi.
- `perhitungan_manual.md`: jumlah n per daun pohon ke-1 (256) tidak konsisten dengan bagging 80% dari 339 obs; jangan tampilkan n per daun sampai dijelaskan.
