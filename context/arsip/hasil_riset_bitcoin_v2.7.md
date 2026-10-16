# Riset Skripsi v2.7: Stabilitas Kinerja Relatif LightGBM terhadap HAR-RV dalam Peramalan *Realized Variance* Bitcoin

> **Status (13 Oktober 2026):** desain **terkunci dan sudah dieksekusi**. Eksperimen penuh selesai 6 Okt 2026 (config hash `0af5b5b98c60`); rincian hasil dan source code ada di `hasil_eksperimen_bitcoin_v2_5.md`. Praskripsi (Bab I–III) di LaTeX selesai sampai Bab III (repo `ferdiendahas/skripsi-latex`). **Seluruh referensi sudah dibaca** (F/WP/B); daftar perbaikan teks naskah ada di Lampiran A.
>
> **Aturan anti-HARKing:** uji konfirmatori sudah dijalankan, jadi RQ, hipotesis, uji konfirmatori, dan kandidat judul **tidak boleh diubah** mengikuti hasil. Perubahan setelah ini hanya boleh masuk sebagai eksploratori, sensitivitas, atau keterbatasan.
>
> **Aturan Bab I–III:** hasil *out-of-sample* (QLIKE rata-rata, ΔL, UDmax, p-value hipotesis, kurva window) tidak boleh muncul. Yang boleh: desain, deskripsi data, hasil di window awal (VIF, hyperparameter terkunci), dan perhitungan manual.
>
> **Notasi:** BTC/USDT = pasar spot (yang dipakai). BTCUSDT tanpa garis miring = perpetual; hanya muncul sebagai nama berkas arsip Binance.
>
> **Status baca referensi:** F = full text seluruhnya · WP = full text versi working paper/preprint · B = PDF, bagian relevan · M = metadata saja · ✗ = belum dicek. Kuartil = kuartil terbaik SCImago **SJR 2025** (dicek 10 Okt 2026), kecuali disebut lain.
>
> **Urutan otoritas bila bertentangan:** brief terbaru > dokumen ini (v2.7) > source code di `hasil_eksperimen` > versi lama dokumen riset. `KOREKSI.md` di repo sudah diserap ke dokumen ini; yang masih terbuka ada di Bagian XII.

---

## 0. Ringkasan Perubahan

### Update v2.7 (12–13 Okt 2026)

| Aspek | v2.6 | v2.7 | Dasar |
|---|---|---|---|
| Status baca | 4 F, 2 WP, 32 B, 5 M, 6 ✗ | **6 F, 2 WP, 43 B, 0 M, 0 ✗** + 3 sumber web | 15 PDF dibaca 12–13 Okt |
| Daftar pustaka | 50 entri `.bib` | **54**: + `pesaran2007`, `breiman2001`, `lightgbmfeatures`, `lightgbmtuning` | Dipakai di naskah tanpa sitasi asli |
| Klaim yang salah sitasi | — | **5 temuan:** (1) leaf-wise/overfitting dan gambar pohon bukan dari Ke dkk., melainkan dokumentasi LightGBM; (2) Grinsztajn: "kecil hingga menengah" → "menengah, ±10 ribu"; (3) klaim autoregresif bukan dari Pesaran & Timmermann (2007); (4) Feng, Zhang & Wang: "berpengaruh" → "berganti sepanjang waktu"; (5) DM: "dua model" → "dua ramalan" | Pembacaan PDF |
| Verifikasi kode vs paper | — | Abdi–Ranaldo, Corwin–Schultz, bandwidth Andrews: **sesuai** | Bagian III.4 |
| Preseden desain baru | — | Lag HAR **1/7/30** untuk kripto 24/7 (Qiu dkk., 2025); aturan differencing ADF+KPSS (Kwiatkowski dkk., 1992); koreksi bias & batas bawah (Christensen dkk., 2023) | III.4 |
| Temuan untuk Bab V | — | Grinsztajn membuang dataset yang bisa diselesaikan model linear; HAR tidak peka window (Feng, Zhang & Wang) | III.4, VII |
| Mendeley | — | Daftar perbaikan metadata (Lampiran B) | Screenshot 12 Okt |

### Update v2.6 (12 Okt 2026, ringkas)
Status dokumen jadi "terkunci & dieksekusi"; isi `KOREKSI.md` diserap ke Bagian V; uji konfirmatori per hipotesis; kuartil SJR 2025; checklist novelty (Chassot & Audrino, Feng/Qi/Lucey, Trucíos & Taylor) selesai; paper pembimbing disisihkan.

### Riwayat singkat
- **v1:** "Apakah ML mengalami degradasi saat pasar berubah?" (error absolut; trivial karena efek skala).
- **v2–v2.2:** reframing ke kinerja relatif (ΔL), desain 2×2, strategi pembaruan.
- **v2.3:** OOS ~Sep 2018, uji konfirmatori + Holm, justifikasi spot dan 5 menit.
- **v2.4:** UDmax sebagai uji konfirmatori, lag 1/7/30, proporsi RS⁻/RV, realized Amihud, Abdi-Ranaldo, KS, forward-chaining.
- **v2.5:** dua kandidat judul (≤ 15 kata), efisiensi vs keterramalan volatilitas, rantai argumen proxy.
- **Pilot → kelayakan → eksperimen penuh (Okt 2026):** lihat `hasil_eksperimen` §2.

---

## I. Posisi Riset

### Pertanyaan utama
Dalam meramal *realized variance* Bitcoin, **apakah kinerja relatif LightGBM terhadap HAR-RV stabil sepanjang waktu, atau berubah mengikuti kondisi pasar?** Jika berubah, karakteristik pasar apa yang berasosiasi dengannya, dan apakah strategi pembaruan model memengaruhinya?

### Kalimat inti
> "Saya menguji apakah kinerja LightGBM dibanding model sederhana HAR dalam meramal volatilitas Bitcoin itu stabil, atau berubah mengikuti kondisi pasar dan cara model diperbarui."

### Paper acuan: Dudek dkk. (2024), *Applied Soft Computing* (Q1)

| Aspek | Dudek dkk. (2024) | Riset ini |
|---|---|---|
| Hasil | Satu angka agregat 2019–2021 | Kestabilan kinerja relatif diuji sepanjang waktu (UDmax; Fluctuation test sebagai grafik) |
| Kondisi pasar | Error di 5% hari RV terendah/tertinggi, tanpa uji | Regresi ΔL pada karakteristik pasar dengan uji formal (RQ2) |
| Strategi window | Satu skema (rolling 23 bulan, latih ulang harian) | Static vs expanding vs rolling, antarera (RQ3) |
| Periode | Berakhir 2021 | Sep 2018 – Sep 2026, era transition dan institutional |
| Sumber keunggulan | Tidak dipisahkan | Dekomposisi 2×2 (non-linearitas vs informasi tambahan) |

**Acuan pendukung:**
- **Chassot & Audrino (2026)**, IJF (Q1): perlakuan window HAR menentukan hasil perbandingan ML vs HAR.
- **Christensen dkk. (2023)**, JFEC (Q1): rujukan utama ML vs HAR-RV.
- **Feng, Zhang & Wang (2024)**, J. Forecasting (Q2): rolling vs expanding untuk HAR; skema terbaik berganti sepanjang waktu.

Kalimat posisi: *"Penelitian ini memperluas Dudek dkk. (2024) dengan menguji apakah kinerja relatif LightGBM terhadap HAR-RV stabil sepanjang waktu, faktor pasar apa yang berasosiasi dengan perubahannya, serta bagaimana strategi pembaruan model memengaruhinya, dengan perlakuan window yang setara bagi HAR-RV (Chassot & Audrino, 2026)."*

### Kenapa framing ini kuat
1. **Menghindari temuan trivial.** Loss absolut naik saat volatilitas tinggi karena skala target. ΔL pada hari yang sama menetralkan efek ini, dan QLIKE homogen berderajat nol (Patton, 2011).
2. **Pertanyaan praktis jelas:** kapan model ML layak dipakai dibanding model sederhana, dan bagaimana memperbaruinya.
3. **Kontribusi Informatika:** rancangan evaluasi model ML pada data yang berubah, memadukan strategi pembaruan dari literatur concept drift dengan uji kestabilan dari ekonometrika (Suárez-Cetrulo dkk., 2023).
4. **Hasil negatif tetap valid** dan bisa dibela (Bagian VII).

### Yang TIDAK diklaim
- Tidak mengklaim *concept drift* atau *covariate shift* formal; yang diukur hanya pergeseran distribusi fitur (Moreno-Torres dkk., 2012).
- Tidak mengklaim menjelaskan mikrostruktur Bitcoin; semua variabel pasar diturunkan dari OHLCV.
- Tidak mengklaim kausalitas; RQ2 bersifat asosiatif.
- Tidak mengklaim memisahkan efek jumlah dan umur data latih (S1 vs S2 = efek gabungan; Tashman, 2000).
- Kesimpulan terbatas pada BTC/USDT spot Binance.

---

## II. Konsep Kunci

| Konsep | Pengertian | Peran |
|---|---|---|
| Realized variance (RV) | Σ kuadrat return 5 menit dalam satu hari UTC (288 return) | Target |
| HAR-RV | Regresi ln RV pada rata-rata RV 1, 7, 30 hari (Corsi, 2009; lag 7/30 untuk kripto 24/7: Qiu dkk., 2025) | Baseline |
| QLIKE | Loss robust terhadap proxy berisik, homogen derajat nol (Patton, 2011) | Metrik utama |
| ΔL | `ΔL_t = L_t(ML) − L_t(HAR)`; negatif = ML unggul | Objek analisis |
| D_t | `ΔL_t(S2-365) − ΔL_t(S1)`; positif = expanding lebih baik bagi ML | Objek uji H3 |
| Uji DM | H0: E[ΔL_t] = 0; berlaku untuk loss non-kuadratik dan asimetris (Diebold & Mariano, 1995) | Lanjutan H1 |
| Forecast instability | Kinerja relatif berubah sepanjang waktu (Rossi, 2013) | Fenomena yang diuji |
| UDmax | Uji Bai–Perron untuk 1 s.d. M perubahan rata-rata | Uji konfirmatori H1 |
| Fluctuation test | Statistik DM bergulir, nilai kritis Giacomini & Rossi (2010) | Grafik eksploratori |
| Forecast breakdown | Loss OOS signifikan lebih buruk dari in-sample (Giacomini & Rossi, 2009) | Pembeda konsep |
| Pergeseran distribusi fitur | Rata-rata statistik KS antarfitur antara window latih dan bulan uji (dipakai sebagai besaran, bukan keputusan uji) | Regresor RQ2 |
| Updating vs recalibration | Data baru tanpa estimasi ulang vs estimasi ulang (Tashman, 2000) | S0 vs S1/S2 |
| Prequential in blocks | Latih-uji bergantian per blok (Cerqueira dkk., 2020) | Kerangka S1/S2 |
| Uji konfirmatori | **Satu uji per hipotesis**, ditetapkan sebelum melihat hasil OOS | Mencegah temuan kebetulan |

**Istilah drift (kerangka Moreno-Torres):**

| Perubahan | Gama dkk. (2014) | Moreno-Torres dkk. (2012) |
|---|---|---|
| P(x) berubah | *Virtual drift* | *Covariate shift* (syarat P(y\|x) tetap) |
| P(y\|x) berubah | *Real concept drift* | *Concept shift* (syarat P(x) tetap) |

---

## III. Literatur

> **Aturan:** referensi metode/teori tanpa batas tahun; referensi gap 2021–2026. Klaim isi paper harus sesuai isi paper yang dibaca (Bagian III.4 dan Lampiran A).

**Ringkasan 54 entri (setelah 4 tambahan masuk `.bib`):**

| Status | Jumlah |
|---|---|
| F (full text seluruhnya) | 6 |
| WP (working paper) | 2 |
| B (PDF, bagian relevan) | 43 |
| Sumber web | 3 |
| **Total** | **54** |

| Jenis | Jumlah |
|---|---|
| Artikel jurnal | 45 (Q1: 37 · Q2: 6 · belum terverifikasi: 2 — Dickey & Fuller, Qiu) |
| Prosiding (NeurIPS, KDD) | 4 |
| Bab buku | 2 |
| Sumber web | 3 |

Q1 yang sudah dibaca dari PDF: **37**. Jangan menyebut "semua full text"; tulis "seluruh referensi telah ditelaah, sebagian pada bagian yang relevan".

### III.1 Referensi metode dan teori

**Volatilitas, pengukuran, fitur**

| Key `.bib` | Referensi | Status | Kuartil | Dipakai untuk |
|---|---|---|---|---|
| `andersen1998` | Andersen & Bollerslev (1998), IER 39(4), 885–905 | B | Q1 | RV intraday sebagai proxy |
| `corsi2009` | Corsi (2009), JFEC 7(2), 174–196 | WP (2004) | Q1 | HAR-RV |
| `liu2015` | Liu, Patton & Sheppard (2015), J. Econometrics 187(1), 293–311 | B | Q1 | RV 5 menit sulit dikalahkan |
| `parkinson1980` | Parkinson (1980), J. Business 53(1), 61–65 | F | Q1 (historis) | Fitur range |
| `barndorff2010` | Barndorff-Nielsen, Kinnebrock & Shephard (2010), bab buku OUP, hlm. 117–136 | WP (2008) | — | Definisi RS⁻ |
| `patton2015` | Patton & Sheppard (2015), REStat 97(3), 683–697 | B | Q1 | RS⁻ sebagai prediktor |
| `amihud2002` | Amihud (2002), JFM 5(1), 31–56 | B | Q1 | Definisi Amihud |
| `brauneis2021` | Brauneis dkk. (2021), JBF 124, 106041 | B | Q1 | Amihud untuk level, Abdi-Ranaldo untuk variasi waktu |
| `abdi2017` | Abdi & Ranaldo (2017), RFS 30(12), 4437–4480 | **B** (WP 2017) | Q1 | Proxy likuiditas RQ2; **rumus = kode ✅** |
| `corwin2012` | Corwin & Schultz (2012), J. Finance 67(2), 719–760 | **B** (WP ±2009) | Q1 | Sensitivitas likuiditas; **rumus = kode ✅** |

**Model ML**

| Key | Referensi | Status | Kuartil | Dipakai untuk |
|---|---|---|---|---|
| `ke2017` | Ke dkk. (2017), LightGBM, NeurIPS 30 | **F** | CORE A\* | Definisi LightGBM, GOSS, EFB; akurasi hampir sama dengan XGBoost |
| `chen2016` | Chen & Guestrin (2016), XGBoost, KDD | **B** | CORE A\* | Identitas XGBoost; regularisasi L2 bobot daun (`reg_lambda`) |
| `grinsztajn2022` | Grinsztajn, Oyallon & Varoquaux (2022), NeurIPS D&B | **B** | CORE A\* | Model pohon > deep learning pada data tabular menengah |
| `breiman2001` | **Breiman (2001)**, Machine Learning 45(1), 5–32, DOI 10.1023/A:1010933404324 | **B** | Q1 | Random Forest (sensitivitas) — **tambah ke `.bib`** |
| `lightgbmfeatures` | Dokumentasi LightGBM: *Features* (Microsoft Corporation) | web | — | Leaf-wise; sumber gambar pohon — **tambah ke `.bib`** |
| `lightgbmtuning` | Dokumentasi LightGBM: *Parameters Tuning* | web | — | `num_leaves`, `min_data_in_leaf` — **tambah ke `.bib`** |

**Metrik dan uji statistik**

| Key | Referensi | Status | Kuartil | Dipakai untuk |
|---|---|---|---|---|
| `patton2011` | Patton (2011), J. Econometrics 160(1), 246–256 | B | Q1 | QLIKE |
| `diebold1995` | Diebold & Mariano (1995), JBES 13(3), 253–263 | **B** (NBER WP 1994) | Q1 | Uji DM |
| `newey1987` | Newey & West (1987), Econometrica 55(3), 703–708 | B | Q1 | HAC |
| `andrews1991` | Andrews (1991), Econometrica 59(3), 817–858 | **B** (Cowles DP 877R) | Q1 | Bandwidth HAC otomatis; **rumus = kode ✅** |
| `giacomini2009` | Giacomini & Rossi (2009), REStud 76(2), 669–705 | B | Q1 | Konsep breakdown |
| `giacomini2010` | Giacomini & Rossi (2010), JAE 25(4), 595–620 | B | Q1 | Fluctuation test; syarat rolling/fixed |
| `rossi2013` | Rossi (2013), Handbook of Economic Forecasting vol. 2, 1203–1324 | B (bab buku) | — | Survei instabilitas |
| `martins2016` | Martins & Perron (2016), JTSA 37(5), 650–659 | B | Q1 | Dasar UDmax pada ΔL |
| `bai1998` | Bai & Perron (1998), Econometrica 66(1), 47–78 | B | Q1 | UDmax |
| `bai2003` | Bai & Perron (2003), JAE 18(1), 1–22 | B | Q1 | UDmax lalu uji berurutan |
| `holm1979` | Holm (1979), Scand. J. Statistics 6(2), 65–70 | B | **Q2** | Koreksi uji berganda |
| `dickey1979` | Dickey & Fuller (1979), JASA 74(366a), 427–431 | **B** | belum dicek | Uji akar unit |
| `kwiatkowski1992` | Kwiatkowski dkk. (1992), J. Econometrics 54, 159–178 | **B** (Cowles DP 979) | Q1 | Uji KPSS; dasar aturan differencing |
| `pesaran2007` | **Pesaran & Timmermann (2007)**, J. Econometrics 137(1), 134–161, DOI 10.1016/j.jeconom.2006.03.010 | **B** (versi 2006) | Q1 | Dasar H3 — **tambah ke `.bib`** |

**Evaluasi dan adaptasi model**

| Key | Referensi | Status | Kuartil | Dipakai untuk |
|---|---|---|---|---|
| `tashman2000` | Tashman (2000), IJF 16(4), 437–450 | B | Q1 | Updating vs recalibration |
| `cerqueira2020` | Cerqueira dkk. (2020), Machine Learning 109, 1997–2028 | B | Q1 | Forward-chaining |
| `gama2014` | Gama dkk. (2014), ACM CSUR 46(4), Art. 44 | F | Q1 | Taksonomi window |
| `zliobaite2015` | Žliobaitė dkk. (2015), Neurocomputing 150, 240–249 | B | Q1 | S0 sebagai pembanding |
| `morenotorres2012` | Moreno-Torres dkk. (2012), Pattern Recognition 45, 521–530 | B | Q1 | Definisi dataset shift |
| `rabanser2019` | Rabanser, Günnemann & Lipton (2019), NeurIPS 32 | **B** | CORE A\* | Uji KS per fitur |
| `suarez2023` | Suárez-Cetrulo dkk. (2023), ESWA 213, 118934 | F | Q1 (SJR 2024) | Recurring drift |

### III.2 Referensi gap (2021–2026)

**Pilar A — Evolusi pasar Bitcoin**

| Key | Referensi | Status | Kuartil | Kegunaan |
|---|---|---|---|---|
| `do2026` | Do (2026), Borsa Istanbul Review 26, 100869 | F | Q1 | Batas era; persistensi RV per era |
| `mokni2024` | Mokni dkk. (2024), Financial Innovation 10, 39 | B | Q1 | Efisiensi berganti |
| `yi2023` | Yi dkk. (2023), Scientific Reports 13, 4789 | B | Q1 | Efisiensi return |
| `zhang2024` | Zhang dkk. (2024), Financial Innovation 10, 3 | B | Q1 | Proxy likuiditas kripto |
| `nakamoto2008` | Nakamoto (2008), white paper | web | — | Pengenalan Bitcoin |

**Pilar B — Regime**

| Key | Referensi | Status | Kuartil | Kegunaan |
|---|---|---|---|---|
| `agakishiev2025` | Agakishiev dkk. (2025), Digital Finance 7, 107–131 | B | Q2 | Manfaat regime hilang di data uji |
| `oprea2026` | Oprea & Bâra (2026), Computational Economics | B | Q2 | Target harga, tanpa HAR |

**Pilar C — ML untuk volatilitas**

| Key | Referensi | Status | Kuartil | Kegunaan |
|---|---|---|---|---|
| `dudek2024` | **Dudek dkk. (2024)**, Applied Soft Computing 151, 111132 | B | Q1 | **Paper acuan** |
| `huang2024` | Huang dkk. (2024), JIFMIM 97, 102064 | B | Q1 | LSTM unggul tipis; HAR lebih baik saat lonjakan |
| `wang2023` | Wang dkk. (2023), IRFA 90, 102914 | B | Q1 | Prediktor internal terpenting |
| `christensen2023` | Christensen, Siggaard & Veliyev (2023), JFEC 21(5), 1680–1727 | B (arXiv) | Q1 | Rujukan utama ML vs HAR |
| `feng2024ml` | Feng, Qi & Lucey (2024), IRFA 94, 103239 | B | Q1 | Tuning harian; menyarankan LightGBM |
| `qiu2025` | Qiu, Qu, Shi & Xie (2025), Economic Modelling 144, 106986 | **B** | belum terverifikasi | Kombinasi ramalan > model tunggal; **lag 1/7/30 untuk kripto 24/7** |

**Pilar D — Uji instabilitas di kripto**

| Key | Referensi | Status | Kuartil | Kegunaan |
|---|---|---|---|---|
| `trucios2023` | Trucíos & Taylor (2023), J. Forecasting 42(4), 989–1007 | B | Q2 | Fluctuation test untuk VaR/ES kripto |

**Pilar E — Window training**

| Key | Referensi | Status | Kuartil | Kegunaan |
|---|---|---|---|---|
| `chassot2026` | Chassot & Audrino (2026), IJF 42(2), 330–343 | B | Q1 | Skema fitting HAR menentukan hasil |
| `akgun2025` | Akgun & Gulay (2025), Computational Economics 65, 3971–4013 | B | Q2 | Rolling vs expanding (GARCH) |
| `feng2024window` | Feng, Zhang & Wang (2024), J. Forecasting 43(3), 567–582 | **F** | Q2 | Dasar RQ3 |

### III.3 Tidak dipakai (di luar `.bib`)

| Referensi | Alasan |
|---|---|
| Al-Yahyaee dkk. (2020); Teller dkk. (2026) | Tidak dikutip (Teller sisa topik HYPE). Hapus dari Mendeley atau pisahkan collection |
| Berger & Koubová (2024); Arora dkk. (2024); Di-Giorgi dkk. (2025); Catania & Grassi (2022); Souto & Moradi (2024); Lima dkk. (2022); Bakirov dkk. (2021); Andrews (1993); Hansen, Lunde & Nason (2011); Inoue & Rossi (2012) | Tidak dibutuhkan argumen |
| Quiñonero-Candela dkk. (2009); preprint arXiv 2607.05291 | Hanya resensi / belum terbit |
| Paper Parlika dkk. (JOIV ×2; Sisfokom 2026, Sinta 3) | Disisihkan sampai pembimbing setuju |
| Said & Dickey (1984), Biometrika | Opsional: sumber asli versi *augmented* DF yang dipakai `adfuller(autolag="AIC")` |
| Friedman (2001) | Opsional: sumber asli persamaan GBDT di Bab II |

### III.4 Temuan paper (dibaca 10–13 Okt 2026)

**Chassot & Audrino (2026), IJF.** 1.445 saham AS 2015–2023; HAR rolling 630 hari re-estimasi harian vs ML window statis. ML gagal mengalahkan HAR yang di-fitting tepat; frekuensi re-estimasi > panjang window; optimum 2,5–4 tahun. Novelty aman (bukan kripto, perlakuan window tidak simetris, tanpa antarera).

**Feng, Qi & Lucey (2024), IRFA.** BTC/USD 2017–2022, RV 5 menit, HAR-RV benchmark vs Lasso/Ridge/EN; tuning harian lebih baik; kepentingan **indikator blockchain** naik sejak Okt 2022; rolling/expanding hanya robustness; menyarankan LightGBM. Novelty aman.

**Trucíos & Taylor (2023), J. Forecasting.** BTC/ETH harian Binance 17 Agu 2017–Jul 2022; VaR/ES model ekonometrik; Fluctuation test sebagian besar tidak signifikan. Novelty aman.

**Giacomini & Rossi (2010), JAE.** Fluctuation test = DM/GW bergulir, H0 sama akurat di setiap titik; kerangka GW mensyaratkan **rolling/fixed**; nilai kritis hanya α 0,05/0,10; LM2 = uji sup perubahan rata-rata (mendukung UDmax).

**Christensen, Siggaard & Veliyev (2023), JFEC.** 29 saham DJIA 2001–2017; satu split 70/10/20; hanya MSE. Dengan input HAR saja, model pohon **tidak** mengalahkan HAR (RF 1,020; GB 1,054). Dengan 9 prediktor tambahan, RF unggul ~10%. GB terlemah karena peka outlier. Peringkat model berubah dengan panjang data latih (Lampiran A.1 paper). Preseden: koreksi bias exp(ŷ + ½var), batas bawah ramalan, validasi tanpa k-fold.

**Ke dkk. (2017), NeurIPS — F.** Kontribusi baru hanya GOSS dan EFB (algoritme histogram sudah ada sebelumnya). Eksperimen pada data 2–119 juta baris, klasifikasi/ranking; akurasi **hampir sama** dengan XGBoost; leaf-wise hanya disebut satu kalimat (merujuk Shi, 2007). **Tidak memuat** klaim "leaf-wise rentan overfitting di data kecil" dan **tidak punya** gambar leaf-wise vs level-wise → keduanya dari dokumentasi LightGBM. Implementasi penelitian ini memakai boosting standar + bagging 80% (bukan GOSS); EFB tidak berperan (9 fitur padat); dengan `num_leaves` = 3, beda leaf-wise vs level-wise praktis hilang.

**Dokumentasi LightGBM (versi "latest" 4.7.0.99; kutip versi yang sama dengan `.venv`).** *Features:* pada jumlah daun yang sama leaf-wise umumnya mencapai loss lebih rendah, tetapi dapat overfitting pada data kecil. *Parameters Tuning:* leaf-wise konvergen lebih cepat; `num_leaves` dan `min_data_in_leaf` parameter utama pencegah overfitting.

**Feng, Zhang & Wang (2024), J. Forecasting — F.** RV 5 menit S&P 500 (Oxford-Man) 2000–2022, OOS 2.500 hari; **HAR saja**, rolling vs expanding; strategi MoP memilih window berdasarkan kinerja k hari terakhir. Rata-rata rolling ≈ expanding; skema terbaik **berganti sepanjang waktu tetapi persisten**; saat resesi expanding sedikit lebih baik. ⚠ Besaran keunggulan MoP sulit dijelaskan (loss MoP jauh di bawah kedua komponen); kutip temuan kualitatif saja. Novelty aman (tanpa ML, tanpa era, tanpa uji formal beda skema).

**Grinsztajn dkk. (2022), NeurIPS.** 45 dataset; model pohon (RF, GBT, XGBoost; **LightGBM tidak diuji**) > deep learning pada data **menengah (±10 ribu)** di semua anggaran tuning. Kriteria: dataset < 3.000 sampel dibuang; hanya data i.i.d. (deret waktu dibuang); **dataset dibuang bila model linear selisih < 5% dari model non-linear**. Implikasi: klaim "kecil hingga menengah" salah; paper ini membuktikan pohon > deep learning, **bukan** pohon > model linear.

**Abdi & Ranaldo (2017), versi WP.** Log-harga; mid-range η = (ln H + ln L)/2; versi *two-day corrected*: ŝ_t = √max{4(c_t − η_t)(c_t − η_{t+1}), 0}, lalu rata-rata bulanan; buang periode dua hari dengan hari tanpa perdagangan/range nol. **Kode sesuai**; satu beda kecil: 27 hari bar tidak lengkap ikut masuk perhitungan likuiditas (opsional ditulis di keterbatasan). Jangan menyebut nomor persamaan paper (WP vs terbit bisa beda).

**Corwin & Schultz (2012), versi WP.** β = jumlah dua [ln(H/L)]² harian; γ = [ln(H/L)]² dua hari; α = (√(2β) − √β)/(3 − 2√2) − √(γ/(3 − 2√2)); S = 2(e^α − 1)/(1 + e^α); spread dua hari negatif → 0 lalu rata-rata bulanan. **Kode sesuai.** Penyesuaian overnight tidak perlu (BTC 24/7).

**Rabanser, Günnemann & Lipton (2019), NeurIPS.** Deteksi dataset shift (data gambar, deep learning); uji KS per dimensi + Bonferroni sebagai "simple baseline" dengan kinerja sebanding uji multivariat; juga pada fitur asli (NoRed). Penelitian ini memakai **rata-rata statistik D** sebagai besaran, bukan p-value — tulis sebagai pilihan desain sendiri.

**Diebold & Mariano (1995), NBER WP 1994.** H0 akurasi sama ⇔ E[d_t] = 0; S₁ = d̄ / √(2π f̂_d(0)/T) ~ N(0,1); loss **tidak harus kuadratik, simetris, atau kontinu**; error boleh tidak normal, berautokorelasi, dan berkorelasi antarmodel; menyebut Bartlett (Newey–West) dan bandwidth Andrews (1991) sebagai pilihan sah. Membandingkan **ramalan**, bukan model.

**Chen & Guestrin (2016), KDD.** Kontribusi: skalabilitas (sparsity-aware, weighted quantile sketch, cache/out-of-core). Objektif teregularisasi: penalti jumlah daun (γ) dan L2 bobot daun (λ) + shrinkage + subsampling kolom. Tidak membandingkan dengan LightGBM (terbit lebih dulu).

**Breiman (2001), Machine Learning.** Random Forest = rata-rata pohon dengan vektor acak independen; pemilihan fitur acak di atas bagging; error konvergen seiring jumlah pohon (menambah pohon tidak overfit); error hutan ≤ ρ × error pohon. **Setelan 300 pohon, min 20 per daun, 33% fitur bukan dari paper** — keputusan desain di `config.py`.

**Pesaran & Timmermann (2007), versi Jan 2006.** Menyertakan data pre-break menambah bias tetapi dapat menurunkan varians error ramalan; sering kali optimal memakai sebagian data pre-break selama perubahan tidak terlalu besar; bila perubahan besar, hanya data post-break; perubahan kecil → kombinasi window. Asumsi regresor eksogen ketat. **Kasus autoregresif ada di Pesaran & Timmermann (2005)**, bukan paper ini.

**Kwiatkowski, Phillips & Schmidt (1992), Cowles DP 979.** Uji DF berdaya rendah; KPSS membalik H0 menjadi stasioner (varians komponen random walk = 0). Menjalankan keduanya: **"terima akar unit (ADF) dan tolak stasioneritas (KPSS) = ditemukan akar unit"** — persis aturan differencing RQ2.

**Andrews (1991), Cowles DP 877R.** Bandwidth otomatis plug-in dengan AR(1) per komponen; Bartlett: Ŝ_T = 1,1447 (α̂(1)T)^(1/3) (Pers. 6.2), α̂(1) Pers. 6.4; bobot intersep 0. **Kode `andrews_bw` sesuai.** Penulis merekomendasikan kernel QS; Bartlett asimtotik kurang efisien, tetapi di sampel terbatas tidak selalu jauh tertinggal.

**Dickey & Fuller (1979), JASA.** Y_t = ρY_{t−1} + e_t, H0 ρ = 1; H0 ini **setara dengan "deret sebaiknya di-differencing"**; distribusi tidak standar (tabel khusus); varian dengan intersep/tren. Kode memakai versi *augmented* (lag selisih, `autolag="AIC"`).

**Qiu, Qu, Shi & Xie (2025), Economic Modelling.** 10 aset kripto Binance 5 menit, mulai 2018–2019 s.d. 30 Agu 2021; 7 varian HAR + 2 rough volatility + 7 metode kombinasi; ℓ2-relaxation terbaik di 23/30 kasus; rolling (robustness recursive); **lag HAR 1/7/30 karena kripto 24/7**; QLIKE tidak dipakai karena ada ramalan RV negatif (riset ini tidak punya masalah itu: model pada ln RV + batas bawah). Motivasi: model berspesifikasi tetap tidak selalu berlaku universal.

### III.5 Sintesis literatur

1. Karakteristik pasar Bitcoin berubah substansial (Do, 2026), tapi tidak mulus: efisiensi naik-turun (Mokni dkk., 2024) dan regime bisa berulang (Suárez-Cetrulo dkk., 2023). **Bukan kontribusi.**
2. ML vs HAR untuk volatilitas sudah banyak, hampir semuanya satu periode uji dan hasil agregat (Christensen dkk., 2023; Huang dkk., 2024; Wang dkk., 2023; Dudek dkk., 2024; Feng, Qi & Lucey, 2024; Qiu dkk., 2025). Dengan input HAR saja, model pohon tidak mengalahkan HAR (Christensen dkk., 2023). **Benchmarking saja bukan kontribusi.**
3. Kinerja relatif berubah antarperiode uji sudah dikenal (Tashman, 2000; Gama dkk., 2014); peringkat model bergantung pada periode uji (Christensen dkk., 2023). Alat ujinya ada (Giacomini & Rossi, 2010; Martins & Perron, 2016; Rossi, 2013) dan sudah dipakai di kripto untuk VaR/ES (Trucíos & Taylor, 2023). **Menerapkan uji saja bukan kontribusi.**
4. Pilihan window dan frekuensi re-estimasi berpengaruh (Akgun & Gulay, 2025; Chassot & Audrino, 2026); skema terbaik berganti sepanjang waktu (Feng, Zhang & Wang, 2024); data pre-break sering kali tetap berguna (Pesaran & Timmermann, 2007). **"Window berpengaruh" bukan kontribusi.**
5. Kepentingan fitur tidak stabil antarstudi dan antarperiode (Wang dkk., 2023 vs Feng, Qi & Lucey, 2024).
6. **Efisiensi return ≠ volatilitas tak teramalkan** (Corsi, 2009).
7. **Rantai proxy dan loss:** Andersen & Bollerslev (1998) → QLIKE (Patton, 2011) → RV 5 menit (Liu dkk., 2015); DM sah untuk loss asimetris seperti QLIKE (Diebold & Mariano, 1995).
8. **Keunggulan model pohon pada data tabular** ditunjukkan relatif terhadap deep learning, pada dataset yang sengaja tidak bisa diselesaikan model linear (Grinsztajn dkk., 2022) — jadi tidak menjamin keunggulan atas HAR.
9. **Celah:** gabungan (a) uji kestabilan kinerja relatif ML terhadap HAR-RV pada RV Bitcoin lintas era, (b) dekomposisi 2×2, (c) asosiasi dengan karakteristik pasar dan pergeseran distribusi fitur, (d) interaksi strategi pembaruan × era, dengan perlakuan window setara untuk HAR-RV.

---

## IV. Research Gap

Penelitian peramalan volatilitas Bitcoin umumnya melaporkan kinerja ML terhadap HAR sebagai satu hasil agregat untuk satu periode uji. Padahal literatur *forecasting under instability* menunjukkan rata-rata dapat menyembunyikan perubahan kinerja relatif, dan pasar Bitcoin berubah substansial. **Sejauh literatur yang diperiksa**, belum ditemukan penelitian yang (1) menguji kestabilan kinerja relatif ML terhadap HAR secara formal pada periode panjang lintas era pasar; (2) mengaitkannya dengan karakteristik pasar terukur; dan (3) mengevaluasi pengaruh strategi pembaruan model antarera dengan perlakuan window setara.

**Checklist novelty: selesai (semua dari PDF).**

| Paper | Hasil | Yang wajib diakui |
|---|---|---|
| Akgun & Gulay (2025) | Aman | Rolling vs expanding pada BTC sudah ada (rinci untuk GARCH) |
| Chassot & Audrino (2026) | Aman | Skema fitting HAR menentukan hasil |
| Feng, Qi & Lucey (2024) | Aman | Rolling/expanding sebagai robustness; kepentingan fitur berubah waktu |
| Trucíos & Taylor (2023) | Aman | Fluctuation test sudah dipakai di kripto (VaR/ES) |
| Christensen dkk. (2023) | Aman | Peringkat ML vs HAR bergantung prediktor dan periode uji, tanpa uji formal |
| Feng, Zhang & Wang (2024) | Aman | Skema terbaik HAR berganti sepanjang waktu; tanpa ML, tanpa era |
| Qiu dkk. (2025) | Aman | Kombinasi ramalan HAR/rough volatility di 10 kripto; tanpa ML pohon, tanpa uji kestabilan |

---

## V. Rancangan Penelitian (seperti diimplementasikan)

> Bagian ini mengikuti kode final (`rvlib/`, config hash `0af5b5b98c60`).

### 1. Data

| Komponen | Keputusan |
|---|---|
| Sumber | Binance Public Data (data.binance.vision), arsip bulanan klines, checksum diverifikasi |
| Pair | BTC/USDT spot (berkas `BTCUSDT`, folder `spot`) |
| Resolusi | 5 menit (288 bar per hari UTC) |
| Periode | **17 Agu 2017 – 30 Sep 2026**: 957.865 bar, 3.332 hari (tanggal mulai Binance juga dipakai Trucíos & Taylor, 2023) |
| OOS | Mulai **1 Sep 2018** (S0/S1/S2-365): 2.914 hari (transition 829, institutional 2.085) |
| Volume dolar | *Quote asset volume* (USDT) |

**Kenapa spot:** histori sejak 2017 (perpetual ~Sep 2019); tanpa efek funding/likuidasi/basis; keterbandingan literatur. **Kenapa 5 menit:** kompromi noise vs presisi (Andersen & Bollerslev, 1998; Liu dkk., 2015); preseden kripto 5 menit: Dudek dkk. (2024), Feng, Qi & Lucey (2024), Qiu dkk. (2025, Binance). **Kelebihan:** satu venue sepanjang periode.

**Audit (sesuai kode):** timestamp **mikrodetik → milidetik** (arsip sejak 1 Jan 2025); hari bar < 95% (< 274/288) ditandai (**27 hari**); pasangan (t, t+1) dibuang bila t atau t+1 tidak lengkap atau RV = 0, tanpa interpolasi; hari ekstrem dipertahankan; bar volume nol dikecualikan dari Amihud; **5 penanda peristiwa:** crash Mar 2020, Terra (Mei 2022), FTX (Nov 2022), flash crash 17 Agu 2023, "10/10" (10 Okt 2025); batas era 1 Jan 2021.

### 2. Target
`RV_t = Σ_{i=1}^{288} r²_{t,i}` (realized **variance**); target `RV_{t+1}`; model dilatih pada `ln RV`.
- **Koreksi bias:** `exp(ŷ + σ̂²/2)`, σ̂² dari residual 20% akhir window latih (model dilatih di 80% awal), lalu dilatih ulang di seluruh window. Preseden: Christensen dkk. (2023). Sensitivitas: tanpa koreksi.
- **Batas bawah ramalan:** persentil ke-1 RV window latih (preseden serupa: RV minimum in-sample di Christensen dkk., 2023).

### 3. Fitur

| Kelompok | Fitur | Dipakai oleh |
|---|---|---|
| HAR | `ln RV_d`, `ln RV_w`, `ln RV_m` (1, 7, 30 hari; sensitivitas 1/5/22). **Preseden lag 1/7/30 untuk kripto 24/7: Qiu dkk. (2025)** | Semua |
| X | Proporsi RS⁻/RV; return harian; log volume dolar; Δ log volume; log range Parkinson | HAR-X, LGBM-X |
| X | Log realized Amihud | **LGBM-X saja** (VIF window awal 19,6) |

### 4. Model: desain 2×2

| | Input HAR | Input HAR + X |
|---|---|---|
| **Linear (OLS)** | HAR (baseline) | HAR-X |
| **Non-linear (LightGBM)** | LGBM-HAR | LGBM-X |

Ditambah naive (sanity check) dan Random Forest (Breiman, 2001; input LGBM-X; 300 pohon, min 20 per daun, 33% fitur — setelan desain) **hanya sebagai sensitivitas**.

**Implementasi LightGBM:** objective regresi kuadrat, boosting standar (gbdt) + **bagging 80% per pohon** sebagai regularisasi; **GOSS tidak dipakai**, EFB tidak berperan (9 fitur padat). Dengan `num_leaves` = 3, setiap pohon hanya punya dua pemecahan, sehingga beda leaf-wise vs level-wise praktis hilang.

**Kenapa LightGBM:**
1. Model pohon > deep learning pada data tabular menengah (Grinsztajn dkk., 2022) — dasar pemilihan kelas model, bukan jaminan kinerja (data latih 365–±2.900 baris, deret waktu).
2. Akurasi hampir sama dengan XGBoost (Ke dkk., 2017; Chen & Guestrin, 2016).
3. Arahan pembimbing (ML non-deep).
4. Disarankan Feng, Qi & Lucey (2024).

Kecepatan bukan alasan. Antisipasi: gradient boosting peka outlier (Christensen dkk., 2023); model pohon meremehkan volatilitas ekstrem (Dudek dkk., 2024); transformasi log mengurangi masalah ini.

### 5. Tuning
- Hanya window awal (target < 1 Sep 2018; ±339 observasi), forward-chaining 5 fold, QLIKE pada exp(ŷ).
- Grid: num_leaves {3, 7, 15}, min_child_samples {10, 20, 40, 80}, n_estimators {50, 100, 300, 600}, lr 0,03, reg_lambda {1, 10} (penalti L2 bobot daun; Chen & Guestrin, 2016); perluasan tepi maks. 2 kali; batas bawah min_child_samples 5.
- **Terkunci:** LGBM-HAR: leaves 3, min_child 10, n_est 300, lr 0,03, λ 1. LGBM-X: leaves 3, min_child **5 (batas bawah)**, n_est 300, lr 0,03, λ 1.
- Tidak ada scaler/standarisasi.

### 6. Strategi pembaruan (latih ulang bulanan)

| Kode | Strategi | Istilah literatur |
|---|---|---|
| S0 | Static | Updating tanpa rekalibrasi (Tashman, 2000); Žliobaitė dkk. (2015) |
| S1 | Expanding | Landmark window (Gama dkk., 2014) |
| S2 | Rolling W ∈ {365, 730}; eksploratori 180, 1095, rolling tertunda | Sliding window |

Perlakuan setara untuk HAR (Chassot & Audrino, 2026); uji formal di S2 (Giacomini & Rossi, 2010; Rossi, 2013; Tashman, 2000).

### 7. Evaluasi
- **Loss:** QLIKE (utama), MSE (pelengkap).
- **HAC:** Bartlett + bandwidth otomatis Andrews (1991), replika `sandwich::kernHAC(prewhite=FALSE)`, identik dengan R.

| Hipotesis | Uji konfirmatori |
|---|---|
| H1 | UDmax rata-rata ΔL(LGBM-X − HAR), S2-365, QLIKE, HAC, ε 0,15, M 5; nilai kritis disimulasikan (CV 5% 9,01). Bila tidak menolak → DM |
| H2a | Uji-F bersama HAC, regresi ΔL bulanan pada 4 karakteristik (+ dummy era) |
| H2b | Dua uji-t HAC beda era kontribusi fitur X; Holm |
| H3 | Uji-t HAC dua sisi rata-rata D_t, era institutional |

**Variabel RQ2:** rata-rata ln RV; SD ln RV; spread Abdi–Ranaldo *two-day corrected* rata-rata bulanan (sensitivitas Corwin–Schultz); rata-rata D^KS (PSI deskriptif). **Stasioneritas:** differencing bila ADF gagal menolak **dan** KPSS menolak = kombinasi "ditemukan akar unit" (Kwiatkowski dkk., 1992; Dickey & Fuller, 1979).

**Sensitivitas belum dijalankan:** RV 5 menit subsampled; retuning tahunan → jalankan atau tulis keterbatasan.

### 8. Kontrol leakage
Fitur t hanya data s.d. akhir t; tuning hanya window awal; σ̂² dan batas bawah dari window latih; batas era bukan fitur; pasangan konfirmatori tidak dilihat saat pilot.

---

## VI. Rumusan Masalah, Tujuan, Hipotesis (terkunci)

| | Rumusan masalah | Hipotesis |
|---|---|---|
| RQ1 | Sejauh mana kinerja relatif LightGBM terhadap HAR-RV stabil sepanjang periode pengujian? | H1: rata-rata ΔL(LGBM-X − HAR) tidak konstan |
| RQ2 | Apakah variasinya berasosiasi dengan karakteristik pasar dan pergeseran distribusi fitur? | H2a: ΔL berasosiasi dengan ≥1 karakteristik. H2b: kontribusi fitur X berbeda antarera |
| RQ3 | Apakah strategi pembaruan dan panjang window memengaruhi kinerja relatif secara berbeda antarera? | H3: di era institutional, rolling > expanding bagi ML (rata-rata D_t < 0) |

**Dasar H3:** trade-off bias–varians (Pesaran & Timmermann, 2007; Rossi, 2013); persistensi RV berubah antarera (Do, 2026). **Hipotesis tandingan:** data pre-break sering kali tetap berguna (Pesaran & Timmermann, 2007); untuk model autoregresif dapat menurunkan bias dan varians sekaligus (Pesaran & Timmermann, 2005, via Rossi, 2013); regime berulang (Gama dkk., 2014; Suárez-Cetrulo dkk., 2023).

---

## VII. Status Eksekusi dan Ringkasan Hasil

> **Tidak untuk Bab I–III.** Rincian di `hasil_eksperimen_bitcoin_v2_5.md`.

**Sanity (QLIKE, S2-365):** Naive 0,5293 · HAR **0,3592** · HAR-X 0,3627 · LGBM-HAR 0,3968 · LGBM-X 0,3761.

| Hipotesis | Hasil | Rumusan Bab IV |
|---|---|---|
| H1 | UDmax 4,78 (CV 9,01), p 0,37; 0 break; DM mean ΔL +0,0169, p 0,25 | Tidak didukung; tidak ada bukti perubahan; daya memadai hanya untuk pergeseran ≥ ~1–2 sd |
| H2a | F 0,81, p 0,52 (CS p 0,47) | Tidak didukung |
| H2b | p Holm 0,53 | Tidak didukung |
| H3 | Mean D +0,0241, t 2,37, p 0,018 | **Tidak didukung; arah sebaliknya signifikan (expanding lebih baik).** Jangan tulis "H3 ditolak" |

Eksploratori kunci: S0 memburuk tajam (retraining wajib); efek RQ3 bertahan tanpa 20 hari ekstrem; **tidak bertahan dengan MSE**; kurva window monoton (makin panjang makin baik bagi LGBM-X); loss HAR datar di semua window.

**Hubungan dengan literatur untuk Bab V:**

| Temuan | Pembanding |
|---|---|
| LGBM-HAR kalah dari HAR | Christensen dkk. (2023): pohon dengan input HAR saja tidak mengalahkan HAR. Grinsztajn dkk. (2022): bukti keunggulan pohon hanya vs deep learning, pada data yang tidak bisa diselesaikan model linear |
| Kekalahan LightGBM saat lonjakan | GB peka outlier (Christensen dkk., 2023); QLIKE menghukum under-forecast (Patton, 2011) |
| Expanding > rolling-365 bagi LightGBM | Pesaran & Timmermann (2007): data pre-break sering tetap berguna; Chassot & Audrino (2026): window lebih panjang lebih baik |
| HAR tidak peka panjang window | Feng, Zhang & Wang (2024): rata-rata rolling ≈ expanding untuk HAR. Kontras linear vs non-linear = temuan yang bisa ditonjolkan |
| H1 tidak menolak | Trucíos & Taylor (2023): Fluctuation test BTC sebagian besar tidak signifikan (konteks berbeda) |

---

## VIII. Ide Tambahan

| No | Ide | Status |
|---|---|---|
| 1 | Kurva panjang window | ✅ Eksploratori |
| 2 | Rolling tertunda | ✅ Eksploratori |
| 3 | Early warning pergeseran fitur | Belum |
| 4 | Replikasi ETH/USDT spot | Belum — tambahan termurah bila paper diincar Q2 |
| 5 | Horizon 5/22 hari | Belum (keunggulan ML membesar di horizon panjang: Christensen dkk., 2023) |
| 6 | Kombinasi ramalan rolling+expanding / switching | Belum (Feng, Zhang & Wang, 2024; Qiu dkk., 2025) |
| 7 | Dashboard pemantauan | Tergantung arahan pembimbing |
| 8 | Fluctuation μ = 0,1; HAR WLS | Opsional |

---

## IX. Risiko dan Mitigasi

| Risiko | Mitigasi |
|---|---|
| "ML tidak unggul, apa kontribusinya?" | Hasil negatif valid; kontribusi pada uji kestabilan, dekomposisi, strategi pembaruan; sejalan Christensen dkk. (input HAR saja) dan Chassot & Audrino |
| "UDmax tidak menolak = stabil?" | Tidak; "tidak ditemukan bukti perubahan" + analisis daya |
| RQ3 hanya di QLIKE | Wajib disebut; QLIKE (kesalahan relatif, hari tenang) vs MSE (didominasi lonjakan) |
| "Kenapa bisa pakai QLIKE padahal Qiu dkk. tidak?" | Model dilatih pada ln RV + batas bawah → ramalan selalu positif |
| "Andrews merekomendasikan QS, kenapa Bartlett?" | Bartlett = Newey–West, kovarians dijamin non-negatif, paling umum; disebut sah oleh Diebold & Mariano; di sampel terbatas tidak selalu jauh tertinggal (Andrews, 1991) |
| "Kenapa bagging, bukan GOSS?" | GOSS untuk mempercepat data besar; data latih ratusan–ribuan baris; bagging sebagai regularisasi |
| "Grinsztajn untuk data ≥3.000 i.i.d., data Anda deret waktu kecil" | Dipakai sebagai dasar kelas model, bukan jaminan kinerja; ditulis eksplisit di Bab II |
| Hyperparameter terkunci (Feng, Qi & Lucey memakai tuning harian) | Kestabilan sebuah metode hanya terukur bila setelannya tetap |
| min_child_samples LGBM-X di batas bawah | Keputusan desain; sebut terbuka |
| Koreksi bias mungkin merugikan LightGBM | Tanpa koreksi ΔL turun ke +0,004; satu paragraf keadilan prosedur |
| **Sumber data: tugas pembimbing cron Indodax vs arsip Binance** | **Klarifikasi di bimbingan**: cron hanya maju ke depan, tidak mencakup 2017–2026 |
| Judul belum final | Kandidat 1 sementara |

---

## X. Kandidat Judul (tidak berubah)

| No | Judul | Kata |
|---|---|---|
| 1 | Analisis Stabilitas Kinerja Relatif LightGBM terhadap HAR-RV dalam Peramalan *Realized Variance* Bitcoin | 12 (**dipakai sementara**) |
| 2 | Stabilitas Kinerja Relatif LightGBM terhadap HAR-RV dalam Peramalan *Realized Variance* Bitcoin pada Berbagai Kondisi Pasar | 15 |

---

## XI. Yang Perlu Dikuasai Sebelum Bimbingan

| Topik | Harus bisa menjelaskan |
|---|---|
| Kalimat inti | Tanpa catatan |
| Acuan | Dudek dkk.; Chassot & Audrino; Christensen dkk.; Feng, Zhang & Wang |
| RV 5 menit, HAR 1/7/30 | Kompromi lintas era; kripto 24/7 (Qiu dkk., 2025) |
| QLIKE vs MSE | Kenapa hasil RQ3 berbeda; kenapa QLIKE bisa dipakai |
| LightGBM | GOSS/EFB tidak berperan; bagging; num_leaves 3; kenapa bukan deep learning |
| Desain 2×2, walk-forward | Non-linearitas vs informasi tambahan; hyperparameter terkunci |
| UDmax vs Fluctuation | H0 berbeda; daya uji; nilai kritis simulasi |
| HAC | Bartlett + Andrews; kenapa bukan QS |
| Stasioneritas RQ2 | Aturan ADF + KPSS |
| Hasil H3 | "Tidak didukung; arah sebaliknya signifikan" |
| Sumber data | Kenapa arsip Binance, bukan cron Indodax |

---

## XII. Roadmap dan Tindak Lanjut

| Tahap | Status |
|---|---|
| Verifikasi literatur & novelty | ✅ Semua referensi dibaca (13 Okt) |
| Eksperimen | ✅ 6 Okt 2026 |
| Praskripsi Bab I–III | ✅ Draf; **revisi teks di Lampiran A** |
| Bimbingan (judul, sumber data, output sistem, pembimbing II, jadwal) | ⏳ |
| Bab IV–V | Setelah praskripsi disetujui |

**Daftar kerja:**
1. Terapkan revisi Lampiran A, lalu `make check`.
2. Tambah 4 entri `.bib` (Lampiran B) dan lengkapi `barndorff2010` (editor, DOI).
3. Rapikan Mendeley agar sama dengan `.bib` (Lampiran B).
4. **Klarifikasi Indodax vs Binance** di bimbingan.
5. Putuskan dua sensitivitas yang belum jalan.
6. Verifikasi:
   - tabel asli Bai–Perron (q = 1, ε = 0,15);
   - n per daun di perhitungan manual (dugaan: bagging LightGBM memilih tiap baris dengan peluang 80%, sehingga jumlah per pohon berfluktuasi — pohon 1: 256, pohon 2: 272; cek `leaf_count` beberapa pohon);
   - kuartil 2025 ESWA, Economic Modelling, JASA;
   - versi LightGBM di `.venv` untuk URL dokumentasi.
7. Lengkapi pembimbing II, jadwal, spesifikasi perangkat.

---

## Lampiran A. Revisi teks LaTeX

> Nomor baris perkiraan (repo per 10 Okt 2026). Setelah diterapkan, hapus `% CEK:` terkait.

### A.1 `% CEK:` yang bisa diselesaikan

| Lokasi | Tindakan |
|---|---|
| Bab 1 ±55 (Christensen) | Status B; perinci: perbandingan luas ML vs HAR di saham DJIA, satu periode uji, hanya MSE. Hapus CEK |
| Bab 1 ±71 (GR 2010, Trucíos) | Keduanya B, kalimat sesuai. Hapus CEK |
| Bab 1 ±89 (Feng 2024 dkk.) | Semua sudah dibaca; ganti kalimat Feng, Zhang & Wang (A.2 no. 1). Hapus CEK |
| Bab 2 ±30 (Feng, Qi & Lucey; Qiu) | Revisi A.2 no. 2 dan 3. Hapus CEK |
| Bab 2 Tabel posisi ±107 | Isi sel (A.3). Hapus CEK |
| Bab 2 ±311 (Grinsztajn, Chen) | Revisi A.2 no. 4. Hapus CEK |
| Bab 2 ±400 (DM, Andrews) | Revisi A.2 no. 6. Hapus CEK |
| Bab 2 ±438 (GR 2010) | Kutip langsung; tambahkan bahwa kerangka GW mensyaratkan rolling/fixed. Hapus CEK |
| Bab 2 ±590 (Rabanser) | Revisi A.2 no. 7. Hapus CEK |
| Bab 3 ±571 (n per daun) | Tetap sampai `leaf_count` dicek (Bagian XII no. 6) |
| Bab 3 ±707 (tabel Bai–Perron) | Tetap |
| Bab 3 ±787 (sensitivitas belum jalan) | Tetap sampai diputuskan |

### A.2 Usulan kalimat

1. **Bab 1 ±82 (Feng, Zhang & Wang):**
   ```latex
   Tidak ada skema yang selalu lebih unggul: skema yang lebih akurat berganti
   sepanjang waktu, dan keunggulan relatifnya cenderung bertahan dalam periode
   tertentu \cite{feng2024window}.
   ```
2. **Bab 2 ±20 (Feng, Qi & Lucey):** "kepentingan fitur berubah sejak Oktober 2022" → "kepentingan **indikator blockchain** meningkat sejak Oktober 2022"; objeknya volatilitas **Bitcoin (BTC/USD) 2017–2022**.
3. **Bab 2 ±26 (Qiu):**
   ```latex
   Qiu dkk. menunjukkan bahwa pada RV sepuluh aset kripto di Binance,
   kombinasi ramalan dari beberapa model HAR dan \textit{rough volatility}
   umumnya mengungguli model tunggal, karena model dengan spesifikasi tetap
   tidak selalu berlaku di semua skenario peramalan \cite{qiu2025}.
   ```
   Tambahkan juga di bagian lag HAR (Bab 2 subbab HAR-RV atau Bab 3 fitur): "rata-rata RV 1, 7, dan 30 hari, menyesuaikan perdagangan aset kripto yang berlangsung 24 jam setiap hari \cite{qiu2025}".
4. **Bab 2 ±300 (alasan LightGBM, Grinsztajn):**
   ```latex
   LightGBM dipilih dengan tiga pertimbangan. Pertama, pada data tabular
   berukuran menengah (sekitar 10 ribu sampel), model berbasis pohon seperti
   Random Forest dan XGBoost konsisten mengungguli model \textit{deep learning},
   bahkan setelah \textit{tuning hyperparameter} dengan anggaran besar
   \cite{grinsztajn2022}. Benchmark tersebut memakai data i.i.d. dengan minimal
   3.000 sampel, sedangkan data latih penelitian ini berupa fitur lag deret
   waktu sebanyak 365 hingga sekitar 2.900 baris; temuan itu karena itu dipakai
   sebagai dasar pemilihan kelas model, bukan jaminan kinerja.
   ```
   Kalimat "akurasinya setara dengan XGBoost" → "**hampir sama**" (`\cite{ke2017,chen2016}` tetap).
5. **Bab 2 ±248 (subbab LightGBM, leaf-wise):**
   ```latex
   LightGBM merupakan implementasi GBDT yang dirancang untuk efisiensi pada data
   besar melalui dua teknik, yaitu \textit{Gradient-based One-Side Sampling}
   (GOSS) dan \textit{Exclusive Feature Bundling} (EFB), dengan akurasi yang
   hampir sama dengan implementasi GBDT lain \cite{ke2017}. LightGBM menumbuhkan
   pohon secara \textit{leaf-wise}, yaitu memecah daun dengan penurunan
   \textit{loss} terbesar, berbeda dari pertumbuhan \textit{level-wise} yang
   memecah seluruh daun pada kedalaman yang sama (Gambar~\ref{fig:pohon-lgbm}).
   Pada jumlah daun yang sama, pertumbuhan \textit{leaf-wise} umumnya mencapai
   \textit{loss} lebih rendah, tetapi dapat mengalami \textit{overfitting} pada
   data berukuran kecil \cite{lightgbmfeatures}. Karena itu, jumlah daun
   (\texttt{num\_leaves}) dan jumlah minimum data per daun
   (\texttt{min\_data\_in\_leaf}) menjadi parameter utama untuk mengendalikan
   kompleksitas pohon \cite{lightgbmtuning}.
   ```
   Sumber gambar: `\sumber{Digambar ulang, diadaptasi dari dokumentasi LightGBM \cite{lightgbmfeatures}}`.
6. **Bab 2 ±381 (DM):**
   ```latex
   Uji Diebold--Mariano (DM) menguji apakah dua ramalan memiliki akurasi yang
   sama, dengan hipotesis nol $E[\Delta L_t] = 0$; fungsi \textit{loss} yang
   dipakai tidak harus kuadratik maupun simetris \cite{diebold1995}.
   ```
7. **Bab 2 ±585 (KS, Rabanser):**
   ```latex
   Uji KS per fitur merupakan salah satu pendekatan sederhana untuk mendeteksi
   pergeseran data, dengan kinerja yang sebanding dengan uji multivariat
   \cite{rabanser2019}. Berbeda dari penggunaan sebagai uji hipotesis, penelitian
   ini tidak memakai \textit{p-value}-nya; nilai $D^{\text{KS}}$ dirata-ratakan
   antarfitur sebagai ukuran besaran pergeseran per bulan.
   ```
8. **Bab 2 ±526 (Pesaran & Timmermann):**
   ```latex
   Pilihan strategi melibatkan \textit{trade-off} bias dan varians. Menyertakan
   data sebelum perubahan struktural menambah bias tetapi dapat mengurangi
   varians kesalahan ramalan, sehingga sering kali optimal untuk tetap memakai
   sebagian data tersebut selama perubahannya tidak terlalu besar; bila
   perubahannya besar, hanya data setelah perubahan yang sebaiknya dipakai
   \cite{pesaran2007}. Secara umum, \textit{rolling window} cenderung lebih baik
   ketika perubahan besar dan berulang, sedangkan skema rekursif
   (\textit{expanding}) lebih baik ketika perubahan kecil \cite{pesaran2007,rossi2013}.
   Untuk model autoregresif seperti HAR, data sebelum perubahan bahkan dapat
   mengurangi bias dan varians sekaligus \cite{rossi2013}.
   ```
9. **Bab 3 ±274 (LightGBM & RF):** tambahkan setelah butir LGBM:
   ```latex
   Penelitian ini menggunakan mode \textit{boosting} standar LightGBM dengan
   \textit{bagging} sebagai regularisasi; GOSS dan EFB yang dirancang untuk
   mempercepat pelatihan pada data besar dan fitur jarang tidak berperan karena
   data latih hanya berisi ratusan hingga ribuan baris dengan sembilan fitur
   padat. Dengan \texttt{num\_leaves} = 3, setiap pohon hanya memiliki dua
   pemecahan sehingga perbedaan pertumbuhan \textit{leaf-wise} dan
   \textit{level-wise} praktis hilang.
   ```
   Butir RF:
   ```latex
   \item \textbf{Random Forest} \cite{breiman2001}, yaitu rata-rata banyak pohon
         regresi yang masing-masing dilatih pada sampel \textit{bootstrap} dengan
         pemilihan fitur acak di setiap pemisahan, dengan masukan yang sama dengan
         LGBM-X (300 pohon, minimum 20 observasi per daun, 33\% fitur per
         pemisahan) digunakan hanya sebagai uji sensitivitas jenis model pohon.
   ```
10. **Bab 3 ±747 (Corwin–Schultz):**
    ```latex
    Sebagai uji sensitivitas, estimator Corwin--Schultz \cite{corwin2012}
    digunakan sebagai pengganti; penyesuaian harga \textit{overnight} pada
    estimator tersebut tidak diperlukan karena BTC/USDT diperdagangkan
    24 jam tanpa jeda.
    ```
11. **Bab 3 ±762 (ADF + KPSS):**
    ```latex
    ... regresor di-\textit{differencing} bila ADF gagal menolak akar unit
    ($p > 0{,}05$) \textbf{dan} KPSS menolak stasioneritas ($p < 0{,}05$),
    yaitu kombinasi hasil yang menunjukkan adanya akar unit
    \cite{kwiatkowski1992}.
    ```
12. **Opsional Bab 3 (aturan teknis ±279):** Christensen dkk. (2023) sebagai preseden koreksi bias dan batas bawah; `chen2016` saat menjelaskan `reg_lambda`.

### A.3 Tabel posisi Bab 2

| Penelitian | Objek | Pembanding HAR | Evaluasi sepanjang waktu | Variasi strategi window | Asosiasi kondisi pasar |
|---|---|---|---|---|---|
| Feng, Qi & Lucey | RV BTC/USD, 2017–2022 | Ya | Kepentingan fitur antarperiode | Hanya robustness (rolling, expanding) | Tidak |
| Chassot & Audrino | RV 1.445 saham AS, uji 2022–2023 | Ya | Tidak (grafik selisih error kumulatif, tanpa uji) | Ya (window & frekuensi re-estimasi HAR; ML statis) | Tidak (hanya per kapitalisasi) |
| *(opsional)* Christensen dkk. | RV saham DJIA, 2001–2017 | Ya | Tidak (agregat) | Tidak | Tidak |
| *(opsional)* Feng, Zhang & Wang | RV S&P 500, 2000–2022 | Ya (HAR saja, tanpa ML) | Tidak | Ya (rolling vs expanding, switching) | Sebagian (resesi/ekspansi, deskriptif) |

---

## Lampiran B. Metadata, `.bib`, dan Mendeley

### B.1 Entri baru `.bib`

```bibtex
@article{pesaran2007,
  author  = {Pesaran, M. Hashem and Timmermann, Allan},
  title   = {Selection of Estimation Window in the Presence of Breaks},
  journal = {Journal of Econometrics},
  volume  = {137}, number = {1}, pages = {134--161}, year = {2007},
  doi     = {10.1016/j.jeconom.2006.03.010}
}
@article{breiman2001,
  author  = {Breiman, Leo},
  title   = {Random Forests},
  journal = {Machine Learning},
  volume  = {45}, number = {1}, pages = {5--32}, year = {2001},
  doi     = {10.1023/A:1010933404324}
}
@online{lightgbmfeatures,
  author = {{Microsoft Corporation}}, title = {Features},
  organization = {LightGBM Documentation}, version = {4.x.x},
  url = {https://lightgbm.readthedocs.io/en/v4.x.x/Features.html},
  urldate = {2026-10-12}
}
@online{lightgbmtuning,
  author = {{Microsoft Corporation}}, title = {Parameters Tuning},
  organization = {LightGBM Documentation}, version = {4.x.x},
  url = {https://lightgbm.readthedocs.io/en/v4.x.x/Parameters-Tuning.html},
  urldate = {2026-10-12}
}
```
Ganti `4.x.x` dengan hasil `pip show lightgbm` di `.venv` (atau pakai `/en/stable/` tanpa `version`). Verifikasi DOI lewat Crossref sesuai aturan repo.

`barndorff2010`: tambah `editor = {Bollerslev, Tim and Russell, Jeffrey R. and Watson, Mark W.}` dan `doi = {10.1093/acprof:oso/9780199549498.003.0007}` (cek Crossref).

### B.2 Perbaikan Mendeley

| Entri | Perbaikan |
|---|---|
| Holm (1979) | Judul → *A Simple Sequentially Rejective Multiple Test Procedure* |
| Newey & West (1987) | Penulis → Newey, Whitney K.; West, Kenneth D. |
| Andersen & Bollerslev (1998) | Penulis → Andersen, Torben G.; Bollerslev, Tim |
| Bai & Perron (1998) | Sumber → Econometrica |
| Corsi (2009) | Versi jurnal: *A Simple Approximate Long-Memory Model of Realized Volatility*, JFEC 7(2), 174–196 |
| Christensen dkk. | Tahun 2026 → **2023**, JFEC 21(5), 1680–1727 |
| Ke dkk. (2017) | Tipe → Conference Proceedings (NeurIPS 30) |
| Microsoft Corporation | Judul → **Parameters Tuning** |
| Barndorff-Nielsen (2010) | Tipe Book Section + editor |
| Al-Yahyaee (2020), Teller (2026) | Hapus/pisahkan (tidak dipakai) |
| Entri kurang | Tambah 12: Abdi & Ranaldo, Corwin & Schultz, Dickey & Fuller, KPSS, Diebold & Mariano, Andrews, Grinsztajn, Chen & Guestrin, Rabanser, Qiu, Pesaran & Timmermann, Breiman |

Format nama: *Nama belakang, Nama depan*; urutan penulis sama persis dengan paper.

### B.3 Catatan lain
- Kutip **versi terbit** untuk semua yang dibaca versi WP/arXiv (Corsi, Barndorff-Nielsen, Christensen, Abdi & Ranaldo, Corwin & Schultz, Diebold & Mariano, Andrews, KPSS, Pesaran & Timmermann, Breiman); jangan menyebut nomor persamaan paper.
- Rossi (2013): cek nama editor handbook. Oprea & Bâra (2026): cek volume/halaman.
- Kuartil di dokumen ini SJR 2025; tulis tahunnya bila disebut di naskah.
- Format sitasi: IEEE (biblatex).
