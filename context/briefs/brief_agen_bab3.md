# Brief 3: Isi Bab III (Metodologi) — Praskripsi

**Repo:** `ferdiendahas/skripsi-latex`
**Berkas yang diubah:** `chapters/bab3-metodologi.tex` (ditulis ulang), `bibliography/references.bib`, `frontmatter/daftar-notasi.tex`, `assets/gambar/`

## Aturan umum

1. **Ini praskripsi.** Bab III **tidak boleh** memuat hasil *out-of-sample*: rata-rata QLIKE, ΔL, UDmax, p-value uji hipotesis, kurva window, dan sejenisnya. Yang boleh: deskripsi data, keputusan desain, hasil pemeriksaan di **window awal** (VIF, hyperparameter terkunci), dan perhitungan manual di Subbab 3.3.
2. Tulis dalam bentuk netral ("penelitian ini menggunakan …"), bukan bentuk lampau ("telah diperoleh …").
3. **Jangan mengarang.** Semua angka, parameter, dan rumus ada di brief ini. Bila ada yang tidak bisa dipastikan, pasang `% CEK:` dan jangan menebak.
4. Jangan mengubah Bab I, Bab II, atau komentar `% CEK:` yang sudah ada.
5. Notasi wajib sama dengan Bab II dan Daftar Notasi: $RV_t$, $\Delta L_t$, $D_t$, $D^{\text{KS}}$, $P^H_t$, $P^L_t$, $F_t$, $W$, $F_b$, $n_F$. Rujuk persamaan dan tabel Bab II dengan `\ref`/`\eqref`; jangan menyalin ulang.
6. Label yang sudah ada di Bab II: `eq:return`, `eq:rv`, `eq:rata-rv`, `eq:har`, `eq:gbdt`, `eq:semivarians`, `eq:parkinson`, `eq:amihud`, `eq:loss`, `eq:delta-loss`, `eq:dm`, `eq:udmax`, `eq:ks`, `tab:strategi`, `tab:desain`, `tab:ringkasan`, `fig:strategi`, `fig:kerangka`, `subsec:likuiditas`.
7. Notasi pasar: BTC/USDT (spot). Istilah asing dicetak miring pada kemunculan pertama di bab ini.
8. Setelah selesai, jalankan `make` dan `make check`, lalu kirim laporan per butir (bagian akhir brief).

---

## A. Persiapan berkas

### A1. Gambar data
- Salin `results/manual/gambar-3-x-harga-rv.pdf` (dari paket `skripsi_rv`, diberikan Ferdi) ke `assets/gambar/gambar-3-2-harga-rv.pdf`.
- Hapus `assets/gambar/gambar-1-1-harga-rv.pdf` **setelah** memastikan tidak dirujuk di mana pun (`grep -r gambar-1-1`).
- Bila berkas PDF baru belum ada di repo, berhenti di butir ini dan laporkan; butir lain tetap dikerjakan dengan `\includegraphics` yang menunjuk path di atas.

### A2. Referensi baru di `references.bib`
Tambahkan entri berikut. Ambil metadata lengkap dari `https://api.crossref.org/works/<DOI>` dengan aturan yang sama seperti brief 1–2 (jangan menimpa dengan data Crossref yang lebih buruk). Bila judul hasil Crossref **berbeda substansi** dari judul di bawah, jangan tambahkan entri itu; laporkan ke Ferdi.

| Key | Referensi | DOI |
|---|---|---|
| abdi2017 | Abdi & Ranaldo (2017), A simple estimation of bid-ask spreads from daily close, high, and low prices, *Review of Financial Studies* 30(12) | 10.1093/rfs/hhx084 |
| corwin2012 | Corwin & Schultz (2012), A simple way to estimate bid-ask spreads from daily high and low prices, *Journal of Finance* 67(2) | 10.1111/j.1540-6261.2012.01729.x |
| dickey1979 | Dickey & Fuller (1979), Distribution of the estimators for autoregressive time series with a unit root, *JASA* 74(366) | 10.1080/01621459.1979.10482531 |
| kwiatkowski1992 | Kwiatkowski, Phillips, Schmidt & Shin (1992), Testing the null hypothesis of stationarity against the alternative of a unit root, *Journal of Econometrics* 54(1–3) | 10.1016/0304-4076(92)90104-Y |

Di atas keempat entri tambahkan `% CEK: ditambahkan untuk Bab III; isi paper belum dibaca, klaim terbatas pada definisi rumus/uji`.

Komentar `% CEK:` lama tentang Abdi–Ranaldo dan Corwin–Schultz di Bab II 2.2.12 diganti dengan sitasi `\cite{abdi2017}` dan `\cite{corwin2012}` pada kalimat yang menyebut kedua estimator. Ini satu-satunya perubahan yang boleh menyentuh Bab II.

---

## B. Isi Bab III

Ganti seluruh isi `chapters/bab3-metodologi.tex` dengan struktur dan isi berikut (judul bab tetap `\chapter{Metodologi}`). Teks di bawah adalah isi yang harus diketik; boleh merapikan kalimat, tidak boleh mengubah substansi atau angka.

### Paragraf pembuka bab
Bab ini menguraikan rancangan penelitian yang digunakan untuk menjawab ketiga rumusan masalah pada Subbab 1.2, meliputi jenis dan alur penelitian, data, rancangan model dan skema pembaruan, contoh perhitungan, serta rancangan evaluasi dan pengujian hipotesis.

### 3.1 Metode Penelitian

**Paragraf 1 (jenis penelitian).** Penelitian ini merupakan penelitian kuantitatif eksperimental dengan data sekunder deret waktu. Objek yang dievaluasi adalah kinerja relatif model LightGBM terhadap model HAR-RV dalam meramalkan *realized variance* harian BTC/USDT spot satu hari ke depan. Penelitian bersifat implementatif: seluruh tahapan, mulai dari pengolahan data, pelatihan model, hingga pengujian statistik, diimplementasikan sebagai satu *pipeline* perangkat lunak yang dapat dijalankan ulang.

**Paragraf 2 (prinsip praregistrasi).** Seluruh keputusan desain, termasuk pasangan model, skema, fungsi *loss*, dan uji konfirmatori untuk setiap hipotesis (Tabel~\ref{tab:ringkasan}), ditetapkan dalam satu berkas konfigurasi sebelum hasil *out-of-sample* pasangan konfirmatori dilihat. Nilai *hash* berkas konfigurasi dicatat pada setiap keluaran sehingga perubahan desain setelah hasil diketahui dapat terdeteksi. Prinsip ini mencegah pemilihan uji atau hipotesis berdasarkan hasil.

#### 3.1.1 Alur Penelitian
Alur penelitian ditunjukkan pada Gambar~\ref{fig:alur} dan terdiri atas tahapan berikut: (1) pengunduhan data dan verifikasi *checksum*; (2) audit dan pembentukan tabel harian; (3) pembentukan target dan fitur; (4) pemeriksaan kolinearitas dan *tuning hyperparameter* pada *window* awal; (5) peramalan *walk-forward* untuk setiap skema pembaruan dan model; (6) perhitungan *loss* harian dan selisih *loss*; (7) pengujian hipotesis konfirmatori dan analisis eksploratori untuk RQ1–RQ3.

**Gambar 3.1** (`fig:alur`), TikZ, diagram alir vertikal, lebar ≤ `\textwidth`:
1. "Arsip Binance BTC/USDT spot 5 menit" →
2. "Audit data & tabel harian" →
3. "Target $RV_{t+1}$ dan fitur (HAR, X)" →
4. "Window awal: cek VIF dan *tuning* (*forward-chaining*)" →
5. "*Walk-forward* bulanan: S0, S1, S2" →
6. "HAR, HAR-X, LGBM-HAR, LGBM-X, *naive*" →
7. "*Loss* harian QLIKE dan MSE" →
8. "$\Delta L_t$ terhadap HAR-RV" → bercabang ke tiga kotak sejajar: "RQ1: UDmax → DM", "RQ2: regresi $\Delta L$ bulanan", "RQ3: $D_t$ antarstrategi" → ketiganya ke "Kesimpulan".

Tambahkan kotak samping "Karakteristik pasar bulanan" yang menerima panah dari kotak 2 dan mengirim panah hanya ke kotak RQ2.

Caption: `Alur Penelitian`.

#### 3.1.2 Tahap Uji Kelayakan
Sebelum desain dikunci, dilakukan tahap uji kelayakan dengan pasangan eksploratori LGBM-HAR dan HAR-RV. Tahap ini memeriksa kelengkapan data, kebenaran *pipeline*, kolinearitas fitur, prosedur *tuning*, dan daya uji. Pasangan konfirmatori LGBM-X terhadap HAR-RV tidak dievaluasi secara *out-of-sample* pada tahap tersebut, dan hasil uji kelayakan tidak digunakan untuk mengubah rumusan masalah, hipotesis, maupun uji konfirmatori.

`% CEK: tahap ini wajib diungkap terbuka (lihat hasil_eksperimen §5). Jangan menambahkan angka hasil pilot.`

#### 3.1.3 Peralatan Penelitian
Implementasi menggunakan bahasa Python 3.12 dengan pustaka `pandas`, `numpy`, `lightgbm` (versi 4 ke atas), `scikit-learn`, `statsmodels`, `scipy`, dan `matplotlib`. Estimator kovarians HAC diimplementasikan sendiri mengikuti kernel Bartlett dengan *bandwidth* otomatis Andrews \cite{andrews1991} dan diverifikasi menghasilkan nilai yang identik dengan fungsi `kernHAC` paket R `sandwich`. Seluruh pelatihan memakai *seed* tetap (42) dan mode deterministik LightGBM.

`% CEK: spesifikasi perangkat keras (laptop/OS) bila diminta pedoman; isi dari Ferdi.`

### 3.2 Desain Sistem

#### 3.2.1 Data
Data yang digunakan adalah *klines* (OHLCV) BTC/USDT pasar spot dengan resolusi 5 menit dari arsip publik Binance (`data.binance.vision`), diunduh per bulan dan diverifikasi dengan *checksum* SHA-256 resmi. Periode data adalah 17 Agustus 2017, yaitu awal ketersediaan arsip, hingga 30 September 2026. Kolom yang digunakan adalah harga pembukaan, tertinggi, terendah, penutupan, serta *quote asset volume* (volume dalam USDT) sebagai volume dolar. Ringkasan data ditunjukkan pada Tabel~\ref{tab:data} dan pergerakannya pada Gambar~\ref{fig:data}.

**Tabel 3.1** (`tab:data`), caption `Ringkasan Data Penelitian`:

| Komponen | Keterangan |
|---|---|
| Sumber | Binance Public Data, folder *spot*, simbol berkas BTCUSDT |
| Resolusi | 5 menit (288 bar per hari UTC) |
| Periode | 17 Agustus 2017 – 30 September 2026 |
| Jumlah bar | 957.865 |
| Jumlah hari | 3.332 |
| Hari dengan bar < 95% | 27 (dibuang, Subbab 3.2.2) |
| Hari dengan RV = 0 | 0 |

Pemilihan pasar spot didasarkan pada tiga alasan: histori spot tersedia sejak 2017 sementara kontrak perpetual baru sejak sekitar September 2019, padahal RQ3 membutuhkan data era awal; harga perpetual mengandung efek *funding rate*, likuidasi, dan basis; serta keterbandingan dengan literatur \cite{dudek2024}. Penggunaan satu bursa sepanjang periode juga mencegah perubahan antarera tercampur dengan efek pergantian sumber data, berbeda dengan Do yang berganti dari Bitstamp ke Binance pada November 2019 \cite{do2026}. Resolusi 5 menit dipilih sebagai kompromi yang aman lintas era likuiditas (Subbab 2.2.3) \cite{liu2015}.

**Gambar 3.2** (`fig:data`): `\includegraphics[width=\textwidth]{assets/gambar/gambar-3-2-harga-rv.pdf}`.
Caption: `Harga Penutupan dan \textit{Realized Variance} Harian BTC/USDT Spot, 17 Agustus 2017--30 September 2026`.
Tepat di bawah gambar (paragraf biasa, ukuran `\small`):
> Keterangan: garis putus-putus menandai batas era *transition* dan *institutional* (1 Januari 2021) mengikuti Do \cite{do2026}; arsir menandai crash Maret 2020, Terra (Mei 2022), dan FTX (November 2022); garis merah menandai *flash crash* 17 Agustus 2023 dan 10 Oktober 2025 ("10/10"). Sumbu vertikal berskala logaritmik. Sumber: data Binance, diolah.

#### 3.2.2 Audit dan Pra-pemrosesan Data
Tahapan audit adalah sebagai berikut.
1. **Standarisasi *timestamp*.** Arsip Binance sejak 1 Januari 2025 mencatat waktu dalam mikrodetik, sedangkan arsip sebelumnya dalam milidetik; seluruh *timestamp* diseragamkan ke milidetik UTC, lalu duplikat dibuang dan data diurutkan.
2. **Kelengkapan hari.** Hari dengan jumlah bar kurang dari 95% (kurang dari 274 dari 288 bar) ditandai tidak lengkap. Pasangan observasi (fitur hari $t$, target hari $t+1$) dibuang bila hari $t$ **atau** hari $t+1$ tidak lengkap atau memiliki RV nol. Sebanyak 27 hari ditandai tidak lengkap. Sebagai uji sensitivitas, hari-hari tersebut dipertahankan.
3. **Hari ekstrem dipertahankan** dan tidak dipangkas, karena lonjakan volatilitas justru bagian dari fenomena yang diteliti.
4. **Volume nol.** Bar dengan volume dolar nol dikecualikan dari perhitungan Amihud (Persamaan~\eqref{eq:amihud}).

#### 3.2.3 Target dan Fitur
Target peramalan adalah $RV_{t+1}$ (Persamaan~\eqref{eq:rv}); model dilatih pada $\ln RV_{t+1}$ lalu ramalannya dikembalikan ke skala level (Subbab 3.2.5). Seluruh fitur hari $t$ hanya memakai data hingga akhir hari $t$. Tiga puluh hari pertama digunakan sebagai periode pemanasan untuk rata-rata bulanan. Fitur dan model yang memakainya ditunjukkan pada Tabel~\ref{tab:fitur}.

**Tabel 3.2** (`tab:fitur`), caption `Fitur dan Model Pemakainya`:

| Fitur | Definisi | Dipakai oleh |
|---|---|---|
| $\ln RV_t$, $\ln RV^{(w)}_t$, $\ln RV^{(m)}_t$ | Persamaan \eqref{eq:rata-rv}, rata-rata 1, 7, 30 hari | semua model |
| Proporsi semivarians negatif | $RS^-_t / RV_t$, Persamaan \eqref{eq:semivarians} | HAR-X, LGBM-X |
| *Return* harian | $\ln(C_t / C_{t-1})$ | HAR-X, LGBM-X |
| Log volume dolar | $\ln \sum_i QV_{t,i}$ | HAR-X, LGBM-X |
| Perubahan log volume dolar | selisih log volume dolar hari $t$ dan $t-1$ | HAR-X, LGBM-X |
| Log *range* Parkinson | $\ln \sigma^2_{P,t}$, Persamaan \eqref{eq:parkinson} | HAR-X, LGBM-X |
| Log Amihud | $\ln \text{Amihud}_t$, Persamaan \eqref{eq:amihud} | LGBM-X |

`% CEK: $C_t$ di baris return harian = harga penutupan bar terakhir hari t; pastikan konsisten dengan Daftar Notasi.`

**Paragraf kolinearitas.** Kolinearitas diperiksa dengan *variance inflation factor* (VIF) pada *window* awal, sebelum fitur dikunci. Log Amihud (VIF 19,6) dan log volume dolar (VIF 18,2) menunjukkan kolinearitas tinggi; secara konstruksi log Amihud mendekati setengah $\ln RV$ dikurangi log volume dolar. Sesuai aturan yang ditetapkan sebelumnya, log Amihud dibuang dari HAR-X saja, sehingga VIF maksimum fitur X pada HAR-X menjadi 6,9. LGBM-X tetap memakai kesembilan fitur karena model pohon tidak terpengaruh kolinearitas dalam estimasi.

#### 3.2.4 Model
Model yang digunakan mengikuti desain 2×2 pada Tabel~\ref{tab:desain}, ditambah model *naive persistence* $\widehat{RV}_{t+1} = RV_t$ sebagai pemeriksaan kewajaran.
- **HAR-RV dan HAR-X** diestimasi dengan *ordinary least squares* (OLS) pada $\ln RV_{t+1}$ (Persamaan~\eqref{eq:har}); HAR-X menambahkan fitur X sebagai regresor.
- **LGBM-HAR dan LGBM-X** menggunakan LightGBM \cite{ke2017} dengan *objective* regresi kuadrat, *bagging* 80% data per pohon, dan *hyperparameter* hasil *tuning* (Subbab 3.2.6).
- **Random Forest** dengan masukan yang sama dengan LGBM-X (300 pohon, minimum 20 observasi per daun, 33% fitur per pemisahan) digunakan hanya sebagai uji sensitivitas jenis model pohon.

#### 3.2.5 Aturan Teknis Peramalan
Aturan berikut berlaku sama untuk semua model.
1. **Koreksi bias transformasi log.** Karena ramalan optimal di bawah QLIKE dan MSE adalah nilai harapan kondisional \cite{patton2011}, $\exp(\hat y)$ tanpa koreksi akan sistematis terlalu rendah. Ramalan dikoreksi menjadi $\exp(\hat y_{t+1} + \hat\sigma^2/2)$. Nilai $\hat\sigma^2$ adalah varians residual model yang dilatih pada 80% awal *window* latih, dihitung pada 20% akhir *window*; setelah itu model dilatih ulang pada seluruh *window*. Residual *in-sample* tidak dipakai karena LightGBM cenderung *overfit*.
2. **Batas bawah ramalan.** Ramalan dibatasi minimal sebesar persentil ke-1 target $RV$ pada *window* latih, $\underline{F}$, karena QLIKE menghukum ramalan yang terlalu rendah jauh lebih berat \cite{patton2011}.

Ramalan akhir adalah:
```latex
\begin{equation}
  F_{t+1} = \max\!\left\{ \exp\!\left(\hat y_{t+1} + \tfrac{1}{2}\hat\sigma^2\right),\; \underline{F} \right\}
  \label{eq:ramalan}
\end{equation}
```
dengan blok keterangan untuk $F_{t+1}$, $\hat y_{t+1}$, $\hat\sigma^2$, dan $\underline{F}$. Sebagai uji sensitivitas, koreksi bias ditiadakan.

#### 3.2.6 *Tuning Hyperparameter*
*Hyperparameter* LightGBM dituning **sekali** pada *window* awal (Agustus 2017 – Agustus 2018) dengan validasi *forward-chaining* lima lipatan \cite{cerqueira2020}, lalu dikunci untuk seluruh periode pengujian. Metrik pemilihan adalah rata-rata QLIKE ramalan $\exp(\hat y)$ antarlipatan. Bila kombinasi terbaik berada di tepi ruang pencarian untuk `min_child_samples` atau `n_estimators`, ruang pencarian diperluas satu langkah ke arah tepi tersebut, maksimal dua kali, dengan batas bawah `min_child_samples` sebesar 5 untuk menjaga regularisasi. Ruang pencarian dan nilai terkunci ditunjukkan pada Tabel~\ref{tab:tuning}.

**Tabel 3.3** (`tab:tuning`), caption `Ruang Pencarian dan \textit{Hyperparameter} Terkunci`:

| Parameter | Ruang pencarian awal | LGBM-HAR | LGBM-X |
|---|---|---|---|
| `num_leaves` | 3, 7, 15 | 3 | 3 |
| `min_child_samples` | 10, 20, 40, 80 | 10 | 5 |
| `n_estimators` | 50, 100, 300, 600 | 300 | 300 |
| `learning_rate` | 0,03 | 0,03 | 0,03 |
| `reg_lambda` | 1, 10 | 1 | 1 |

Kalimat setelah tabel: Nilai `min_child_samples` = 5 pada LGBM-X merupakan batas bawah ruang pencarian yang ditetapkan sebelumnya, sehingga dicatat sebagai keputusan desain untuk menjaga regularisasi.

#### 3.2.7 Skema Pembaruan Model (*Walk-Forward*)
Peramalan dilakukan secara *walk-forward* bulanan: pada awal setiap bulan uji, model dilatih ulang (kecuali S0) menggunakan data dengan tanggal target sebelum bulan tersebut, lalu meramalkan setiap hari dalam bulan itu. Ketiga strategi utama mengikuti Tabel~\ref{tab:strategi} dan Gambar~\ref{fig:strategi}. Model HAR-RV memakai strategi dan *window* yang sama dengan model ML pada setiap sel perbandingan \cite{chassot2026}. Awal periode *out-of-sample* setiap skema ditunjukkan pada Tabel~\ref{tab:oos}; perbandingan antarskema selalu dilakukan pada periode bersama.

**Tabel 3.4** (`tab:oos`), caption `Skema Pembaruan dan Awal Periode \textit{Out-of-Sample}`:

| Skema | Data latih | Awal OOS | Peran |
|---|---|---|---|
| S0 | *Window* awal, tidak dilatih ulang | 1 Sep 2018 | pembanding manfaat adaptasi |
| S1 | Seluruh data tersedia (*expanding*) | 1 Sep 2018 | utama (RQ3) |
| S2-365 | 365 hari terakhir | 1 Sep 2018 | utama (RQ1, RQ2, RQ3) |
| S2-730 | 730 hari terakhir | 1 Sep 2019 | eksploratori |
| S2-180 | 180 hari terakhir | 1 Sep 2018 | eksploratori |
| S2-1095 | 1.095 hari terakhir | 1 Sep 2020 | eksploratori |
| Tertunda-365 | hari ke-730 s.d. ke-365 sebelum bulan uji | 1 Sep 2019 | eksploratori (umur data) |

Paragraf penutup: Pembagian era mengikuti Do \cite{do2026}, dengan batas 1 Januari 2021 antara era *transition* dan *institutional*; data tahun 2026 diperlakukan sebagai kelanjutan era *institutional* dan diuji sensitivitasnya. Batas era hanya digunakan dalam analisis, tidak sebagai fitur model.

#### 3.2.8 Kontrol Kebocoran Data
Langkah pencegahan kebocoran informasi masa depan:
1. fitur hari $t$ hanya memakai data hingga akhir hari $t$, sedangkan target adalah hari $t+1$;
2. *tuning* hanya dilakukan pada *window* awal dengan *forward-chaining*, bukan validasi silang acak \cite{cerqueira2020};
3. $\hat\sigma^2$ dan batas bawah $\underline{F}$ dihitung hanya dari *window* latih;
4. batas era tidak digunakan sebagai fitur;
5. tidak ada ambang atau label yang dibentuk dengan melihat data *out-of-sample*.

**Jangan** menulis apa pun tentang *scaler* atau standarisasi fitur; tidak ada standarisasi dalam implementasi.

### 3.3 Perhitungan Manual

**Paragraf pembuka.** Subbab ini memberikan contoh perhitungan satu kali peramalan untuk model HAR-RV dan LGBM-HAR. Agar tidak memuat hasil pengujian, contoh diambil dari *window* awal: hari $t^* = $ 30 Agustus 2018 digunakan untuk meramalkan $RV$ tanggal 31 Agustus 2018, dengan 339 observasi latih (tanggal target 16 September 2017 s.d. 30 Agustus 2018). Seluruh angka ditulis dengan enam digit bermakna dan telah dicocokkan dengan keluaran implementasi.

Buat empat sub-subbab berikut, isinya **persis** mengikuti `perhitungan_manual.md` (salinan ada di bagian F brief ini). Format angka Indonesia (koma desimal, titik ribuan); notasi ilmiah ditulis $5{,}37199 \times 10^{-4}$.

**3.3.1 *Realized Variance* dan Komponen HAR**
- Tabel 3.5 (`tab:manual-rv`): lima bar pertama (timestamp, close, $r$, $r^2$, $r<0$). Tulis di atas tabel bahwa return bar pertama memakai close bar terakhir 29 Agustus 2018 (7.031,22).
- Uraikan: 288 bar; $RV_{t^*} = 0{,}000537199$; $RS^- = 0{,}000267476$ (154 bar negatif); proporsi 0,497908.
- Tabel 3.6 (`tab:manual-har`): tujuh nilai RV untuk rata-rata mingguan, lalu rata-rata mingguan, ringkasan 30 nilai bulanan (min, maks, rata-rata), dan ketiga nilai ln.

**3.3.2 Fitur X**
- Tabel 3.7 (`tab:manual-x`): enam fitur dengan input mentah dan hasil, sesuai Bagian 3 file manual. Tambahkan satu kalimat bahwa HAR-X tidak memakai log Amihud.

**3.3.3 Peramalan HAR-RV dan LGBM-HAR**
- HAR-RV: tabel koefisien atau penulisan sejajar; tulis penjumlahan $\hat y$ langkah demi langkah dalam `align`; lalu $\hat\sigma^2 = 0{,}497938$ (dilatih pada 271 observasi awal, residual 68 observasi akhir); $\exp(\hat y + \hat\sigma^2/2)$; batas bawah; $F_{\text{HAR}}$. Rujuk Persamaan~\eqref{eq:ramalan}.
- LGBM-HAR: jelaskan bahwa nilai awal (rata-rata $\ln RV_{t+1}$ data latih, $-6{,}03756$) dilebur ke nilai daun pohon pertama sehingga $\hat y$ adalah jumlah nilai daun 300 pohon (Persamaan~\eqref{eq:gbdt}). Tampilkan struktur pohon ke-1 dan ke-2 sebagai diagram TikZ kecil berdampingan (Gambar 3.3, `fig:manual-pohon`), dengan lintasan hari $t^*$ ditebalkan. **Jangan cantumkan jumlah observasi ($n$) per daun.** Lalu tulis: kontribusi pohon ke-1, ke-2, jumlah pohon ke-3 s.d. ke-300, $\hat y = -7{,}32044$, $\hat\sigma^2 = 0{,}511547$, $\exp(\cdot)$, batas bawah, $F_{\text{LGBM}}$.

`% CEK: jumlah n per daun pohon ke-1 (256) tidak konsisten dengan bagging 80% dari 339 obs (~271); sedang dicek di chat script. Karena itu n tidak ditampilkan.`

**3.3.4 Evaluasi Satu Hari**
- Tabel 3.8 (`tab:manual-loss`): RV aktual, ramalan, $RV/F$, QLIKE, MSE untuk kedua model.
- $\Delta L = 0{,}209076 - 0{,}236783 = -0{,}0277067$.
- Kalimat wajib setelahnya: Nilai negatif menunjukkan LGBM-HAR lebih akurat **pada hari contoh ini saja**; satu hari tidak dapat dijadikan dasar kesimpulan, sehingga pengujian dilakukan atas seluruh periode *out-of-sample* sebagaimana diuraikan pada Subbab 3.4.

### 3.4 Evaluasi dan Pengujian Hipotesis

#### 3.4.1 Fungsi *Loss* dan Selisih *Loss*
Setiap ramalan dievaluasi dengan QLIKE sebagai *loss* utama dan MSE pada skala level sebagai pelengkap (Persamaan~\eqref{eq:loss}). Objek analisis adalah selisih *loss* harian $\Delta L_t$ (Persamaan~\eqref{eq:delta-loss}). Pasangan konfirmatori adalah LGBM-X terhadap HAR-RV pada skema S2-365; pasangan lain, yaitu LGBM-HAR–HAR, HAR-X–HAR, LGBM-X–LGBM-HAR, dan LGBM-X–HAR-X, digunakan untuk dekomposisi secara eksploratori.

#### 3.4.2 Uji Konfirmatori
Uji konfirmatori setiap hipotesis mengikuti Tabel~\ref{tab:ringkasan}. Rincian pelaksanaannya:
1. **RQ1.** UDmax (Persamaan~\eqref{eq:udmax}) pada rata-rata $\Delta L_t$ dengan *trimming* $\varepsilon = 0{,}15$ dan maksimum lima perubahan, statistik Wald memakai kovarians HAC \cite{bai1998,bai2003,martins2016}. Bila UDmax tidak menolak $H_0$, dilanjutkan dengan uji tipe Diebold–Mariano (Persamaan~\eqref{eq:dm}) pada seluruh sampel.
2. **RQ2.** H2a diuji dengan regresi rata-rata $\Delta L$ bulanan pada empat karakteristik pasar (Subbab 3.4.3), dengan uji-F bersama berbasis kovarians HAC. H2b diuji dengan regresi $\Delta L_t = a + b\,\text{Era}_t + e_t$ untuk dua pasangan kontribusi fitur X (HAR-X–HAR dan LGBM-X–LGBM-HAR), uji-t HAC pada $b$, dengan koreksi Holm atas dua uji tersebut \cite{holm1979}.
3. **RQ3.** Uji-t HAC dua sisi pada rata-rata $D_t$ (Subbab 2.4) di era *institutional*, pada periode bersama S2-365 dan S1. H3 didukung bila rata-rata $D_t$ negatif dan signifikan; rata-rata positif yang signifikan dibaca sebagai dukungan bagi hipotesis tandingan.

Semua uji menggunakan taraf signifikansi 5% dan kovarians HAC Newey–West dengan kernel Bartlett dan *bandwidth* otomatis Andrews \cite{newey1987,andrews1991}.

**Paragraf nilai kritis.** Nilai kritis UDmax, uji perubahan berurutan, dan *Fluctuation test* diperoleh dengan simulasi Monte Carlo, bukan dikutip dari tabel: 3.000 replikasi deret normal baku sepanjang 1.000 observasi untuk UDmax, dan 5.000 replikasi gerak Brown diskret untuk *Fluctuation test*. *p-value* dihitung sebagai proporsi statistik simulasi yang tidak lebih kecil dari statistik amatan, $(k+1)/(R+1)$. Nilai kritis simulasi dibandingkan dengan tabel Bai–Perron sebagai pemeriksaan \cite{bai1998}.

`% CEK: tabel asli Bai–Perron (1998) untuk q = 1, ε = 0,15 belum dicocokkan langsung.`

#### 3.4.3 Variabel Karakteristik Pasar (RQ2)
Untuk setiap bulan uji dihitung empat variabel (Tabel~\ref{tab:rq2var}).

**Tabel 3.9** (`tab:rq2var`), caption `Variabel Karakteristik Pasar Bulanan`:

| Variabel | Definisi |
|---|---|
| Level volatilitas | rata-rata $\ln RV_t$ dalam bulan |
| Volatilitas dari volatilitas | deviasi standar $\ln RV_t$ dalam bulan |
| Likuiditas | rata-rata *spread* Abdi–Ranaldo harian \cite{abdi2017} |
| Pergeseran distribusi fitur | rata-rata $D^{\text{KS}}$ (Persamaan \eqref{eq:ks}) antara *window* latih S2-365 dan bulan uji atas sembilan fitur LGBM-X |

Rumus *spread* Abdi–Ranaldo harian, dengan $\eta_t = (\ln P^H_t + \ln P^L_t)/2$ dan $c_t$ log harga penutupan:
```latex
\begin{equation}
  s_t = \sqrt{\max\{4\,(c_t - \eta_t)(c_t - \eta_{t+1}),\, 0\}}
  \label{eq:abdi}
\end{equation}
```
Nilai negatif di bawah akar dijadikan nol sebelum dirata-rata. Sebagai uji sensitivitas, estimator Corwin–Schultz \cite{corwin2012} digunakan sebagai pengganti. Sebagai pelengkap deskriptif, dihitung pula *population stability index* (PSI) antara *window* latih dan bulan uji.

**Paragraf regresi dan stasioneritas.** Regresi H2a dirumuskan sebagai
```latex
\begin{equation}
  \overline{\Delta L}_m = \alpha + \sum_{k=1}^{4} \gamma_k\, z_{k,m} + \delta\, \text{Era}_m + u_m
  \label{eq:rq2}
\end{equation}
```
dengan $\overline{\Delta L}_m$ rata-rata $\Delta L_t$ bulan $m$, $z_{k,m}$ keempat variabel, dan $\text{Era}_m$ dummy era *institutional* yang selalu disertakan. Untuk menghindari regresi palsu, setiap regresor diuji dengan ADF \cite{dickey1979} dan KPSS \cite{kwiatkowski1992}; regresor di-*differencing* bila ADF gagal menolak akar unit ($p > 0{,}05$) **dan** KPSS menolak stasioneritas ($p < 0{,}05$). Hipotesis yang diuji adalah $\gamma_1 = \gamma_2 = \gamma_3 = \gamma_4 = 0$. Interpretasi bersifat asosiatif, bukan kausal.

#### 3.4.4 Analisis Eksploratori
Analisis berikut bersifat eksploratori dan *p-value*-nya dikoreksi dengan prosedur Holm per keluarga rumusan masalah \cite{holm1979}:
1. uji perubahan berurutan $\sup F(\ell+1 \mid \ell)$ untuk menentukan jumlah dan tanggal perubahan \cite{bai2003};
2. *Fluctuation test* dengan $\mu = 0{,}3$ dan $0{,}2$ sebagai grafik deskriptif \cite{giacomini2010};
3. pasangan dekomposisi, skema S0 dan S2 lain, serta *loss* MSE;
4. kurva panjang *window* (S2-180 s.d. S1) dan perbandingan efek jumlah data (S2-730 terhadap S2-365) dengan efek umur data (Tertunda-365 terhadap S2-365);
5. analisis daya UDmax dengan *bootstrap* blok 30 hari.

#### 3.4.5 Uji Sensitivitas
Kesimpulan konfirmatori diperiksa terhadap variasi pada Tabel~\ref{tab:sensitivitas}.

**Tabel 3.10** (`tab:sensitivitas`), caption `Variasi Uji Sensitivitas`:

| Variasi | Perubahan terhadap desain utama |
|---|---|
| Tanpa 2026 | data uji dibatasi hingga 31 Desember 2025 |
| Hari tidak lengkap dipertahankan | aturan audit Subbab 3.2.2 butir 2 tidak diterapkan |
| *Window* awal 24 bulan | *tuning* dan awal OOS memakai *window* awal 730 hari |
| Lag 1, 5, 22 | horizon HAR mengikuti hari perdagangan saham |
| Random Forest | LGBM-X diganti Random Forest |
| RV 15 menit | target dan fitur HAR dari *return* 15 menit |
| Tanpa koreksi bias | $\hat\sigma^2 = 0$ pada Persamaan \eqref{eq:ramalan} |
| HAR re-estimasi harian | HAR dilatih ulang setiap hari, bukan bulanan |
| Likuiditas Corwin–Schultz | khusus H2a |

`% CEK: sensitivitas RV 5 menit subsampled (butuh data 1 menit) dan retuning tahunan ada di rencana v2.5 tetapi belum dijalankan. Tambahkan ke tabel hanya jika Ferdi memutuskan akan menjalankannya.`

### 3.5 Jadwal Penelitian
Pertahankan tabel `tab:jadwal`, tetapi ganti baris kegiatannya dengan:
1. Studi literatur dan verifikasi kebaruan
2. Pengumpulan dan audit data
3. Uji kelayakan (pilot)
4. Implementasi *pipeline* dan eksperimen
5. Analisis dan pengujian hipotesis
6. Penulisan Bab IV dan V
7. Seminar hasil dan sidang

Kolom bulan dan tanda centang **dikosongkan** dengan `% CEK: diisi Ferdi sesuai rencana dan kalender prodi`. Jangan menebak durasi.

---

## C. Daftar Notasi
Tambahkan ke `frontmatter/daftar-notasi.tex` (urut sesuai kemunculan pertama di Bab III), dengan arti dari teks di atas:
$C_t$ (bila belum ada), $\hat y_{t+1}$, $\hat\sigma^2$, $\underline{F}$, $F_{t+1}$, $\eta_t$, $c_t$, $s_t$, $\overline{\Delta L}_m$, $z_{k,m}$, $\gamma_k$, $\delta$, $\text{Era}_m$, $\text{Era}_t$, $u_m$, $t^*$.
Periksa bentrok dengan simbol yang sudah ada:
- $\delta$ di Bab II dipakai untuk besar pergeseran dalam analisis daya? Bila sudah dipakai, ganti koefisien era di Persamaan \eqref{eq:rq2} menjadi $\theta$.
- $D$, $L$, $m$ tidak boleh mendapat makna baru. $m$ pada Persamaan \eqref{eq:rq2} adalah **indeks bulan**; bila bentrok dengan $m$ (jumlah titik patah), ganti indeks bulan menjadi $j$ di persamaan, tabel, dan teks Bab III.
Laporkan semua penggantian simbol.

---

## D. Daftar Tabel dan Gambar Bab III (harus terbentuk otomatis)
- Gambar 3.1 Alur Penelitian
- Gambar 3.2 Harga Penutupan dan *Realized Variance* Harian BTC/USDT Spot, 17 Agustus 2017–30 September 2026
- Gambar 3.3 Struktur Pohon ke-1 dan ke-2 LGBM-HAR pada Contoh Perhitungan
- Tabel 3.1–3.10 sesuai caption di atas, ditambah tabel jadwal (menjadi Tabel 3.11)

---

## E. Laporan balik
1. Ringkasan per bagian A–D; butir yang tidak bisa dikerjakan beserta alasannya.
2. Hasil verifikasi Crossref keempat referensi baru (judul, penulis, volume, halaman).
3. Daftar penggantian simbol (bila ada).
4. Output `make check` (jumlah halaman, *overfull box*, rujukan menggantung, *missing character*).
5. Konfirmasi tidak ada angka hasil *out-of-sample* di Bab III (cari "0,3592", "UDmax =", "p =", "t =" di bab3; seharusnya hanya muncul di Subbab 3.3 untuk contoh *window* awal).

---

## F. Salinan `perhitungan_manual.md` (sumber angka Subbab 3.3)

Window awal: target_date < 2018-09-01. Hari contoh t* = 2018-08-30, diramal untuk t*+1 = 2018-08-31. Data latih ilustrasi: 339 observasi (target 2017-09-16 s.d. 2018-08-30). Config hash `0af5b5b98c60`.

**1. RV hari t\***. Return bar pertama memakai close bar terakhir 2018-08-29 (C = 7031.22).

| Timestamp (UTC) | Close | r | r² | r < 0 |
|---|---|---|---|---|
| 2018-08-30 00:00 | 7038.22 | 0.000995065 | 9.90153e-07 | tidak |
| 2018-08-30 00:05 | 7036.24 | -0.000281361 | 7.91638e-08 | ya |
| 2018-08-30 00:10 | 7031.41 | -0.000686682 | 4.71532e-07 | ya |
| 2018-08-30 00:15 | 7039.17 | 0.00110301 | 1.21663e-06 | tidak |
| 2018-08-30 00:20 | 7039.01 | -2.27302e-05 | 5.16662e-10 | ya |

288 bar; RV = 0.000537199; RS⁻ = 0.000267476 (154 bar negatif); RS⁻/RV = 0.497908.

**2. Komponen HAR.** RV 24–30 Agustus 2018: 0.000628396, 0.000350138, 0.000482313, 0.000499351, 0.000454143, 0.000440669, 0.000537199. Rata-rata mingguan = 0.000484601. Bulanan (30 nilai, 1–30 Agustus 2018): min 0.000350138, maks 0.0038063, rata-rata 0.00127306. ln RV_d = −7.52914; ln RV_w = −7.63218; ln RV_m = −6.66633.

**3. Fitur X.**

| Fitur | Input mentah | Hasil |
|---|---|---|
| ret | close t* = 6984.84, close t*−1 = 7031.22 | −0.00661815 |
| ln_dvol | volume dolar t* = 3.09357e+08 | 19.55 |
| d_ln_dvol | volume dolar t*−1 = 3.04565e+08 | 19.55 − 19.5344 = 0.0156107 |
| ln_parkinson | H = 7063.63, L = 6784.81 | −7.44394 |
| ln_amihud | 10⁶ × rata-rata \|r\|/QV = 0.00116494 | −6.75508 |
| neg_share | Bagian 1 | 0.497908 |

**4. HAR (OLS).** β0 = −0.56989; βd = 0.478542; βw = 0.0689003; βm = 0.384379.
ŷ = (−0.56989) + (0.478542)(−7.52914) + (0.0689003)(−7.63218) + (0.384379)(−6.66633) = (−0.56989) + (−3.60301) + (−0.525859) + (−2.5624) = −7.26116.
σ̂² (fit 271 obs awal, residual 68 obs akhir, ddof 1) = 0.497938. exp(−7.26116 + 0.248969) = 0.000900836. Batas bawah = 0.000290955. F_HAR = 0.000900836.

**5. LGBM-HAR.** num_leaves 3, min_child_samples 10, n_estimators 300, learning_rate 0.03, reg_lambda 1. Init score = −6.03756 (dilebur ke pohon ke-1).
- Pohon 1: jika ln_rv_m ≤ −5.80353 → daun 0 (−6.06517); selain itu jika ln_rv_d ≤ −5.05151 → daun 1 (−6.02747), selain itu daun 2 (−5.99638). Hari t*: ln_rv_m = −6.66633 → daun 0.
- Pohon 2: jika ln_rv_m ≤ −5.80353 → daun 0 (−0.0260821); selain itu jika ln_rv_d ≤ −4.88302 → daun 1 (0.00821454), selain itu daun 2 (0.0432716). Hari t*: daun 0.
- Pohon 1: −6.06517 (≈ −6.03756 + −0.0276166); pohon 2: −0.0260821; pohon 3–300: −1.22919; ŷ = −7.32044.
- σ̂² = 0.511547; exp(−7.32044 + 0.255773) = 0.000854778; batas bawah 0.000290955; F_LGBM = 0.000854778.

**6. Evaluasi 31 Agustus 2018.** RV aktual = 0.00041419.

| Model | F | RV/F | QLIKE | MSE |
|---|---|---|---|---|
| HAR | 0.000900836 | 0.459784 | 0.236783 | 2.36825e-07 |
| LGBM-HAR | 0.000854778 | 0.484558 | 0.209076 | 1.94118e-07 |

ΔL = 0.209076 − 0.236783 = −0.0277067.
