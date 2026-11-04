# Riset Skripsi v3.0: Prediksi Harga BTC/IDR Jangka Pendek dengan Model Boosting dan Optimasi Hyperparameter

> **Status (1 November 2026):** desain sudah dijalankan pada data satu minggu (14–20 Okt 2026); hasil dan kode ada di `hasil_eksperimen_v3.0.md`. Referensi ada di `kartu_paper_v3.md` (46 kartu). **Judul, rumusan masalah, dan tujuan di dokumen ini masih USULAN** dan perlu disetujui dosen pembimbing.
>
> **Menggantikan:** `hasil_riset_bitcoin_v2.9.md` (versi realized variance / HAR-RV, sekarang arsip).
>
> **Aturan sumber:** klaim tentang isi paper hanya boleh ditulis bila tercatat di `kartu_paper_v3.md`, beserta lokasinya. Kode kartu ditulis dalam kurung, misalnya (A1). Tanda ⚠ = belum terverifikasi atau masih menunggu keputusan.
>
> **Aturan Bab I–III:** hasil eksperimen (angka MAE, peringkat model, metode optimasi terbaik, horizon terbaik) **tidak boleh** muncul di Bab I–III. Yang boleh: desain, data, alasan pemilihan metode, dan literatur.
>
> **Notasi:** BTC/IDR = pasar spot Indodax. "Naive" = prediksi bahwa harga h menit lagi sama dengan harga sekarang. "MAE vs Naive (%)" negatif = model lebih akurat dari Naive.

---

## 0. Ringkasan perubahan dari v2.9

| Aspek | v2.9 (arsip) | v3.0 (sekarang) | Dasar |
|---|---|---|---|
| Target | Realized variance harian | **Harga** BTC/IDR beberapa menit ke depan (lewat return) | Bimbingan 20 dan 23 Okt 2026 |
| Data | Binance BTC/USDT 2017–2026, arsip | **Indodax BTC/IDR**, dikumpulkan sendiri lewat API (candle 1 menit, ticker 5 menit) | Arahan dosen |
| Model | HAR, HAR-X, LGBM-HAR, LGBM-X | **XGBoost, LightGBM, CatBoost, AdaBoost** | Arahan dosen |
| Pembanding | HAR-RV | **Naive** | HAR tidak cocok untuk target harga |
| Fokus | Kestabilan kinerja relatif lintas era | **Model, metode optimasi, rasio split, dan time frame** terbaik | Arahan dosen |
| Metrik | QLIKE | MAE, RMSE, MAPE, akurasi arah, uji DM (koreksi HLN) | — |
| Istilah realized variance | Inti penelitian | **Tidak dipakai** | Dosen: membingungkan |

---

## I. Posisi riset

### Pertanyaan utama
Model boosting mana, dengan optimasi hyperparameter apa, dan pada time frame berapa, yang memberi prediksi harga BTC/IDR beberapa menit ke depan paling akurat, **dibandingkan dengan Naive**?

### Kalimat inti
> "Saya membandingkan empat model boosting yang dioptimasi dengan berbagai metode, untuk memprediksi harga Bitcoin di Indodax beberapa menit ke depan, lalu menguji apakah prediksinya benar-benar lebih baik dari tebakan paling sederhana, yaitu harga tidak berubah."

### Acuan utama: Rodrigues & Machado (2025), *Information* 16(4), 300 (A1)

| Aspek | Rodrigues & Machado (2025) | Riset ini |
|---|---|---|
| Data | Harga per menit 10 kripto, 30 hari, YFinance, USD (hlm. 9–10) | BTC/IDR Indodax, candle 1 menit dan ticker 5 menit, dikumpulkan sendiri |
| Target | Nilai harga (regresi), horizon utama 60 menit (hlm. 10) | Nilai harga lewat return, horizon 1, 5, 15, 30, 60 menit |
| Model boosting | XGBoost dan LightGBM, **setelan bawaan** (hlm. 11) | XGBoost, LightGBM, CatBoost, AdaBoost, **semua dituning** |
| Optimasi | Grid search hanya untuk LSTM/GRU (hlm. 10–11) | 7 metode (default, grid, random, TPE, CMA-ES, GA, QMC) + 4 teknik tambahan |
| Pembanding | **Tidak ada naive** | Naive |
| Uji statistik | Wilcoxon, memakai data di luar periode dataset (Tabel 4, hlm. 12) | Diebold-Mariano dengan koreksi HLN |
| Pembagian data | Satu split 80/10/10; **MinMaxScaler dipasang sebelum split** (hlm. 9) | Tiga rasio (80:20, 70:30, 60:40), berurutan waktu, tanpa scaler, *purging* |

**Kalimat posisi:** *"Penelitian ini mengembangkan Rodrigues & Machado (2025) dengan membandingkan empat model boosting yang dioptimasi dengan berbagai metode hyperparameter pada data BTC/IDR per menit, memakai Naive sebagai pembanding, dan menguji perbedaan akurasinya dengan uji Diebold-Mariano."*

Tulis "mengembangkan", bukan "mengikuti". Model terbaik di A1 adalah GRU, bukan boosting.

### Acuan pendukung

| Peran | Paper | Kode |
|---|---|---|
| Cara evaluasi (MDM, kontrol *data snooping*) | Wei dkk. (2023), J. Forecasting 42(4) | A2 |
| Horizon menit 1–60 dan uji DM | Jaquart dkk. (2021), JFDS 7 | B2 |
| Preseden beberapa rasio split pada Bitcoin intraday | Akyildirim dkk. (2023), AnnOR 330 | B3 |
| Naive sulit dikalahkan | Puoti dkk. (2024), AIMLSystems | B5 |
| LightGBM dan AdaBoost kompetitif untuk BTC | Bouteska dkk. (2024), IRFA 92 | B1 |

### Yang TIDAK diklaim
- Tidak mengklaim model ML mengalahkan pasar atau memberi keuntungan trading. Biaya transaksi tidak diuji.
- Tidak mengklaim pemetaan horizon ke tipe trader sebagai fakta di pasar kripto. Pemetaan itu **asumsi penelitian** berdasarkan teori pasar heterogen (C1, C2) dan bukti terbatas di kripto (C5, C6).
- Tidak mengklaim hasil berlaku umum untuk semua periode. Data hanya satu minggu (⚠ menunggu keputusan dosen).
- Tidak mengklaim sebagai studi pertama yang membandingkan boosting untuk kripto. Yang belum ditemukan adalah **gabungan** unsur di Bagian IV.

---

## II. Konsep kunci

| Konsep | Pengertian | Peran |
|---|---|---|
| Return log | ln(harga t+h / harga t) | Target yang dipelajari model |
| Konversi ke rupiah | harga_prediksi = harga_sekarang × exp(return_prediksi) | Supaya metrik dalam rupiah |
| Naive | Prediksi harga h menit lagi = harga sekarang | Pembanding utama |
| Horizon / time frame | Berapa menit ke depan harga diprediksi | Variabel yang diuji |
| Harga typical | (high + low + close) / 3 untuk candle | Mengurangi efek loncatan bid-ask |
| Harga mid | (bid + ask) / 2 untuk ticker | Sama |
| Gradient boosting | Gabungan pohon yang dibangun berurutan, tiap pohon memperbaiki galat sebelumnya (E1) | Dasar XGBoost, LightGBM, CatBoost |
| AdaBoost.R2 | Boosting regresi dengan pembobotan ulang sampel dan median berbobot (E9) | Versi AdaBoost yang dipakai |
| Walk-forward CV | Validasi berurutan waktu: latih di masa lalu, uji di masa depan (G4) | Tuning tanpa kebocoran |
| *Purging* | Membuang h baris terakhir data latih karena targetnya masuk periode uji | Mencegah kebocoran |
| Uji DM + HLN | Uji apakah dua **ramalan** berbeda akurasinya, dengan koreksi sampel kecil (G1, G2) | Uji model vs Naive |
| Pasar heterogen | Pelaku pasar berbeda menurut horizon waktu (C1) | Dasar kaitan time frame dan trader |
| Efisiensi bentuk lemah | Harga tidak bisa diprediksi dari histori harga (D4) | Alasan Naive sulit dikalahkan |

---

## III. Literatur

### III.1 Penelitian terdahulu (research gap, 2021–2026)

| Kode | Paper | Data | Target | Model boosting | Tuning | Naive harga | Uji signifikansi |
|---|---|---|---|---|---|---|---|
| A1 | Rodrigues & Machado (2025) | Menit, 30 hari | Harga | XGB, LGBM | ✗ (bawaan) | ✗ | Wilcoxon |
| A2 | Wei dkk. (2023) | Harian | Return (kombinasi ramalan) | XGB, LGBM | tidak dicatat | ✗ | MDM, MCS, SPA |
| B1 | Bouteska dkk. (2024) | Harian | Return | AdaBoost, LGBM | Grid | ✗ (RW pada return) | Friedman |
| B2 | Jaquart dkk. (2021) | Menit, 1–60 mnt | **Arah** | XGB (GBC) | Grid | ✗ (acak 50%) | DM |
| B3 | Akyildirim dkk. (2023) | 5–60 menit, *futures* CME | **Arah** | XGB | tidak dicatat | ✗ (RW = 50%) | Uji t |
| B4 | Akyildirim dkk. (2021) | 15–60 menit + harian | **Arah** | ✗ | — | ✗ | ✗ |
| B5 | Puoti dkk. (2024) | Harian | Harga | XGB | tidak disebut | ✓ | tidak jelas |
| B8 | Oprea & Bâra (2026) | Harian | Harga | XGB (*meta-learner*) | tidak dicatat | tidak dicatat | DM |
| — | **Riset ini** | Menit (1 dan 5) | Harga | **4 model** | **7 metode + 4 teknik** | ✓ | DM + HLN |

Pendukung minor: B6 Dudek dkk. (2025, preprint; target volatilitas), B7 Nadarajah dkk. (2025; boosting bawaan untuk volatilitas).

### III.2 Horizon waktu dan tipe trader

| Kode | Isi yang boleh dikutip | Batasan |
|---|---|---|
| C1 Müller dkk. (1997) | Pasar terdiri dari komponen dengan horizon berbeda. Tabel 3 (hlm. 226): komponen 1 (7–80 menit) dealer intraday jangka pendek dan *market maker*; komponen 2 (16 menit – 3,5 jam) dealer intraday; komponen 5 (1–3,5 hari) trader jangka menengah | Data FX; penulis menyebut deskripsinya "tentative" |
| C2 Dacorogna dkk. (1995) | Strategi dengan horizon dan frekuensi berbeda punya profil risiko berbeda | Data FX |
| C3 Barber dkk. (2014) | Kurang dari 1% *day trader* konsisten untung setelah biaya | Saham Taiwan; isi dari versi WP |
| C4 Kirilenko dkk. (2017) | Tipe trader (HFT, *market maker*, fundamental) bisa dibedakan dari horizon dan perilaku | Futures S&P 500 |
| C5 Kakinaka & Umeno (2022) | Perilaku harga BTC dan ETH berbeda antara horizon pendek dan panjang (*crossover* ±10 hari) | "Pendek" di sini < 10 hari, bukan menit |
| C6 Liu dkk. (2023) | Pengguna Bitcoin terbagi menjadi tipe trader menurut lama pegang posisi: teknikal ≤ 5 hari, fundamental ±22 hari, HFT harian (hlm. 10) | Data *on-chain*, bukan bursa; tidak memakai istilah scalper/swing |

**Kesimpulan untuk skripsi:** literatur mendukung bahwa pelaku pasar berbeda menurut horizon waktunya, termasuk di kripto (C5, C6). Tetapi belum ada paper yang memetakan **horizon menit tertentu ke scalper atau swing trader di pasar kripto**. Pemetaan horizon di skripsi ditulis sebagai asumsi berdasarkan C1, bukan temuan.

### III.3 Pasar Bitcoin dan efisiensi

| Kode | Isi | Dipakai untuk |
|---|---|---|
| D4 Yi dkk. (2023) | Bitcoin mendekati efisien bentuk lemah | Alasan Naive sulit dikalahkan |
| D3 Mokni dkk. (2024) | Efisiensi Bitcoin berubah-waktu | Alasan hasil bisa berbeda antar-periode uji |
| D2 Do (2026) | Era institusional mendekati *random walk* (Hurst 0,48; hlm. 9) | Sama dengan D4, untuk periode terbaru |
| D1 Nakamoto (2008) | Definisi Bitcoin | Latar belakang (PDF belum dibaca, jangan kutip isi spesifik) |

### III.4 Landasan metode

| Topik | Kode | Catatan penting |
|---|---|---|
| Gradient boosting, loss absolut (LAD), *learning rate* | E1 Friedman (2001) | Dasar loss L1 (Alg. 3, hlm. 1196) |
| XGBoost | E5 Chen & Guestrin (2016) | Regularisasi L2 bobot daun |
| LightGBM | E4 Ke dkk. (2017), E6 dokumentasi | *Leaf-wise* dan risiko *overfitting* berasal dari dokumentasi, bukan paper |
| CatBoost | E3 Prokhorenkova dkk. (2018) | *Ordered boosting*, pohon simetris; mode Ordered berguna di data kecil |
| AdaBoost | E2 Freund & Schapire (1997) + **E9 Drucker (1997)** + E10 dokumentasi sklearn | `AdaBoostRegressor` = AdaBoost.R2 (Drucker), bukan AdaBoost asli |
| Pemilihan model pohon | E7 Grinsztajn dkk. (2022), E8 Makridakis dkk. (2022) | Grinsztajn mengeluarkan deret waktu; M5 bergantung banyak deret |
| Grid vs Random Search | F1 Bergstra & Bengio (2012) | Random lebih efisien; dimensi efektif rendah |
| TPE | F2 Bergstra dkk. (2011) | Definisi ℓ(x), g(x), kuantil γ |
| Optuna | F3 Akiba dkk. (2019) + F7 dokumentasi 5.0.0 | Paper tidak membahas NSGA-II, QMC, MedianPruner |
| CMA-ES | F4 Hansen & Ostermeier (2001) + F7 | Optuna tidak mendukung parameter kategorikal di CMA-ES |
| Genetic Algorithm | F5 Deb dkk. (2002) | Pada satu objektif praktis menjadi GA elitis biasa |
| Hyperband | F6 Li dkk. (2018) | Untuk HyperbandPruner, bukan MedianPruner |
| Quasi-Monte Carlo (Sobol) | F8 Sobol' (1967), F9 Roy dkk. (2023), F10 dokumentasi SciPy | Keseimbangan Sobol hanya terjamin bila jumlah sampel pangkat 2 |
| Uji DM | G2 Diebold & Mariano (1995) + G1 Harvey dkk. (1997) | Tulis "dua ramalan", bukan "dua model" |
| Validasi deret waktu | G4 Cerqueira dkk. (2020) | Istilah paper: *prequential in blocks* |
| Satu periode uji rentan | G5 Tashman (2000) | Dasar memakai beberapa rasio split |
| Uji berganda | G3 Holm (1979) | Untuk membahas 92 uji |
| Fitur range | H1 Parkinson (1980) | Bila fitur range high-low disebut |

### III.5 Tidak dipakai

| Paper | Alasan |
|---|---|
| Kharola (2026), Oyedele (2023), Qureshi (2025), Zhu (2023) | Kejanggalan metodologi berat (K1–K4) |
| Petukhina dkk. (2021) | Tidak meramal dan tidak memetakan horizon ke trader (K5) |
| Gradojevic dkk. (2023), Karaa dkk. (2024) | Keputusan 1 Nov 2026 |
| **Zhivkov & Kandilarov (2026)** | **Tidak ditemukan di mana pun; kemungkinan referensi karangan. Jangan dikutip.** Konsekuensinya, klaim "TPE terbukti terbaik untuk prediksi kripto" tidak punya sumber. |
| Semua literatur HAR, realized variance, uji kestabilan, likuiditas | Arsip v2.9 |

### III.6 Sintesis literatur

1. **Prediksi harga kripto dengan boosting sudah banyak dilakukan,** tetapi sebagian besar memakai data harian (A2, B1, B5, B8). **Benchmarking saja bukan kontribusi.**
2. **Studi data menit kebanyakan memprediksi arah, bukan nilai harga** (B2, B3, B4). Studi nilai harga per menit yang paling dekat (A1) tidak menuning boosting dan tidak memakai naive.
3. **Pembanding naive harga jarang dipakai dengan benar.** Bouteska dkk. menghitung *random walk* pada return, sehingga bukan naive harga (B1, poin 11). Pada studi arah, *random walk* hanya berarti akurasi 50% (B2, B3).
4. **Ketika naive dipakai, naive sulit dikalahkan** (B5). Ini sejalan dengan Bitcoin yang mendekati efisien bentuk lemah (D2, D4).
5. **Optimasi hyperparameter sering diabaikan atau hanya satu metode.** A1 dan B7 memakai setelan bawaan; B1 dan B2 hanya grid search. Literatur metode menunjukkan Random Search lebih efisien dari Grid (F1) dan TPE lebih baik dari Random pada tugas sulit (F2), tetapi bukti itu dari jaringan saraf, bukan boosting untuk harga kripto.
6. **Keterdugaan Bitcoin jangka pendek kecil.** Akurasi arah sekitar 51–56% (B2, B3); keuntungan sebelum biaya bisa berubah menjadi rugi setelah biaya (B2). Di saham, kurang dari 1% *day trader* konsisten untung setelah biaya (C3).
7. **Satu periode uji rentan terhadap kejadian unik** (G5), dan efisiensi Bitcoin berubah-waktu (D3). Beberapa rasio split sudah dipakai pada Bitcoin intraday (B3), tetapi untuk target arah.
8. **Pelaku pasar berbeda menurut horizon waktu** (C1, C2), juga di Bitcoin (C5, C6). Belum ditemukan pemetaan langsung horizon menit ke tipe trader kripto.

---

## IV. Research gap

**Sejauh literatur yang diperiksa,** belum ditemukan penelitian yang sekaligus:
1. memprediksi **nilai harga** Bitcoin (bukan arah) pada **data per menit** dengan beberapa horizon;
2. membandingkan **keempat model boosting** (XGBoost, LightGBM, CatBoost, AdaBoost) yang **semuanya dituning**;
3. membandingkan **banyak metode optimasi hyperparameter** sekaligus (grid, random, TPE, CMA-ES, GA, QMC) beserta teknik tambahan;
4. memakai **naive harga** sebagai pembanding dan **uji Diebold-Mariano** untuk menilai perbedaan akurasi;
5. memakai data **BTC/IDR** dari bursa Indonesia yang dikumpulkan langsung.

### Checklist novelty

| Paper | Yang sudah dilakukan (wajib diakui) | Yang belum |
|---|---|---|
| A1 Rodrigues & Machado (2025) | Harga per menit, XGB dan LGBM, horizon pendek | Tuning boosting, CatBoost/AdaBoost, naive, DM, beberapa split |
| A2 Wei dkk. (2023) | XGB vs LGBM untuk BTC, MDM + MCS + SPA | Data intraday, naive harga, peramal langsung |
| B1 Bouteska dkk. (2024) | AdaBoost vs LightGBM untuk BTC, grid search | Data intraday, naive harga, DM, XGB/CatBoost |
| B2 Jaquart dkk. (2021) | Horizon 1–60 menit, DM, biaya transaksi | Target nilai harga, 4 booster, banyak metode optimasi |
| B3 Akyildirim dkk. (2023) | Data intraday, tiga rasio split | Target harga, pasar spot, naive harga, DM |
| B5 Puoti dkk. (2024) | Naive vs ML untuk harga kripto | Data intraday, tuning, DM yang jelas |

**Kontribusi Informatika:** rancangan eksperimen yang membandingkan model dan metode optimasi secara setara (jatah trial sama, walk-forward CV, tanpa kebocoran data), dengan pembanding naive dan uji statistik. Kontribusinya bukan pada teori keuangan.

---

## V. Rancangan penelitian (ringkas)

Rincian lengkap dan kode: `hasil_eksperimen_v3.0.md` Bagian 3 dan Lampiran B.

| Komponen | Keputusan | Dasar |
|---|---|---|
| Data | Indodax BTC/IDR, candle 1 menit dan ticker 5 menit, dikumpulkan via API di VPS | Arahan dosen |
| Periode | 14–20 Okt 2026 (satu minggu) | Arahan dosen 23 Okt; ⚠ kemungkinan diperpanjang sampai Februari 2027 |
| Harga | candle: typical; ticker: mid | Mengurangi loncatan bid-ask (autokorelasi return 1 menit: close −0,273, typical −0,073) |
| Target | Log return h menit ke depan, lalu dikonversi ke rupiah | Model pohon tidak bisa memprediksi di luar rentang data latih |
| Horizon | 1, 5, 15, 30, 60 menit | Dosen: time frame dicari lewat eksperimen. Rentang ini setara komponen 1–2 di C1 dan horizon B2 |
| Fitur | 42 (candle) / 32 (ticker): lag return, statistik bergulir 5–240 menit, range, volume, spread, jam | Hanya data sampai waktu t |
| Model | XGBoost (E5), LightGBM (E4), CatBoost (E3), AdaBoost.R2 (E9, E10) | Arahan dosen; model pohon untuk data tabular (E7) |
| Pembanding | Naive | Naive sulit dikalahkan (B5); efisiensi bentuk lemah (D4) |
| Optimasi | Default, Grid (27), Random, TPE, CMA-ES, GA (NSGA-II), QMC (30 trial) | F1–F10; dosen: "optimasi sebanyak mungkin" |
| Teknik tambahan | Early stopping, seleksi top-15 fitur, loss L1, pruner median | E1 (loss LAD), F6–F7 (pruning) |
| Validasi | Walk-forward 5 fold, jeda = horizon, hanya data latih | G4 |
| Split | 80:20, 70:30, 60:40 berurutan waktu + *purging* | Arahan dosen; G5; preseden B3 |
| Metrik | MAE (utama, relatif terhadap Naive), RMSE, MAPE, akurasi arah | — |
| Uji | DM dengan koreksi HLN, autokovarians lag h−1 | G1, G2; dipakai juga di B2 dan A2 |
| Tahapan | Tahap 1 time frame → Tahap 2 optimasi → Tahap 3 split → Tahap 4 teknik; aturan pemilihan dikunci 27 Okt 2026 10:08 WIB | Mencegah pemilihan mengikuti hasil |

### Catatan desain yang wajib ditulis di Bab 3

1. **AdaBoost memakai AdaBoost.R2** (E9, E10), bukan AdaBoost asli (E2). Pengaturan loss L1/L2 dan early stopping tidak berlaku untuk AdaBoost; AdaBoost punya parameter `loss` sendiri (linear, square, exponential) yang ikut dituning.
2. **TPE di Optuna bersifat multivariat** untuk satu objektif (F7), berbeda dari TPE independen di Bergstra dkk. (2011).
3. **CMA-ES tidak mendukung parameter kategorikal** (F7). Parameter `loss` AdaBoost pada run CMA-ES diambil acak oleh RandomSampler.
4. **NSGA-II dipakai untuk satu objektif.** Pada satu objektif, *nondominated sorting* sama dengan mengurutkan nilai objektif, jadi praktis GA elitis (F5). Dokumentasi Optuna tidak menyebut pemakaian ini (F7).
5. **QMC (Sobol) dengan 30 trial bukan pangkat 2**, sehingga sifat keseimbangan Sobol tidak terjamin (F10). Tulis sebagai keterbatasan.
6. **Random, TPE, CMA-ES, dan GA memakai seed yang sama,** sehingga beberapa trial awal identik.
7. **Grid Search 27 kombinasi, metode lain 30 trial.** Jumlah evaluasinya tidak persis sama.
8. **MedianPruner tidak punya rujukan paper** (F7). Kutip dokumentasi Optuna.

---

## VI. Usulan rumusan masalah, tujuan, dan judul (perlu persetujuan dosen)

> **Catatan anti-HARKing:** eksperimen data satu minggu sudah dijalankan. Karena itu rumusan masalah ditulis **netral** (bertanya "bagaimana", tidak mengandaikan model unggul), dan tidak boleh disusun ulang supaya cocok dengan hasil.

### Rumusan masalah (usulan)

| | Rumusan masalah | Tujuan |
|---|---|---|
| RM1 | Bagaimana perbandingan akurasi XGBoost, LightGBM, CatBoost, dan AdaBoost dalam memprediksi harga BTC/IDR beberapa menit ke depan, dibandingkan dengan Naive? | Membandingkan akurasi keempat model terhadap Naive |
| RM2 | Bagaimana pengaruh metode optimasi hyperparameter dan teknik optimasi tambahan terhadap akurasi keempat model tersebut? | Menganalisis pengaruh optimasi terhadap akurasi |
| RM3 | Pada time frame berapa model boosting memberikan akurasi relatif terhadap Naive yang terbaik? | Menentukan time frame dengan akurasi relatif terbaik |

Rasio split (80:20, 70:30, 60:40) masuk sebagai bagian dari desain pengujian di RM1–RM2, bukan rumusan tersendiri. Bisa dijadikan RM4 bila dosen menghendaki.

### Kandidat judul (≤ 15 kata)

| No | Judul | Kata |
|---|---|---|
| 1 | Perbandingan XGBoost, LightGBM, CatBoost, dan AdaBoost dengan Optimasi Hyperparameter untuk Prediksi Harga Bitcoin Jangka Pendek | 15 |
| 2 | Optimasi Hyperparameter Model Boosting untuk Prediksi Harga Bitcoin Jangka Pendek pada Berbagai Time Frame | 14 |
| 3 | Analisis Kinerja Model Boosting dan Optimasi Hyperparameter dalam Prediksi Harga BTC/IDR Beberapa Menit ke Depan | 15 |

Kandidat 1 paling eksplisit menyebut keempat model; kandidat 2 menonjolkan time frame; kandidat 3 menyebut objek BTC/IDR.

### Batasan penelitian (usulan)
- Objek BTC/IDR spot di Indodax saja.
- Data candle 1 menit dan ticker 5 menit periode 14–20 Okt 2026 (⚠ atau sampai Feb 2027).
- Model terbatas pada empat model boosting; pembanding Naive.
- Tidak menguji strategi trading, biaya transaksi, atau keuntungan.
- Fitur hanya dari data harga, volume, dan ticker Indodax (tanpa sentimen, berita, atau data *on-chain*).

---

## VII. Ringkasan hasil dan kaitannya dengan literatur (untuk Bab IV–V, bukan Bab I–III)

Rincian: `hasil_eksperimen_v3.0.md` Bagian 4–5.

| Temuan (data satu minggu) | Kaitan literatur | Batasan saat menulis |
|---|---|---|
| Hampir semua model tidak signifikan lebih baik dari Naive; 1 dari 92 run signifikan | Sejalan dengan B5 (naive sulit dikalahkan) dan D2, D4 (mendekati efisien bentuk lemah) | B5 data harian; 1 temuan tidak lolos koreksi uji berganda (G3) |
| Tanpa tuning, model 4–14% lebih buruk dari Naive | Menjelaskan kelemahan A1 dan B7 yang memakai setelan bawaan | — |
| TPE rata-rata terbaik, Random kedua, Grid di bawah Random | Sejalan dengan F1 (Random > Grid) dan F2 (TPE > Random) | Bukti F1–F2 dari jaringan saraf; tidak ada paper kripto yang mendukung "TPE terbaik" |
| LightGBM + loss L1 konfigurasi terbaik | LightGBM kompetitif untuk BTC (B1); loss absolut sesuai metrik MAE (E1) | B1 data harian dan target return |
| AdaBoost paling lemah | Berbeda dengan B1 (AdaBoost kompetitif harian) | Bedanya data harian vs menit |
| Keunggulan hanya di horizon 1 menit | **Berlawanan** dengan B2: keterdugaan naik seiring horizon makin panjang | B2 target arah; kemungkinan ada sisa efek bid-ask di data 1 menit |
| Keunggulan < 1% dan gerakan 1 menit ≈ spread | Untung sebelum biaya bisa jadi rugi setelah biaya (B2); <1% *day trader* untung setelah biaya (C3) | Biaya transaksi tidak diuji di skripsi |
| Hasil berbeda antar-rasio split | Satu periode uji rentan (G5); efisiensi berubah-waktu (D3) | — |
| Pruner median hemat ±36% waktu dengan akurasi hampir sama | Prinsip menghentikan trial jelek lebih awal (F6, F7) | MedianPruner tanpa rujukan paper |
| Seleksi top-15 fitur memperburuk hasil | — | Temuan sendiri, tanpa pembanding literatur |

---

## VIII. Risiko dan antisipasi pertanyaan penguji

| Pertanyaan | Jawaban |
|---|---|
| "Modelnya kalah dari Naive, apa kontribusinya?" | Hasil negatif tetap sah. Kontribusinya ada pada desain perbandingan yang setara dan jujur: semua model dituning, ada Naive, ada uji DM. Banyak penelitian sebelumnya tidak memakai naive (A1, A2) atau memakai *random walk* pada return (B1). |
| "Kenapa prediksi return, bukan harga langsung?" | Model pohon tidak bisa memprediksi di luar rentang data latih. Return kemudian dikonversi ke rupiah. |
| "Kenapa harga typical, bukan close?" | Close di data 1 menit meloncat antara harga bid dan ask (autokorelasi −0,273). Typical mengurangi efek ini (−0,073). |
| "Kenapa data cuma seminggu?" | Arahan dosen 23 Okt. ⚠ Bila diperpanjang, eksperimen diulang dengan aturan yang sama. |
| "AdaBoost yang dipakai yang mana?" | AdaBoost.R2 (Drucker, 1997), sesuai implementasi `AdaBoostRegressor` scikit-learn. |
| "Kenapa NSGA-II yang multiobjektif dipakai untuk satu objektif?" | Pada satu objektif, NSGA-II praktis menjadi GA elitis biasa (F5). |
| "Hubungan time frame dengan scalper/swing trader?" | Teori pasar heterogen (C1) membagi pelaku pasar menurut horizon; di Bitcoin tipe trader juga berbeda menurut lama pegang posisi (C6). Pemetaan spesifik ke scalper dan swing trader merupakan asumsi penelitian. |
| "Apakah hasilnya bisa dipakai trader?" | Belum. Keunggulan kurang dari 1% dan setara spread; biaya transaksi tidak diuji. |
| "Kenapa tidak deep learning?" | Arahan dosen (ML non-deep). Model pohon juga unggul pada data tabular berukuran menengah (E7), dengan catatan deret waktu dikeluarkan dari benchmark itu. |

---

## IX. Hal terbuka (⚠)

### Menunggu dosen
1. Data satu minggu atau sampai Februari 2027 (±40.000 baris).
2. Perlu output berupa aplikasi/dashboard atau tidak.
3. Cara menentukan model terbaik: konfigurasi terbaik (LightGBM) atau paling konsisten (XGBoost/LightGBM). **Aturannya belum dikunci**; kunci sebelum eksperimen ulang.
4. Judul, rumusan masalah, tujuan (Bagian VI).
5. Istilah data primer atau sekunder.

### Verifikasi referensi (sebelum masuk `.bib`)
- Kuartil jurnal *Information* (A1) di SCImago dan Sinta.
- Halaman dan judul versi ACM Puoti dkk. (B5).
- DOI dan judul resmi Kirilenko dkk. (C4).
- Volume dan halaman Liu dkk. (C6).
- Halaman prosiding ICML Drucker (E9).
- Nomor volume NIPS Bergstra dkk. 2011 (F2).
- Jurnal terjemahan Sobol' (F8).
- Semua DOI dibuka di doi.org.
- PDF Nakamoto (D1) belum dibaca.

### Keterbatasan eksperimen yang sudah diketahui
- QMC 30 trial bukan pangkat 2 (F10).
- 92 uji tanpa koreksi uji berganda pada hasil utama (G3).
- Seed sama untuk metode berbasis acak.
- Biaya transaksi dan spread tidak masuk evaluasi.

---

## X. Langkah berikutnya

| Tahap | Status |
|---|---|
| Eksperimen data satu minggu | ✅ 28 Okt 2026 (`hasil_eksperimen_v3.0.md`) |
| Kartu paper v3 | ✅ 1 Nov 2026 (46 kartu) |
| Dokumen riset v3.0 | ✅ dokumen ini |
| Bimbingan: 5 hal di Bagian IX | ⏳ 2 Nov 2026 |
| Verifikasi DOI dan kuartil | ⏳ |
| Bab III Metodologi | Bisa mulai setelah bimbingan |
| Bab II Tinjauan Pustaka | Setelah Bab III |
| Bab I Pendahuluan | Setelah rumusan masalah disetujui |
| Eksperimen ulang (bila data diperpanjang) | Setelah aturan pemilihan model dikunci |
