# Riset Skripsi v3.2: Prediksi Harga BTC/IDR pada Berbagai Time Frame dengan Model Boosting dan Optimasi Hyperparameter

> **Status (13 November 2026):** dua uji coba sudah dijalankan (P1: 14–20 Okt 2026; P2: 10 Okt – 10 Nov 2026). Desain final **v4** hasil review dosen 11 Nov 2026 sudah diimplementasikan di kode (`prediksi_btc`, commit `ed8b735`) dan sejalan dengan Bab III di repo `skripsi-latex` (v1.9). Eksperimen final dijalankan **Februari 2027**. Rincian hasil dan kode: `hasil_eksperimen_v3.3.md`. Referensi: `kartu_paper_v3.3.md` (A1–J4). **Judul masih sementara**; rumusan masalah mengikuti versi 6 Nov 2026 yang sudah dipakai di Bab I.
>
> **Menggantikan:** `hasil_riset_v3.1.md` dan `hasil_riset_v3.0.md` (arsip). Versi v2.9 (realized variance / HAR-RV) tetap arsip.
>
> **Aturan sumber:** klaim tentang isi paper hanya boleh ditulis bila tercatat di `kartu_paper_v3.3.md`, beserta lokasinya. Kode kartu ditulis dalam kurung, misalnya (A1). Tanda ⚠ = belum terverifikasi atau masih menunggu keputusan.
>
> **Aturan Bab I–III:** hasil eksperimen (angka MAE, peringkat model, metode optimasi terbaik, *time frame* terbaik) **tidak boleh** muncul di Bab I–III, termasuk hasil uji coba P1/P2. Yang boleh: desain, data, alasan pemilihan metode, dan literatur.
>
> **Notasi:** BTC/IDR = pasar spot Indodax. "Naive" = prediksi bahwa harga h menit lagi sama dengan harga sekarang. "MAE vs Naive (%)" negatif = model lebih akurat dari Naive. *Time frame* = jarak waktu prediksi (horizon), bukan resolusi *candle*.

---

## 0. Ringkasan perubahan

### Dari v3.1 ke v3.2 (13 Nov 2026, perbaikan)

| Bagian | v3.1 | v3.2 | Alasan |
|---|---|---|---|
| Peran Tashman (G5) | "Dasar menjaga blok uji tetap" | Dasar validasi *walk-forward* beberapa *fold* + **keterbatasan** blok uji final tunggal | G5 justru menyarankan *rolling origin* dan beberapa periode uji (kartu G5 v3.3) |
| *Time frame* di tabel desain | "utama 5 menit" | Dihapus; *time frame* dipilih di Tahap 1 dari skor validasi | Bertentangan dengan aturan Tahap 1 |
| Periode pengembangan | "80% data awal" | "±80% data awal (sedikit kurang karena *purging*)" | Sesuai kode: baris dengan t + h < t_u |
| Peran B3 | Preseden beberapa rasio split | ML untuk Bitcoin intraday; rasio split tidak lagi dipakai | Desain v4 |
| Aturan duplikat Holm | Hanya dicatat sebagai ketidaksesuaian | Rekomendasi: Bab III mengikuti kode (Bagian IX) | Aturan lintas tahap ambigu |
| Verifikasi referensi | Daftar 1 Nov | Diperbarui sesuai `references.bib` (Crossref 4 dan 10 Nov) | Banyak butir sudah selesai |

### Dari v3.0 ke v3.1

| Aspek | v3.0 (1 Nov 2026) | v3.1 | Dasar |
|---|---|---|---|
| Dataset | candle 1 menit + **ticker 5 menit** | candle 1 menit + **candle 5 menit** (agregasi candle 1 menit) | Indodax tidak menyediakan candle 5 menit (H3); keputusan 4 Nov; review dosen 11 Nov |
| Harga | typical (candle), mid (ticker) | typical saja | Ticker tidak dipakai |
| Periode | satu minggu (⚠ mungkin sampai Feb) | **Okt 2026 – Feb 2027** (Bab I: 10 Okt 2026 – 10 Feb 2027) | Keputusan 6 Nov; uji coba hanya sementara |
| Pembagian data | split 80:20 / 70:30 / 60:40 berbasis baris | **blok uji final tetap 20% terakhir**; Tahap 3 memvariasikan **panjang data latih** 100/75/50%; purging berbasis waktu | Review dosen 11 Nov |
| Pemilihan Tahap 1–2 | dari data uji | **dari skor validasi saja**; dikunci sebelum blok uji dibuka | Review dosen 11 Nov |
| Objektif tuning | MAE return | **MAE rupiah** + skor Naive di validasi | Review dosen 11 Nov |
| Seleksi top-15 | di luar fold | **di dalam fold** | Review dosen 11 Nov |
| Uji signifikansi | DM + HLN | DM + HLN pada grid waktu rapat + **koreksi Holm** per tahap (G3) | Review dosen 11 Nov |
| Akurasi arah | proporsi arah benar | + baseline tanda return bar terakhir, % harga tetap/naik/turun (I7) | Review dosen 11 Nov |
| Rumusan masalah | usulan RM1–RM3 (perbandingan, optimasi, time frame) | **RM 6 Nov**: membangun model → pengaruh optimasi → model terbaik (Bagian VI) | Bab I |
| Referensi | 46 kartu (`kartu_paper_v3.md`) | `kartu_paper_v3.2.md`: tambah D5, H2, H3, I1–I7, J1–J4 | Kartu v3.1–v3.2 |
| Hasil | P1 saja | P1 + P2 (uji coba) | `hasil_eksperimen_v3.2.md` |

### Dari v2.9 ke v3 (tetap berlaku)

| Aspek | v2.9 (arsip) | v3 | Dasar |
|---|---|---|---|
| Target | Realized variance harian | **Harga** BTC/IDR beberapa menit ke depan (lewat return) | Bimbingan 20 dan 23 Okt 2026 |
| Data | Binance BTC/USDT 2017–2026 | **Indodax BTC/IDR**, dikumpulkan sendiri lewat API | Arahan dosen |
| Model | HAR, HAR-X, LGBM-HAR, LGBM-X | **XGBoost, LightGBM, CatBoost, AdaBoost** | Arahan dosen |
| Pembanding | HAR-RV | **Naive** | HAR tidak cocok untuk target harga |
| Istilah realized variance | Inti penelitian | **Tidak dipakai** | Dosen: membingungkan |

---

## I. Posisi riset

### Pertanyaan utama
Bagaimana membangun dan mengoptimasi empat model boosting untuk memprediksi harga BTC/IDR beberapa menit ke depan pada berbagai *time frame*, dan model mana yang paling akurat **dibandingkan dengan Naive**?

### Kalimat inti
> "Saya membangun empat model boosting, mengoptimasinya dengan berbagai metode, untuk memprediksi harga Bitcoin di Indodax beberapa menit ke depan, lalu menguji apakah prediksinya benar-benar lebih baik dari tebakan paling sederhana, yaitu harga tidak berubah."

### Acuan utama: Rodrigues & Machado (2025), *Information* 16(4), 300 (A1)

| Aspek | Rodrigues & Machado (2025) | Riset ini |
|---|---|---|
| Data | Harga per menit 10 kripto, 30 hari, YFinance, USD (hlm. 9–10) | BTC/IDR Indodax, candle 1 menit dan candle 5 menit (agregasi), dikumpulkan sendiri ±4 bulan |
| Target | Nilai harga (regresi), horizon utama 60 menit (hlm. 10) | Nilai harga lewat return, *time frame* 1, 5, 15, 30, 60 menit |
| Model boosting | XGBoost dan LightGBM, **setelan bawaan** (hlm. 11) | XGBoost, LightGBM, CatBoost, AdaBoost, **semua dituning** |
| Optimasi | Grid search hanya untuk LSTM/GRU (hlm. 10–11) | 7 strategi (default, grid, random, TPE, CMA-ES, GA, QMC) + 4 teknik tambahan |
| Pembanding | **Tidak ada naive** | Naive |
| Uji statistik | Wilcoxon, memakai data di luar periode dataset (Tabel 4, hlm. 12) | Diebold-Mariano + HLN, koreksi Holm |
| Pembagian data | Satu split 80/10/10; **MinMaxScaler dipasang sebelum split** (hlm. 9) | Blok uji final tetap 20% terakhir, purging berbasis waktu, tanpa scaler; pemilihan hanya dari validasi |

**Kalimat posisi:** *"Penelitian ini mengembangkan Rodrigues & Machado (2025) dengan membandingkan empat model boosting yang dioptimasi dengan berbagai metode hyperparameter pada data BTC/IDR per menit, memakai Naive sebagai pembanding, dan menguji perbedaan akurasinya dengan uji Diebold-Mariano."*

Tulis "mengembangkan", bukan "mengikuti". Model terbaik di A1 adalah GRU, bukan boosting.

### Acuan pendukung

| Peran | Paper | Kode |
|---|---|---|
| Cara evaluasi (MDM, kontrol *data snooping*) | Wei dkk. (2023), J. Forecasting 42(4) | A2 |
| Horizon menit 1–60 dan uji DM | Jaquart dkk. (2021), JFDS 7 | B2 |
| ML untuk Bitcoin intraday (memakai tiga rasio split; desain v4 tidak lagi memakai rasio split) | Akyildirim dkk. (2023), AnnOR 330 | B3 |
| Naive sulit dikalahkan | Puoti dkk. (2024), AIMLSystems | B5 |
| LightGBM dan AdaBoost kompetitif untuk BTC | Bouteska dkk. (2024), IRFA 92 | B1 |
| Metrik relatif terhadap naive | Hyndman & Koehler (2006), IJF 22(4) | I5 |

### Yang TIDAK diklaim
- Tidak mengklaim model ML mengalahkan pasar atau memberi keuntungan trading. Biaya transaksi tidak diuji.
- Tidak mengklaim pemetaan *time frame* ke tipe trader sebagai fakta di pasar kripto. Pemetaan itu **asumsi penelitian** berdasarkan teori pasar heterogen (C1, C2) dan bukti terbatas di kripto (C5, C6).
- Tidak mengklaim hasil berlaku umum untuk semua periode. Data hanya ±4 bulan dari satu bursa, dan evaluasi akhir hanya pada satu blok uji (G5).
- Tidak mengklaim sebagai studi pertama yang membandingkan boosting untuk kripto. Yang belum ditemukan adalah **gabungan** unsur di Bagian IV.

---

## II. Konsep kunci

| Konsep | Pengertian | Peran |
|---|---|---|
| Return log | ln(harga t+h / harga t) | Target yang dipelajari model |
| Konversi ke rupiah | harga_prediksi = harga_sekarang × exp(return_prediksi) | Supaya metrik dalam rupiah |
| Naive | Prediksi harga h menit lagi = harga sekarang (I5, J2) | Pembanding utama |
| *Time frame* / horizon | Berapa menit ke depan harga diprediksi | Variabel yang diuji; dipilih di Tahap 1 dari skor validasi |
| Harga typical | (high + low + close) / 3 | Mengurangi efek loncatan bid-ask; perataan bisa menimbulkan autokorelasi semu (H2) |
| Candle 5 menit | Agregasi 5 candle 1 menit: open pertama, high tertinggi, low terendah, close terakhir, volume dijumlah | Dataset kedua, karena Indodax tidak menyediakan tf 5 menit (H3) |
| Gradient boosting | Gabungan pohon yang dibangun berurutan, tiap pohon memperbaiki galat sebelumnya (E1) | Dasar XGBoost, LightGBM, CatBoost |
| AdaBoost.R2 | Boosting regresi dengan pembobotan ulang sampel dan median berbobot (E9) | Versi AdaBoost yang dipakai |
| Periode pengembangan | ±80% data awal: baris yang waktu targetnya (t + h) sebelum t_u, jadi sedikit kurang dari 80% karena *purging*; seluruh tuning dan pemilihan dilakukan di sini | Mencegah pemilihan melihat data uji |
| Blok uji final | 20% bar terakhir, mulai waktu t_u; sama untuk semua skenario per dataset × *time frame* | Evaluasi akhir RM3 |
| Walk-forward CV | Validasi berurutan waktu: latih di masa lalu, uji di masa depan (G4); beberapa *fold* mengurangi kerentanan satu periode uji (G5) | Tuning tanpa kebocoran |
| *Purging* | Membuang baris latih yang waktu targetnya (t + h) masuk periode validasi/uji (J4) | Mencegah kebocoran |
| Skor validasi vs Naive | MAE rupiah model dibanding MAE Naive di fold yang sama | Dasar pemilihan Tahap 1–2 |
| Uji DM + HLN | Uji apakah dua **ramalan** berbeda akurasinya, dengan koreksi sampel kecil (G1, G2) | Uji model vs Naive |
| Koreksi Holm | Prosedur *sequentially rejective* untuk banyak uji (G3); satu keluarga uji = satu tahap | Keputusan "signifikan" pada uji berganda |
| Akurasi arah | Proporsi tanda perubahan yang tertebak benar (I7) | Metrik pendukung, dengan baseline |
| Pasar heterogen | Pelaku pasar berbeda menurut horizon waktu (C1) | Dasar kaitan *time frame* dan trader |
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
| B8 | Oprea & Bâra (2026) | Harian | Harga | XGB (*meta-learner*) | tidak dicatat | ✗ (tidak ada naive; Tabel 3) | DM |
| — | **Riset ini** | Menit (1 dan 5) | Harga | **4 model** | **7 strategi + 4 teknik** | ✓ | DM + HLN + Holm |

Pendukung minor: B6 Dudek dkk. (2025, preprint; target volatilitas; contoh Optuna untuk LightGBM pada Bitcoin), B7 Nadarajah dkk. (2025; boosting bawaan untuk volatilitas).

### III.2 *Time frame* dan tipe trader

| Kode | Isi yang boleh dikutip | Batasan |
|---|---|---|
| C1 Müller dkk. (1997) | Pasar terdiri dari komponen dengan horizon berbeda. Tabel 3 (hlm. 226): komponen 1 (7–80 menit) dealer intraday jangka pendek dan *market maker*; komponen 2 (16 menit – 3,5 jam) dealer intraday; komponen 5 (1–3,5 hari) trader jangka menengah | Data FX; penulis menyebut deskripsinya "tentative" |
| C2 Dacorogna dkk. (1995) | Strategi dengan horizon dan frekuensi berbeda punya profil risiko berbeda | Data FX |
| C3 Barber dkk. (2014) | Kurang dari 1% *day trader* konsisten untung setelah biaya | Saham Taiwan; isi dari versi WP |
| C4 Kirilenko dkk. (2017) | Tipe trader (HFT, *market maker*, fundamental) bisa dibedakan dari horizon dan perilaku | Futures S&P 500 |
| C5 Kakinaka & Umeno (2022) | Perilaku harga BTC dan ETH berbeda antara horizon pendek dan panjang (*crossover* ±10 hari) | "Pendek" di sini < 10 hari, bukan menit |
| C6 Liu dkk. (2023) | Pengguna Bitcoin terbagi menjadi tipe trader menurut lama pegang posisi: teknikal ≤ 5 hari, fundamental ±22 hari, HFT harian (hlm. 10) | Data *on-chain*, bukan bursa; tidak memakai istilah scalper/swing |

**Kesimpulan untuk skripsi:** literatur mendukung bahwa pelaku pasar berbeda menurut horizon waktunya, termasuk di kripto (C5, C6). Tetapi belum ada paper yang memetakan **horizon menit tertentu ke scalper atau swing trader di pasar kripto**. Pemetaan *time frame* di skripsi ditulis sebagai asumsi berdasarkan C1, bukan temuan. Definisi *scalper* belum punya sumber (⚠ Silber 1984 belum didapat).

### III.3 Pasar Bitcoin dan efisiensi

| Kode | Isi | Dipakai untuk |
|---|---|---|
| D1 Nakamoto (2008) | Bitcoin sebagai uang elektronik *peer-to-peer* tanpa lembaga keuangan perantara (abstrak, hlm. 1) | Definisi Bitcoin (sudah dibaca dari PDF) |
| D5 Baur & Dimpfl (2021) | Volatilitas Bitcoin hampir 10 kali kurs mata uang utama (abstrak, hlm. 2663) | Latar belakang volatilitas tinggi |
| D4 Yi dkk. (2023) | Bitcoin mendekati efisien bentuk lemah | Alasan Naive sulit dikalahkan |
| D3 Mokni dkk. (2024) | Efisiensi Bitcoin berubah-waktu | Alasan hasil bisa berbeda antarperiode uji |
| D2 Do (2026) | Era institusional mendekati *random walk* (Hurst 0,4821; hlm. 8) | Sama dengan D4, untuk periode terbaru |

### III.4 Landasan metode

| Topik | Kode | Catatan penting |
|---|---|---|
| Gradient boosting, loss absolut (LAD), *learning rate*, *relative importance* | E1 Friedman (2001) | LAD Alg. 3 hlm. 1196; *overfitting* & M sebagai regularisasi hlm. 1203; importance bagian 8.1 |
| XGBoost | E5 Chen & Guestrin (2016) | Regularisasi L2 bobot daun |
| LightGBM | E4 Ke dkk. (2017), E6 dokumentasi | *Leaf-wise* dan risiko *overfitting* berasal dari dokumentasi, bukan paper |
| CatBoost | E3 Prokhorenkova dkk. (2018) | *Ordered boosting*, pohon simetris; mode Ordered paling berguna di dataset kecil (hlm. 8) |
| AdaBoost | E2 Freund & Schapire (1997) + **E9 Drucker (1997)** + E10 dokumentasi sklearn | `AdaBoostRegressor` = AdaBoost.R2 |
| Sifat model pohon | J3 Hastie dkk. (2009) | Tidak sensitif skala (10.7); prediksi = rata-rata per daerah (9.2.2) → batas ekstrapolasi [PR] |
| Pemilihan model pohon | E7 Grinsztajn dkk. (2022), E8 Makridakis dkk. (2022) | Grinsztajn mengeluarkan deret waktu; M5 bergantung banyak deret |
| Grid vs Random Search | F1 Bergstra & Bengio (2012) | Random lebih efisien; dimensi efektif rendah |
| TPE | F2 Bergstra dkk. (2011) | Definisi ℓ(x), g(x), kuantil γ |
| Optuna | F3 Akiba dkk. (2019) + F7 dokumentasi 5.0.0 | Paper tidak membahas NSGA-II, QMC, MedianPruner |
| CMA-ES | F4 Hansen & Ostermeier (2001) + F7 | Optuna tidak mendukung parameter kategorikal di CMA-ES |
| Genetic Algorithm | F5 Deb dkk. (2002) | Pada satu objektif praktis menjadi GA elitis biasa |
| Hyperband | F6 Li dkk. (2018) | Untuk HyperbandPruner, bukan MedianPruner |
| Quasi-Monte Carlo (Sobol) | F8 Sobol' (1967), F9 Roy dkk. (2023), F10 dokumentasi SciPy | Keseimbangan Sobol hanya terjamin bila jumlah sampel pangkat 2 |
| *Early stopping* | J1 Zhang & Yu (2005), J3 10.12, E1 hlm. 1203 | Boosting yang dijalankan terlalu lama dapat *overfit* |
| Deret waktu, naive, lag, sin/cos | J2 Hyndman (2014) | Bahan ajar; fitur statistik bergulir belum ada sumber |
| *Purging* | J4 López de Prado (2018) | Bab 7, Snippet 7.1; narasi bab belum dibaca (⚠) |
| Validasi deret waktu | G4 Cerqueira dkk. (2020) | Istilah paper: *prequential in blocks* |
| Satu periode uji rentan | G5 Tashman (2000) | Dasar validasi *walk-forward* dengan beberapa *fold*; **keterbatasan** blok uji final tunggal. Tashman menyarankan *rolling origin*, jadi jangan dipakai sebagai alasan blok uji tetap |
| Uji DM | G2 Diebold & Mariano (1995) + G1 Harvey dkk. (1997) | Tulis "dua ramalan", bukan "dua model"; contoh "no change" vs forward rate (G2) |
| Uji berganda | G3 Holm (1979) | Satu keluarga uji = satu tahap |
| MAE, RMSE | I1 Chai & Draxler (2014), I2 Hodson (2022), I4 Willmott & Matsuura (2005), I5 | MAE satuan sama dengan data; RMSE menekan galat besar; pakai lebih dari satu metrik |
| MAPE | I5, I6 Kim & Kim (2016) | Aman untuk harga BTC/IDR karena jauh dari nol [PR] |
| Ukuran relatif terhadap naive | I5 bagian 2.4 | "MAE vs Naive (%)" = (RelMAE − 1) × 100% |
| Loss L1 ↔ median | I3 Gneiting (2011), E1 Alg. 3, I2 | Loss latih diselaraskan dengan metrik |
| Akurasi arah | I7 Pesaran & Timmermann (1992) | Return nol harus ditangani khusus |
| Fitur range | H1 Parkinson (1980) | Bila fitur range high-low disebut |
| Harga rata-rata | H2 Working (1960) | Jangan pakai angka +0,25 untuk (H+L+C)/3 |
| Sumber data | H3 dokumentasi API Indodax | tf candle 1, 15, 30, 60, 240, 1D, 3D, 1W; kelipatan harga Rp1.000; satuan timestamp perlu dicocokkan |

### III.5 Tidak dipakai

| Paper | Alasan |
|---|---|
| Kharola (2026), Oyedele (2023), Qureshi (2025), Zhu (2023) | Kejanggalan metodologi berat (K1–K4) |
| Petukhina dkk. (2021) | Tidak meramal dan tidak memetakan horizon ke trader (K5) |
| Gradojevic dkk. (2023), Karaa dkk. (2024) | Keputusan 1 Nov 2026 |
| **Zhivkov & Kandilarov (2026)** | **Tidak ditemukan di mana pun; kemungkinan referensi karangan. Jangan dikutip.** Klaim "TPE terbukti terbaik untuk prediksi kripto" tidak punya sumber. |
| Pyrlik dkk. (2021) | Target volatilitas saham Rusia, *working paper* (keputusan 4 Nov 2026) |
| Semua literatur HAR, realized variance, uji kestabilan, likuiditas | Arsip v2.9 |

### III.6 Sintesis literatur

1. **Prediksi harga kripto dengan boosting sudah banyak dilakukan,** tetapi sebagian besar memakai data harian (A2, B1, B5, B8). **Benchmarking saja bukan kontribusi.**
2. **Studi data menit kebanyakan memprediksi arah, bukan nilai harga** (B2, B3, B4). Studi nilai harga per menit yang paling dekat (A1) tidak menuning boosting dan tidak memakai naive.
3. **Pembanding naive harga jarang dipakai dengan benar.** Bouteska dkk. menghitung *random walk* pada return (B1, poin 11). Pada studi arah, *random walk* hanya berarti akurasi 50% (B2, B3). Oprea & Bâra tidak memakai naive sama sekali (B8).
4. **Ketika naive dipakai, naive sulit dikalahkan** (B5; contoh "no change" di G2). Ini sejalan dengan Bitcoin yang mendekati efisien bentuk lemah (D2, D4).
5. **Optimasi hyperparameter sering diabaikan atau hanya satu metode.** A1 dan B7 memakai setelan bawaan; B1 dan B2 hanya grid search. Bukti Random > Grid (F1) dan TPE > Random (F2) berasal dari jaringan saraf, bukan boosting untuk harga kripto.
6. **Keterdugaan Bitcoin jangka pendek kecil.** Akurasi arah sekitar 51–56% (B2, B3); keuntungan sebelum biaya bisa menjadi rugi setelah biaya (B2). Di saham, kurang dari 1% *day trader* konsisten untung setelah biaya (C3).
7. **Satu periode uji rentan terhadap kejadian unik** (G5), dan efisiensi Bitcoin berubah-waktu (D3). Karena itu tuning dan pemilihan memakai validasi *walk-forward* dengan beberapa *fold* (G4, G5). Evaluasi akhir tetap memakai satu blok uji, dan hal ini dicatat sebagai keterbatasan (G5).
8. **Pelaku pasar berbeda menurut horizon waktu** (C1, C2), juga di Bitcoin (C5, C6). Belum ditemukan pemetaan langsung horizon menit ke tipe trader kripto.
9. **Pilihan metrik harus selaras dengan tugas** (I3) dan sebaiknya lebih dari satu (I1, I2). MAE dipakai sebagai metrik utama karena satuannya rupiah (I4, I5); RMSE dan MAPE sebagai pendukung.

---

## IV. Research gap

**Sejauh literatur yang diperiksa,** belum ditemukan penelitian yang sekaligus:
1. memprediksi **nilai harga** Bitcoin (bukan arah) pada **data per menit** dengan beberapa *time frame*;
2. membandingkan **keempat model boosting** (XGBoost, LightGBM, CatBoost, AdaBoost) yang **semuanya dituning**;
3. membandingkan **banyak metode optimasi hyperparameter** sekaligus (grid, random, TPE, CMA-ES, GA, QMC) beserta teknik tambahan;
4. memakai **naive harga** sebagai pembanding, **uji Diebold-Mariano**, dan **koreksi uji berganda** untuk menilai perbedaan akurasi;
5. memakai data **BTC/IDR** dari bursa Indonesia yang dikumpulkan langsung.

### Checklist novelty

| Paper | Yang sudah dilakukan (wajib diakui) | Yang belum |
|---|---|---|
| A1 Rodrigues & Machado (2025) | Harga per menit, XGB dan LGBM, horizon pendek | Tuning boosting, CatBoost/AdaBoost, naive, DM, pembagian tanpa kebocoran |
| A2 Wei dkk. (2023) | XGB vs LGBM untuk BTC, MDM + MCS + SPA | Data intraday, naive harga, peramal langsung |
| B1 Bouteska dkk. (2024) | AdaBoost vs LightGBM untuk BTC, grid search | Data intraday, naive harga, DM, XGB/CatBoost |
| B2 Jaquart dkk. (2021) | Horizon 1–60 menit, DM, biaya transaksi | Target nilai harga, 4 booster, banyak metode optimasi |
| B3 Akyildirim dkk. (2023) | Data intraday, tiga rasio split | Target harga, pasar spot, naive harga, DM |
| B5 Puoti dkk. (2024) | Naive vs ML untuk harga kripto | Data intraday, tuning, DM yang jelas |

**Kontribusi Informatika:** rancangan eksperimen yang membandingkan model dan metode optimasi secara setara (jatah trial sama, walk-forward CV, purging berbasis waktu, pemilihan hanya dari validasi, blok uji tetap), dengan pembanding naive, uji DM, dan koreksi Holm. Kontribusinya bukan pada teori keuangan.

---

## V. Rancangan penelitian (ringkas, desain v4)

Rincian lengkap dan kode: `hasil_eksperimen_v3.3.md` Bagian 3 dan Lampiran B. Bab III repo `skripsi-latex` sudah memakai desain ini.

| Komponen | Keputusan | Dasar |
|---|---|---|
| Data | API publik Indodax BTC/IDR; collector Python cron tiap 1 menit di VPS (UTC), SQLite; candle 1 menit `tradingview/history_v2` `tf=1` | Arahan dosen; H3 |
| Dataset | candle 1 menit + candle 5 menit (agregasi). Snapshot ticker disimpan tetapi tidak dipakai | H3 (tidak ada tf 5 menit); review dosen |
| Periode | Okt 2026 – Feb 2027 (⚠ tanggal pasti) | Keputusan 6 Nov |
| Harga | typical (H+L+C)/3 | Mengurangi loncatan bid-ask; H2 |
| Target | Log return h menit ke depan, dikonversi ke rupiah | Model pohon tidak bisa ekstrapolasi (J3 [PR]) |
| *Time frame* | 1, 5, 15, 30, 60 menit (1 menit hanya candle 1 menit) → 9 pasangan; satu pasangan dipilih di Tahap 1 | Dosen: dicari lewat eksperimen; setara komponen 1–2 C1 dan horizon B2 |
| Fitur | 42 fitur dari OHLCV dan waktu: lag return, statistik bergulir 5–240 menit, range, posisi bar, volume, jam sin/cos | Hanya data sampai t; J2 (lag, sin/cos) |
| Model | XGBoost (E5), LightGBM (E4), CatBoost (E3), AdaBoost.R2 (E9, E10) + Naive | Arahan dosen; E7 |
| Pembagian data | Periode pengembangan ±80% awal (t + h < t_u); blok uji final 20% bar terakhir (mulai t_u, tetap) | J4; review dosen |
| Validasi | Walk-forward 5 fold di periode pengembangan, purging berbasis waktu per fold | G4, G5, J4 |
| Objektif tuning | MAE rupiah rata-rata fold; skor Naive di fold yang sama | Selaras metrik utama (I3) |
| Optimasi | Default, Grid (27), Random, TPE, CMA-ES, GA (NSGA-II), QMC (30 trial), seed 42 | F1–F10; dosen: "optimasi sebanyak mungkin" |
| Teknik tambahan | Early stopping (≤2.000 pohon, sabar 50), top-15 fitur di dalam fold, loss L1, pruner median; AdaBoost + early stop/L1 tidak berlaku | J1, J3, E1, F7 |
| Tahap 1 | Pilih (dataset, *time frame*) dari skor validasi vs Naive | — |
| Tahap 2 | Pilih strategi tuning dari rata-rata skor validasi 4 model; default boleh terpilih | — |
| Tahap 3 | Panjang data latih 100/75/50% (bagian akhir), blok uji tetap; tanpa pemilihan | Review dosen |
| Tahap 4 | 4 teknik tambahan; tanpa pemilihan | — |
| Penguncian | Pilihan Tahap 1–2 dikunci (file + hash) sebelum blok uji dibuka | Anti-HARKing |
| Metrik | MAE (utama), MAE vs Naive (%), RMSE, MAPE, akurasi arah (+ baseline, % tetap/naik/turun) | I1–I7 |
| Uji | DM dua sisi + HLN, autokovarians lag h_b−1 pada grid waktu, t(n−1); Holm, satu keluarga uji = satu tahap | G1, G2, G3 |
| Model terbaik (RM3) | MAE vs Naive terkecil di blok uji final; RMSE dan MAPE pendukung; "lebih baik dari Naive" hanya bila lolos Holm | Bab III (⚠ konfirmasi dosen) |

### Catatan desain yang wajib ditulis di Bab III

1. **AdaBoost memakai AdaBoost.R2** (E9, E10), bukan AdaBoost asli (E2). Loss L1/L2 dan early stopping tidak berlaku; AdaBoost punya parameter `loss` sendiri (linear, square, exponential) yang ikut dituning.
2. **TPE di Optuna bersifat multivariat** untuk satu objektif (F7), berbeda dari TPE independen di F2.
3. **CMA-ES tidak mendukung parameter kategorikal** (F7). Parameter `loss` AdaBoost pada run CMA-ES diambil acak oleh RandomSampler.
4. **NSGA-II dipakai untuk satu objektif.** Pada satu objektif praktis menjadi GA elitis (F5); dokumentasi Optuna tidak menyebut pemakaian ini (F7).
5. **QMC (Sobol) 30 trial bukan pangkat 2**, sehingga keseimbangan Sobol tidak terjamin (F10). ⚠ Belum diputuskan 30 atau 32.
6. **Random, TPE, CMA-ES, dan GA memakai seed yang sama,** sehingga beberapa trial awal identik.
7. **Grid Search 27 kombinasi, metode lain 30 trial.**
8. **MedianPruner tidak punya rujukan paper** (F7).
9. **Candle 5 menit dibentuk dari candle 1 menit;** bar dengan data < 5 menit dicatat sebagai bar parsial. Menit tanpa transaksi tidak menghasilkan candle.
10. **Harga typical bergerak dalam kelipatan ±Rp333** (karena OHLC kelipatan Rp1.000, H3). Harga dianggap tetap bila selisih < Rp1; bar tersebut tidak dihitung dalam akurasi arah.
11. **Timestamp** di dokumentasi Indodax disebut milidetik, tetapi contoh `Time` OHLC bernilai detik (H3 poin 11). Cocokkan dengan data collector.
12. **Keluarga uji Holm** = semua perbandingan model vs Naive dalam satu tahap; tag `tahap4_*` digabung menjadi satu keluarga. Konfigurasi yang muncul lagi di tahap lain ikut diuji di keluarga tahap itu (sesuai kode v4; lihat Bagian IX).

---

## VI. Rumusan masalah, tujuan, dan judul

> **Catatan anti-HARKing:** uji coba sudah dijalankan. Rumusan masalah ditulis **netral** dan tidak boleh disusun ulang supaya cocok dengan hasil.

### Rumusan masalah (versi 6 Nov 2026, sudah di Bab I)

| | Rumusan masalah | Tujuan | Bagian eksperimen |
|---|---|---|---|
| RM1 | Bagaimana membangun model XGBoost, LightGBM, CatBoost, dan AdaBoost untuk memprediksi harga BTC/IDR pada berbagai *time frame*? | Membangun keempat model untuk berbagai *time frame* | Tahap 1 + pipeline |
| RM2 | Bagaimana pengaruh optimasi *hyperparameter* terhadap akurasi keempat model tersebut? | Menganalisis pengaruh optimasi | Tahap 2 dan 4 |
| RM3 | Model mana yang memiliki performa terbaik berdasarkan nilai MAE, RMSE, dan MAPE dibandingkan dengan Naive? | Menentukan model terbaik terhadap Naive | Blok uji final + Holm |

Tahap 3 (panjang data latih) tidak dipetakan ke RM tertentu.

### Judul

Judul sementara di repo LaTeX (`metadata.tex`): **"Prediksi Harga BTC/IDR pada Berbagai Time Frame dengan Model Boosting dan Optimasi Hyperparameter"** (13 kata). Diputuskan bersama dosen.

### Batasan penelitian (sesuai Bab I)
- Objek BTC/IDR spot Indodax melalui API publik.
- Data candle 1 menit dan candle 5 menit (agregasi), periode 10 Okt 2026 – 10 Feb 2027 (⚠).
- Model XGBoost, LightGBM, CatBoost, AdaBoost; pembanding Naive.
- Optimasi Grid, Random, TPE, CMA-ES, GA (NSGA-II), QMC.
- *Time frame* 1, 5, 15, 30, 60 menit; 1 menit hanya candle 1 menit.
- Fitur hanya dari OHLCV dan waktu candle (tanpa sentimen, berita, *on-chain*, *order book*).
- Tidak menguji strategi trading, biaya transaksi, atau keuntungan.
- ⚠ Ada/tidaknya aplikasi atau dashboard.

---

## VII. Gambaran uji coba dan kaitannya dengan literatur (untuk Bab IV–V, bukan Bab I–III)

Rincian: `hasil_eksperimen_v3.3.md` Bagian 4–5. Angka di bawah dari **uji coba** dengan kode lama (P1: 92 run, P2: 120 run); hasil skripsi menunggu eksperimen final v4.

| Temuan uji coba | Kaitan literatur | Batasan saat menulis |
|---|---|---|
| Tidak ada run yang lolos Holm sebagai lebih baik dari Naive (P1 0/92, P2 0/120) | Sejalan dengan B5 dan G2 (naive sulit dikalahkan) serta D2, D4 (mendekati efisien) | B5 data harian |
| Tanpa tuning, model +9% (P1) dan +12% (P2) lebih buruk dari Naive | Menjelaskan kelemahan A1 dan B7 yang memakai setelan bawaan | Sebagian perbaikan tuning berasal dari prediksi yang makin "datar" |
| TPE rata-rata terbaik untuk XGB/LGBM/Cat di kedua periode; Random > Grid di P1 | Sejalan dengan F1 dan F2 | Bukti F1–F2 dari jaringan saraf; tidak ada paper kripto yang mendukung "TPE terbaik" |
| LightGBM + loss L1 satu-satunya run ✓ di kedua periode (tidak lolos Holm) | LightGBM kompetitif untuk BTC (B1); loss absolut ↔ median ↔ MAE (E1, I3) | Run P2 datar (korelasi ≈ 0) |
| AdaBoost paling lemah dan tidak stabil | Berbeda dengan B1 (AdaBoost kompetitif harian) | Bedanya data harian vs menit |
| Sinyal (korelasi, akurasi arah di atas baseline) hanya di *time frame* 1 menit, di kedua periode | **Berlawanan** dengan B2 (keterdugaan naik seiring horizon) | B2 target arah; kemungkinan efek bid-ask/perataan harga typical (H2) |
| MAE dan RMSE berlawanan di 1 menit karena 14–17% menit harganya tetap | Pentingnya lebih dari satu metrik (I1, I2) | — |
| *Time frame* terpilih berubah (1 menit → 60 menit) mengikuti kondisi pasar periode uji | Satu periode uji rentan (G5); efisiensi berubah-waktu (D3) | Alasan desain v4 memilih dari validasi *walk-forward* dan memakai Holm |
| Keunggulan < 1% dan jauh di bawah spread | Untung sebelum biaya bisa jadi rugi setelah biaya (B2); <1% *day trader* untung setelah biaya (C3) | Biaya transaksi tidak diuji |
| Pruner median hemat ±36% waktu dengan akurasi hampir sama (P1) | Prinsip menghentikan trial jelek lebih awal (F6, F7) | MedianPruner tanpa rujukan paper |

---

## VIII. Risiko dan antisipasi pertanyaan penguji

| Pertanyaan | Jawaban |
|---|---|
| "Modelnya kalah dari Naive, apa kontribusinya?" | Hasil negatif tetap sah. Kontribusinya ada pada desain perbandingan yang setara dan jujur: semua model dituning, ada Naive, ada uji DM dan koreksi Holm, dan pemilihan tidak melihat data uji. Banyak penelitian sebelumnya tidak memakai naive (A1, A2, B8) atau memakai *random walk* pada return (B1). |
| "Kenapa prediksi return, bukan harga langsung?" | Model pohon memprediksi rata-rata target data latih di tiap daerah (J3), jadi tidak bisa memprediksi di luar rentang data latih. Return kemudian dikonversi ke rupiah. |
| "Kenapa harga typical, bukan close?" | Close 1 menit meloncat antara harga bid dan ask. Pada data uji coba minggu pertama, autokorelasi return 1 menit close −0,273 dan typical −0,073 (dihitung ulang pada data final). Perataan bisa menimbulkan autokorelasi semu (H2), jadi dicatat sebagai keterbatasan. |
| "Kenapa candle 5 menit dibuat sendiri?" | Indodax hanya menyediakan candle 1, 15, 30, 60, 240 menit, harian, 3 harian, dan mingguan (H3). Candle 5 menit dibentuk dari lima candle 1 menit dengan aturan OHLCV standar. |
| "Kenapa ticker tidak dipakai?" | Supaya kedua dataset berasal dari jenis data yang sama (candle), sehingga perbedaan hasil hanya dari resolusi. Snapshot ticker tetap disimpan oleh collector. |
| "Kenapa blok uji dibuat tetap, bukan split 80:20/70:30/60:40?" | Kalau rasio split diubah, periode uji ikut berubah, sehingga perbedaan hasil bercampur dengan perbedaan kondisi pasar (D3). Dengan blok uji tetap, Tahap 3 hanya mengubah panjang data latih, jadi pengaruhnya bisa dipisahkan. Ini keputusan desain (review dosen), bukan rekomendasi Tashman. |
| "Satu blok uji kan rentan?" | Benar (G5). Karena itu tuning dan pemilihan memakai validasi *walk-forward* 5 *fold*, bukan satu periode. Blok uji final dipakai sekali untuk evaluasi akhir, dan kerentanannya ditulis sebagai keterbatasan. |
| "Kenapa pemilihan memakai validasi, bukan data uji?" | Supaya data uji hanya dipakai sekali untuk evaluasi akhir dan pemilihan tidak menyesuaikan diri dengan data uji. |
| "Kenapa ada koreksi Holm?" | Banyak uji DM dijalankan sekaligus. Tanpa koreksi, sebagian hasil "signifikan" bisa muncul karena kebetulan (G3). |
| "AdaBoost yang dipakai yang mana?" | AdaBoost.R2 (Drucker, 1997), sesuai `AdaBoostRegressor` scikit-learn (E9, E10). |
| "Kenapa NSGA-II yang multiobjektif dipakai untuk satu objektif?" | Pada satu objektif, NSGA-II praktis menjadi GA elitis biasa (F5). |
| "Hubungan *time frame* dengan scalper/swing trader?" | Teori pasar heterogen (C1) membagi pelaku pasar menurut horizon; di Bitcoin tipe trader juga berbeda menurut lama pegang posisi (C6). Pemetaan spesifik ke scalper dan swing trader merupakan asumsi penelitian. |
| "Apakah hasilnya bisa dipakai trader?" | Belum. Biaya transaksi dan spread tidak diuji, dan keunggulan pada uji coba jauh di bawah spread. |
| "Kenapa tidak deep learning?" | Arahan dosen (ML non-deep). Model pohon juga unggul pada data tabular berukuran menengah (E7), dengan catatan deret waktu dikeluarkan dari benchmark itu. |
| "Data dikumpulkan sendiri, primer atau sekunder?" | ⚠ Menunggu istilah dari dosen. Faktanya: data diambil langsung dari API publik Indodax oleh program collector buatan sendiri. |

---

## IX. Hal terbuka (⚠)

### Menunggu dosen
1. Tanggal pasti periode data final (Bab I menulis 10 Okt 2026 – 10 Feb 2027).
2. Perlu output aplikasi/dashboard atau tidak.
3. Aturan "model terbaik" untuk RM3 (usulan Bab III: MAE vs Naive terkecil di blok uji + Holm). Kunci sebelum eksperimen final.
4. Judul final.
5. Istilah data primer atau sekunder.
6. QMC 30 atau 32 trial; `has_time=True` CatBoost; beberapa seed untuk Tahap 2.

### Perlu disamakan sebelum Februari
- **Aturan duplikat Holm.** Bab III menulis "konfigurasi yang sama persis dan muncul di lebih dari satu tahap dihitung satu kali", sedangkan kode v4 membentuk keluarga per tahap dan hanya membuang duplikat **di dalam** satu tahap.
  - **Rekomendasi:** Bab III mengikuti kode. Aturan lintas tahap ambigu, karena tidak jelas konfigurasi masuk keluarga tahap mana. Di kode v4, duplikat di dalam satu tahap praktis tidak terjadi, jadi cukup ditulis "setiap tahap merupakan satu keluarga uji".
  - Kalimat usulan Bab III: *"Satu keluarga uji berisi seluruh perbandingan model terhadap Naive dalam satu tahap. Keempat teknik pada Tahap 4 digabung menjadi satu keluarga."*
  - ⚠ Keputusan Ferdi.
- Bab I baris 148 menulis "10 February 2027" (ejaan Inggris) → "10 Februari 2027".
- Repo `skripsi-latex/context/` masih berisi `hasil_riset_v3.0.md` dan `hasil_eksperimen_v3.0.md`. Ganti dengan dokumen ini, `hasil_eksperimen_v3.3.md`, dan `kartu_paper_v3.3.md`; pindahkan versi lama ke `context/arsip/`.

### Verifikasi referensi (status `references.bib`, 13 Nov 2026)
Sudah dicek ke Crossref oleh agen `.bib` (4 dan 10 Nov 2026): DOI seluruh entri aktif, termasuk B5 versi ACM, C4 Kirilenko, C6 Liu 32(13), G2 Diebold, H1 Parkinson, H2 Working (10.2307/1907574), I7 Pesaran (10.1080/07350015.1992.10509922), D5 Baur. Volume F2 (24) dan versi `lightgbm` 4.7.0 (E6) juga sudah dipastikan.

Masih terbuka:
- Kuartil jurnal *Information* (A1) di SCImago dan Sinta.
- Halaman prosiding: Drucker (E9), Prokhorenkova (E3), Ke (E4), Bergstra 2011 (F2).
- URL `hyndman2014fpp` dicocokkan dengan alamat PDF yang diunduh.
- Satuan timestamp API Indodax (H3).
- `optunapruners` belum ada di `.bib` dan belum punya kartu; tambahkan bila Bab II/III membahas MedianPruner dari halaman pruner.

### Klaim Bab II yang belum punya sumber
- Definisi log return (T2): Tsay (2010) belum didapat.
- Seleksi fitur top-k (T6): Guyon & Elisseeff (2003) belum didapat.
- Narasi *purging* (T5): teks bab 7 López de Prado belum dibaca.
- Definisi *scalper*: Silber (1984) belum didapat.
- Fitur statistik bergulir: belum ada sumber.
- Indodax berizin dan beroperasi 24 jam: belum ada sumber resmi tercetak.

### Keterbatasan eksperimen yang sudah diketahui
- Evaluasi akhir hanya pada satu blok uji (G5).
- QMC 30 trial bukan pangkat 2 (F10).
- Seed sama untuk metode berbasis acak.
- Biaya transaksi dan spread tidak masuk evaluasi.
- Data satu bursa, ±4 bulan; kondisi pasar periode uji memengaruhi hasil (uji coba P1 vs P2).
- Harga typical dapat menimbulkan pola mekanis pada return 1 menit (H2).
- Holm konservatif karena uji saling berkorelasi; bias pemilihan antartahap tidak ditangani (saran lanjutan: SPA/MCS seperti A2).

---

## X. Langkah berikutnya

| Tahap | Status |
|---|---|
| Uji coba P1 (14–20 Okt) | ✅ 28 Okt 2026 |
| Kartu paper v3.2 → v3.3 | ✅ 13 Nov 2026 |
| Uji coba P2 (10 Okt – 10 Nov) + analisis | ✅ 11 Nov 2026 |
| Review dosen → kode v4 | ✅ 12 Nov 2026 (commit `ed8b735`) |
| Dokumen riset v3.2 dan eksperimen v3.3 | ✅ dokumen ini |
| Bab I–III (LaTeX) | 🔄 v1.9 (12 Nov 2026) |
| Samakan aturan duplikat Holm (Bab III vs kode) | ⏳ rekomendasi di Bagian IX |
| Perbarui `context/` di repo LaTeX | ⏳ |
| Verifikasi kuartil dan halaman prosiding | ⏳ |
| Keputusan dosen (Bagian IX) | ⏳ |
| Eksperimen final v4 | ⏳ Februari 2027 |
| Bab IV–V | Setelah eksperimen final |
