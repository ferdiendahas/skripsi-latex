# Kartu Paper v3 — Skripsi v3.0 (Prediksi Harga BTC/IDR dengan Boosting)

> Disusun 30 Okt 2026, diperbarui 1 Nov 2026, dari PDF yang dikirim di chat. **Menggantikan `kartu_paper.md` untuk skripsi v3.0.** Kartu lama yang tidak relevan dengan topik v3.0 tidak dibawa.
> **Isi:** 29 kartu baru (paper dan dokumentasi yang dibaca dari PDF atau halaman resmi) + 17 kartu lama yang masih relevan (isinya tidak diubah, hanya diberi kode baru dan baris "Relevansi v3").
> **Pembaruan 1 Nov 2026:** tambah E9–E10, F7–F10, C5–C6; metadata A2, C3, C4, F2, F3 dilengkapi; Petukhina dkk. (2021) dibuang (K5).
> **Pembaruan 3 Nov 2026:** D2–D4 dibaca ulang dari PDF; judul dan DOI dilengkapi; halaman Hurst D2 dikoreksi (hlm. 8); satu catatan kejanggalan D4 dikoreksi.
> **Pembaruan 3 Nov 2026 (2):** 13 kartu lama lain dibaca ulang dari PDF yang dikirim ulang (B6–B8, E4–E8, G2–G5, H1). Isi lama tetap; yang berubah hanya lokasi halaman yang salah, DOI dari PDF, catatan "Untuk v3", dan temuan baru yang ditandai. Hanya D1 (Nakamoto) yang belum dibaca dari PDF.
> **Tujuan:** acuan saat menulis narasi dan sitasi. Kutip hanya klaim yang tercatat di kartu, beserta lokasinya. Bila klaim tidak ada di kartu, anggap belum terverifikasi.
> **Format:** review 11 poin. Poin 1–7 dan bagian "disebut paper" di poin 8 hanya berisi isi paper; yang tidak ada ditulis "tidak disebut" atau "tidak dicatat". Poin 9–11 dan usulan di poin 8 diberi label **[PR]** (penilaian reviewer).
> **Lokasi:** "hlm." = nomor halaman cetak; "hlm. PDF" = urutan halaman berkas. Tiap kartu menyebut mana yang dipakai.
> **Kolom `.bib`:** semua key kartu baru berstatus **belum** (key usulan). Kartu lama mengikuti status `.bib` v2 dan perlu dicek ulang untuk v3.
> **DOI:** doi.org tidak bisa dibuka dari sesi ini. Metadata dicek lewat PDF, IDEAS/RePEc, repositori kampus, atau halaman resmi. Tetap buka DOI di doi.org sebelum masuk `.bib`.

## Peran acuan

- **Acuan utama desain masalah:** A1 `rodrigues2025` (data menit, horizon pendek, boosting vs model lain).
- **Acuan cara evaluasi:** A2 `wei2023` (MDM Harvey dkk., MCS, SPA) + G1 `harvey1997`.
- **Pendukung terkuat:** B2 `jaquart2021` (horizon menit, DM, biaya transaksi), B3 `akyildirim2023` (tiga rasio split), B5 `puoti2024` (naive sulit dikalahkan), B1 `bouteska2024` (LightGBM untuk BTC).
- **Horizon ↔ tipe trader:** C6 `liu2023` (satu-satunya bukti di kripto yang membedakan tipe trader menurut lama pegang posisi), C1 `muller1997` dan C2 `dacorogna1995` (teori pasar heterogen, data FX), C5 `kakinaka2022` (perilaku kripto beda antara horizon pendek dan panjang).
- **Sumber implementasi:** E9–E10 (AdaBoost.R2), F7 (Optuna 5.0.0), F8–F10 (QMC/Sobol).

## Indeks

| Kode | Key | Sumber | Versi dibaca |
|---|---|---|---|
| A1 | `rodrigues2025` | Rodrigues & Machado (2025), Information 16(4), 300 | terbit |
| A2 | `wei2023` | Wei, Sermpinis & Stasinakis (2023), Journal of Forecasting 42(4), 852–871 | terbit |
| B1 | `bouteska2024` | Bouteska, Abedin, Hajek & Yuan (2024), Int. Review of Financial Analysis 92, 103055 | terbit |
| B2 | `jaquart2021` | Jaquart, Dann & Weinhardt (2021), J. Finance and Data Science 7, 45–66 | terbit |
| B3 | `akyildirim2023` | Akyildirim, Cepni, Corbet & Uddin (2023), Annals of Operations Research 330, 553–584 | terbit (ZORA) |
| B4 | `akyildirim2021` | Akyildirim, Goncu & Sensoy (2021), Annals of Operations Research 297, 3–36 | terbit |
| B5 | `puoti2024` | Puoti, Pittorino & Roveri (2024), AIMLSystems 2024, ACM | versi penulis arXiv |
| B6 | `dudek2025lgbm` | Dudek, Kasprzyk & Pełka (2025), arXiv:2511.20105 *(kartu lama)* | preprint |
| B7 | `nadarajah2025` | Nadarajah dkk. (2025), J. Risk and Financial Management 18(2), 52 *(kartu lama)* | terbit |
| B8 | `oprea2026` | Oprea & Bâra (2026), Computational Economics *(kartu lama)* | terbit daring |
| C1 | `muller1997` | Müller dkk. (1997), Journal of Empirical Finance 4, 213–239 | terbit |
| C2 | `dacorogna1995` | Dacorogna dkk. (1995), European Journal of Finance 1(4), 383–403 | terbit |
| C3 | `barberdt` | Barber, Lee, Liu & Odean (2014), Journal of Financial Markets 18, 1–24 | WP 2012 |
| C4 | `kirilenko2017` | Kirilenko, Kyle, Samadi & Tuzun (2017), Journal of Finance 72(3), 967–998 | SSRN |
| C5 | `kakinaka2022` | Kakinaka & Umeno (2022), Finance Research Letters 46, 102319 | terbit |
| C6 | `liu2023` | Liu, Jahanshahloo, Chen & Eshraghi (2023), European Journal of Finance | terbit daring |
| D1 | `nakamoto2008` | Nakamoto (2008), white paper *(kartu lama)* | PDF belum ada |
| D2 | `do2026` | Do (2026), Borsa Istanbul Review 26, 100869 *(kartu lama)* | terbit |
| D3 | `mokni2024` | Mokni dkk. (2024), Financial Innovation 10:39 *(kartu lama)* | terbit |
| D4 | `yi2023` | Yi dkk. (2023), Scientific Reports 13:4789 *(kartu lama)* | terbit |
| E1 | `friedman2001` | Friedman (2001), Annals of Statistics 29(5), 1189–1232 | terbit |
| E2 | `freund1997` | Freund & Schapire (1997), J. Computer and System Sciences 55, 119–139 | terbit |
| E3 | `prokhorenkova2018` | Prokhorenkova dkk. (2018), NeurIPS 31 (CatBoost) | prosiding |
| E4 | `ke2017` | Ke dkk. (2017), NeurIPS 30 (LightGBM) *(kartu lama)* | prosiding |
| E5 | `chen2016` | Chen & Guestrin (2016), KDD 2016 (XGBoost) *(kartu lama)* | arXiv v3 |
| E6 | `lightgbmfeatures`, `lightgbmtuning` | Dokumentasi LightGBM *(kartu lama)* | halaman web (PDF cetak 3 Nov 2026, versi 4.7.0.99) |
| E7 | `grinsztajn2022` | Grinsztajn dkk. (2022), NeurIPS 35 *(kartu lama)* | arXiv v1 |
| E8 | `makridakis2022` | Makridakis dkk. (2022), Int. J. Forecasting 38(4), 1346–1364 *(kartu lama)* | terbit |
| E9 | `drucker1997` | Drucker (1997), ICML 1997 (AdaBoost.R2) | versi penulis |
| E10 | `sklearnadaboost` | Dokumentasi scikit-learn 1.9.1, AdaBoostRegressor | halaman web (PDF cetak) |
| F1 | `bergstra2012` | Bergstra & Bengio (2012), JMLR 13, 281–305 | terbit |
| F2 | `bergstra2011` | Bergstra dkk. (2011), NIPS 2011, 2546–2554 (TPE) | prosiding |
| F3 | `akiba2019` | Akiba dkk. (2019), KDD 2019, 2623–2631 (Optuna) | preprint arXiv |
| F4 | `hansen2001` | Hansen & Ostermeier (2001), Evolutionary Computation 9(2), 159–195 | versi penulis + errata |
| F5 | `deb2002` | Deb dkk. (2002), IEEE Trans. Evolutionary Computation 6(2), 182–197 | terbit |
| F6 | `li2018` | Li dkk. (2018), JMLR 18, 1–52 (Hyperband) | terbit |
| F7 | `optunadocs` | Dokumentasi Optuna 5.0.0 (sampler dan pruner) | halaman web |
| F8 | `sobol1967` | Sobol' (1967), Zh. Vychisl. Mat. Mat. Fiz. 7(4), 784–802 | terjemahan Inggris |
| F9 | `roy2023qmc` | Roy dkk. (2023), JOSS 8(84), 5309 | terbit |
| F10 | `scipysobol` | Dokumentasi SciPy v1.18.0, qmc.Sobol | halaman web (PDF cetak) |
| G1 | `harvey1997` | Harvey, Leybourne & Newbold (1997), Int. J. Forecasting 13, 281–291 | terbit |
| G2 | `diebold1995` | Diebold & Mariano (1995), J. Business & Economic Statistics 13(3), 253–263 *(kartu lama)* | WP NBER No. 169 (Nov 1994), scan |
| G3 | `holm1979` | Holm (1979), Scandinavian Journal of Statistics 6(2), 65–70 *(kartu lama)* | terbit |
| G4 | `cerqueira2020` | Cerqueira, Torgo & Mozetič (2020), Machine Learning 109 *(kartu lama)* | terbit |
| G5 | `tashman2000` | Tashman (2000), Int. J. Forecasting 16(4), 437–450 *(kartu lama)* | terbit |
| H1 | `parkinson1980` | Parkinson (1980), Journal of Business 53(1), 61–65 *(kartu lama)* | terbit |
| K1–K5 | — | Kharola 2026, Oyedele 2023, Qureshi 2025, Zhu 2023, Petukhina 2021 | **dibuang** |

---

## A. Acuan utama

### A1. `rodrigues2025` — Rodrigues & Machado (2025), "High-Frequency Cryptocurrency Price Forecasting Using Machine Learning Models: A Comparative Study", Information 16(4), 300, doi 10.3390/info16040300
- **Peran:** **acuan utama desain masalah** (data menit, horizon pendek, boosting vs model lain).
- **Alasan dipilih sebagai acuan utama [PR]:**
  - Paling mirip desain skripsi: prediksi **nilai harga** (regresi), data **per menit**, horizon pendek (60 menit, plus Tabel 5 untuk 30–1.440 menit), dan membandingkan XGBoost serta LightGBM dengan model lain.
  - Terbit 2025, sehingga masuk syarat lima tahun terakhir untuk celah riset.
  - Kelemahannya langsung menjadi celah yang diisi skripsi: boosting tanpa *tuning*, tanpa pembanding naive, tanpa uji DM, kebocoran MinMaxScaler, hanya 30 hari data, dan pasar USD (bukan BTC/IDR).
  - Paper lain kalah dekat: A2 harian dan berupa kombinasi ramalan; B1 harian dan targetnya return; B2–B4 klasifikasi arah; B5 harian.
  - Kuartil jurnal *Information* (MDPI) di SCImago dan Sinta belum dicek.
- **Versi dibaca:** terbit (MDPI, 21 hlm.); utuh. Nomor halaman = "x of 21".
1. **Penulis, tahun:** Fátima Rodrigues, Miguel Machado, 2025.
2. **Data:** harga per menit sepuluh kripto teratas, 12 Mei – 11 Jun 2024 (Tabel 2, hlm. 9). Eksperimen utama memakai Bitcoin.
3. **Bentuk data & sumber:**
   - Data mentah OHLCV per menit dari API YFinance (hlm. 9). YFinance hanya memberi 30 hari terakhir untuk data menit (hlm. 10).
   - Pencilan dibuang dengan metode IQR (hlm. 9).
   - Semua atribut diskalakan dengan MinMaxScaler ke rentang 0–1 (hlm. 9).
   - Pembagian 80% latih, 10% uji, 10% validasi; 60 titik terakhir untuk validasi (hlm. 9).
4. **Masalah:** metode peramalan yang ada kesulitan menghadapi harga kripto yang tidak stasioner dan kompleks (abstrak).
5. **Metode:**
   - LSTM dan GRU (Keras) dengan *grid search* jumlah neuron (30, 50, 75, 100) dan lapisan; terpilih 50 neuron, 2 lapisan (hlm. 10–11).
   - SARIMA, regresi linear (LR), Random Forest (100 pohon), XGBoost (100 pohon, *learning rate* 0,1), LightGBM dengan konfigurasi bawaan (hlm. 11).
   - Horizon 60 menit: 60 menit terakhir dipakai untuk meramal 60 menit berikutnya (hlm. 10).
   - Model dilatih dengan semua atribut dan dengan Close saja (hlm. 10).
6. **Hasil:**
   - GRU terbaik: MAE 60,20; RMSE 77,17; MAPE 0,09% (abstrak; Tabel 3, hlm. 12).
   - LR kedua terbaik (hlm. 11–12).
   - XGBoost dan LightGBM jauh lebih buruk dari GRU (Tabel 3, hlm. 12).
   - Uji Wilcoxon: MAE GRU signifikan lebih rendah dari LR, p = 0,00195 (hlm. 12; Tabel 4).
   - Kinerja GRU stabil sampai horizon 240 menit, lalu memburuk tajam pada 1.440 menit (Tabel 5, hlm. 13).
   - Model GRU dipasang di aplikasi web Streamlit dengan horizon 1–4 jam (hlm. 16).
7. **Metrik:** MSE, RMSE, MAE, MAPE, nRMSE (hlm. 10); uji Shapiro–Wilk lalu Wilcoxon (hlm. 12).
8. **Riset lanjutan:**
   - *Disebut paper:* validasi dengan data berbulan-bulan atau bertahun-tahun; teknik penanganan *concept drift* (hlm. 17).
   - *[PR]:* tambahkan pembanding naive dan uji DM; *tuning* untuk model boosting.
9. **Kelebihan [PR]:** data menit; banyak horizon; ada aplikasi nyata; membandingkan keluarga model yang beragam.
10. **Kekurangan [PR]:**
    - Hanya 30 hari data.
    - Boosting memakai konfigurasi bawaan, sedangkan RNN di-*tuning*. Perbandingannya tidak setara.
    - Tidak ada pembanding naive atau *random walk*. Tidak ada uji DM.
11. **Kejanggalan [PR]:**
    - **MinMaxScaler dipasang sebelum pembagian data** (hlm. 9). Statistik data uji ikut bocor ke data latih.
    - Uji Wilcoxon memakai data 1–10 Sep 2024, di luar periode dataset (Tabel 4, hlm. 12).
    - MSE horizon 60 menit di Tabel 5 bernilai 955, padahal Tabel 3 melaporkan 5.954,89 untuk model yang sama (hlm. 12–13).
    - Baris nRMSE di Tabel 5 hanya berisi 8 nilai untuk 9 horizon (hlm. 13).
    - Horizon 30 dan 45 menit lebih buruk dari 60 menit (Tabel 5). Ini tidak lazim dan tidak dijelaskan.
    - Angka MSE XGBoost tertulis "420,6051.13" (Tabel 3), salah ketik pemisah ribuan.
- **Boleh dikutip untuk:** peramalan harga kripto data menit dengan horizon pendek; boosting dengan setelan bawaan kalah dari GRU; kinerja memburuk saat horizon makin panjang (Tabel 5). **Jangan** untuk klaim boosting memang lebih buruk dari RNN (boosting tidak di-*tuning*); sebut kebocoran MinMaxScaler bila membandingkan angka.

---

### A2. `wei2023` — Wei, Sermpinis & Stasinakis (2023), "Forecasting and trading Bitcoin with machine learning techniques and a hybrid volatility/sentiment leverage", Journal of Forecasting 42(4), 852–871, doi 10.1002/for.2922
- **Peran:** **acuan cara evaluasi** (MDM Harvey dkk. + kontrol *data snooping*).
- **Versi dibaca:** terbit (20 hlm.); hlm. PDF. Volume, nomor, dan halaman (42(4), 852–871) dicek dari repositori Univ. Glasgow (Enlighten), 30 Okt 2026.
1. **Penulis, tahun:** Mingzhe Wei, Georgios Sermpinis, Charalampos Stasinakis, 2023.
2. **Data:** 1.749 harga harian BTC, 1 Jan 2014 – 1 Jan 2019 (hlm. PDF 3). Tiga *exercise* bergulir F1–F3; out-of-sample 110, 140, dan 139 hari (Tabel 1, hlm. PDF 4).
3. **Bentuk data & sumber:**
   - Harga harian dari Bitstamp, diolah menjadi return harian (hlm. PDF 3).
   - Dikombinasikan dengan indeks sentimen naratif dari berita (TextBlob, 10 topik harian) (hlm. PDF 3–4).
4. **Masalah:** meramal dan memperdagangkan BTC dengan ML dan sentimen, sambil memperhitungkan *data snooping* (abstrak).
5. **Metode:**
   - Pool 295 model individual linear: SMA, EMA, AR, ARMA, PMA. Model terbaik dari pool menjadi *benchmark* (hlm. PDF 4–5).
   - MLP, LSTM, ε-SVR, ν-SVR, XGBoost, LightGBM dipakai untuk **mengombinasikan** ramalan pool, dengan fitur pilihan RFE-RF dan 30 komponen PCA (hlm. PDF 5–8).
   - Strategi *leverage* berubah-waktu berbasis volatilitas dan sentimen (hlm. PDF 10–11).
6. **Hasil:**
   - Semua teknik ML mengungguli model individual terbaik; XGBoost terbaik (abstrak; Tabel 5, hlm. PDF 8).
   - MDM signifikan untuk XGBoost terhadap semua model lain, loss MAE dan MSE (Tabel 6, hlm. PDF 9).
   - XGBoost bertahan di MCS (p = 1) dan p SPA > 0,5 (Tabel 7, hlm. PDF 10).
   - Strategi *leverage* hibrida memberi profit tertinggi (abstrak).
7. **Metrik:** MAE, MSE, RMSE; MDM Harvey dkk. (1997); MCS; SPA Hansen (2005) (hlm. PDF 2, 9–10).
8. **Riset lanjutan:**
   - *Disebut paper:* memakai data intraday; meneliti pengaruh media sosial (kesimpulan, hlm. PDF 17).
   - *[PR]:* menambah *random walk* harga sebagai pembanding.
9. **Kelebihan [PR]:** satu-satunya paper kripto di set ini yang memakai MDM, MCS, dan SPA sekaligus; XGBoost dan LightGBM dibandingkan langsung.
10. **Kekurangan [PR]:**
    - Data harian dan out-of-sample pendek (110–140 hari).
    - Tidak ada *random walk*/naive harga di pool.
    - ML dipakai sebagai penggabung ramalan, bukan peramal langsung.
11. **Kejanggalan [PR]:**
    - Teks menyebut statistik MDM negatif berarti XGBoost lebih baik (hlm. PDF 9), tetapi semua nilai di Tabel 6 positif.
    - Beberapa baris MDM F1 identik antarpanel (Tabel 6).
    - Tanggal "31/06/2017" di Tabel 1 (Juni hanya 30 hari).
    - Biaya transaksi tidak ditemukan dalam penelusuran teks.
- **Boleh dikutip untuk:** pemakaian MDM (Harvey dkk., 1997) dengan loss MAE dan MSE pada peramalan BTC; kontrol *data snooping* dengan MCS dan SPA; XGBoost unggul dalam kombinasi ramalan harian. **Jangan** untuk klaim intraday atau perbandingan dengan naive harga.

---

## B. Peramalan kripto dengan boosting dan ML

### B1. `bouteska2024` — Bouteska, Abedin, Hajek & Yuan (2024), "Cryptocurrency price forecasting – A comparative analysis of ensemble learning and deep learning methods", International Review of Financial Analysis 92, 103055, doi 10.1016/j.irfa.2023.103055
- **Versi dibaca:** terbit (OA, 12 hlm.); utuh.
1. **Penulis, tahun:** Ahmed Bouteska, Mohammad Zoynul Abedin, Petr Hajek, Kunpeng Yuan, 2024.
2. **Data:** BTC/USD, ETH/USD, LTC/USD, XRP/USD harian, 1 Apr 2016 – 31 Agu 2023. Dibagi pra-Covid (1.370 obs.) dan pasca-Covid (1.339 obs.), titik potong 1 Jan 2020 (Tabel 2, hlm. 5).
3. **Bentuk data & sumber:** harga harian dari investing.com (hlm. 4), diolah menjadi selisih pertama log harga, yaitu return log (hlm. 5). Input 5 atau 10 harga sebelumnya (hlm. 6).
4. **Masalah:** belum ada perbandingan menyeluruh *ensemble* dan *deep learning* untuk kripto, termasuk kinerja strategi trading (hlm. 2).
5. **Metode:**
   - AdaBoost dan LightGBM; RNN sederhana, GRU, LSTM; hibrida ARIMA+MLP dan ARIMA+LSTM; ARIMA dan MLP (hlm. 3–4).
   - *Grid search* dengan *rolling window cross-validation*, minimasi MSE (hlm. 4; Tabel 1).
   - Grid boosting: n_estimators 10–100, *learning rate* {0,001; 0,01; 0,1; 1,0}; loss {linear, square, exponential} (Tabel 1, hlm. 4).
   - Pembanding naive: *random walk* (nilai terakhir), *white noise*, *buy & sell* (hlm. 6).
6. **Hasil:**
   - Untuk BTC, MAE LightGBM 0,0205 (pra) dan 0,0168 (pasca); AdaBoost 0,0221 dan 0,0170; RW 0,0421 dan 0,0324 (Tabel 4, hlm. 7).
   - LightGBM dan AdaBoost terbaik pada metrik regresi untuk BTC dan ETH (hlm. 7).
   - Uji Friedman: LightGBM peringkat pertama untuk BTC, ETH, LTC; RNN sederhana untuk XRP (hlm. 8).
7. **Metrik:** MAPE, ME, MAE, MPE, RMSE, R, MIN-MAX; SP, Return, MDA (hlm. 6); uji Friedman (hlm. 7–8). Tidak ada uji DM.
8. **Riset lanjutan:** *disebut paper:* return portofolio (hlm. 10); data *real-time* lebih sering dan data multivariat (hlm. 11).
9. **Kelebihan [PR]:** empat koin; dua subperiode; pembanding naive tersedia; metrik investor.
10. **Kekurangan [PR]:** data harian; tidak ada uji DM; hanya dua booster; biaya transaksi tidak disebut.
11. **Kejanggalan [PR]:**
    - **RW dihitung pada seri return**, sehingga ramalannya return kemarin. Itu bukan naive harga. *White noise* (≈ return nol) lebih setara naive harga, dan WN mengalahkan RW di semua tabel.
    - MAPE dihitung pada return yang mendekati nol, sehingga tidak stabil.
    - Teks hlm. 4 menyebut tiga fungsi loss untuk LightGBM, sedangkan Tabel 1 menaruhnya di AdaBoost.
    - Catatan kaki 1 (hlm. 4) menyebut metode *ensemble* diimplementasikan dengan Scikit-Learn, padahal LightGBM adalah pustaka terpisah.
- **Boleh dikutip untuk:** LightGBM dan AdaBoost kompetitif untuk return BTC harian (Tabel 4, hlm. 7–8). **Jangan** kutip "mengalahkan *random walk*" sebagai bukti mengalahkan naive harga.

---

### B2. `jaquart2021` — Jaquart, Dann & Weinhardt (2021), "Short-term bitcoin market prediction via machine learning", The Journal of Finance and Data Science 7, 45–66, doi 10.1016/j.jfds.2021.03.001
- **Versi dibaca:** terbit (OA, 22 hlm.); hlm. PDF (hlm. PDF 1 = hlm. 45).
1. **Penulis, tahun:** Patrick Jaquart, David Dann, Christof Weinhardt, 2021.
2. **Data:** data menit 4 Mar – 10 Des 2019 (hlm. PDF 4); sampel akhir 11 Mar – 10 Des 2019 karena butuh histori 7 hari (hlm. PDF 7).
3. **Bentuk data & sumber:**
   - Dikombinasikan dari Bloomberg (harga BTC, emas, minyak, indeks, kurs), Blockchain.com (fitur *blockchain*), dan Twitter (sentimen #bitcoin) (hlm. PDF 4–5).
   - Akhir pekan dibuang karena celah data Bloomberg (hlm. PDF 7).
   - Fitur distandardisasi dengan statistik data latih (hlm. PDF 6). Model tanpa memori memakai 169 fitur agregat dari 120 menit terakhir (hlm. PDF 6).
4. **Masalah:** keterdugaan pasar bitcoin jangka pendek (di bawah 1 jam) belum dianalisis secara menyeluruh (hlm. PDF 1, 4).
5. **Metode:**
   - Klasifikasi biner: return m menit ke depan ≥ median return data latih, m ∈ {1, 5, 15, 60} (hlm. PDF 6).
   - Split kronologis: 5/9 latih, 1/9 validasi, 3/9 uji (hlm. PDF 7).
   - GRU, LSTM, FNN, regresi logistik, *gradient boosting classifier* (XGBoost), RF, *ensemble* (hlm. PDF 5, 7). *Tuning* grid dengan akurasi validasi (Tabel 2, hlm. PDF 7).
6. **Hasil:**
   - Semua model mengungguli klasifikasi acak (abstrak).
   - Akurasi GBC 0,5111 / 0,5293 / 0,5373 / 0,5570 untuk 1, 5, 15, 60 menit (Tabel 3, hlm. PDF 11).
   - Keterdugaan naik seiring horizon makin panjang (abstrak; hlm. PDF 11).
   - Strategi *long-short* kuantil memberi return bulanan hingga 39% sebelum biaya, tetapi negatif setelah biaya 30 bps per *round-trip* (abstrak; hlm. PDF 11–13).
7. **Metrik:** akurasi; uji binomial terhadap 50% (Tabel 4); uji Diebold–Mariano antarmodel (hlm. PDF 10–11); return trading.
8. **Riset lanjutan:** *disebut paper:* efek momentum; fitur volume trading; bias perilaku seperti *disposition effect*; apakah mekanisme pasar tetap bertahan (hlm. PDF 13–14).
9. **Kelebihan [PR]:** horizon 1–60 menit hampir sama dengan skripsi; split kronologis; standardisasi tanpa kebocoran; ada uji DM dan biaya transaksi.
10. **Kekurangan [PR]:** target arah, bukan nilai harga; data tanpa akhir pekan; sembilan bulan data.
11. **Kejanggalan [PR]:** GBC terpilih dengan kedalaman pohon 1 (Tabel 2, hlm. PDF 7), artinya *stump*. Tidak dibahas.
- **Boleh dikutip untuk:** keterdugaan BTC jangka pendek kecil tetapi di atas acak; makin panjang horizon makin mudah diramal; untung sebelum biaya bisa menjadi rugi setelah biaya (hlm. PDF 11–13). **Jangan** untuk klaim regresi harga.

---

### B3. `akyildirim2023` — Akyildirim, Cepni, Corbet & Uddin (2023), "Forecasting mid-price movement of Bitcoin futures using machine learning", Annals of Operations Research 330, 553–584, doi 10.1007/s10479-021-04205-x
- **Versi dibaca:** terbit (salinan ZORA Univ. Zurich, 33 hlm.); hlm. PDF (hlm. PDF 1 = sampul repositori).
1. **Penulis, tahun:** Erdinc Akyildirim, Oguzhan Cepni, Shaen Corbet, Gazi Salah Uddin, 2023.
2. **Data:** CME Bitcoin *futures* jatuh tempo 1–5 bulan, data menit 2 Jan – 10 Sep 2020 (hlm. PDF 6–7).
3. **Bentuk data & sumber:** *mid-price* dihitung dari harga *ask* dan *bid* terbaik pada tiap frekuensi (hlm. PDF 6); frekuensi 5, 10, 15, 30, 60 menit (Tabel 1, hlm. PDF 7).
4. **Masalah:** kinerja berbagai algoritme ML dalam meramal arah *mid-price* Bitcoin *futures* (abstrak).
5. **Metode:**
   - kNN, regresi logistik, Naive Bayes, RF, SVM, XGBoost (hlm. PDF 7–12).
   - Target tanda return *mid-price* periode berikutnya (hlm. PDF 12).
   - **Tiga pembagian *hold-out*: 0,7/0,3; 0,8/0,2; 0,9/0,1** (Tabel 1, hlm. PDF 7; hlm. PDF 12).
   - Pembanding ARIMA dan *random walk* (hlm. PDF 13; Tabel 9).
6. **Hasil:**
   - Akurasi rata-rata lima dari enam algoritme konsisten di atas 50% (abstrak).
   - XGBoost sekitar 55% out-of-sample; SVM sekitar 56%; ARIMA sekitar 52% (hlm. PDF 28).
   - RF punya akurasi in-sample tertinggi, tetapi out-of-sample jauh lebih rendah (hlm. PDF 13).
7. **Metrik:** *success ratio* (akurasi tanda) dan *ideal profit ratio* (hlm. PDF 12); uji t beda rata-rata berpasangan (Tabel 10, hlm. PDF 29).
8. **Riset lanjutan:** *disebut paper:* ML untuk prediksi dan valuasi opsi dan *swap* (hlm. PDF 30).
9. **Kelebihan [PR]:** banyak frekuensi intraday; tiga rasio split; lima jatuh tempo.
10. **Kekurangan [PR]:** pasar *futures* CME dengan jam terbatas, bukan spot 24/7; target arah; tidak ada uji DM; biaya transaksi tidak dimasukkan.
11. **Kejanggalan [PR]:** *random walk* hanya berarti akurasi 50% (hlm. PDF 13), bukan model ramalan harga.
- **Boleh dikutip untuk:** preseden menguji beberapa rasio split (70:30, 80:20, 90:10) pada data Bitcoin intraday; RF *overfitting* (in-sample jauh di atas out-of-sample). **Jangan** untuk klaim pasar spot.

---

### B4. `akyildirim2021` — Akyildirim, Goncu & Sensoy (2021), "Prediction of cryptocurrency returns using machine learning", Annals of Operations Research 297, 3–36, doi 10.1007/s10479-020-03575-y
- **Versi dibaca:** terbit (34 hlm.); hlm. PDF (hlm. PDF 1 = hlm. 3); bagian data, desain, dan hasil ditelusuri.
1. **Penulis, tahun:** Erdinc Akyildirim, Ahmet Goncu, Ahmet Sensoy, 2021.
2. **Data:** 12 kripto paling likuid; BTC 1 Apr 2013 – 23 Jun 2018 (hlm. PDF 5).
3. **Bentuk data & sumber:** harga dalam USD dari bursa Bitfinex (hlm. PDF 4); frekuensi 15, 30, 60 menit, dan harian (catatan kaki 4, hlm. PDF 5); 40 fitur harga lampau dan indikator teknikal (hlm. PDF 6; tabel fitur hlm. PDF 12).
4. **Masalah:** keterdugaan return kripto pada frekuensi harian dan menit (abstrak).
5. **Metode:** klasifikasi tanda return periode berikutnya; harian memakai return *open-to-close* hari berikutnya (hlm. PDF 15). SVM, regresi logistik, ANN, RF (sklearn) (abstrak; hlm. PDF 13–16). Data harian 80% latih; data menit dibagi tiga subperiode dan diuji juga dengan 90/10 (hlm. PDF 16).
6. **Hasil:** akurasi rata-rata 55–65%; SVM paling konsisten (abstrak).
7. **Metrik:** akurasi klasifikasi in-sample dan out-of-sample.
8. **Riset lanjutan:** tidak dicatat.
9. **Kelebihan [PR]:** 12 koin dan empat frekuensi.
10. **Kekurangan [PR]:** tidak ada boosting; target arah; pembanding naive, uji DM, dan biaya transaksi tidak ditemukan.
11. **Kejanggalan [PR]:** tidak ditemukan pada bagian yang ditelusuri.
- **Boleh dikutip untuk:** ada keterdugaan arah kripto di atas 50% pada data intraday dan harian (abstrak). **Jangan** untuk klaim boosting.

---

### B5. `puoti2024` — Puoti, Pittorino & Roveri (2024), "Quantifying Cryptocurrency Unpredictability: A Comprehensive Study of Complexity and Forecasting", AIMLSystems 2024, ACM, doi 10.1145/3703412.3703420
- **Versi dibaca:** **versi penulis arXiv 2502.09079v1** (8 hlm.); hlm. PDF. Versi rekam ACM perlu dicek.
1. **Penulis, tahun:** Francesco Puoti, Fabrizio Pittorino, Manuel Roveri, 2024.
2. **Data:** harga harian LTC, BNB, BTC, ETH, XRP dalam USD, 3 Jul 2020 – 21 Des 2023 (hlm. 3).
3. **Bentuk data & sumber:** Yahoo Finance; tanpa praproses (hlm. 3). Data uji 180 titik terakhir mulai 4 Jul 2023; window latih 3 tahun, 1 tahun, 6 bulan (hlm. 3).
4. **Masalah:** seberapa besar keterdugaan univariat deret harga kripto (abstrak).
5. **Metode:**
   - Analisis kompleksitas: bidang Complexity-Entropy dan *power spectral density*, dibandingkan dengan derau berwarna (hlm. 3–5).
   - Model peramalan (Darts): NaiveDrift, NaiveSeasonal, ARIMA/AutoARIMA, AutoETS, AutoCES, TBATS, RandomForest, XGBModel, RNN, LSTM, dll. (Tabel 1, hlm. 4).
   - Horizon 1, 7, 30 hari; *backtest* bergulir dengan pelatihan ulang (hlm. 4).
6. **Hasil:**
   - Deret kripto paling mirip derau Brown (Tabel 2, hlm. 4–5).
   - **Model naive konsisten mengungguli model ML dan DL** (abstrak). Contoh BTC, window 3 tahun, h = 1: MAPE NaiveSeasonal 1,296; RandomForest 1,675; XGBModel 1,902 (Tabel 3, hlm. 6).
   - Model statistik canggih tidak lebih baik secara signifikan dari naive (hlm. 5, 7).
7. **Metrik:** MAPE (hlm. 4); jarak Jensen–Shannon ke derau (Tabel 2).
8. **Riset lanjutan:** *disebut paper:* mencari kovariat yang paling relevan dan cara memasukkan kovariat masa depan tanpa menambah ketidakpastian berlebihan (hlm. 7–8).
9. **Kelebihan [PR]:** menggabungkan analisis kompleksitas dan peramalan; banyak model; backtest bergulir.
10. **Kekurangan [PR]:** data harian; univariat; hanya MAPE; prosiding konferensi.
11. **Kejanggalan [PR]:** klaim "tidak signifikan" tidak disertai nama uji statistik yang jelas; *tuning* hiperparameter tidak disebut.
- **Boleh dikutip untuk:** model naive sulit dikalahkan pada peramalan harga kripto univariat (abstrak; Tabel 3). **Jangan** untuk klaim intraday.

---

### B6. `dudek2025lgbm` *(usulan key)* — Dudek, Kasprzyk & Pełka (2025), "Multivariate Forecasting of Bitcoin Volatility with Gradient Boosting: Deterministic, Probabilistic, and Feature Importance Perspectives", arXiv:2511.20105
- **Relevansi v3 [PR]:** contoh LightGBM untuk Bitcoin, tetapi targetnya volatilitas (RV), bukan harga. Pakai sebagai pendukung minor; status preprint. *(Kartu lama; dibaca ulang 3 Nov 2026.)* **Untuk v3 [PR]:** contoh Optuna untuk *tuning* LightGBM pada Bitcoin (hlm. PDF 24), tetapi *tuning* hanya sekali sebelum periode uji. **Catatan:** poin 10–11 dan "Boleh dikutip" ditulis untuk v2 (target volatilitas); untuk v3 pegang baris "Untuk v3".
- **Status:** **preprint** (diajukan ke Expert Systems with Applications, belum terbit); **belum di `.bib`**.
- **Versi dibaca:** preprint v1 (25 Nov 2025); hlm. PDF; bagian data, desain, hasil, dan penutup dibaca.
1. **Penulis, tahun:** Grzegorz Dudek, Mateusz Kasprzyk, Paweł Pełka, 2025.
2. **Data:**
   - RV harian BTC/USD dari return 5 menit, 2 Agu 2017 – 31 Mar 2023; **hanya Senin–Jumat**, 1.478 observasi (hlm. PDF 8).
   - Uji deterministik 1 Jan 2020 – 31 Mar 2023 (848 hari); uji probabilistik tahun 2021 (261 hari) (hlm. PDF 23).
3. **Bentuk data & sumber:** dataset publik dari Fiszeder dkk. (2025) dengan 69 prediktor (pasar, perilaku, makro), log RV dan lag harian/mingguan/bulanan (hlm. PDF 8); *winsorization* 1–99% dan standardisasi yang dihitung dari data latih saja (hlm. PDF 23).
4. **Masalah:** meramal volatilitas Bitcoin secara deterministik dan probabilistik serta mengidentifikasi pendorongnya (abstrak).
5. **Metode:**
   - LightGBM (variasi dengan/tanpa indikator *shock*, *ensemble* 32 model); kuantil dengan *pinball loss* dan simulasi residual (QRS).
   - Model dilatih ulang setiap hari dengan data sebelumnya yang terus bertambah (hlm. PDF 23).
   - Hiperparameter dicari **sekali** sebelum periode uji (Optuna, validasi silang 3 lipat); **GOSS tidak lebih baik dari GBDT standar, jadi dipakai GBDT** (hlm. PDF 24).
   - Pembanding: HAR, BMA, LASSO, RF (dari Fiszeder dkk., 2025) (hlm. PDF 25).
6. **Hasil:**
   - LGBM lebih rendah MSE (8,9e-6 vs HAR 2,37e-5) dan lebih tinggi R² (0,67 vs 0,13) (Tabel 2, hlm. PDF 28).
   - **Uji DM hanya signifikan pada satu perbandingan**; perbedaan umumnya tidak signifikan (hlm. PDF 29).
   - Uji Wilcoxon: LGBM lebih baik dari HAR, BMA, LASSO, **tetapi tidak dari RF** (hlm. PDF 29).
   - Volume, lag RV, Google Trends, dan kapitalisasi pasar paling penting (hlm. PDF 48).
7. **Metrik:** MAE, sMAPE, MSE, R²; CRPS, Winkler, MARFE (probabilistik); uji DM dan Wilcoxon. **Tidak memakai QLIKE.**
8. **Riset lanjutan:** *disebut paper:* kerangka GBM probabilistik seperti NGBoost (hlm. PDF 45); definisi indikator *shock* yang lebih baik atau kerangka *regime switching* (hlm. PDF 48).
9. **Kelebihan [PR]:** banyak prediktor; ramalan probabilistik; pelatihan ulang harian; kebocoran informasi dicegah pada praproses.
10. **Kekurangan [PR]:** satu periode uji; hiperparameter statis; hari akhir pekan dibuang untuk aset 24/7; status preprint.
11. **Kejanggalan [PR]:**
   - Kesimpulan menyatakan LGBM "outperforms econometric and random forest baselines" (hlm. PDF 48), padahal uji Wilcoxon menunjukkan LGBM **tidak** lebih baik dari RF dan uji DM hampir tidak pernah signifikan (hlm. PDF 29).
   - Uji DM dijelaskan sebagai uji pada "residuals (E)", bukan selisih loss (hlm. PDF 28).
   - Disebut *rolling-origin*, tetapi data latih bertambah (*expanding*) (hlm. PDF 23).
- **Boleh dikutip untuk:** LightGBM sudah dipakai untuk RV Bitcoin; GOSS tidak memperbaiki hasil; keunggulan atas HAR tidak signifikan menurut DM. **Jangan** dikutip sebagai bukti kuat LightGBM unggul atas HAR; tulis sebagai preprint.

---

### B7. `nadarajah2025` *(usulan key)* — Nadarajah, Mba, Rakotomarolahy & Ratolojanahary (2025), Journal of Risk and Financial Management 18(2), 52, doi 10.3390/jrfm18020052
- **Relevansi v3 [PR]:** contoh boosting (termasuk LightGBM) untuk kripto dengan setelan bawaan. Pendukung argumen bahwa *tuning* sering diabaikan. *(Kartu lama; dibaca ulang 3 Nov 2026.)* DOI dicek dari PDF 3 Nov 2026 (diterima 28 Okt 2024, terbit 24 Jan 2025). **Untuk v3 [PR]:** bukti studi kripto memakai setelan boosting tetap tanpa *tuning* (LightGBM 31 daun, 100 iterasi, lr 0,1; hlm. 11). **Catatan:** poin 10–11 dan "Boleh dikutip" ditulis untuk v2 (target volatilitas); untuk v3 pegang baris "Untuk v3".
- **Status:** terbit (MDPI); **belum di `.bib`**; kuartil belum dicek.
- **Versi dibaca:** terbit; utuh.
1. **Penulis, tahun:** Saralees Nadarajah, Jules Clement Mba, Patrick Rakotomarolahy, Henri T. J. E. Ratolojanahary, 2025.
2. **Data:** harga penutupan harian BTC, ETH, LTC, 1 Jan 2017 – 31 Jan 2024 (hlm. 8); latih 2017–2021, evaluasi 1 Jan 2022 – 31 Jan 2024 (hlm. 10).
3. **Bentuk data & sumber:** data mentah dari investing.com, diolah menjadi log return (hlm. 8). **Target volatilitas untuk model ML tidak dijelaskan eksplisit** pada bagian yang dibaca.
4. **Masalah:** membandingkan GARCH, *ensemble* pohon, dan ANFIS untuk volatilitas kripto (abstrak).
5. **Metode:** GARCH-type (sGARCH, eGARCH, dll.), GBM, XGBM, LightGBM (pengaturan bawaan: 31 daun, 100 iterasi, lr 0,1), ANFIS (hlm. 11).
6. **Hasil:** XGBM paling akurat; beberapa GARCH tidak jauh tertinggal (abstrak; Tabel 8, hlm. 12).
7. **Metrik:** RMSE dan RSE (hlm. 10).
8. **Riset lanjutan:** tidak dicatat pada bagian yang dibaca.
9. **Kelebihan [PR]:** membandingkan tiga keluarga model sekaligus.
10. **Kekurangan [PR]:** tidak ada HAR atau RV intraday; satu pembagian data; hanya RMSE/RSE; tidak ada uji signifikansi; hiperparameter bawaan.
11. **Kejanggalan [PR]:** target volatilitas untuk model ML tidak didefinisikan jelas; GARCH dievaluasi juga pada data latih (in-sample) bersama out-of-sample.
- **Boleh dikutip untuk:** contoh studi *ensemble* pohon (termasuk LightGBM) untuk volatilitas kripto dengan satu periode uji. **Jangan** untuk klaim ML vs HAR.

---

### B8. `oprea2026` — Oprea & Bâra (2026), "Regime-Aware Adaptive Forecasting Framework for Bitcoin Prices Using Probabilistic Generative Models", Computational Economics, doi 10.1007/s10614-026-11338-3
- **Relevansi v3 [PR]:** peramalan **harga** Bitcoin dengan XGBoost sebagai *meta-learner* dan uji DM. Relevan karena targetnya harga. *(Kartu lama; dibaca ulang 3 Nov 2026.)* DOI dicek dari PDF 3 Nov 2026 (diterima 25 Okt 2025, disetujui 4 Mar 2026). **Untuk v3 [PR]:** target harga dan uji DM; contoh pembanding yang **tanpa naive** (lihat poin 11). **Catatan:** poin 10–11 dan "Boleh dikutip" ditulis untuk v2 (target volatilitas); untuk v3 pegang baris "Untuk v3".
- **Versi dibaca:** terbit daring (DOI 10.1007/s10614-026-11338-3); bagian abstrak, desain, dan hasil dibaca.
1. **Penulis, tahun:** Simona-Vasilica Oprea, Adela Bâra, 2026.
2. **Data:** log return dan harga harian Bitcoin Jan 2012 – Jun 2025; evaluasi Jan–Jun 2025 (abstrak; hlm. PDF 16, 19).
3. **Bentuk data & sumber:** harga harian dikombinasikan dengan indikator teknikal (RSI, MACD, Bollinger) dan metrik volatilitas (abstrak).
4. **Masalah:** meramal **harga** Bitcoin yang berpindah rezim (abstrak).
5. **Metode:** HMM untuk tiga rezim (*bull*, *bear*, *sideways*); ARIMAX, SARIMAX, NeuralProphet per rezim; *meta-learner* XGBoost; *rolling-window backtesting* (abstrak).
6. **Hasil:** model sadar-rezim mengungguli model tanpa rezim (MAE turun sekitar 56%; R² 0,82 → 0,91) (abstrak); uji DM signifikan (hlm. PDF 22–23).
7. **Metrik:** R², MAE, RMSE; DM; *backtest* perdagangan.
8. **Riset lanjutan:** tidak dicatat pada bagian yang dibaca.
9. **Kelebihan [PR]:** kerangka adaptif yang menggabungkan rezim dan *meta-learning*.
10. **Kekurangan [PR]:** **target harga, bukan volatilitas; tidak ada HAR**; periode uji enam bulan.
11. **Kejanggalan [PR]:**
   - Ablasi "per tahun" hanya untuk satu tahun (Tabel 5, hlm. PDF 24).
   - *(Ditambah 3 Nov 2026.)* Pembanding hanya NeuralProphet dan ARIMAX tanpa rezim; **tidak ada naive/random walk** (Tabel 3, hlm. 22).
   - *(Ditambah 3 Nov 2026.)* Paper menyatakan tidak memakai data masa depan (hlm. 10), tetapi rezim diestimasi dengan algoritme Viterbi atas urutan state (hlm. 14). Bila dijalankan pada seluruh deret, ini memakai informasi masa depan; tidak jelas apakah dijalankan per window.
   - *(Ditambah 3 Nov 2026.)* Tabel 3 menulis "1 Jan. − 31 Jun., 2025", padahal Juni hanya 30 hari (hlm. 22).
- **Boleh dikutip untuk:** rezim pasar Bitcoin dan model adaptif untuk **harga**. **Jangan** untuk klaim tentang volatilitas, RV, atau ukuran kesalahan proksi volatilitas.

---

## C. Horizon waktu dan tipe trader

### C1. `muller1997` — Müller, Dacorogna, Davé, Olsen, Pictet & von Weizsäcker (1997), "Volatilities of different time resolutions – Analyzing the dynamics of market components", Journal of Empirical Finance 4, 213–239
- **Versi dibaca:** terbit (27 hlm.); nomor halaman = halaman jurnal.
1. **Penulis, tahun:** Ulrich A. Müller, Michel M. Dacorogna, Rakhal D. Davé, Richard B. Olsen, Olivier V. Pictet, Jacob E. von Weizsäcker, 1997.
2. **Data:** USD-DEM harian 6 Jun 1973 – 1 Feb 1995 (Gambar 1, hlm. 218); data intraday grid 30 menit dalam waktu ϑ, lebih dari 8 tahun (hlm. 219); kurs lain dan emas sebagai pembanding (hlm. 218–219).
3. **Bentuk data & sumber:** kuotasi FX Olsen & Associates; data intraday dideseasonalisasi dengan skala waktu ϑ (hlm. 219).
4. **Masalah:** pelaku pasar berbeda horizon waktunya, sehingga volatilitas pada resolusi waktu berbeda berperilaku berbeda (abstrak; hlm. 214).
5. **Metode:** korelasi berlag antara volatilitas kasar (*coarse*) dan halus (*fine*); model HARCH yang memakai kuadrat perubahan harga dari interval berbeda ukuran (abstrak; bagian 3).
6. **Hasil:**
   - Volatilitas kasar memprediksi volatilitas halus lebih baik daripada sebaliknya (abstrak; hlm. 215).
   - HARCH mereproduksi asimetri ini, sedangkan GARCH tidak (hlm. 215).
   - Tabel 3 (hlm. 226) membagi pasar menjadi 7 komponen:
     - 1 (7–80 menit): dealer intraday jangka pendek, arbitrase, *market maker*;
     - 2 (16 menit – 3,5 jam): dealer intraday dengan beberapa transaksi per hari;
     - 3 (50 menit – 9 jam): dealer dengan posisi semalam;
     - 4 (4 jam – 1 hari);
     - 5 (1 – 3,5 hari): trader jangka menengah, tanpa trading intraday;
     - 6 (3,5 – 21 hari): trader jangka panjang;
     - 7 (3 – 12 minggu): investor jangka panjang, bank sentral.
7. **Metrik:** korelasi berlag; parameter HARCH dan dampak tiap komponen (Tabel 4, hlm. 229).
8. **Riset lanjutan:** *disebut paper:* pemodelan volatilitas perlu mempertimbangkan memori selektif pasar geografis dan zona waktunya (hlm. 221).
9. **Kelebihan [PR]:** pemetaan eksplisit horizon waktu ke tipe pelaku pasar; dasar hipotesis pasar heterogen.
10. **Kekurangan [PR]:** data FX, bukan kripto; pasar dengan jam aktif berbeda per zona waktu.
11. **Kejanggalan [PR]:** tidak ditemukan. Penulis sendiri menyebut deskripsi komponen "tentative" dan skemanya tidak kaku (catatan Tabel 3, hlm. 226).
- **Boleh dikutip untuk:** pelaku pasar berbeda menurut horizon waktu; pemetaan horizon menit ke dealer intraday (komponen 1–2) dan horizon hari ke trader jangka menengah (komponen 5) (Tabel 3, hlm. 226). **Jangan** tulis pemetaan ini sebagai hasil di pasar kripto.

---

### C2. `dacorogna1995` — Dacorogna, Müller, Jost, Pictet & Ward (1995), "Heterogeneous real-time trading strategies in the foreign exchange market", The European Journal of Finance 1(4), 383–403, doi 10.1080/13518479500000026
- **Versi dibaca:** terbit (unduhan Taylor & Francis; hlm. PDF 1 = sampul); nomor halaman = halaman jurnal.
1. **Penulis, tahun:** M.M. Dacorogna, U.A. Müller, C. Jost, O.V. Pictet, J.R. Ward, 1995.
2. **Data:** harga tik FX, sekitar 5.000 harga per hari untuk USD-DEM (abstrak; hlm. 386); contoh model USD-DEM Mar 1986 – Sep 1992 (Tabel 1, hlm. 392).
3. **Bentuk data & sumber:** kuotasi FX Olsen & Associates, difilter (hlm. 386).
4. **Masalah:** dealer FX berbeda zona waktu, jam kerja, horizon, akses informasi, dan biaya transaksi; asumsi pasar homogen 24 jam tidak realistis (abstrak; hlm. 383–384).
5. **Metode:** model trading intraday *real-time* Olsen & Associates yang hanya trading pada jam buka pasar dan memperhitungkan biaya transaksi penuh (hlm. 385); diuji ex ante lebih dari tiga tahun (abstrak).
6. **Hasil:**
   - Semua model menguntungkan tetapi berbeda perilaku risiko dan frekuensi transaksi (abstrak).
   - Kinerja berubah bila jam kerja diganti ke pasar lain (Frankfurt, London, New York, Singapura, Tokyo, Wina) (Tabel 3, hlm. 394).
   - Model dikelompokkan menurut frekuensi transaksi per minggu (Tabel 2, hlm. 393).
7. **Metrik:** *effective return* X_eff yang memasukkan risiko; *maximum drawdown*; kritik atas rasio Sharpe (hlm. 388–390).
8. **Riset lanjutan:** tidak dicatat.
9. **Kelebihan [PR]:** uji ex ante nyata; biaya transaksi dihitung; ukuran kinerja yang memasukkan risiko.
10. **Kekurangan [PR]:** FX, bukan kripto; algoritme trading tidak dijelaskan rinci (merujuk Pictet dkk., 1992).
11. **Kejanggalan [PR]:** tidak ditemukan.
- **Boleh dikutip untuk:** strategi dengan horizon dan frekuensi trading berbeda menghasilkan profil risiko berbeda; pasar terdiri dari pelaku heterogen (abstrak). **Jangan** untuk klaim jam buka pasar pada kripto 24/7.

---

### C3. `barberdt` *(usulan key)* — Barber, Lee, Liu & Odean (2014), "The cross-section of speculator skill: Evidence from day trading", Journal of Financial Markets 18, 1–24, doi 10.1016/j.finmar.2013.05.006
- **Versi dibaca:** **working paper Des 2012** (44 hlm.); hlm. PDF. Data terbit dicek dari IDEAS/RePEc (30 Okt 2026). Isi kartu dari versi WP; angka dan halaman bisa berbeda dari versi terbit.
1. **Penulis, tahun:** Brad M. Barber, Yi-Tsung Lee, Yu-Jane Liu, Terrance Odean (WP 2012).
2. **Data:** seluruh *day trader* di Bursa Efek Taiwan, 1992–2006 (abstrak, hlm. PDF 2).
3. **Bentuk data & sumber:** data transaksi dari Taiwan Stock Exchange (hlm. PDF 1).
4. **Masalah:** apakah sebagian investor individu punya keahlian spekulasi yang konsisten (hlm. PDF 3–4).
5. **Metode:** *day trading* didefinisikan sebagai beli dan jual saham yang sama oleh investor yang sama pada hari yang sama (hlm. PDF 4). Trader diurutkan menurut return tahun y, lalu kinerjanya di tahun y+1 diamati (abstrak).
6. **Hasil:**
   - *Day trading* menyumbang 17% volume TWSE (hlm. PDF 4).
   - Mayoritas *day trader* rugi (hlm. PDF 4).
   - 500 trader teratas: 61,3 bps per hari sebelum biaya dan 37,9 bps setelah biaya; trader terbawah −11,5 dan −28,9 bps (abstrak).
   - Kurang dari 1% *day trader* yang konsisten untung setelah biaya (abstrak; hlm. PDF 5).
7. **Metrik:** return harian sebelum dan sesudah biaya (bps). Biaya: pajak jual 30 bps dan komisi hingga 14,25 bps satu arah (hlm. PDF 6, 10).
8. **Riset lanjutan:** tidak dicatat.
9. **Kelebihan [PR]:** data populasi lengkap selama 15 tahun.
10. **Kekurangan [PR]:** saham Taiwan, bukan kripto; status WP pada versi yang dibaca.
11. **Kejanggalan [PR]:** tidak ditemukan.
- **Boleh dikutip untuk:** horizon sangat pendek identik dengan spekulasi; biaya transaksi menggerus untung trader jangka pendek; sangat sedikit trader yang konsisten untung (abstrak). **Jangan** untuk klaim di pasar kripto.

---

### C4. `kirilenko2017` *(usulan key)* — Kirilenko, Kyle, Samadi & Tuzun (2017), "The Flash Crash: High-Frequency Trading in an Electronic Market", Journal of Finance 72(3), 967–998, doi 10.1111/jofi.12498
- **Versi dibaca:** **versi SSRN 1686004** (42 hlm.); hlm. PDF. Volume, nomor, halaman, dan DOI dari halaman CFTC; tahun 2017 dari repositori Cambridge. Halaman CFTC menulis judul sedikit berbeda, jadi **cek di doi.org**.
1. **Penulis, tahun:** Andrei Kirilenko, Albert S. Kyle, Mehrdad Samadi, Tugkan Tuzun.
2. **Data:** data *audit trail* tingkat transaksi E-mini S&P 500 *futures*, 3–6 Mei 2010 (abstrak; hlm. PDF 5).
3. **Bentuk data & sumber:** data transaksi per akun dari CFTC; lebih dari 15.000 akun (hlm. PDF 11).
4. **Masalah:** bagaimana intermediari intraday nonresmi bertindak saat tekanan jual besar dan sementara (hlm. PDF 4–5).
5. **Metode:** akun diklasifikasi menurut pola inventaris dan volume. Intermediari intraday = akun tanpa posisi arah besar dan inventarisnya *mean-reverting* (hlm. PDF 5). Kategori: High Frequency Traders (16 akun paling aktif), Market Makers, Fundamental Buyers, Fundamental Sellers, Small Traders (lebih dari 6.000 akun), Opportunistic Traders (hlm. PDF 13–14).
6. **Hasil:** pola trading HFT tidak berubah saat harga jatuh di Flash Crash (abstrak); perubahan inventaris HFT terkait perubahan harga dalam hitungan detik (hlm. PDF 6).
7. **Metrik:** inventaris bersih, volume, regresi perubahan inventaris terhadap perubahan harga.
8. **Riset lanjutan:** tidak dicatat.
9. **Kelebihan [PR]:** data per akun yang sangat langka; klasifikasi tipe trader berbasis perilaku.
10. **Kekurangan [PR]:** empat hari data; satu kontrak; bukan studi peramalan.
11. **Kejanggalan [PR]:** tidak ditemukan.
- **Boleh dikutip untuk:** tipe trader dapat dibedakan dari horizon dan perilaku inventaris (HFT, *market maker*, trader fundamental) (hlm. PDF 5, 13–14). **Jangan** untuk klaim prediksi harga.

---

### C5. `kakinaka2022` — Kakinaka & Umeno (2022), "Cryptocurrency market efficiency in short- and long-term horizons during COVID-19: An asymmetric multifractal analysis approach", Finance Research Letters 46, 102319, doi 10.1016/j.frl.2021.102319
- **Versi dibaca:** terbit (OA, CC BY); hlm. PDF.
1. **Penulis, tahun:** Shinji Kakinaka, Ken Umeno, 2022.
2. **Data:** harga per jam BTC/USDT dan ETH/USDT, 1 Jan 2019 – 31 Des 2020; dibagi 2019 (sebelum wabah) dan 2020 (sesudah wabah) (hlm. PDF 2; Gambar 1).
3. **Bentuk data & sumber:** harga dari bursa Poloniex, diolah menjadi return log (hlm. PDF 2; Tabel 1, hlm. PDF 3).
4. **Masalah:** studi efisiensi kripto saat COVID-19 belum membedakan horizon investasi pendek dan panjang (hlm. PDF 2).
5. **Metode:** *asymmetric multifractal detrended fluctuation analysis* (A-MFDFA) dengan eksponen Hurst umum untuk tren naik dan turun; skala 20 sampai N/10 (hlm. PDF 3–4). Latar teorinya *Fractal Market Hypothesis*: investor jangka pendek dan panjang punya horizon dan penilaian informasi berbeda (hlm. PDF 2).
6. **Hasil:**
   - Ada titik *crossover* s* ≈ 10 hari di kedua pasar. Di bawahnya disebut jangka pendek, di atasnya jangka panjang (hlm. PDF 4).
   - "The presence of the crossover uncovers that investors' behaviors differ depending on horizons" (hlm. PDF 4).
   - Setelah wabah, multifraktalitas naik di jangka pendek dan turun di jangka panjang (Tabel 2, hlm. PDF 6). Penulis menafsirkan ada *herding* kuat di jangka pendek (hlm. PDF 6).
7. **Metrik:** eksponen Hurst umum, derajat multifraktalitas (MDM), ukuran asimetri; uji deret acak dan *surrogate* (Tabel 3, hlm. PDF 7).
8. **Riset lanjutan:** tidak dicatat.
9. **Kelebihan [PR]:** memisahkan perilaku jangka pendek dan panjang secara eksplisit di pasar kripto.
10. **Kekurangan [PR]:** dua koin, satu bursa, dua tahun; bukan studi peramalan.
11. **Kejanggalan [PR]:**
    - Klaim "perilaku investor berbeda menurut horizon" adalah tafsiran dari pola statistik, bukan data per investor.
    - "Jangka pendek" di sini berarti di bawah sekitar 10 hari dari data per jam. Ini jauh lebih panjang dari horizon menit di skripsi.
- **Boleh dikutip untuk:** perilaku harga kripto berbeda antara horizon pendek dan panjang (hlm. PDF 4, 6). **Jangan** untuk membenarkan horizon 1–60 menit secara langsung, atau untuk klaim tentang scalper dan swing trader.

---

### C6. `liu2023` — Liu, Jahanshahloo, Chen & Eshraghi (2023), "Trading patterns in the bitcoin market", The European Journal of Finance, doi 10.1080/1351847X.2023.2241883
- **Versi dibaca:** terbit daring 2 Agu 2023 (OA, CC BY-NC-ND); volume dan halaman cetak belum tercantum di PDF. Nomor halaman = halaman artikel (hlm. PDF − 1).
1. **Penulis, tahun:** Anqi Liu, Hossein Jahanshahloo, Jing Chen, Arman Eshraghi, 2023.
2. **Data:** transaksi *blockchain* Bitcoin tingkat alamat, 1 Jan 2018 – 31 Jan 2021; sekitar 6,1 juta alamat (hlm. 4–5, 8).
3. **Bentuk data & sumber:** Cardiff University Bitcoin Database (CUBiD), diolah menjadi 12 fitur per alamat: frekuensi transaksi, interval antartransaksi, dan rasio waktu aktif (Tabel 1, hlm. 8). Nilai transaksi tidak dipakai (hlm. 7).
4. **Masalah:** masih sedikit yang diketahui tentang siapa yang trading dan bertransaksi Bitcoin (abstrak, hlm. 1).
5. **Metode:** K-means (sklearn), dijalankan 10 kali; 5.215.499 dari 6.108.128 alamat konsisten masuk kelas yang sama (hlm. 8).
6. **Hasil:**
   - Kurang dari 1% pengguna menyumbang lebih dari 95% volume pasar (abstrak).
   - Lima kelas (Tabel 2, hlm. 8; hlm. 8–10):
     - #1 *Bitcoin tasters*, tidak aktif;
     - #2 *liquidity takers* ≈ trader fundamental, memegang posisi rata-rata **22 hari** (Tabel 3(b), hlm. 9; teks hlm. 10);
     - #3 *liquidity takers* ≈ trader teknikal, memegang posisi **tidak lebih dari 5 hari**, kemungkinan memakai sinyal momentum dan *reversal* jangka pendek (hlm. 10);
     - #4 *liquidity providers* ≈ *market maker*;
     - #5 ≈ *high-frequency traders*, transaksi setiap hari, kemungkinan strategi intraday profesional (hlm. 10).
   - Frekuensi trading di Bitcoin tidak bisa setinggi pasar saham karena waktu *mining* (hlm. 10).
7. **Metrik:** centroid K-means dan konsistensi antar-*run*.
8. **Riset lanjutan:** *disebut paper:* mengenali tipe trader (jangka pendek, jangka panjang, aktif, pasif, frekuensi tinggi) penting bagi regulator (hlm. 14–15).
9. **Kelebihan [PR]:** data populasi alamat yang sangat besar; tipe trader dibedakan dari lama pegang posisi dan frekuensi transaksi.
10. **Kekurangan [PR]:** data transaksi *on-chain*, bukan order di bursa seperti Indodax; label tipe trader adalah tafsiran dari centroid.
11. **Kejanggalan [PR]:** tidak ditemukan. Penulis sendiri menyebut istilah "trader" dipakai longgar dan alamat tidak selalu berarti investasi langsung (catatan 3–4, hlm. 15).
- **Boleh dikutip untuk:** pengguna Bitcoin dapat dikelompokkan menjadi tipe trader yang berbeda menurut lama pegang posisi dan frekuensi transaksi; trader teknikal memegang posisi ≤ 5 hari dan trader fundamental sekitar 22 hari (hlm. 10). **Jangan** untuk klaim tentang trader di bursa terpusat, atau sebagai definisi scalper dan swing trader (istilah itu tidak dipakai paper).

---

## D. Pasar Bitcoin dan efisiensi

### D1. `nakamoto2008` — Nakamoto (2008), white paper
- **Relevansi v3 [PR]:** latar belakang Bitcoin di Bab I. *(Kartu lama, isi tidak diubah.)*
- **Status:** PDF tidak tersedia di chat ini; kartu tidak diisi dari ingatan.
- Rujukan: https://bitcoin.org/bitcoin.pdf (diakses 5 Okt 2026).
- **Boleh dikutip untuk:** definisi Bitcoin sebagai sistem uang elektronik *peer-to-peer* (rujukan umum). PDF belum dibaca, jadi jangan kutip isi spesifik.

---

### D2. `do2026` — Do (2026), "Maturation of Bitcoin market microstructure: Evidence of institutional-grade liquidity and efficiency (2012–2025)", Borsa Istanbul Review 26, 100869, doi 10.1016/j.bir.2026.100869
- **Relevansi v3 [PR]:** pasar Bitcoin berubah antar-era. Dipakai untuk menjelaskan mengapa hasil antar-rasio split tidak stabil dan mengapa data terbaru dipakai. *(Kartu lama; dibaca ulang 3 Nov 2026.)* DOI dicek dari PDF 3 Nov 2026. **Untuk v3 [PR]:** sumber data 1 menit BTC/USDT dari arsip Binance (hlm. 3) dan Hurst era *institutional* 0,4821 "Near-Random Walk" (Tabel, hlm. 8) mendukung argumen bahwa naive sulit dikalahkan pada BTC terbaru.
- **Versi yang dibaca:** terbit; dibaca utuh (hlm. = halaman artikel 1–13).

1. **Penulis dan tahun:** Kim-Oanh Do, 2026.
2. **Dataset dan rentang waktu:** data 1 menit Bitcoin 2012–2025, dibagi menjadi tiga era: *niche* 2012–2016, *transition* 2017–2020, *institutional* 2021–2025 (abstrak).
3. **Bentuk dataset dan sumber:**
   - Dikombinasikan dari dua sumber (hlm. 3):
     - OHLCV 1 menit BTC/USD Bitstamp, Jan 2012 – Okt 2019;
     - OHLCV 1 menit BTC/USDT Binance, Nov 2019 – Des 2025, dari arsip historis Binance.
   - Diformulasikan menjadi RV harian, *realized* Amihud, spread Abdi–Ranaldo, volume, dan VR bergulir 180 hari (hlm. 3; Gambar 5, hlm. 9).
   - Hari kosong atau tak hingga diinterpolasi linear (catatan Tabel 2, hlm. 5).
4. **Permasalahan utama:** apakah Bitcoin sudah menjadi pasar berkualitas institusional pada 2025, dan bagaimana ketahanan likuiditas terhadap guncangan berubah antarera (hlm. 1).
5. **Metode / model:** statistik deskriptif per era; AR(1) pada seri log; uji VR Lo–MacKinlay (k = 5); eksponen Hurst; VAR-X dengan *impulse response* (dua urutan Cholesky); FEVD; uji Chow (hlm. 3–10).
6. **Hasil:**
   - RV turun tajam, volume naik, biaya transaksi turun (abstrak).
   - Efisiensi bergerak menuju bentuk lemah; era *institutional* mendekati *random walk* (Hurst 0,4821; hlm. 8).
   - Respons *illiquidity* terhadap guncangan volatilitas melemah besaran dan persistensinya di era *institutional* (Gambar 4, hlm. 8; hlm. 10).
7. **Metrik:** koefisien ρ dan R² AR(1) (Tabel 2, hlm. 5); statistik VR; Hurst; OIRF; FEVD; uji Chow. Tidak ada peramalan out-of-sample.
8. **Potensi penelitian selanjutnya:**
   - *Disebut paper:* meneliti bagaimana tonggak regulasi, struktur bursa, dan intermediasi institusional membentuk mikrostruktur aset digital (hlm. 10).
   - *[Penilaian reviewer]:* menguji apakah perubahan antarera juga mengubah keterdugaan volatilitas dan kinerja model peramalan.
9. **Kelebihan utama [Penilaian reviewer]:**
   - Periode sangat panjang (2012–2025) dengan data 1 menit.
   - Memadukan likuiditas, efisiensi, dan volatilitas dalam satu kerangka.
   - Uji ketahanan urutan Cholesky.
10. **Kekurangan utama [Penilaian reviewer]:**
    - Batas era ditetapkan di awal, bukan diuji.
    - Pergantian sumber data (Bitstamp → Binance) jatuh di tengah era *transition*.
    - Tidak ada peramalan.
11. **Tidak konsisten, tidak lazim, tidak logis [Penilaian reviewer]:**
    - **Penyambungan dua bursa dan dua mata uang kutipan** (USD → USDT) pada Nov 2019. Penulis sendiri mengakui perbedaan bursa dan mata uang kutipan dapat memengaruhi level variabel (hlm. 3). Penurunan rata-rata Amihud dari 53.881 (*transition*) ke 25 (*institutional*) (Tabel 2) bisa ikut dipengaruhi pergantian ini.
    - **Interpolasi linear** untuk hari yang hilang pada RV dan Amihud (hlm. 5) tidak lazim untuk data volatilitas.
    - **Tabel 2 tidak menyebut seri mana** yang dihitung persistensinya (ρ 0,697 / 0,833 / 0,723). Catatannya hanya berbunyi "each daily series is log-transformed".

- **Kalimat kunci:**
  - Kematangan Bitcoin dikaitkan dengan likuiditas lebih dalam, efisiensi lebih baik, dan ketahanan lebih besar terhadap guncangan volatilitas (abstrak).
  - Di sampel penuh, respons *illiquidity* modest dan sementara, kembali ke garis dasar dalam beberapa hari (hlm. 6).
- **Jawaban pertanyaan khusus:**
  - **Pembagian era:**
    - *Niche*: *early adopters* dan *retail* spekulatif.
    - *Transition*: partisipasi *retail* arus utama, CME *futures*, ekspansi bursa seperti Binance.
    - *Institutional*: integrasi dengan keuangan tradisional, *corporate treasury*, ETF spot Jan 2024.
    - Sumber: abstrak; hlm. 1.
  - **Persistensi per era:** ρ 0,697 / 0,833 / 0,723 (Tabel 2, hlm. 5); seri yang diukur tidak disebut eksplisit.
  - **Respons likuiditas di era *institutional*:** lebih kecil dan kurang persisten (abstrak; hlm. 6; Gambar 4, hlm. 8; hlm. 10).
- **Boleh dikutip untuk:** pasar Bitcoin berubah antar-era (niche, transition, institutional): RV turun, likuiditas naik, respons *illiquidity* terhadap guncangan volatilitas melemah. Sebut keterbatasan: penyambungan dua bursa dan mata uang kutipan.

---

### D3. `mokni2024` — Mokni, El Montasser, Ajmi & Bouri (2024), "On the efficiency and its drivers in the cryptocurrency market: the case of Bitcoin and Ethereum", Financial Innovation 10:39, doi 10.1186/s40854-023-00566-3
- **Relevansi v3 [PR]:** efisiensi Bitcoin berubah-waktu. Pendukung penjelasan hasil yang berbeda antarperiode uji. *(Kartu lama; dibaca ulang 3 Nov 2026.)* DOI dicek dari PDF 3 Nov 2026.
- **Versi yang dibaca:** terbit; dibaca utuh (hlm. = "Page x of 25").

1. **Penulis dan tahun:** Khaled Mokni, Ghassen El Montasser, Ahdi Noomen Ajmi, Elie Bouri, 2024.
2. **Dataset dan rentang waktu:**
   - Bitcoin dan Ethereum, data harian 7 Agu 2016 – 15 Feb 2023 (abstrak, hlm. 1).
   - Seri AMIM berwindow 1 tahun mencakup 8 Agu 2017 – 15 Feb 2023 (catatan Tabel 2, hlm. 10).
3. **Bentuk dataset dan sumber:**
   - Diformulasikan dan dikombinasikan: log return diolah menjadi AMIM (ukuran inefisiensi berwindow bergulir 1 tahun).
   - AMIM digabung dengan variabel makro dan pasar: FSI, MSCI, FFR, GSCI, emas, EPU, VIX.
   - Variabel internal: volatilitas = kuadrat return; likuiditas = nilai transaksi ÷ kapitalisasi; aliran dana (hlm. 10).
   - *Dummy* COVID mulai 11 Mar 2020 (hlm. 10).
   - Sumber per variabel tercantum di Tabel 4 dan teks sekitar hlm. 10.
4. **Permasalahan utama:** studi efisiensi kripto sebelumnya membahas perubahan efisiensi dari waktu ke waktu tetapi tidak menjelaskan faktor penggeraknya (abstrak, hlm. 1).
5. **Metode / model:** AMIM untuk efisiensi berubah-waktu; regresi OLS dan kuantil (q 0,1–0,9) untuk faktor penggerak.
6. **Hasil:**
   - Efisiensi berubah-waktu, berganti antara periode efisien dan tidak efisien; Bitcoin umumnya lebih lama efisien daripada Ethereum (Gambar 2, hlm. 11; hlm. 20).
   - Stres keuangan menurunkan AMIM (Tabel 5, hlm. 14).
   - Likuiditas menaikkan AMIM secara signifikan di hampir semua kuantil (Tabel 5, hlm. 14).
   - COVID menaikkan inefisiensi (abstrak).
   - Sebelum/sesudah COVID, estimasi berubah besar (Tabel 8, hlm. 19).
7. **Metrik:** koefisien regresi dan signifikansinya; uji ketahanan dengan window AMIM 3 bulan s.d. 2 tahun (Gambar 4, hlm. 21) dan sampel sebelum/sesudah COVID (Tabel 8–9).
8. **Potensi penelitian selanjutnya:**
   - *Disebut paper:* asumsi normalitas AMIM tidak sesuai dengan return kripto yang berekor tebal; pendekatan perlu diperluas untuk distribusi *fat-tailed* (hlm. 21).
   - *[Penilaian reviewer]:* memakai data intraday dan memisahkan efek peristiwa 2022 (Terra, FTX) dari efek COVID.
9. **Kelebihan utama [Penilaian reviewer]:**
   - Menghubungkan efisiensi berubah-waktu dengan faktor penggeraknya.
   - Regresi kuantil memungkinkan efek berbeda saat pasar efisien dan tidak efisien.
   - Ada beberapa uji ketahanan.
10. **Kekurangan utama [Penilaian reviewer]:**
    - Asumsi normalitas AMIM (diakui penulis, hlm. 21).
    - Data harian saja.
    - Tidak ada variabel mikrostruktur langsung seperti spread.
11. **Tidak konsisten, tidak lazim, tidak logis [Penilaian reviewer]:**
    - **Tidak lazim:** likuiditas yang lebih tinggi justru menaikkan inefisiensi (Tabel 5), berlawanan dengan intuisi umum dan dengan pernyataan paper sendiri bahwa likuiditas tinggi memudahkan jual-beli tanpa banyak memengaruhi harga (hlm. 4).
    - *Dummy* COVID bernilai 1 sejak 11 Mar 2020 sampai akhir sampel (Feb 2023), sehingga ikut mencakup *crash* 2022. Efeknya tidak murni COVID.
    - Koefisien LIQ Bitcoin sebelum COVID berganti tanda antarkuantil (+0,476 di q0,1; −0,849 di q0,9; Tabel 8), tetapi ringkasan uji ketahanan hanya menyebut likuiditas berpengaruh positif dan signifikan (hlm. 18).

- **Kalimat kunci:**
  - Dua pasar kripto menunjukkan efisiensi berubah-waktu, yaitu pergantian periode efisien dan tidak efisien (hlm. 20).
  - Estimasi parameter berubah besar setelah pandemi dibanding sebelumnya (hlm. 18).
- **Jawaban pertanyaan khusus:**
  - **Efisiensi berubah:** hlm. 20; Gambar 2 (hlm. 11).
  - **Likuiditas sebelum/sesudah COVID (Bitcoin, Tabel 8, hlm. 19):**
    - Sebelum COVID: koefisien LIQ +0,476 (q0,1), +0,271 (q0,5), **−0,849** (q0,9).
    - Sesudah COVID: koefisien LIQ +3,197, +3,272, +2,822.
    - Arahnya berbalik pada kuantil 0,9 sebelum COVID, dan besarannya naik tajam sesudah COVID.
- **Boleh dikutip untuk:** efisiensi Bitcoin berubah-waktu; likuiditas, stres keuangan, dan COVID memengaruhi efisiensi. Hati-hati: arah efek likuiditas tidak lazim (menaikkan inefisiensi) dan *dummy* COVID ikut mencakup 2022.

---

### D4. `yi2023` — Yi, Yang, Jeong, Sohn & Ahn (2023), "Market efficiency of cryptocurrency: evidence from the Bitcoin market", Scientific Reports 13:4789, doi 10.1038/s41598-023-31618-4
- **Relevansi v3 [PR]:** efisiensi bentuk lemah Bitcoin. Dasar argumen mengapa mengalahkan naive (ŷ = harga terakhir) sulit. *(Kartu lama; dibaca ulang 3 Nov 2026.)* DOI dicek dari PDF 3 Nov 2026.
- **Versi yang dibaca:** terbit; dibaca utuh.

1. **Penulis dan tahun:** Eojin Yi, Biao Yang, Minhyuk Jeong, Sungbin Sohn, Kwangwon Ahn, 2023.
2. **Dataset dan rentang waktu:**
   - Harga harian Bitcoin 1 Sep 2010 – 31 Mar 2019, dengan pembanding emas, USD/EUR, dan S&P 500 (hlm. 2, 7).
   - Dibagi menjadi *low price regime* (1 Sep 2010 – 26 Feb 2013) dan *high price regime* (27 Feb 2013 – 31 Mar 2019) (hlm. 4).
3. **Bentuk dataset dan sumber:**
   - Data mentah harga penutupan harian dari Quandl.com, diolah menjadi log return.
   - Pencilan lebih dari 2,58 × simpangan baku dibuang untuk estimasi (hlm. 5).
   - Kapitalisasi pasar diambil dari Quandl dan CRSP (hlm. 7).
4. **Permasalahan utama:** apakah pasar Bitcoin memenuhi hipotesis pasar efisien bentuk lemah, dan apakah QHO dapat mengatasi keterbatasan uji VR (hlm. 1–2).
5. **Metode / model:** uji *variance ratio* (VR) dan model *quantum harmonic oscillator* (QHO); efisiensi diukur dari probabilitas *ground state* P0, yaitu distribusi Gaussian (hlm. 2–4).
6. **Hasil:**
   - Uji VR memberi bukti campuran: *random walk* ditolak sebagian (Tabel 2, hlm. 4).
   - P0 tinggi, menandakan pasar mendekati efisien (abstrak, hlm. 1).
   - P0 tahunan berfluktuasi di atas 90%, tanpa perubahan signifikan antartahun (Gambar 2, hlm. 6).
7. **Metrik:** statistik VR(q) untuk q = 2, 4, 8, 16 (Tabel 2); uji LR QHO vs *random walk* (Tabel 5, hlm. 6); P0. Tidak ada peramalan.
8. **Potensi penelitian selanjutnya:**
   - *Disebut paper:* regulator sebaiknya memantau efisiensi pasar sebagai indeks distorsi harga (abstrak; hlm. 8). Arah riset lanjutan yang eksplisit tidak disebut.
   - *[Penilaian reviewer]:* memperpanjang data setelah 2019 dan memakai data intraday atau per bursa.
9. **Kelebihan utama [Penilaian reviewer]:**
   - Mengukur efisiensi dari bentuk distribusi return, bukan hanya satu statistik uji.
   - Hasil diperiksa per tahun dan dibandingkan dengan aset tradisional.
10. **Kekurangan utama [Penilaian reviewer]:**
    - Data berakhir Mar 2019, sudah lama untuk paper terbitan 2023.
    - Data harga dari agregator (Quandl), tidak per bursa.
    - Hanya keterdugaan return; volatilitas tidak dibahas.
11. **Tidak konsisten, tidak lazim, tidak logis [Penilaian reviewer]:**
    - **Tidak lazim:** efisiensi disamakan dengan besarnya bobot distribusi Gaussian (P0). Distribusi yang tidak normal tidak otomatis berarti return dapat diprediksi, dan sebaliknya.
    - Uji VR dijalankan pada deret **log harga** (Tabel 2, hlm. 4), sedangkan kesimpulan efisiensi dibuat tentang return. *(Koreksi 3 Nov 2026: ini prosedur standar Lo–MacKinlay, yang menguji apakah log harga mengikuti random walk lewat kenaikannya; bukan kejanggalan.)*
    - Pembagian rezim memakai level harga (titik potong Feb 2013), bukan uji perubahan struktural.
    - Temuan "efisiensi stabil antartahun" (Gambar 2) **berbeda** dengan Mokni dkk. (2024) yang menemukan efisiensi berubah-waktu. Keduanya memakai ukuran dan periode berbeda.

- **Kalimat kunci:**
  - Menurut EMH bentuk lemah, harga tidak dapat diprediksi dari histori harga dan return (hlm. 1).
  - Analisis teknikal atas histori harga tidak memberi keunggulan jangka panjang di pasar Bitcoin (hlm. 6).
- **Jawaban pertanyaan khusus:** yang diuji adalah efisiensi bentuk lemah, yaitu keterdugaan **harga/return** dari histori; data harian Bitcoin Quandl, 1 Sep 2010 – 31 Mar 2019 (hlm. 1–2).
- **Boleh dikutip untuk:** efisiensi bentuk lemah Bitcoin (harga/return) dan bukti campuran uji VR. **Jangan** untuk klaim efisiensi berubah-waktu (temuannya justru stabil antartahun) atau klaim tentang volatilitas.

---

## E. Model boosting (sumber metode)

### E1. `friedman2001` — Friedman (2001), "Greedy function approximation: A gradient boosting machine", Annals of Statistics 29(5), 1189–1232 *(paper metode)*
- **Versi dibaca:** terbit (44 hlm. PDF); nomor halaman = halaman jurnal.
1. **Penulis, tahun:** Jerome H. Friedman, 2001.
2. **Data:** simulasi dan contoh terapan (bagian 6–7).
3. **Bentuk data & sumber:** tidak relevan.
4. **Masalah:** estimasi fungsi dilihat sebagai optimasi numerik di ruang fungsi, bukan ruang parameter (abstrak).
5. **Metode:**
   - Algorithm 1 *Gradient Boost* generik (hlm. 1193).
   - Varian loss: LS_Boost (Alg. 2), **LAD_TreeBoost untuk loss absolut (Alg. 3, hlm. 1196)**, M_TreeBoost untuk Huber (Alg. 4), LK_TreeBoost untuk klasifikasi (Alg. 5–6).
   - *Base learner* pohon regresi dengan J daun dan pembaruan terpisah per daun (hlm. 1195–1196).
   - *Shrinkage*: F_m = F_{m−1} + ν·ρ_m·h, 0 < ν ≤ 1, disebut "learning rate" (pers. 36, hlm. 1203).
6. **Hasil:** *shrinkage* memberi hasil lebih baik daripada membatasi jumlah komponen; *learning rate* ν dan jumlah komponen M menjadi dua parameter regularisasi (hlm. 1203).
7. **Metrik:** galat prediksi pada simulasi.
8. **Riset lanjutan:** tidak dicatat.
9. **Kelebihan [PR]:** dasar teori gradient boosting yang dipakai XGBoost, LightGBM, dan CatBoost.
10. **Kekurangan [PR]:** tidak membahas deret waktu.
11. **Kejanggalan [PR]:** tidak ditemukan.
- **Boleh dikutip untuk:** definisi gradient boosting; boosting dengan loss absolut (LAD, Alg. 3) sebagai dasar objektif L1; *learning rate* dan jumlah pohon sebagai parameter regularisasi (hlm. 1203).

---

### E2. `freund1997` — Freund & Schapire (1997), "A Decision-Theoretic Generalization of On-Line Learning and an Application to Boosting", Journal of Computer and System Sciences 55, 119–139 *(paper metode)*
- **Versi dibaca:** terbit (21 hlm.); nomor halaman = halaman jurnal.
1. **Penulis, tahun:** Yoav Freund, Robert E. Schapire, 1997.
2. **Data:** tidak relevan (teori).
3. **Bentuk data & sumber:** tidak relevan.
4. **Masalah:** alokasi sumber daya *on-line* di antara banyak strategi, dan cara mengubah *weak learner* menjadi *learner* yang akurat (abstrak).
5. **Metode:**
   - Bagian 1: algoritme Hedge(β) dengan pembaruan bobot multiplikatif (hlm. 119–125).
   - Bagian 2: algoritme boosting baru, **AdaBoost** (Gambar 2, hlm. 126). Bobot contoh yang salah diprediksi dinaikkan, sehingga *weak learner* berikutnya fokus ke contoh sulit.
   - Perluasan ke multikelas (AdaBoost.M1, AdaBoost.M2) dan regresi (**AdaBoost.R**) (bagian 4–5, hlm. 130–131).
6. **Hasil:** AdaBoost tidak butuh pengetahuan awal tentang kinerja *weak learner* (abstrak); batas galat latih turun eksponensial (Teorema 6).
7. **Metrik:** batas galat teoretis.
8. **Riset lanjutan:** tidak dicatat.
9. **Kelebihan [PR]:** sumber asli AdaBoost.
10. **Kekurangan [PR]:** fokus klasifikasi biner; regresi hanya perluasan.
11. **Kejanggalan [PR]:** tidak ditemukan.
- **Boleh dikutip untuk:** asal-usul AdaBoost dan mekanisme pembobotan ulang contoh. **Jangan** untuk `AdaBoostRegressor` sklearn; itu memakai **AdaBoost.R2 (Drucker, 1997; kartu E9)**.

---

### E3. `prokhorenkova2018` — Prokhorenkova, Gusev, Vorobev, Dorogush & Gulin (2018), "CatBoost: unbiased boosting with categorical features", Advances in Neural Information Processing Systems 31 (NeurIPS 2018) *(paper metode)*
- **Versi dibaca:** prosiding NeurIPS 2018 (11 hlm.); hlm. PDF.
1. **Penulis, tahun:** Liudmila Prokhorenkova, Gleb Gusev, Aleksandr Vorobev, Anna Veronika Dorogush, Andrey Gulin, 2018.
2. **Data:** dataset publik seperti Adult, Amazon, Epsilon, Internet (Tabel 2, hlm. 8).
3. **Bentuk data & sumber:** tidak relevan (bukan deret waktu).
4. **Masalah:** semua implementasi gradient boosting mengalami *prediction shift*, sejenis *target leakage* (abstrak; bagian 4.1, hlm. 4).
5. **Metode:**
   - *Ordered boosting*: dengan permutasi acak, model untuk contoh ke-i hanya dilatih dari contoh sebelumnya (Algorithm 1, hlm. 5–6).
   - *Ordered target statistics* untuk fitur kategorikal, terinspirasi pembelajaran *online* yang memproses data berurutan waktu (hlm. 4).
   - Pohon dasar *oblivious* (simetris) (hlm. 6). Dua mode: Ordered dan Plain (hlm. 6).
6. **Hasil:**
   - CatBoost mengungguli XGBoost dan LightGBM pada logloss dan *zero-one loss* di dataset yang diuji (Tabel 2, hlm. 8).
   - Mode Ordered paling berguna pada dataset kecil; sekitar 1,7 kali lebih lambat dari Plain dan LightGBM (hlm. 8).
7. **Metrik:** logloss, *zero-one loss*; waktu latih.
8. **Riset lanjutan:** tidak dicatat.
9. **Kelebihan [PR]:** mengidentifikasi sumber kebocoran yang tidak disadari sebelumnya.
10. **Kekurangan [PR]:** tidak ada uji pada deret waktu atau data keuangan.
11. **Kejanggalan [PR]:** tidak ditemukan.
- **Boleh dikutip untuk:** definisi CatBoost (*ordered boosting*, *ordered TS*, pohon simetris); mode Ordered bermanfaat pada data kecil (hlm. 8). **Catatan desain [PR]:** permutasi di paper acak; untuk deret waktu, pastikan urutan waktu dihormati di implementasi skripsi.

---

### E4. `ke2017` — Ke dkk. (2017), Advances in Neural Information Processing Systems 30 (NeurIPS 2017)
- **Relevansi v3 [PR]:** definisi LightGBM (model dengan hasil terbaik di eksperimen). *(Kartu lama; dibaca ulang 3 Nov 2026.)*
- **Versi yang dibaca:** terbit (prosiding); dibaca utuh; halaman ditulis hlm. PDF.

1. **Penulis dan tahun:** Guolin Ke, Qi Meng, Thomas Finley, Taifeng Wang, Wei Chen, Weidong Ma, Qiwei Ye, Tie-Yan Liu, 2017.
2. **Dataset dan rentang waktu:** lima dataset publik besar (Tabel 1, hlm. PDF 6–7):
   - Allstate;
   - Flight Delay (10 juta baris, 700 fitur);
   - LETOR (2 juta, 136);
   - KDD10 (19 juta, 29 juta fitur);
   - KDD12 (119 juta, 54 juta fitur).
   Rentang waktu tidak relevan (bukan deret waktu).
3. **Bentuk dataset dan sumber:**
   - Dataset kompetisi dan publik; KDD10 dan KDD12 memakai fitur dari solusi pemenang NTU (hlm. PDF 6).
   - Allstate dan Flight Delay banyak berisi fitur *one-hot* (hlm. PDF 6).
4. **Permasalahan utama:** implementasi GBDT yang ada lambat pada data besar berdimensi tinggi, karena setiap fitur memindai semua data untuk mencari titik *split* (abstrak).
5. **Metode / model:**
   - LightGBM = GBDT berbasis histogram ditambah dua teknik baru (abstrak; bagian 3–4):
     - **GOSS** (mempertahankan data dengan gradien besar dan mengambil sampel acak dari sisanya);
     - **EFB** (menggabungkan fitur yang saling eksklusif).
   - Pembanding: XGBoost (pre-sorted dan histogram) dan lgb_baseline.
   - *Leaf-wise growth* dipakai untuk xgb_his, lgb_baseline, dan LightGBM (hlm. PDF 6).
6. **Hasil:**
   - Pelatihan hingga lebih dari 20 kali lebih cepat dengan akurasi hampir sama (abstrak; Tabel 2–3, hlm. PDF 7).
   - GOSS lebih akurat daripada SGB pada rasio sampel yang sama (Tabel 4, hlm. PDF 7; pembahasan hlm. PDF 8).
7. **Metrik:** waktu per iterasi; AUC (klasifikasi); NDCG@10 (ranking); penggunaan memori.
8. **Potensi penelitian selanjutnya:** *disebut paper:* pemilihan optimal parameter a dan b GOSS, dan perbaikan EFB untuk fitur yang banyak, baik jarang maupun padat (hlm. PDF 8).
9. **Kelebihan utama [Penilaian reviewer]:** dasar teori (batas galat GOSS, NP-hard EFB) disertai eksperimen skala besar; implementasi terbuka dan menjadi standar industri.
10. **Kekurangan utama [Penilaian reviewer]:**
    - Fokus pada kecepatan; akurasi hanya "hampir sama".
    - Tidak ada uji signifikansi perbedaan akurasi.
    - Tidak ada data kecil maupun deret waktu.
    - Tidak membandingkan *leaf-wise* vs *level-wise* secara sistematis.
11. **Tidak konsisten, tidak lazim, tidak logis [Penilaian reviewer]:**
    - Abstrak menyebut LightGBM "almost the same accuracy", sedangkan penutup menyebut LightGBM "significantly outperform XGBoost and SGB". Penutup merujuk ke **kecepatan dan memori**, bukan akurasi (hlm. PDF 8), jadi pembaca perlu berhati-hati agar tidak membacanya sebagai klaim akurasi.
    - Paper **tidak memuat** klaim "*leaf-wise* rentan *overfitting* pada data kecil" dan **tidak punya** gambar *leaf-wise* vs *level-wise*; keduanya berasal dari dokumentasi LightGBM.

- **Kalimat kunci:** GBDT dengan GOSS dan EFB disebut LightGBM (abstrak).
- **Jawaban pertanyaan khusus:** definisi singkat: "We call our new GBDT implementation with GOSS and EFB LightGBM" (abstrak, hlm. PDF 1). Artinya LightGBM adalah implementasi GBDT berbasis histogram yang dilengkapi GOSS dan EFB.
- **Boleh dikutip untuk:** definisi LightGBM (GBDT + GOSS + EFB, abstrak); lebih cepat dengan akurasi hampir sama. **Jangan** untuk klaim akurasi lebih tinggi dari XGBoost, *leaf-wise* rentan *overfitting* pada data kecil, atau gambar *leaf-wise* (itu dari dokumentasi, kartu I6).

---

### E5. `chen2016` — Chen & Guestrin (2016), "XGBoost: A Scalable Tree Boosting System", KDD 2016, 785–794, doi 10.1145/2939672.2939785
- **Relevansi v3 [PR]:** definisi XGBoost dan regularisasinya. *(Kartu lama; dibaca ulang 3 Nov 2026.)* DOI tidak tercetak di PDF arXiv; DOI dari halaman arXiv dan `.bib` lama.
- **Versi dibaca:** arXiv 1603.02754v3 (isi sama dengan versi KDD); hlm. PDF; bagian 1–2 dibaca.
1. **Penulis, tahun:** Tianqi Chen, Carlos Guestrin, 2016.
2. **Data:** dataset besar publik (Allstate, Higgs, Yahoo LTRC, Criteo) (bagian eksperimen).
3. **Bentuk data & sumber:** tidak relevan untuk riset ini.
4. **Masalah:** sistem *tree boosting* yang skalabel untuk data sangat besar (abstrak).
5. **Metode:** objektif teregularisasi Ω(f) = γT + ½λ‖w‖² (penalti jumlah daun dan L2 bobot daun) (hlm. PDF 2); *shrinkage* dan *column subsampling* (hlm. PDF 3); algoritme *sparsity-aware*, *weighted quantile sketch*, *cache-aware*, *out-of-core* (hlm. PDF 1–2).
6. **Hasil:** 17 dari 29 solusi pemenang Kaggle 2015 memakai XGBoost (hlm. PDF 1); skalabel hingga miliaran contoh.
7. **Metrik:** waktu dan akurasi (AUC dll.).
8. **Riset lanjutan:** tidak dicatat.
9. **Kelebihan [PR]:** sistem standar industri.
10. **Kekurangan [PR]:** fokus skalabilitas; tidak membahas data kecil atau deret waktu.
11. **Kejanggalan [PR]:** tidak ditemukan.
- **Boleh dikutip untuk:** regularisasi L2 bobot daun (`reg_lambda`) dan identitas XGBoost. **Jangan** untuk perbandingan dengan LightGBM (terbit lebih dulu).

---

### E6. `lightgbmfeatures`, `lightgbmtuning` — Dokumentasi LightGBM (Microsoft Corporation), halaman *Features* dan *Parameters Tuning*
- **Relevansi v3 [PR]:** dasar `num_leaves` dan `min_data_in_leaf` di ruang *tuning* LightGBM. Kutip URL versi yang sesuai `lightgbm` di `requirements.txt`. *(Kartu lama; dibaca ulang 3 Nov 2026.)*
- **Versi dibaca:** cetak PDF dua halaman web (masing-masing 7 hlm.), versi "latest" 4.7.0.99, diakses 3 Nov 2026 (sebelumnya tangkapan layar 12 Okt 2026). **4.7.0.99 merupakan build pengembangan, bukan rilis.** Kutip URL versi yang sama dengan `lightgbm` di `.venv` (cek `pip show lightgbm`) dan pastikan isinya sama.
- ***Features:*** LightGBM memilih daun dengan *max delta loss* untuk dipecah; pada jumlah daun yang sama, pertumbuhan *leaf-wise* umumnya mencapai loss lebih rendah daripada *level-wise*, **tetapi dapat *overfitting* pada data kecil**; karena itu ada parameter `max_depth`; ada gambar *leaf-wise* vs *level-wise* (hlm. PDF 1–2).
- ***Parameters Tuning:*** *leaf-wise* konvergen lebih cepat; `num_leaves` dan `min_data_in_leaf` adalah parameter utama untuk mencegah *overfitting*; bila `max_depth` diatur, `num_leaves` ≤ 2^`max_depth` (contoh: `max_depth`=7 dengan `num_leaves`=127 dapat *overfitting*) (hlm. PDF 1). Halaman ini juga menautkan Optuna untuk *tuning* otomatis.
- **Boleh dikutip untuk:** klaim *leaf-wise* dan risiko *overfitting* pada data kecil, gambar pohon, serta parameter pencegah *overfitting*. **Klaim ini tidak ada di Ke dkk. (2017).**

---

### E7. `grinsztajn2022` — Grinsztajn, Oyallon & Varoquaux (2022), NeurIPS 35 (Datasets and Benchmarks)
- **Relevansi v3 [PR]:** alasan memilih model pohon untuk data tabular. Ingat, deret waktu dikeluarkan dari benchmark ini. *(Kartu lama; dibaca ulang 3 Nov 2026.)* Dicek ulang: kata "LightGBM" tidak muncul sama sekali di paper.
- **Versi dibaca:** arXiv 2207.08815v1; hlm. PDF; bagian 1–3 dibaca.
1. **Penulis, tahun:** Léo Grinsztajn, Edouard Oyallon, Gaël Varoquaux, 2022.
2. **Data:** 45 dataset tabular dari berbagai domain (hlm. PDF 1, 3).
3. **Bentuk data & sumber:** dataset publik (OpenML) yang disaring dengan kriteria: hanya data i.i.d. (**deret waktu dibuang**); data latih dipotong ke 10.000 sampel; **dataset dibuang bila skor Logistic/Linear Regression default selisih relatifnya kurang dari 5% terhadap Resnet default dan HistGradientBoosting default** ("Not too easy", hlm. PDF 3).
4. **Masalah:** mengapa model pohon masih mengungguli *deep learning* pada data tabular (abstrak).
5. **Metode:** benchmark XGBoost, RF, GBT vs MLP, ResNet, Transformer dengan anggaran *tuning* yang sama.
6. **Hasil:** model pohon tetap terbaik pada data **berukuran menengah (±10 ribu sampel)**; NN lemah karena fitur tidak informatif, fungsi target tidak mulus, dan invariansi rotasi (abstrak; hlm. PDF 2).
7. **Metrik:** skor uji relatif dalam berbagai anggaran *tuning*.
8. **Riset lanjutan:** *disebut paper:* arah arsitektur NN khusus tabular (abstrak).
9. **Kelebihan [PR]:** benchmark yang terkontrol.
10. **Kekurangan [PR]:** **LightGBM tidak diuji**; deret waktu dikeluarkan; dataset yang mudah diselesaikan model linear dibuang.
11. **Kejanggalan [PR]:** tidak ditemukan.
- **Boleh dikutip untuk:** model pohon > *deep learning* pada data tabular menengah. **Jangan** untuk klaim pohon > model linear, atau "data kecil hingga menengah", atau keunggulan pada deret waktu.

---

### E8. `makridakis2022` *(usulan key)* — Makridakis, Spiliotis & Assimakopoulos (2022), "M5 accuracy competition: Results, findings, and conclusions", International Journal of Forecasting 38(4), 1346–1364, doi 10.1016/j.ijforecast.2021.11.013
- **Relevansi v3 [PR]:** popularitas LightGBM dalam kompetisi peramalan; juga bukti bahwa *benchmark* statistik sederhana sulit dikalahkan (hanya 7,5% tim mengalahkan ES_bu). *(Kartu lama; dibaca ulang 3 Nov 2026.)* DOI dicek dari PDF 3 Nov 2026. **Catatan:** poin 10–11 dan "Boleh dikutip" ditulis untuk v2 (target volatilitas); untuk v3 pegang baris "Untuk v3".
- **Status:** terbit; **belum di `.bib`**.
- **Versi dibaca:** terbit; bagian 1–4 dibaca.
1. **Penulis, tahun:** Spyros Makridakis, Evangelos Spiliotis, Vassilios Assimakopoulos, 2022.
2. **Data:** 42.840 deret penjualan Walmart yang hierarkis; horizon 28 hari (abstrak; hlm. 1346–1348).
3. **Bentuk data & sumber:** data penjualan ritel nyata, dikombinasikan dengan kalender, harga, promosi.
4. **Masalah:** mengevaluasi metode peramalan pada data penjualan nyata yang intermiten (abstrak).
5. **Metode:** kompetisi Kaggle; metrik WRMSSE; 24 *benchmark* statistik dan ML (hlm. 1348–1350).
6. **Hasil:**
   - 5.507 tim dari 101 negara (hlm. 1349); hanya 415 tim (7,5%) yang mengalahkan *benchmark* terbaik ES_bu (hlm. 1350).
   - **LightGBM dipakai oleh seluruh 50 tim teratas** (hlm. 1346).
   - **M5 adalah kompetisi pertama di mana semua metode teratas murni ML dan lebih baik dari semua *benchmark* statistik** (*Finding 1*, hlm. 1356). Finding 1 dibuka dengan pernyataan bahwa studi empiris selama bertahun-tahun menunjukkan metode sederhana seakurat metode kompleks (hlm. 1356).
   - Keunggulan didukung *cross-learning* dari banyak deret berkorelasi dan variabel eksogen (*Finding 3*).
7. **Metrik:** WRMSSE.
8. **Riset lanjutan:** *disebut paper* di bagian penutup (tidak dicatat rinci).
9. **Kelebihan [PR]:** skala besar dan data nyata.
10. **Kekurangan [PR]:** domain ritel; keunggulan bergantung pada banyak deret dan fitur eksogen.
11. **Kejanggalan [PR]:** pemakaian model pohon oleh tim **diasumsikan** dari kebiasaan komunitas Kaggle, bukan dilaporkan semua tim (hlm. 1349).
- **Boleh dikutip untuk:** popularitas dan keunggulan LightGBM dalam kompetisi peramalan berskala besar. **Jangan** untuk klaim keunggulan pada satu deret RV; sebutkan bahwa kondisinya berbeda (banyak deret + data eksogen).

---

### E9. `drucker1997` — Drucker (1997), "Improving Regressors using Boosting Techniques", Proceedings of the Fourteenth International Conference on Machine Learning (ICML 1997), Morgan Kaufmann *(paper metode)*
- **Versi dibaca:** PDF versi penulis (9 hlm.), tanpa header prosiding. **Nomor halaman prosiding belum diketahui**; lokasi ditulis hlm. PDF.
1. **Penulis, tahun:** Harris Drucker, 1997.
2. **Data:** fungsi nonlinear Friedman #1, #2, #3 (200 latih, 40 *pruning*, 5.000 uji) dan Boston Housing (401 latih, 80 *pruning*, 25 uji) (hlm. PDF 4–5).
3. **Bentuk data & sumber:** data simulasi dan data UCI (hlm. PDF 5).
4. **Masalah:** belum ada studi eksperimen yang menggabungkan regresor dengan boosting (hlm. PDF 1).
5. **Metode:** modifikasi AdaBoost.R (hlm. PDF 2):
   - bobot awal w_i = 1; probabilitas sampel p_i = w_i/Σw; data latih diambil ulang dengan pengembalian sesuai p_i;
   - loss per sampel dinormalisasi dengan D = galat absolut terbesar:
     - linear L_i = |ŷ_i − y_i|/D;
     - *square law* L_i = |ŷ_i − y_i|²/D²;
     - *exponential* L_i = 1 − exp(−|ŷ_i − y_i|/D);
   - rata-rata loss L̄ = Σ L_i p_i; β = L̄/(1 − L̄);
   - pembaruan bobot w_i ← w_i·β^(1 − L_i);
   - iterasi berhenti bila L̄ ≥ 0,5;
   - prediksi akhir = **median berbobot** dengan bobot log(1/β_t).
   - Pohon regresi tipe CART dengan *pruning* pada set terpisah 20% (bagian 4, hlm. PDF 3–4).
6. **Hasil:**
   - Loss terbaik berbeda per masalah: linear untuk Friedman #1, *exponential* untuk #2, *square* untuk #3 (Tabel I–IV, hlm. PDF 6).
   - Boosting lebih baik dari *bagging* pada #1 dan #3; #2 tanpa pemenang jelas (hlm. PDF 5; Tabel IV).
   - Boston Housing: galat prediksi *bagging* 12,4 vs boosting 10,7; boosting menang 72% dari 100 *run* (bagian 6.3, hlm. PDF 8).
7. **Metrik:** *modeling error* dan *prediction error* (MSE); uji binomial jumlah kemenangan boosting (hlm. PDF 1, 5).
8. **Riset lanjutan:** tidak dicatat.
9. **Kelebihan [PR]:** sumber asli AdaBoost.R2; algoritme ditulis langkah demi langkah.
10. **Kekurangan [PR]:** hanya data simulasi dan Boston Housing; tidak ada deret waktu; tidak ada bukti konvergensi (diakui penulis, hlm. PDF 3).
11. **Kejanggalan [PR]:** tidak ditemukan. Catatan: paper ini **tidak punya parameter *learning rate***; itu tambahan implementasi sklearn.
- **Boleh dikutip untuk:** definisi AdaBoost.R2 (langkah, tiga fungsi loss, pembaruan bobot, median berbobot) (hlm. PDF 2–3); loss terbaik bergantung masalah, sehingga `loss` layak masuk ruang *tuning* (Tabel I–IV). **Jangan** untuk klaim tentang *learning rate* atau deret waktu.

---

### E10. `sklearnadaboost` — Dokumentasi scikit-learn 1.9.1, `sklearn.ensemble.AdaBoostRegressor`
- **Versi dibaca:** cetak halaman web, diakses 1 Nov 2026 pukul 20:52 (8 hlm.). URL: https://scikit-learn.org/1.9/modules/generated/sklearn.ensemble.AdaBoostRegressor.html
- "This class implements the algorithm known as AdaBoost.R2 [2]." Rujukan [2] = Drucker (1997); [1] = Freund & Schapire, ditulis tahun "1995" (hlm. 1, 3).
- Nilai bawaan: `estimator` = DecisionTreeRegressor(max_depth=3), `n_estimators=50`, `learning_rate=1.0`, `loss='linear'` (hlm. 1).
- `n_estimators` adalah batas maksimum; pelatihan berhenti lebih awal bila *fit* sempurna (hlm. 1).
- `learning_rate` adalah bobot tiap regresor; ada *trade-off* dengan `n_estimators` (hlm. 1).
- `loss` {'linear', 'square', 'exponential'} dipakai saat memperbarui bobot (hlm. 1).
- `random_state` juga mengatur *bootstrap* bobot di tiap iterasi (hlm. 2). Ini sejalan dengan *resampling* berbobot di Drucker.
- Prediksi = median berbobot dari regresor dalam *ensemble* (hlm. 4).
- **Boleh dikutip untuk:** implementasi AdaBoostRegressor yang dipakai skripsi, nilai bawaan, dan arti parameternya. **Catatan [PR]:** skripsi menyetel `max_depth` pohon dasar 1–6, `learning_rate` 0,001–1,0, dan `loss` kategorikal.

---

## F. Optimasi hiperparameter (sumber metode)

### F1. `bergstra2012` — Bergstra & Bengio (2012), "Random Search for Hyper-Parameter Optimization", Journal of Machine Learning Research 13, 281–305 *(paper metode)*
- **Versi dibaca:** terbit (25 hlm.); nomor halaman = halaman jurnal.
1. **Penulis, tahun:** James Bergstra, Yoshua Bengio, 2012.
2. **Data:** pembanding studi besar sebelumnya pada jaringan saraf dan DBN (abstrak).
3. **Bentuk data & sumber:** dataset gambar (MNIST dan variannya).
4. **Masalah:** grid search dan pencarian manual paling umum dipakai, padahal belum tentu efisien (abstrak).
5. **Metode:** perbandingan empiris dan analisis teoretis random search vs grid search (abstrak).
6. **Hasil:**
   - Random search menemukan model sama baik atau lebih baik dengan sebagian kecil waktu komputasi (abstrak).
   - Alasannya, fungsi respons punya **dimensi efektif rendah**; hanya sedikit hiperparameter yang penting, dan itu berbeda antar-dataset (abstrak; hlm. 283; Gambar 1, hlm. 284).
   - Grid search kena kutukan dimensi; jumlah percobaannya hasil kali banyak nilai tiap variabel (hlm. 282).
   - Grid tetap andal pada ruang 1–2 dimensi (hlm. 283).
7. **Metrik:** akurasi uji model terbaik terhadap jumlah percobaan.
8. **Riset lanjutan:** *disebut paper:* optimasi sekuensial/global untuk mengotomatiskan pencarian manual (hlm. 283; bagian 6, hlm. 301).
9. **Kelebihan [PR]:** argumen teoretis dan empiris yang sederhana.
10. **Kekurangan [PR]:** diuji pada jaringan saraf, bukan boosting.
11. **Kejanggalan [PR]:** tidak ditemukan.
- **Boleh dikutip untuk:** random search lebih efisien dari grid search; dimensi efektif rendah (hlm. 283–284); grid search sebagai baseline.

---

### F2. `bergstra2011` — Bergstra, Bardenet, Bengio & Kégl (2011), "Algorithms for Hyper-Parameter Optimization", Advances in Neural Information Processing Systems (NIPS 2011), 2546–2554 *(paper metode)*
- **Versi dibaca:** prosiding NIPS 2011 (9 hlm.); hlm. PDF. Halaman 2546–2554 dari metadata resmi NeurIPS. **Nomor volume (24) belum terkonfirmasi**; cek sebelum masuk `.bib`.
1. **Penulis, tahun:** James Bergstra, Rémi Bardenet, Yoshua Bengio, Balázs Kégl, 2011.
2. **Data:** tugas jaringan saraf dan DBN; dataset *convex* dan MRBI (hlm. PDF 5–6).
3. **Bentuk data & sumber:** dataset gambar publik.
4. **Masalah:** algoritme dapat menemukan konfigurasi hiperparameter lebih baik daripada manusia (abstrak).
5. **Metode:**
   - Kerangka *Sequential Model-Based Optimization* dengan kriteria *Expected Improvement* (Gambar 1, hlm. PDF 2).
   - Pendekatan Gaussian Process (bagian 3, hlm. PDF 3).
   - **Tree-structured Parzen Estimator (TPE)**: memodelkan p(x|y) dengan densitas ℓ(x) untuk loss di bawah y* dan g(x) untuk sisanya; y* = kuantil γ loss teramati; kandidat dipilih yang rasio g(x)/ℓ(x)-nya kecil (bagian 4, hlm. PDF 4).
6. **Hasil:** γ = 0,15 dan 100 kandidat per iterasi (hlm. PDF 6); random search tidak andal untuk DBN; TPE menemukan hasil lebih baik dari sebelumnya pada *convex* dan MRBI (abstrak; hlm. PDF 7–8).
7. **Metrik:** galat uji.
8. **Riset lanjutan:** tidak dicatat.
9. **Kelebihan [PR]:** sumber asli TPE.
10. **Kekurangan [PR]:** diuji pada jaringan saraf, bukan boosting.
11. **Kejanggalan [PR]:** tidak ditemukan.
- **Boleh dikutip untuk:** definisi TPE (ℓ(x), g(x), kuantil γ) (hlm. PDF 4); TPE lebih baik dari random search pada tugas sulit.

---

### F3. `akiba2019` — Akiba, Sano, Yanase, Ohta & Koyama (2019), "Optuna: A Next-generation Hyperparameter Optimization Framework", Proceedings of the 25th ACM SIGKDD International Conference on Knowledge Discovery & Data Mining, 2623–2631, doi 10.1145/3292500.3330701 *(paper metode)*
- **Versi dibaca:** **preprint arXiv 1907.10902v1** (25 Jul 2019); hlm. PDF. Halaman KDD dari BibTeX resmi di README Optuna; kutip versi KDD di daftar pustaka.
1. **Penulis, tahun:** Takuya Akiba, Shotaro Sano, Toshihiko Yanase, Takeru Ohta, Masanori Koyama, 2019.
2. **Data:** kumpulan fungsi uji dan aplikasi nyata (bagian 5).
3. **Bentuk data & sumber:** tidak relevan.
4. **Masalah:** kerangka optimasi hiperparameter yang ada mengharuskan ruang pencarian didefinisikan statis dan kurang mendukung *pruning* (hlm. PDF 1).
5. **Metode:**
   - API *define-by-run*: ruang pencarian dibangun dinamis di fungsi objektif (bagian 2, hlm. PDF 2–4).
   - Sampling independen (mis. TPE) dan relasional (mis. CMA-ES, GP-BO) (hlm. PDF 4).
   - *Pruning* varian Asynchronous Successive Halving (Algorithm 1, hlm. PDF 4–5).
   - Penyimpanan SQLite/RDB untuk studi terdistribusi; *dashboard* (hlm. PDF 5).
6. **Hasil:** perbandingan fitur dengan SMAC, Hyperopt, dll. (tabel, hlm. PDF 3); evaluasi kinerja sampler dan *pruner* (bagian 5).
7. **Metrik:** nilai objektif terbaik terhadap jumlah percobaan dan waktu.
8. **Riset lanjutan:** *disebut paper:* antarmuka untuk metode berbasis Gaussian Process (hlm. PDF 6).
9. **Kelebihan [PR]:** pustaka terbuka dan banyak dipakai.
10. **Kekurangan [PR]:** paper menggambarkan versi awal pustaka.
11. **Kejanggalan [PR]:** tidak ditemukan.
- **Boleh dikutip untuk:** Optuna, *define-by-run*, sampler TPE dan CMA-ES, *pruning* ASHA. **Jangan** untuk NSGAIISampler, QMCSampler, atau MedianPruner; paper ini tidak menyebutnya (sudah dicek). Pakai kartu F7.

---

### F4. `hansen2001` — Hansen & Ostermeier (2001), "Completely Derandomized Self-Adaptation in Evolution Strategies", Evolutionary Computation 9(2), 159–195 *(paper metode)*
- **Versi dibaca:** versi penulis dengan halaman errata di depan (39 hlm.); hlm. PDF.
1. **Penulis, tahun:** Nikolaus Hansen, Andreas Ostermeier, 2001.
2. **Data:** fungsi uji (bagian 6, Tabel 3).
3. **Bentuk data & sumber:** tidak relevan.
4. **Masalah:** adaptasi parameter strategi pada *evolution strategy* (ES) yang lambat dan bergantung sistem koordinat (hlm. PDF 4–5).
5. **Metode:** CMA-ES: adaptasi matriks kovarians distribusi mutasi normal secara *derandomized*; *cumulation* memakai *evolution path*, bukan satu langkah; kontrol *step size* dengan *cumulative path length control* (abstrak; bagian 3).
6. **Hasil:** invarian terhadap rotasi ruang pencarian (hlm. PDF 4–5); parameter bawaan di Tabel 1 (bagian 5.1).
7. **Metrik:** jumlah evaluasi fungsi hingga target tercapai.
8. **Riset lanjutan:** tidak dicatat.
9. **Kelebihan [PR]:** sumber asli CMA-ES; parameter bawaan tidak perlu disetel.
10. **Kekurangan [PR]:** dirancang untuk ruang kontinu.
11. **Kejanggalan [PR]:** errata penulis mengoreksi catatan kaki 9 bagian 3, bobot w_i Tabel 1, dan parameter c_c (hlm. PDF 1). Pakai nilai yang sudah dikoreksi.
- **Boleh dikutip untuk:** definisi CMA-ES. **Catatan desain [PR]:** ruang tuning skripsi memuat parameter integer dan kategorikal; jelaskan penanganannya dari dokumentasi Optuna (kartu F7), bukan dari paper ini.

---

### F5. `deb2002` — Deb, Pratap, Agarwal & Meyarivan (2002), "A Fast and Elitist Multiobjective Genetic Algorithm: NSGA-II", IEEE Transactions on Evolutionary Computation 6(2), 182–197 *(paper metode)*
- **Versi dibaca:** terbit (16 hlm.); nomor halaman = halaman jurnal.
1. **Penulis, tahun:** Kalyanmoy Deb, Amrit Pratap, Sameer Agarwal, T. Meyarivan, 2002.
2. **Data:** masalah uji multiobjektif, termasuk satu masalah lima objektif tujuh kendala (abstrak).
3. **Bentuk data & sumber:** tidak relevan.
4. **Masalah:** NSGA dikritik karena kompleksitas O(MN³), tidak elitis, dan butuh parameter *sharing* (abstrak).
5. **Metode:** *fast nondominated sorting* O(MN²); *crowding distance* dan *crowded-comparison operator* untuk menjaga keragaman; elitisme dengan menggabungkan populasi induk dan anak lalu memilih N terbaik (abstrak; hlm. 185–186).
6. **Hasil:** sebaran solusi dan konvergensi lebih baik daripada PAES dan SPEA pada sebagian besar masalah (abstrak).
7. **Metrik:** konvergensi dan sebaran solusi Pareto.
8. **Riset lanjutan:** tidak dicatat.
9. **Kelebihan [PR]:** GA multiobjektif standar yang banyak dipakai.
10. **Kekurangan [PR]:** dirancang untuk banyak objektif.
11. **Kejanggalan [PR]:** tidak ditemukan.
- **Boleh dikutip untuk:** NSGA-II sebagai algoritme genetika elitis. **Catatan desain [PR]:** skripsi memakai NSGAIISampler dengan satu objektif. Pada satu objektif, *nondominated sorting* sama dengan mengurutkan nilai objektif, sehingga praktis menjadi GA elitis biasa. Tulis ini eksplisit di Bab 3.

---

### F6. `li2018` — Li, Jamieson, DeSalvo, Rostamizadeh & Talwalkar (2018), "Hyperband: A Novel Bandit-Based Approach to Hyperparameter Optimization", Journal of Machine Learning Research 18, 1–52 *(paper metode)*
- **Versi dibaca:** terbit (52 hlm.); nomor halaman = halaman jurnal.
1. **Penulis, tahun:** Lisha Li, Kevin Jamieson, Giulia DeSalvo, Afshin Rostamizadeh, Ameet Talwalkar, 2018.
2. **Data:** berbagai tugas jaringan saraf dan *kernel* (bagian 4).
3. **Bentuk data & sumber:** dataset publik.
4. **Masalah:** Bayesian optimization memilih konfigurasi secara adaptif tetapi tetap mahal; alternatifnya mempercepat evaluasi konfigurasi (abstrak; hlm. 2).
5. **Metode:** Hyperband mempercepat random search lewat alokasi sumber daya adaptif dan *early stopping*; dirumuskan sebagai *pure-exploration infinite-armed bandit* (abstrak). Memperluas SuccessiveHalving: jalankan banyak konfigurasi dengan anggaran kecil, buang yang terburuk, ulangi (hlm. 6). Sumber daya bisa berupa iterasi, ukuran data latih, atau jumlah fitur (hlm. 2).
6. **Hasil:** 5–30 kali lebih cepat dari Bayesian optimization populer (SMAC, TPE, Spearmint) pada sejumlah tugas (hlm. 3).
7. **Metrik:** galat uji terhadap waktu komputasi.
8. **Riset lanjutan:** *disebut paper:* metode hibrida dengan Bayesian optimization (hlm. 13); distribusi pengambilan sampel yang lebih menjanjikan (hlm. 18); paralelisasi skala besar (hlm. 33).
9. **Kelebihan [PR]:** dasar teori dan bukti empiris luas.
10. **Kekurangan [PR]:** tidak diuji pada boosting untuk deret waktu.
11. **Kejanggalan [PR]:** tidak ditemukan.
- **Boleh dikutip untuk:** HyperbandPruner di Optuna; prinsip SuccessiveHalving. **Jangan** untuk MedianPruner.

---

### F7. `optunadocs` — Dokumentasi Optuna 5.0.0 (sampler dan pruner)
- **Versi dibaca:** halaman `/en/stable/` bertanda "Optuna 5.0.0 documentation", dibuka lewat alat web 30 Okt 2026. Tabel kemampuan sampler diambil dari halaman indeks versi 5.1.0.dev (`/en/latest/`). Lokasi = nama halaman.
- **TPESampler:** "Sampler using TPE (Tree-structured Parzen Estimator) algorithm." Rujukan pertama Bergstra dkk. (2011). Bawaan `n_startup_trials=10`, `n_ei_candidates=24`; `multivariate=None` otomatis **True untuk satu objektif**.
- **CmaEsSampler:** "A sampler using cmaes as the backend." **"Please note that this sampler does not support CategoricalDistribution."** Parameter di luar *relative search space* diambil oleh `independent_sampler` (bawaan RandomSampler). Rujukan utamanya tutorial Hansen (2016) dan beberapa varian CMA-ES; Hansen & Ostermeier (2001) tidak disebut.
- **NSGAIISampler:** "Multi-objective sampler using the NSGA-II algorithm." Rujukan Deb dkk. (2002). Halaman ini **tidak menyebut** pemakaian untuk satu objektif. Bawaan `population_size=50`.
- **QMCSampler:** "A Quasi Monte Carlo Sampler that generates low-discrepancy sequences." Jenis `sobol` (bawaan) atau `halton`; `scramble` mengacak barisan. Trial pertama dan parameter di luar *relative search space* diambil oleh *independent sampler*. Fitur eksperimental sejak v3.0.0. Memakai implementasi QMC SciPy.
- **GridSampler:** pencarian lengkap atas grid yang ditentukan; optimasi berhenti otomatis bila semua kombinasi sudah dievaluasi.
- **MedianPruner:** "Pruner using the median stopping rule." Trial dihentikan bila hasil antara terbaiknya lebih buruk dari median trial sebelumnya pada langkah yang sama. **Tidak ada rujukan paper.**
- **HyperbandPruner:** "Pruner using Hyperband." Rujukan Li dkk. (2018). Dengan TPESampler, tiap *bracket* butuh lebih dari 10 trial untuk *startup*; jumlah *bracket* disarankan sekitar 4–6.
- **Tabel indeks (5.1.0.dev):** kategorikal "works inefficiently" untuk CmaEsSampler dan QMCSampler; float dan integer "works inefficiently" untuk NSGAIISampler.
- **Catatan desain [PR]:**
  - Parameter `loss` AdaBoost (kategorikal) pada *run* CMA-ES sebenarnya diambil acak oleh RandomSampler. Tulis di Bab 3.
  - TPE yang dipakai adalah TPE multivariat, bukan TPE independen seperti di Bergstra dkk. (2011).
  - Pemakaian NSGAIISampler untuk satu objektif dibenarkan lewat argumen sendiri (kartu F5), bukan dari dokumentasi.
- **Boleh dikutip untuk:** cara kerja dan nilai bawaan sampler dan pruner pada versi yang dipakai. Sertakan URL berversi dan tanggal akses.

---

### F8. `sobol1967` — Sobol' (1967), "The distribution of points in a cube and the approximate evaluation of integrals", Zh. Vychisl. Mat. Mat. Fiz. 7(4), 784–802 *(paper metode)*
- **Versi dibaca:** terjemahan bahasa Inggris (27 hlm.; halaman cetak 86–112), sebagian teks hasil OCR. Data terbitan asli dari catatan kaki hlm. 86 (dicek dari gambar halaman). **Nama jurnal terjemahan tidak tercetak di PDF.** Untuk sitasi, pakai terbitan asli seperti di dokumentasi SciPy.
1. **Penulis, tahun:** I. M. Sobol', 1967 (diterima 25 Mei 1966).
2. **Data:** tidak relevan (teori).
3. **Bentuk data & sumber:** tidak relevan.
4. **Masalah:** evaluasi integral di kubus satuan n-dimensi dengan rata-rata nilai fungsi pada sekumpulan titik (*mesh*). Titik yang baik harus tersebar seragam (bagian 1.1, hlm. 86).
5. **Metode:** definisi Π_τ-*mesh* dan LP_τ-*sequence* berbasis *parallelepiped* biner (bagian 1.2, hlm. 87); konstruksi barisan dengan *direction numbers* (bagian 3, hlm. 92 dst.). Di komputer hanya butuh operasi geser dan penjumlahan digit modulo 2, tanpa perkalian atau penjumlahan biasa (hlm. 86).
6. **Hasil:** barisan yang dibangun termasuk yang terbaik dalam keseragaman sebaran (hlm. 86–87).
7. **Metrik:** deviasi dan non-uniformitas sebaran titik.
8. **Riset lanjutan:** tidak dicatat.
9. **Kelebihan [PR]:** sumber asli barisan Sobol.
10. **Kekurangan [PR]:** matematis berat; tidak membahas optimasi hiperparameter.
11. **Kejanggalan [PR]:** tidak ditemukan.
- **Boleh dikutip untuk:** asal-usul barisan Sobol sebagai barisan titik yang tersebar seragam. **Jangan** untuk *scrambling* (itu Owen, 1998) atau implementasi SciPy.

---

### F9. `roy2023qmc` — Roy, Owen, Balandat & Haberland (2023), "Quasi-Monte Carlo Methods in Python", Journal of Open Source Software 8(84), 5309, doi 10.21105/joss.05309 *(paper perangkat lunak)*
- **Versi dibaca:** terbit (3 hlm.); utuh.
1. **Penulis, tahun:** Pamphile T. Roy, Art B. Owen, Maximilian Balandat, Matt Haberland, 2023.
2. **Data:** tidak relevan.
3. **Bentuk data & sumber:** tidak relevan.
4. **Masalah:** bilangan acak semu cenderung membentuk celah dan gerombolan di dimensi tinggi, sehingga metode Monte Carlo konvergen lambat (hlm. 1).
5. **Metode:** submodul `scipy.stats.qmc` yang diperkenalkan di SciPy 1.7.0; QMC mengganti bilangan acak dengan barisan deterministik tanpa celah dan gerombolan (hlm. 1).
6. **Hasil:** tersedia Sobol dan Halton (dengan atau tanpa *scrambling*), Latin Hypercube, ukuran *discrepancy*, dll. (hlm. 1–2). **Optuna memakai implementasi QMC SciPy** (Ishikawa dkk., 2022) (hlm. 2).
7. **Metrik:** tidak relevan.
8. **Riset lanjutan:** tidak dicatat.
9. **Kelebihan [PR]:** menghubungkan QMCSampler Optuna dengan SciPy dan literatur QMC.
10. **Kekurangan [PR]:** paper perangkat lunak, bukan studi empiris.
11. **Kejanggalan [PR]:** tidak ditemukan.
- **Boleh dikutip untuk:** QMC dan *scrambling* menurut SciPy; Optuna memakai implementasi QMC SciPy (hlm. 2).

---

### F10. `scipysobol` — Dokumentasi SciPy v1.18.0, `scipy.stats.qmc.Sobol`
- **Versi dibaca:** cetak halaman web, diakses 1 Nov 2026 pukul 21:08 (4 hlm.). URL: https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.qmc.Sobol.html
- "Engine for generating (scrambled) Sobol' sequences." Sobol adalah barisan *low-discrepancy* dan *quasi-random* (hlm. 1).
- `scramble=True` (bawaan) memakai LMS+shift (hlm. 1). *Scrambling* membuat barisan cocok untuk integran singular, memberi estimasi galat, dan bisa mempercepat konvergensi (Notes, hlm. 3).
- *Direction numbers* dari Joe & Kuo (2008); dimensi maksimum 21.201 (hlm. 3).
- **Peringatan:** barisan Sobol kehilangan sifat keseimbangan bila ukuran sampel bukan pangkat 2, titik pertama dilewati, atau barisan dijarangkan (hlm. 3).
- Rujukan: Sobol (1967); Matoušek (1998); Owen (1998) "Scrambling Sobol and Niederreiter-Xing points"; Joe & Kuo (2008); Owen (2020) (hlm. 3).
- **Catatan desain [PR]:** bila `n_trials` QMCSampler di skripsi bukan pangkat 2 (misalnya 50), sifat keseimbangan Sobol tidak terjamin. Pilihannya memakai 32/64 trial atau menuliskannya sebagai keterbatasan.
- **Boleh dikutip untuk:** cara kerja Sobol dan *scrambling* di SciPy, plus peringatan pangkat 2. Cek versi SciPy yang terpasang dan pakai URL versi yang sama.

---

## G. Evaluasi dan uji statistik

### G1. `harvey1997` — Harvey, Leybourne & Newbold (1997), "Testing the equality of prediction mean squared errors", International Journal of Forecasting 13, 281–291 *(paper metode)*
- **Versi dibaca:** terbit (11 hlm.); nomor halaman = halaman jurnal.
1. **Penulis, tahun:** David Harvey, Stephen Leybourne, Paul Newbold, 1997.
2. **Data:** simulasi Monte Carlo.
3. **Bentuk data & sumber:** tidak relevan.
4. **Masalah:** uji Diebold–Mariano bisa *over-sized* pada sampel sedang, makin parah saat horizon h naik (hlm. 282).
5. **Metode:** uji DM termodifikasi: statistik DM dikali [(n + 1 − 2h + n⁻¹h(h − 1))/n]^{1/2} (pers. 9, hlm. 283); nilai kritis dari distribusi t Student dengan n − 1 derajat bebas (hlm. 283–284).
6. **Hasil:** uji termodifikasi memperbaiki ukuran uji pada sampel kecil dan sedang; direkomendasikan untuk praktik (abstrak; penutup).
7. **Metrik:** ukuran dan daya uji (simulasi).
8. **Riset lanjutan:** tidak dicatat.
9. **Kelebihan [PR]:** koreksi sederhana dan langsung dipakai.
10. **Kekurangan [PR]:** tetap menguji rata-rata kinerja sepanjang sampel.
11. **Kejanggalan [PR]:** tidak ditemukan.
- **Boleh dikutip untuk:** koreksi HLN dan nilai kritis t(n − 1) (hlm. 283–284). **Catatan [PR]:** `dm_test` di kode skripsi sudah memakai faktor koreksi ini, autokovarians sampai lag h − 1, dan `stats.t` dengan df = n − 1 (dicek 30 Okt 2026).

---

### G2. `diebold1995` — Diebold & Mariano (1995), Journal of Business & Economic Statistics 13(3), 253–263 *(paper metode)*
- **Relevansi v3 [PR]:** dasar uji DM. Selalu dipasangkan dengan G1 (koreksi HLN) yang dipakai di kode. *(Kartu lama; dibaca ulang 3 Nov 2026.)* **Untuk v3 [PR]:**
  - Horizon k langkah: selisih loss dianggap (k−1)-dependent, jadi varians memakai k−1 autokovarian dengan jendela uniform (hlm. PDF 6–7). Dasar lag h−1 untuk horizon 5/15/30/60.
  - Simulasi: statistik asimtotik oversized pada sampel kecil dengan korelasi serial (hlm. PDF 18). Motivasi koreksi HLN (G1).
  - Contoh empiris: ramalan "no change" (random walk) vs forward rate untuk kurs USD/NLG bulanan 1977–1991, loss absolut; MAE 1,42 vs 1,53, "The random walk wins", tetapi S1 = −1,3, p = 0,19 (tidak signifikan) (hlm. PDF 19–20). Kutipan kuat untuk naive baseline + DM.
- **Versi dibaca:** **NBER Technical Working Paper 169 (Nov 1994)**; hlm. PDF (dibaca lewat gambar/OCR); dibaca ulang dari scan 35 hlm. Halaman cetak = hlm. PDF − 2 mulai bagian 2.
1. **Penulis, tahun:** Francis X. Diebold, Roberto S. Mariano, 1995.
2. **Data:** simulasi Monte Carlo, minimal 5.000 replikasi (bagian 4, hlm. PDF 15–18); contoh empiris kurs Dolar/Gulden Belanda bulanan 1977.01–1991.12 (bagian 5, hlm. PDF 19).
3. **Bentuk data & sumber:** tidak relevan.
4. **Masalah:** uji formal apakah dua ramalan berbeda akurasinya, dengan fungsi loss sembarang (abstrak, hlm. PDF 2).
5. **Metode:** H0: E[d_t] = 0, dengan d_t = g(e₁t) − g(e₂t) selisih loss (hlm. PDF 5); statistik berbasis rata-rata d_t dibagi akar estimasi densitas spektral di frekuensi nol (hlm. PDF 5).
6. **Hasil:** loss **tidak harus kuadratik, simetris, atau kontinu**; galat ramalan boleh tidak normal, berautokorelasi, dan berkorelasi antarramalan (abstrak, hlm. PDF 2; hlm. PDF 4). Kata **"kontinu"** baru muncul di bagian 2.3 (hlm. PDF 9), bukan di abstrak.
7. **Metrik:** statistik DM, asimtotik N(0,1); juga uji eksak sampel kecil, *sign test* dan *Wilcoxon signed-rank* (bagian 2.2, hlm. PDF 7–9).
8. **Riset lanjutan:** tidak dicatat.
9. **Kelebihan [PR]:** sangat umum dan mudah dipakai.
10. **Kekurangan [PR]:** menguji rata-rata kinerja sepanjang sampel; tidak menangkap perubahan kinerja dari waktu ke waktu.
11. **Kejanggalan [PR]:** tidak ditemukan.
- **Boleh dikutip untuk:** uji perbedaan akurasi dua **ramalan** dengan loss asimetris seperti QLIKE. **Jangan** tulis "membandingkan dua model"; tulis "dua ramalan". Jangan sebut nomor persamaan (versi WP).

---

### G3. `holm1979` — Holm (1979), Scandinavian Journal of Statistics 6(2), 65–70 *(paper metode)*
- **Relevansi v3 [PR]:** koreksi uji berganda, karena v3 menjalankan banyak uji DM (4 model × 7 metode HPO/pruner × 3 split × 5 horizon). Label "H2b" di kartu lama merujuk hipotesis v2. Stable URL JSTOR: http://www.jstor.org/stable/4615733. *(Kartu lama; dibaca ulang 3 Nov 2026.)*
- **Versi dibaca:** terbit (JSTOR); utuh.
1. **Penulis, tahun:** Sture Holm, 1979.
2. **Data:** contoh ilustratif.
3. **Bentuk data & sumber:** tidak relevan.
4. **Masalah:** mengendalikan tingkat kesalahan saat menguji banyak hipotesis sekaligus (abstrak, hlm. 65).
5. **Metode:** prosedur **sequentially rejective**: urutkan p-value, tolak berurutan dengan ambang α/(n − i + 1), berhenti saat gagal menolak.
6. **Hasil:** tingkat signifikansi berganda tetap α seperti Bonferroni, tetapi daya uji bisa jauh lebih tinggi (hlm. 65–66).
7. **Metrik:** tidak relevan.
8. **Riset lanjutan:** tidak dicatat.
9. **Kelebihan [PR]:** sederhana dan berlaku umum.
10. **Kekurangan [PR]:** tidak memanfaatkan korelasi antaruji.
11. **Kejanggalan [PR]:** tidak ditemukan.
- **Boleh dikutip untuk:** koreksi Holm pada uji berganda (H2b).

---

### G4. `cerqueira2020` — Cerqueira, Torgo & Mozetič (2020), Machine Learning 109, 1997–2028
- **Relevansi v3 [PR]:** validasi deret waktu tanpa pengacakan (TimeSeriesSplit) saat *tuning*. *(Kartu lama; dibaca ulang 3 Nov 2026.)* DOI tercetak di PDF (3 Nov 2026). **Untuk v3 [PR]:** `TimeSeriesSplit` sklearn setara skema *prequential in blocks* dengan window bertambah (Gambar 3 kiri, hlm. 2000); di studi ini Rep-Holdout dipakai sebagai acuan perbandingan (hlm. 2013).
- **Versi dibaca:** terbit; abstrak, bagian 1–3, dan penutup dibaca.
1. **Penulis, tahun:** Vitor Cerqueira, Luis Torgo, Igor Mozetič, 2020.
2. **Data:** 174 deret waktu nyata dan 3 deret sintetis (abstrak).
3. **Bentuk data & sumber:** deret publik berbagai domain.
4. **Masalah:** metode estimasi kinerja mana yang tepat untuk peramalan deret waktu (abstrak).
5. **Metode:** membandingkan validasi silang (termasuk *blocked*), *holdout*, *repeated holdout*, dan *prequential in blocks* dengan window bertambah atau bergeser (Gambar 3, hlm. 2000–2001).
6. **Hasil:**
   - Validasi silang biasa memutus urutan waktu (hlm. 1998).
   - *Blocked CV* dapat dipakai untuk deret stasioner, sedangkan untuk deret tidak stasioner estimasi paling akurat datang dari metode out-of-sample, terutama *repeated holdout* pada beberapa periode uji (abstrak).
7. **Metrik:** selisih loss estimasi terhadap loss sebenarnya.
8. **Riset lanjutan:** *disebut paper* di bagian 5.3 (hlm. 2019).
9. **Kelebihan [PR]:** studi empiris besar dan sistematis.
10. **Kekurangan [PR]:** fokus estimasi kinerja, bukan pemilihan hiperparameter untuk volatilitas.
11. **Kejanggalan [PR]:** tidak ditemukan.
- **Catatan istilah:** paper memakai istilah "prequential in blocks" (growing/sliding window), **bukan "forward-chaining"**.
- **Boleh dikutip untuk:** validasi silang acak tidak cocok untuk deret waktu; skema *prequential in blocks* dengan window bertambah. **Jangan** untuk klaim bahwa CV selalu salah (blocked CV boleh untuk deret stasioner).

---

### G5. `tashman2000` — Tashman (2000), International Journal of Forecasting 16(4), 437–450 *(tinjauan)*
- **Relevansi v3 [PR]:** satu periode uji rentan terhadap kejadian unik. Dasar memakai beberapa rasio split. *(Kartu lama; dibaca ulang 3 Nov 2026.)* PII S0169-2070(00)00065-0 tercetak di PDF (3 Nov 2026).
- **Versi yang dibaca:** terbit; bagian 1–4 (hlm. 437–442) dan rekomendasi dibaca; sisanya ditelusuri.

1. **Penulis dan tahun:** Leonard J. Tashman, 2000.
2. **Dataset dan rentang waktu:** tidak relevan (tinjauan); contoh dari studi lain, misalnya Pack (1990), 95 bulan penjualan ritel (Tabel 1, hlm. 441).
3. **Bentuk dataset dan sumber:** tidak relevan.
4. **Permasalahan utama:** bagaimana merancang uji akurasi ramalan out-of-sample yang baik (abstrak, hlm. 437).
5. **Metode / model:** tinjauan tentang:
   - *fixed* vs *rolling origin*;
   - *updating* vs *recalibration*;
   - *fixed* vs *rolling window*;
   - satu vs banyak periode uji;
   - banyak deret waktu;
   - desain kompetisi peramalan.
6. **Hasil:**
   - Evaluasi *fixed origin* punya tiga kelemahan (hlm. 439):
     - hanya satu error per *lead time*;
     - rentan terhadap kejadian unik pada titik awal;
     - meringkas error dengan rata-rata lintas *lead time*.
   - MAPE sangat bergantung pada pilihan periode uji (Tabel 1, hlm. 441).
   - Akurasi relatif metode tidak konsisten antarperiode uji (Fildes dkk. 1998, hlm. 441).
7. **Metrik:** dibahas, misalnya hindari ukuran yang bergantung skala (hlm. 445); tidak relevan sebagai metrik studi.
8. **Potensi penelitian selanjutnya:** *disebut paper:* evaluasi metode untuk hierarki produk adalah arah riset penting (hlm. 447, 449).
9. **Kelebihan utama [Penilaian reviewer]:** rujukan klasik dan rinci tentang desain evaluasi out-of-sample; rekomendasinya konkret.
10. **Kekurangan utama [Penilaian reviewer]:** tidak ada uji statistik formal untuk perubahan kinerja; contoh terbatas pada data bisnis bulanan dan kuartalan.
11. **Tidak konsisten, tidak lazim, tidak logis [Penilaian reviewer]:** tidak ditemukan pada bagian yang dibaca. Satu catatan: rekomendasi memakai ukuran persentase seperti MAPE (hlm. 445) tidak cocok untuk volatilitas yang nilainya bisa mendekati nol. Ini soal konteks penerapan, bukan kesalahan paper.

- **Kalimat kunci:**
  - Satu periode uji kemungkinan hanya mencerminkan satu fase siklus bisnis; sebaiknya dipakai beberapa periode uji (hlm. 441).
  - Rekomendasi: *rolling origin*, kalibrasi ulang koefisien, dan beberapa periode uji (abstrak, hlm. 437).
- **Jawaban pertanyaan khusus:**
  - **Satu titik awal (*fixed origin*):** ramalan dari satu titik awal "susceptible to corruption by occurrences unique to that origin" (hlm. 439).
  - **Satu periode uji:** periode uji adalah satu interval kalender yang mungkin hanya mencerminkan satu fase siklus bisnis (hlm. 441).
- **Boleh dikutip untuk:** kelemahan evaluasi *fixed origin* dan satu periode uji; akurasi relatif metode berubah antarperiode uji (hlm. 439, 441). **Jangan** untuk rekomendasi MAPE pada volatilitas.

---

## H. Fitur

### H1. `parkinson1980` — Parkinson (1980), Journal of Business 53(1), 61–65 *(paper metode)*
- **Relevansi v3 [PR]:** definisi fitur *range* high–low, bila fitur ini dipakai di eksperimen. *(Kartu lama; dibaca ulang 3 Nov 2026.)* DOI tidak tercetak di PDF JSTOR; stable URL http://www.jstor.org/stable/2352357. Dicek ulang: "2½–5 times better" (hlm. 61), N_x = 5N (hlm. 63), simulasi 100 *random walk* × 10.000 langkah (hlm. 63–64).
- **Versi dibaca:** terbit (JSTOR; hlm. PDF 1 = sampul JSTOR); utuh.
1. **Penulis, tahun:** Michael Parkinson, 1980.
2. **Data:** simulasi *random walk* (hlm. 63–64); contoh penerapan pada harga saham dibahas di bagian V.
3. **Bentuk data & sumber:** harga tertinggi (H) dan terendah (L) per periode; tidak ada dataset empiris bernama.
4. **Masalah:** varians return (konstanta difusi) biasanya hanya diestimasi dari harga penutupan, padahal H dan L memuat informasi tambahan (hlm. 61).
5. **Metode:** penduga *extreme value*: D = 0,361 · rata-rata [ln(H/L)]² (hlm. 63).
6. **Hasil:**
   - Penduga H–L **sekitar 2,5–5 kali lebih efisien** daripada penduga dari harga penutupan (hlm. 61).
   - Untuk varians penduga yang sama, metode tradisional butuh sekitar 5 kali lebih banyak observasi (hlm. 63).
7. **Metrik:** varians penduga (efisiensi relatif).
8. **Riset lanjutan:** tidak disebut secara eksplisit.
9. **Kelebihan [PR]:** sederhana, hanya butuh H dan L, efisiensi jauh lebih tinggi.
10. **Kekurangan [PR]:** mengasumsikan *random walk* kontinu tanpa *drift* dan perdagangan tanpa jeda; tidak mempertimbangkan *noise* mikrostruktur.
11. **Kejanggalan [PR]:** tidak ditemukan.
- **Kalimat kunci:** penggunaan nilai ekstrem (H dan L) memberi estimasi varians yang jauh lebih baik daripada harga penutupan saja (hlm. 61).
- **Boleh dikutip untuk:** definisi fitur *range* Parkinson. **Jangan** untuk klaim bahwa *range* lebih baik dari RV intraday (paper ini tidak membandingkan dengan RV).

---

## K. Dibaca, dibuang

Dibaca penuh, lalu dibuang atas keputusan 30 Okt 2026. Jangan dikutip.

- **K1. Kharola dkk. (2026), Discover Artificial Intelligence 6:1346.** *Random walk* tidak didefinisikan (MAE 1266,51, R² ≈ 0; Tabel 4, hlm. 16); definisi MASE tidak konsisten (hlm. 12 vs 16); fitur High/Low pada bar yang sama (hlm. 13); DM hanya untuk dua model teratas (hlm. 17).
- **K2. Oyedele dkk. (2023), Expert Systems with Applications 213, 119233.** Data harian; tanpa naive dan DM; Open/High/Low hari yang sama dipakai untuk meramal Close (Tabel 2, hlm. 5); data "validasi" Bitfinex tumpang tindih dengan periode latih.
- **K3. Qureshi dkk. (2025), PeerJ Computer Science 11:e2626.** Angka mustahil secara matematis (SVC akurasi 0,65, recall 0,69, F1 0,81; Tabel 6, hlm. 30); data 2018–2022 tetapi log trading bertanggal Juni 2024 (Tabel 4, hlm. 27).
- **K4. Zhu dkk. (2023), Mathematics 11(6), 1335.** XGBoost hanya untuk seleksi fitur; harga ETH/LTC hari yang sama dipakai sebagai fitur (hlm. 15); metrik di skala ternormalisasi.
- **K5. Petukhina, Reule & Härdle (2021), European Journal of Finance 27(1–2), 8–30, doi 10.1080/1351847X.2020.1789684.** Dibuang 1 Nov 2026 karena tidak sesuai. Paper ini membahas pola musiman intraday (data 5 menit, 11 koin, Jul–Agu 2018) dan menyimpulkan dampak trading algoritmik "rather negligible" (hlm. 20). Tidak ada peramalan dan tidak memetakan horizon ke tipe trader. *Bisa dipertimbangkan lagi hanya bila fitur jam/hari dipakai sebagai input model.*

**Tidak dipakai (tidak dibaca):** Gradojevic dkk. (2023) dan Karaa dkk. (2024), atas keputusan 1 Nov 2026. **Zhivkov & Kandilarov (2026)** tidak ditemukan di mana pun; kemungkinan referensi karangan. Jangan dikutip.

---

## Belum ada PDF (opsional)

- D1 Nakamoto (2008) — kartu belum diisi dari PDF. Kirim PDF bila ingin mengutip isi spesifik.
- *Opsional:* Hansen (2005) SPA dan Hansen, Lunde & Nason (2011) MCS, hanya bila analisis uji berganda ditambah seperti A2. Metadata MCS sudah terverifikasi: Econometrica 79(2), 453–497, doi 10.3982/ECTA5771.
- *Opsional:* Owen (1998), "Scrambling Sobol and Niederreiter-Xing points", Journal of Complexity 14(4), 466–489, bila *scrambling* QMC perlu dijelaskan dari sumber aslinya.

## Perlu dicek di doi.org atau SCImago/Sinta

- G2 Diebold & Mariano — DOI 10.1080/07350015.1995.10524599 (PDF yang dibaca versi WP, tanpa DOI).
- H1 Parkinson — DOI 10.1086/296071 (PDF JSTOR tidak mencetak DOI; JSTOR 2352357).
- E6 LightGBM — versi `lightgbm` di `.venv` dan URL berversinya.
- A1 Rodrigues & Machado — kuartil jurnal *Information* (MDPI).
- B5 Puoti dkk. — halaman dan judul versi ACM.
- C4 Kirilenko dkk. — DOI 10.1111/jofi.12498 dan judul resmi.
- C6 Liu dkk. — volume, nomor, dan halaman cetak.
- E9 Drucker — nomor halaman prosiding ICML 1997.
- F2 Bergstra dkk. 2011 — nomor volume NIPS (24).
- F8 Sobol' — nama jurnal dan halaman versi terjemahan bahasa Inggris (kemungkinan *USSR Computational Mathematics and Mathematical Physics*; belum terverifikasi).
