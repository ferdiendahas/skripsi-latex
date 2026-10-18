# Brief Agen — Revisi Hasil Audit Bab I–III v1 (18 Okt 2026)

> Dasar: audit eksternal Bab I–III (18 Okt) yang sudah dikaji ulang. Basis repo: commit `19929a8`.
> Sumber klaim paper: `context/kartu_paper.md`. Sumber desain: `context/hasil_riset_bitcoin_v2.9.md`.
> Brief ini berisi **perubahan teks saja**. Kalimat sudah disiapkan; salin apa adanya ke lokasi yang disebut.

## 0. Larangan keras (anti-HARKing)
Uji konfirmatori sudah dijalankan. Karena itu, hal-hal berikut **tidak boleh diubah**, walaupun audit menyarankannya:
- isi Rumusan Masalah RQ1–RQ3;
- isi hipotesis H1, H2a, H2b, H3;
- pasangan konfirmatori (LGBM-X vs HAR-RV, skema S2-365);
- uji konfirmatori dan parameternya;
- judul.

Audit poin 1.1 dan 1.2 dijawab dengan **kalimat penjelas** (Bagian 2, no. 1–2), bukan dengan mengubah desain. Kalau menemukan bagian yang menurutmu perlu mengubah salah satu hal di atas, tulis `% USUL:` dan laporkan ke Ferdi.

Juga dilarang: memasukkan angka hasil *out-of-sample* ke Bab I–III, dan menambah klaim paper yang tidak tercatat di kartu.

## 1. Tugas A — Latar Belakang menjadi 8 paragraf
Ganti **seluruh** isi `\section{Latar Belakang}` di `chapters/bab1-pendahuluan.tex` dengan teks di bawah. Komentar kepala file (baris 1–2) diganti menjadi:
```latex
% Bab I v5 (18 Okt 2026) — sumber: context/briefs/brief_agen_revisi_audit_v1.md.
% Klaim paper hanya dari context/kartu_paper.md. RQ terkunci (anti-HARKing).
```

**Aturan sitasi Bab I tetap berlaku:** satu key dikutip satu kali. Kutipan ulang yang diizinkan hanya `mokni2024` (P1, P2), `chassot2026` (P2, P7), dan `dudek2024` (P5, P8), dan saat diulang nama penulisnya tidak disebut. Kalimat yang menjelaskan skala varians (dari P3 lama) dipindah ke Bab II, sudah ada di subbab RV.

```latex
\section{Latar Belakang}

% P1 — hook: pasar berubah   [kartu C1, C2, C3]
Sejak diperkenalkan sebagai sistem uang elektronik tanpa lembaga perantara
\cite{nakamoto2008}, Bitcoin telah melewati tiga era pasar. Menurut Do, yang
meneliti data 2012--2025, era \textit{niche} didominasi pengguna awal, era
\textit{transition} diikuti investor perorangan secara luas, dan era
\textit{institutional} melibatkan lembaga keuangan, termasuk melalui ETF spot
sejak 2024. Dari era ke era, volatilitas turun tajam, volume transaksi naik,
biaya transaksi turun, dan likuiditas makin tahan terhadap guncangan
\cite{do2026}. Namun, perubahan tersebut tidak berjalan mulus. Tingkat
efisiensi pasar Bitcoin berganti-ganti antara periode efisien dan tidak efisien
\cite{mokni2024}. Kondisi ini memunculkan pertanyaan penting bagi peramalan:
apakah model yang paling akurat pada satu periode masih paling akurat ketika
kondisi pasar sudah berubah?

% P2 — efisiensi, pentingnya ramalan volatilitas, dan RV   [kartu C4, C3, D6, A1, A2]
Penelitian tentang efisiensi pasar Bitcoin umumnya menguji apakah
\textit{return} dapat ditebak dari harga masa lalu \cite{yi2023,mokni2024}.
Sulitnya menebak arah return tidak berarti besarnya perubahan harga, atau
volatilitas, juga sulit diramalkan. Ramalan volatilitas tetap dibutuhkan dalam
pengelolaan risiko, penentuan harga derivatif, dan pembentukan portofolio
\cite{chassot2026}. Karena volatilitas tidak dapat diamati secara langsung,
volatilitas diukur dari data harga, salah satunya dengan \textit{realized
variance} (RV), yaitu jumlah kuadrat return intrahari dalam satu hari. Ukuran
volatilitas dari kuadrat return harian sangat berisik, sehingga model dapat
terlihat buruk padahal ramalannya cukup akurat; ketika diukur dengan RV dari
return lima menit, model yang sama terlihat jauh lebih akurat
\cite{andersen1998}. Pada 31 aset dari lima kelas aset, RV lima menit juga
sulit dikalahkan secara signifikan oleh ukuran lain yang lebih rumit
\cite{liu2015}.
% CEK (Ferdi): tulis ulang kalimat "Sulitnya menebak arah return ..." dengan
% kata-kata sendiri.

% P3 — HAR-RV dan ML   [kartu A3, D7, D4]
Salah satu model untuk meramalkan RV merupakan \textit{Heterogeneous
Autoregressive model of Realized Volatility} (HAR-RV), yang meramalkan RV hari
berikutnya dari rata-rata RV harian, mingguan, dan bulanan. Model ini
memanfaatkan sifat volatilitas yang cenderung bertahan lama. Walaupun hanya
berupa regresi linear sederhana, HAR-RV lebih akurat daripada model
autoregresif biasa dan sebanding dengan model memori panjang yang lebih rumit
\cite{corsi2009}. Pada aset kripto yang diperdagangkan setiap hari, rata-rata
mingguan dan bulanan HAR-RV disesuaikan menjadi 7 dan 30 hari \cite{qiu2025}.
Selain model ekonometrika, model \textit{machine learning} (ML) juga mulai
dipakai. Pada empat aset kripto, \textit{random forest} dan LSTM menghasilkan
ramalan volatilitas yang signifikan lebih akurat daripada GARCH
\cite{wang2023}.

% P4 — LightGBM   [kartu I1, I4, I5]
% Catatan: penelitian ini memakai gbdt + bagging tanpa GOSS; jangan sebut
% GOSS/EFB sebagai alasan memilih LightGBM.
Di antara model ML, penelitian ini memilih LightGBM, yaitu implementasi
\textit{gradient boosting decision tree} yang menggabungkan banyak pohon
keputusan secara bertahap. LightGBM dipilih karena tiga alasan. Pertama,
LightGBM dirancang untuk mempercepat pelatihan dengan akurasi yang hampir sama
\cite{ke2017}, sehingga praktis untuk dilatih ulang berkali-kali. Kedua, pada
data tabular berukuran menengah, model berbasis pohon masih lebih unggul
daripada \textit{deep learning} \cite{grinsztajn2022}. Ketiga, LightGBM banyak
dipakai dalam peramalan; pada kompetisi M5, semua metode teratas merupakan
metode ML dan LightGBM dipakai oleh tim-tim teratas, walaupun keunggulan itu
didukung oleh banyak deret yang saling berkaitan dan data tambahan
\cite{makridakis2022}. Pemilihan ini tidak dimaksudkan untuk menyatakan bahwa
LightGBM lebih unggul daripada model ML lain. LightGBM dipakai sebagai wakil
model berbasis pohon yang efisien untuk dilatih ulang secara berkala.
% CEK (Ferdi): Makridakis hlm. 1346 vs 1349 (angka 50 tim). Kalimat di atas
% sengaja tidak menyebut angka.

% P5 — ML dan pohon vs HAR-RV   [kartu D1, D3, D2, D8, D9, D10, D11]
% Catatan: dudek2025lgbm = preprint; kilic2025 dan pyrlik2021 = working paper.
Hasil perbandingan model ML dengan HAR-RV belum seragam. Pada saham, model
berbasis pohon baru lebih unggul daripada HAR-RV setelah diberi data tambahan
\cite{christensen2023}. Pada empat aset kripto, HAR-RV tidak signifikan lebih
buruk daripada LSTM atau random forest \cite{dudek2024}, dan pada Bitcoin
keunggulan LSTM atas HAR-RV hanya signifikan untuk ramalan 60 hari ke depan
\cite{huang2024}. Untuk LightGBM, keunggulan atas HAR-RV pada RV harian
Bitcoin umumnya tidak signifikan \cite{dudek2025lgbm}, sedangkan pada RV enam
jam Bitcoin HAR-RV justru signifikan lebih akurat menurut QLIKE
\cite{brauneis2026}. Pada RV saham, model berbasis pohon bahkan termasuk yang
paling buruk di antara model ML \cite{kilic2025,pyrlik2021}. Kedua penelitian
tersebut melaporkan hasil per tahun atau per kuartal, tetapi perubahan kinerja
antarperiode hanya dijelaskan, tanpa diuji secara statistik.

% P6 — masalah pertama: satu periode uji   [kartu F5, J1, G2, G4, E3]
Sebagian besar penelitian tersebut menilai model pada satu periode pengujian
dan melaporkan hasil rata-ratanya. Satu periode pengujian mungkin hanya
mencerminkan satu kondisi tertentu, dan metode yang unggul pada satu periode
belum tentu unggul pada periode lain \cite{tashman2000}. Dalam bidang ML,
perubahan hubungan antara data masukan dan target dari waktu ke waktu dikenal
sebagai \textit{concept drift}, dan merata-ratakan akurasi sepanjang waktu
dapat menutupi naik-turunnya kinerja model \cite{gama2014}. Uji statistik untuk
memeriksa apakah keunggulan satu ramalan atas ramalan lain berubah dari waktu
ke waktu sebenarnya sudah tersedia \cite{giacomini2010,martins2016}. Salah
satunya, \textit{Fluctuation test}, pernah dipakai pada Bitcoin dan Ethereum,
tetapi untuk meramalkan ukuran risiko kerugian dengan model ekonometrika,
bukan membandingkan ML dengan HAR-RV dalam meramalkan RV \cite{trucios2023}.
Sejauh penelusuran penulis, belum diketahui apakah kinerja relatif LightGBM
terhadap HAR-RV pada Bitcoin tetap sama sepanjang waktu atau berubah mengikuti
kondisi pasar.

% P7 — masalah kedua: cara memperbarui model   [kartu G3, F1, F2, D5, D6]
Masalah berikutnya menyangkut cara memperbarui model, yaitu berapa banyak data
lama yang dipakai saat model dilatih ulang. Model dapat tidak dilatih ulang
(\textit{static}), dilatih ulang dengan data terbaru saja (\textit{rolling
window}), atau dilatih ulang dengan seluruh data yang tersedia
(\textit{expanding window}). Secara teori, rolling window lebih menguntungkan
bila pola data berubah besar dan sering, sedangkan expanding window lebih
menguntungkan bila perubahannya kecil atau tidak ada \cite{rossi2013}. Pada
volatilitas indeks saham S\&P~500 dengan HAR-RV, \textit{window} yang lebih
akurat berganti-ganti antara keduanya \cite{feng2024window}. Pada aset kripto,
perbandingan keduanya baru dilaporkan rinci untuk model GARCH, tanpa HAR-RV
dan tanpa uji statistik \cite{akgun2025}, sedangkan penelitian ML lain pada
Bitcoin hanya mengubah panjang rolling window \cite{feng2024ml}. Cara
pembaruan juga memengaruhi hasil perbandingan. Pada 1.445 saham, model ML
tidak lebih baik daripada HAR-RV yang dilatih ulang setiap hari, tetapi model
ML pada penelitian tersebut tidak dilatih ulang \cite{chassot2026}. Karena itu,
perbandingan yang adil menuntut kedua model diperbarui dengan cara yang sama.
Sejauh penelusuran penulis, juga belum diketahui apakah pengaruh cara
memperbarui model berbeda pada era pasar yang berbeda.

% P8 — penelitian ini   [kartu H1, D3, J5]
Berdasarkan uraian tersebut, penelitian ini menguji apakah kinerja relatif
LightGBM terhadap HAR-RV dalam meramalkan RV harian Bitcoin stabil dari waktu
ke waktu. Data yang dipakai merupakan harga BTC/USDT pasar spot di Binance
periode 2017--2026, dengan periode evaluasi mulai September 2018. Penelitian
ini membandingkan empat model, yaitu HAR, HAR-X, LGBM-HAR, dan LGBM-X, dengan
huruf X menandakan data pasar tambahan, sehingga sumber perbedaan kinerja
dapat diurai menjadi efek model dan efek data. Cara memperbarui model
\textit{static}, \textit{expanding}, dan \textit{rolling} juga dibandingkan,
dengan perlakuan yang sama untuk HAR-RV. Kesalahan ramalan dibandingkan per
hari dengan QLIKE sebagai ukuran utama. Nilai QLIKE tidak berubah bila nilai
aktual dan ramalan dikalikan konstanta yang sama, dan QLIKE tetap memberi
urutan model yang benar walaupun proksi volatilitasnya berisik, selama proksi
tersebut tidak bias \cite{patton2011}. Penelitian ini mengembangkan salah satu
penelitian terdahulu \cite{dudek2024} pada tiga hal, yaitu kestabilan kinerja
dari waktu ke waktu, kaitannya dengan kondisi pasar, dan pengaruh cara
memperbarui model. Penelitian ini tidak mengusulkan algoritma baru.
Kontribusinya berupa cara mengevaluasi model ML pada data yang terus berubah,
dengan memadukan strategi pembaruan model dari bidang ML dan uji kestabilan
ramalan dari bidang peramalan deret waktu, dua bidang yang keterkaitannya
masih disebut sebagai masalah terbuka \cite{suarez2023}.
```

## 2. Tugas B — Perbaikan teks dari audit

Setiap butir: **lokasi** (cari string *anchor*), lalu **tindakan**.

### 1. Cakupan konfirmatori RQ3 (audit 1.1)
**Bab II**, setelah kalimat yang diakhiri `lebih terdampak data usang daripada HAR.` (paragraf H3), tambahkan:
```latex
Uji konfirmatori untuk RQ3 dibatasi pada perbandingan S2-365 dan S1 di era
\textit{institutional}. Panjang \textit{window} lain (180, 730, dan 1.095 hari
serta Tertunda-365) dan era \textit{transition} dianalisis secara
eksploratori, sehingga kesimpulan konfirmatori RQ3 hanya berlaku untuk
perbandingan tersebut.
```
**Bab III**, Subbab Uji Konfirmatori, di akhir butir **H3** (setelah `... dukungan bagi hipotesis tandingan.`), tambahkan kalimat yang sama, tetapi tanpa kalimat terakhirnya.

### 2. Pasangan konfirmatori = paket model + fitur (audit 1.2)
**Bab II**, di akhir paragraf **H1** (setelah `\cite{rossi2013,martins2016}.`), tambahkan:
```latex
Karena LGBM-X berbeda dari HAR-RV dalam algoritma sekaligus fitur masukan,
H1 menguji kinerja relatif paket model dan fitur, bukan efek algoritma murni.
Sumber perbedaannya diurai melalui pasangan dekomposisi pada desain
$2 \times 2$ (Tabel~\ref{tab:desain}) dan melalui H2b.
```
**Bab III**, Subbab Fungsi Loss dan Selisih Loss, setelah kalimat yang diakhiri `digunakan untuk dekomposisi secara eksploratori.`, tambahkan:
```latex
Dengan demikian, pasangan konfirmatori menilai LightGBM beserta fitur
tambahannya. Efek algoritma dibaca dari pasangan LGBM-HAR--HAR-RV yang
memakai masukan sama, dan efek fitur dari pasangan HAR-X--HAR-RV serta
LGBM-X--LGBM-HAR.
```

### 3. Definisi operasional stabilitas (audit 1.3)
**Bab II**, ganti kalimat
`Penelitian ini menggunakan UDmax sebagai uji konfirmatori kestabilan dan \textit{Fluctuation test} sebagai visualisasi eksploratori.`
dengan:
```latex
Penelitian ini menggunakan UDmax sebagai uji konfirmatori kestabilan dan
\textit{Fluctuation test} sebagai visualisasi eksploratori. Secara
operasional, kinerja relatif disebut stabil bila UDmax tidak menemukan
perubahan struktural yang signifikan pada rata-rata $\Delta L_t$. Hasil yang
tidak signifikan dibaca sebagai tidak ditemukannya bukti perubahan, bukan bukti
bahwa kinerja pasti stabil, karena kesimpulan tersebut bergantung pada daya
uji. Peran kedua uji juga berbeda: UDmax menjawab apakah rata-rata $\Delta L_t$
berubah sepanjang waktu, sedangkan uji DM menjawab apakah rata-rata
$\Delta L_t$ pada seluruh periode berbeda dari nol.
```
**Bab III**, di akhir butir **H1** (setelah `... pada seluruh sampel.`), tambahkan:
```latex
Daya UDmax diperiksa pada analisis eksploratori, sehingga hasil yang tidak
signifikan dapat dibaca bersama besaran perubahan yang mampu dideteksi.
```

### 4. Periode data mentah vs periode evaluasi (audit 1.4 dan 3.5)
**Bab II**, Tabel posisi, baris "Penelitian ini": ganti `RV BTC/USDT spot, 2018--2026` dengan `RV BTC/USDT spot, data 2017--2026, evaluasi 2018--2026`.

**Bab III**, Subbab Data, setelah kalimat yang diakhiri `30 September 2026.` dan sebelum `Tanggal awal yang sama ...`, tambahkan:
```latex
Periode data mentah dibedakan dari periode evaluasi. Data 17 Agustus 2017
hingga 31 Agustus 2018 berfungsi sebagai \textit{window} latih awal dan data
\textit{tuning}, periode evaluasi utama berlangsung 1 September 2018 hingga
30 September 2026, dan skema eksploratori dengan \textit{window} lebih panjang
dimulai lebih lambat (Tabel~\ref{tab:oos}).
```

### 5. Batas era sebagai klasifikasi operasional (audit 2.2)
**Bab III**, paragraf yang diawali `Pembagian era mengikuti Do`, ganti seluruh paragraf dengan:
```latex
Pembagian era mengikuti Do \cite{do2026}, dengan batas 1 Januari 2021 antara
era \textit{transition} dan \textit{institutional}. Batas tersebut merupakan
klasifikasi operasional yang diadopsi dari penelitian terdahulu, bukan titik
perubahan struktural yang diuji dalam penelitian ini. Klasifikasi Do berakhir
pada 2025, sehingga data tahun 2026 diperlakukan sebagai kelanjutan era
\textit{institutional} berdasarkan keputusan operasional dan diuji
sensitivitasnya. Batas era hanya digunakan dalam analisis, tidak sebagai fitur
model.
```

### 6. Batas klaim manfaat (audit 2.5)
**Bab I**, Manfaat Praktis: ganti
`dipakai saat model dilatih ulang. Manfaat ini tetap ada apa pun hasilnya,`
dengan
`dipakai saat model dilatih ulang, pada konfigurasi model dan periode yang diuji dalam penelitian ini. Manfaat ini tetap ada apa pun hasilnya,`

### 7. Log dari rata-rata RV (audit 3.1)
**Bab II**, setelah persamaan `\label{eq:har}` (sebelum `Corsi membentuk rata-rata ...`), tambahkan:
```latex
Regresor mingguan dan bulanan merupakan logaritma dari rata-rata RV, yaitu
$\ln RV_t^{(w)}$ dan $\ln RV_t^{(m)}$ dengan $RV_t^{(w)}$ dan $RV_t^{(m)}$ dari
Persamaan~\eqref{eq:rata-rv}, bukan rata-rata dari logaritma RV.
```

### 8. Kesimpulan berlaku untuk konfigurasi yang diuji (audit 3.2)
**Bab I**, Batasan Masalah, tambahkan butir ke-6:
```latex
  \item Kesimpulan tentang LightGBM berlaku untuk konfigurasi yang diuji, yaitu
        \textit{hyperparameter} hasil \textit{tuning} pada \textit{window} awal
        yang dikunci sepanjang periode pengujian, bukan untuk LightGBM secara
        umum.
```

### 9. Definisi $C_{t,0}$ (audit 4.1)
**Bab II**, setelah persamaan `\label{eq:return}`, ganti baris `\textit{Realized variance} harian merupakan` dengan:
```latex
dengan $C_{t,0}$ harga penutupan bar terakhir hari $t-1$, sehingga
\textit{return} bar pertama setiap hari dihitung terhadap penutupan hari
sebelumnya. \textit{Realized variance} harian merupakan
```
(Sesuai kode: `np.log(close).diff()` atas seluruh deret, dan sesuai perhitungan manual Subbab 3.3.1.)

### 10. Asumsi koreksi bias log (audit 4.2)
**Bab III**, Aturan Teknis butir 1. Setelah kalimat yang berisi `setelah itu model dilatih ulang pada seluruh \textit{window}.` dan sebelum `Residual`, tambahkan:
```latex
Koreksi ini tepat bila galat pada skala logaritma kira-kira berdistribusi
normal dengan varians konstan. Karena asumsi tersebut tidak dijamin, koreksi
dipakai sebagai pendekatan, bukan diklaim optimal, dan uji sensitivitas tanpa
koreksi disertakan. Koreksi diterapkan dengan cara yang sama pada keempat
model; model \textit{naive} tidak memerlukannya karena tidak memakai skala
logaritma.
```

### 11. Latih ulang bulanan vs ramalan harian (audit 4.3)
**Bab III**, Subbab Skema Pembaruan Model, setelah kalimat yang diakhiri `lalu meramalkan setiap hari dalam bulan itu.`, tambahkan:
```latex
Parameter model tetap selama satu bulan uji, tetapi fitur untuk meramalkan
hari $t+1$ dihitung dari data hingga akhir hari $t$. RV aktual selama bulan
berjalan baru masuk ke data latih pada pelatihan ulang bulan berikutnya.
Aturan ini berlaku sama untuk HAR-RV dan LightGBM.
```

### 12. Arti "perlakuan setara" (audit 4.4)
**Bab III**, ganti kalimat
`Model HAR-RV memakai strategi dan \textit{window} yang sama dengan model ML pada setiap sel perbandingan \cite{chassot2026}.`
dengan:
```latex
Model HAR-RV memakai strategi dan \textit{window} yang sama dengan model ML
pada setiap sel perbandingan \cite{chassot2026}. Perlakuan setara dalam
penelitian ini berarti kedua model memakai periode data latih, jadwal
pelatihan ulang, dan periode evaluasi yang sama; struktur dan prosedur
estimasinya tetap berbeda. Koefisien HAR-RV dan pohon LightGBM sama-sama
diestimasi ulang setiap bulan, sedangkan \textit{hyperparameter} LightGBM
dituning sekali pada \textit{window} awal lalu dikunci
(Subbab~\ref{subsec:tuning}).
% CEK (Ferdi): retuning berkala belum dijalankan. Putuskan: jalankan sebagai
% sensitivitas, atau tulis sebagai keterbatasan di Bab V.
```

### 13. Amihud hanya di LGBM-X (audit 4.5)
**Bab II**, paragraf **H2b**, setelah `Karena itu H2b dirumuskan dua arah.`, tambahkan:
```latex
Karena log Amihud hanya dipakai pada LGBM-X, kontribusi fitur X pada HAR dan
pada LightGBM tidak dihitung dari himpunan fitur yang persis sama. Perbedaan
kontribusi antara keduanya tidak dapat sepenuhnya diatribusikan pada
algoritma.
```

### 14. Jumlah bulan regresi RQ2 (audit 4.6)
**Bab III**, ganti `Interpretasi bersifat asosiatif, bukan kausal.` dengan:
```latex
Periode evaluasi utama menyediakan hingga 97 bulan (September 2018 hingga
September 2026); jumlah bulan yang benar-benar masuk regresi setelah
\textit{differencing} dilaporkan pada Bab IV. Interpretasi bersifat
asosiatif, bukan kausal.
```

### 15. Status konfirmatori/eksploratori di tabel ringkasan (audit 4.7)
**Bab II**, Tabel `tab:ringkasan`:
1. Ubah spesifikasi kolom menjadi `{|p{0.18\textwidth}|c|p{0.36\textwidth}|p{0.2\textwidth}|}`.
2. Tambahkan kolom header keempat `\textbf{Eksploratori}`.
3. Isi kolom keempat per baris:
   - **RQ1:** `Uji berurutan $\sup F(\ell+1 \mid \ell)$; Fluctuation test; daya UDmax`
   - **RQ2:** `PSI deskriptif; Corwin--Schultz (sensitivitas)`
   - **RQ3:** `\textit{Window} 180, 730, 1.095, Tertunda-365; era \textit{transition}; skema S0`
4. Jangan ubah isi kolom "Uji konfirmatori".

## 3. Pemeriksaan sebelum lapor
1. Latar Belakang terdiri atas **tepat 8 paragraf** (P1–P8).
2. Jumlah `\cite` per key di Bab I: semuanya 1, kecuali `mokni2024`, `chassot2026`, dan `dudek2024` yang masing-masing 2. Di kalimat kutipan ulang, nama penulis tidak disebut.
3. RQ1–RQ3, H1/H2a/H2b/H3, uji konfirmatori, dan judul tidak berubah. Cek dengan `git diff` pada blok-blok tersebut.
4. Tidak ada angka hasil *out-of-sample* di Bab I–III.
5. Tidak ada kata "GOSS" atau "EFB" di Bab I.
6. Semua `\ref` (`tab:desain`, `tab:oos`, `subsec:tuning`, `eq:rata-rv`) berhasil di-*resolve*, tanpa "??" di PDF.
7. `make` dan `make check` lolos. Kegagalan karena font di mesin tanpa Times New Roman boleh diabaikan, tetapi tidak boleh ada *overfull box* di atas 3pt.
8. **Jangan commit/push.**

## 4. Format laporan ke Ferdi
```
Paragraf Latar Belakang: <n>
Kutipan ulang di Bab I: <daftar key dan jumlahnya>
Butir Bagian 2 yang diterapkan: <1–15, sebutkan yang gagal dan alasannya>
Blok terkunci berubah?: tidak / <rincian>
Halaman: <n>   Overfull > 3pt: <...>   Rujukan menggantung: <...>
% CEK baru: <lokasi>
% USUL (bila ada): <lokasi dan isi>
```
