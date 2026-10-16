# Riset Skripsi v2.9: Stabilitas Kinerja Relatif LightGBM terhadap HAR-RV dalam Peramalan *Realized Variance* Bitcoin

> **Status (16 Oktober 2026):** desain **terkunci dan sudah dieksekusi**. Eksperimen penuh selesai 6 Okt 2026 (config hash `0af5b5b98c60`). Rincian hasil dan source code ada di `hasil_eksperimen_bitcoin_v2_5.md`. Praskripsi (Bab I–III) di LaTeX selesai sampai Bab III (repo `ferdiendahas/skripsi-latex`). Seluruh referensi sudah ditelaah (F/WP/B). Daftar perbaikan teks naskah ada di Lampiran A.
>
> **Aturan anti-HARKing:** uji konfirmatori sudah dijalankan. RQ, hipotesis, uji konfirmatori, dan kandidat judul **tidak boleh diubah** mengikuti hasil. Perubahan setelah ini hanya boleh masuk sebagai eksploratori, sensitivitas, atau keterbatasan. Paper baru di v2.9 hanya menambah literatur pembanding dan pengakuan novelty, tidak mengubah hipotesis.
>
> **Aturan Bab I–III:** hasil *out-of-sample* tidak boleh muncul. Ini mencakup QLIKE rata-rata, ΔL, UDmax, p-value hipotesis, dan kurva window. Yang boleh: desain, deskripsi data, hasil di window awal (VIF, hyperparameter terkunci), dan perhitungan manual.
>
> **Notasi:** BTC/USDT = pasar spot (yang dipakai). BTCUSDT tanpa garis miring = perpetual; hanya muncul sebagai nama berkas arsip Binance.
>
> **Status baca referensi:** F = full text seluruhnya · WP = full text versi working paper/preprint · B = PDF, bagian relevan · M = metadata saja · ✗ = belum dicek. Kuartil = kuartil terbaik SCImago **SJR 2025** (dicek 10 Okt 2026), kecuali disebut lain.
>
> **Sumber klaim isi paper:** `claude/kartu_paper.md` (63 kartu, kode A1–K2). **Klaim tentang isi paper hanya boleh ditulis bila tercatat di kartu, beserta lokasinya.** Klaim yang ditandai ⚠ di dokumen ini belum tercatat di kartu; cek PDF sebelum dikutip.
>
> **Urutan otoritas bila bertentangan:** brief terbaru > `kartu_paper.md` (untuk isi paper) > dokumen ini (v2.9) > source code di `hasil_eksperimen` > versi lama dokumen riset.

---

## 0. Ringkasan Perubahan

### Update v2.9 (16 Okt 2026)

| Aspek | v2.8 | v2.9 | Dasar |
|---|---|---|---|
| Paper baru | — | **8 paper dibaca:** Dudek, Kasprzyk & Pełka (2025, preprint); Brauneis & Sahiner (2026); Kılıç (2025, WP); Pyrlik dkk. (2021, WP); Nadarajah dkk. (2025); Zanotti (2025); Makridakis dkk. (2022, M5); Teller dkk. (2026, tidak dipakai) | Kartu D8–D13, F6, I5 |
| Checklist novelty | 7 paper | **12 paper**: + Dudek dkk. (2025), Brauneis & Sahiner (2026), Kılıç (2025), Pyrlik dkk. (2021), Nadarajah dkk. (2025) | Bagian IV |
| Sintesis III.5 no. 2 | "hampir semuanya satu periode uji dan hasil agregat" | Dilunakkan: sebagian studi melaporkan per periode secara **deskriptif** (Kılıç; Pyrlik), tanpa uji formal kestabilan | Kartu D10, D11 |
| Wang dkk. (2023) | Ikut didaftar sebagai studi "ML vs HAR" | **Dikoreksi:** pembandingnya GARCH, bukan HAR | Kartu D4 |
| Feng, Qi & Lucey (2024) | "rolling/expanding hanya robustness" | **Dikoreksi:** hanya **panjang rolling window** yang diubah (10% dan 30%); expanding tidak dipakai (hlm. 8) | Kartu D5 |
| Cerqueira dkk. (2020) | "Forward-chaining" | Istilah paper: ***prequential in blocks***. "Forward-chaining" tetap boleh sebagai istilah prosedur sendiri, tanpa diatribusikan ke Cerqueira | Kartu F4 |
| Pesaran & Timmermann (2007) | Ikut dikutip untuk "rolling lebih baik bila break besar, rekursif bila kecil" | Kalimat itu dikutip ke **Rossi (2013, hlm. 1230)** saja; P&T untuk data pre-break dan kombinasi window | Kartu F3, G3 |
| Huang dkk. (2024), Dudek dkk. (2024), Chassot & Audrino (2026) | Ringkasan terlalu ringkas | Ditambah batasan: hasil grafik/deskriptif, arah klaim, dan pembanding tidak setara | Kartu D2, D3, D6 |
| Christensen dkk. (2023) | Preseden koreksi bias, batas bawah, "GB peka outlier" | ⚠ **Belum tercatat di kartu**; cek lokasi di PDF sebelum dikutip | Kartu D1 |
| Bab V | — | Pembanding baru: Brauneis & Sahiner (HAR > LightGBM pada BTC, QLIKE, DM signifikan); Kılıç dan Pyrlik (model pohon terburuk); Zanotti (frekuensi latih ulang); Dudek dkk. 2025 (GOSS tidak lebih baik dari GBDT) | Bagian VII, IX |
| `.bib` | — | `breiman2001` dan `lightgbmtuning` sudah ada di repo; **`pesaran2007` dan `lightgbmfeatures` masih belum**. 7 key usulan untuk paper baru (Lampiran B.1) | Lampiran B |
| `hasil_eksperimen` | — | **Tidak terpengaruh** | — |

### Update v2.8 (14 Okt 2026, ringkas)
Corsi (2009) dibaca versi terbit (JFEC 7(2), 174–196). Temuan salah sitasi ke-6: "Corsi memperlihatkan koefisien HAR dapat berubah sepanjang waktu" tidak ada di paper (Lampiran A.2 no. 13). Preseden ln RV sebagai bentuk analog yang menjamin positif (Corsi, hlm. 179 dan cat. kaki 9).

### Update v2.7 (12–13 Okt 2026, ringkas)
Seluruh referensi `.bib` dibaca dari PDF. Ditemukan lima salah sitasi:
1. *Leaf-wise*/*overfitting* dan gambar pohon bukan dari Ke dkk., tetapi dari dokumentasi LightGBM.
2. Grinsztajn: "kecil hingga menengah" diganti "menengah, ±10 ribu".
3. Klaim autoregresif bukan dari Pesaran & Timmermann (2007).
4. Feng, Zhang & Wang: "berpengaruh" diganti "berganti sepanjang waktu".
5. DM: "dua model" diganti "dua ramalan".

Rumus Abdi–Ranaldo, Corwin–Schultz, dan bandwidth Andrews sudah dicocokkan dengan kode. Preseden lag 1/7/30 (Qiu dkk., 2025) dan aturan differencing ADF+KPSS juga ditambahkan.

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
| Kondisi pasar | Error di 5% hari RV terendah/tertinggi, tanpa uji (hlm. 9) | Regresi ΔL pada karakteristik pasar dengan uji formal (RQ2) |
| Strategi window | Satu skema (rolling 23 bulan, latih ulang harian; hlm. 6, 8) | Static vs expanding vs rolling, antarera (RQ3) |
| Periode | Berakhir 2021 | Sep 2018 – Sep 2026, era transition dan institutional |
| Sumber keunggulan | Tidak dipisahkan | Dekomposisi 2×2 (non-linearitas vs informasi tambahan) |

**Lanjutan dari tim yang sama:** Dudek, Kasprzyk & Pełka (2025, **preprint** arXiv) sudah memakai LightGBM untuk RV Bitcoin. Datanya hanya Senin–Jumat, dengan satu periode uji 2020–2023 dan hiperparameter yang dicari sekali. Paper ini tidak menguji kestabilan sepanjang waktu dan tidak memvariasikan strategi window (kartu D8). Posisi riset ini tetap aman, tetapi preprint ini wajib diakui.

**Acuan pendukung:**
- **Chassot & Audrino (2026)**, IJF (Q1): perlakuan window HAR menentukan hasil perbandingan ML vs HAR.
- **Christensen dkk. (2023)**, JFEC (Q1): rujukan utama ML vs HAR-RV.
- **Feng, Zhang & Wang (2024)**, J. Forecasting (Q2): rolling vs expanding untuk HAR; skema terbaik berganti sepanjang waktu.

Kalimat posisi: *"Penelitian ini memperluas Dudek dkk. (2024) dengan menguji apakah kinerja relatif LightGBM terhadap HAR-RV stabil sepanjang waktu, faktor pasar apa yang berasosiasi dengan perubahannya, serta bagaimana strategi pembaruan model memengaruhinya, dengan perlakuan window yang setara bagi HAR-RV (Chassot & Audrino, 2026)."*

### Kenapa framing ini kuat
1. **Menghindari temuan trivial.** Loss absolut naik saat volatilitas tinggi karena skala target. ΔL pada hari yang sama menetralkan efek ini, dan QLIKE homogen berderajat nol (Patton, 2011).
2. **Pertanyaan praktis jelas:** kapan model ML layak dipakai dibanding model sederhana, dan bagaimana memperbaruinya.
3. **Kontribusi Informatika:** rancangan evaluasi model ML pada data yang berubah. Rancangan ini memadukan strategi pembaruan dari literatur concept drift dengan uji kestabilan dari ekonometrika (Suárez-Cetrulo dkk., 2023, hlm. 2, 13, 14).
4. **Hasil negatif tetap valid** dan bisa dibela (Bagian VII).

### Yang TIDAK diklaim
- Tidak mengklaim *concept drift* atau *covariate shift* formal; yang diukur hanya pergeseran distribusi fitur (Moreno-Torres dkk., 2012).
- Tidak mengklaim menjelaskan mikrostruktur Bitcoin; semua variabel pasar diturunkan dari OHLCV.
- Tidak mengklaim kausalitas; RQ2 bersifat asosiatif.
- Tidak mengklaim memisahkan efek jumlah dan umur data latih (S1 vs S2 = efek gabungan; Tashman, 2000).
- Tidak mengklaim sebagai studi pertama yang mengevaluasi ML vs HAR per periode. Evaluasi per tahun dan per kuartal sudah ada secara deskriptif (Kılıç, 2025; Pyrlik dkk., 2021). Yang belum ditemukan adalah **uji formal** kestabilan pada RV Bitcoin.
- Kesimpulan terbatas pada BTC/USDT spot Binance.

---

## II. Konsep Kunci

| Konsep | Pengertian | Peran |
|---|---|---|
| Realized variance (RV) | Σ kuadrat return 5 menit dalam satu hari UTC (288 return) | Target |
| HAR-RV | Regresi ln RV pada rata-rata RV 1, 7, 30 hari (Corsi, 2009; lag 7/30 untuk kripto 24/7: Qiu dkk., 2025) | Baseline |
| QLIKE | Loss robust terhadap proxy berisik, homogen derajat nol (Patton, 2011, Proposition 2–4) | Metrik utama |
| ΔL | `ΔL_t = L_t(ML) − L_t(HAR)`; negatif = ML unggul | Objek analisis |
| D_t | `ΔL_t(S2-365) − ΔL_t(S1)`; positif = expanding lebih baik bagi ML | Objek uji H3 |
| Uji DM | H0: E[d_t] = 0 untuk dua **ramalan**; loss tidak harus kuadratik atau simetris (Diebold & Mariano, 1995) | Lanjutan H1 |
| Forecast instability | Kinerja relatif berubah sepanjang waktu (Rossi, 2013) | Fenomena yang diuji |
| UDmax | Uji Bai–Perron untuk 1 s.d. M perubahan rata-rata (Bai & Perron, 1998, bagian 4.2) | Uji konfirmatori H1 |
| Fluctuation test | Statistik DM bergulir, nilai kritis Giacomini & Rossi (2010) | Grafik eksploratori |
| Forecast breakdown | Loss OOS signifikan lebih buruk dari in-sample, untuk **satu model** (Giacomini & Rossi, 2009) | Pembeda konsep |
| Pergeseran distribusi fitur | Rata-rata statistik KS antarfitur antara window latih dan bulan uji (dipakai sebagai besaran, bukan keputusan uji) | Regresor RQ2 |
| Updating vs recalibration | Data baru tanpa estimasi ulang vs estimasi ulang (Tashman, 2000) | S0 vs S1/S2 |
| Prequential in blocks | Latih-uji bergantian per blok dengan window bertambah atau bergeser (Cerqueira dkk., 2020) | Kerangka S1/S2 |
| Uji konfirmatori | **Satu uji per hipotesis**, ditetapkan sebelum melihat hasil OOS | Mencegah temuan kebetulan |

**Istilah drift (kerangka Moreno-Torres):**

| Perubahan | Gama dkk. (2014) | Moreno-Torres dkk. (2012) |
|---|---|---|
| P(x) berubah | *Virtual drift* | *Covariate shift* (syarat P(y\|x) tetap) |
| P(y\|x) berubah | *Real concept drift* | *Concept shift* (syarat P(x) tetap) |

---

## III. Literatur

> **Aturan:** referensi metode/teori tanpa batas tahun; referensi gap 2021–2026. Klaim isi paper harus sesuai `kartu_paper.md`. Tulis status preprint/WP bila mengutip Dudek dkk. (2025), Kılıç (2025), atau Pyrlik dkk. (2021).

**Ringkasan referensi:**

| Status | Di `.bib` (54) | Usulan baru (7) |
|---|---|---|
| F (full text seluruhnya) | 6 | 0 |
| WP (working paper/preprint) | 1 | 0 |
| B (PDF, bagian relevan) | 44 | 7 (3 di antaranya WP/preprint) |
| Sumber web | 3 | 0 |
| **Total** | **54** | **7** |

| Jenis (54 entri `.bib`) | Jumlah |
|---|---|
| Artikel jurnal | 45 (Q1: 37 · Q2: 6 · belum terverifikasi: 2 — Dickey & Fuller, Qiu) |
| Prosiding (NeurIPS, KDD) | 4 |
| Bab buku | 2 |
| Sumber web | 3 |

Kuartil 7 usulan baru belum dicek. Jangan menyebut "semua full text"; tulis "seluruh referensi telah ditelaah, sebagian pada bagian yang relevan".

### III.1 Referensi metode dan teori

**Volatilitas, pengukuran, fitur**

| Key `.bib` | Referensi | Status | Kuartil | Dipakai untuk |
|---|---|---|---|---|
| `andersen1998` | Andersen & Bollerslev (1998), IER 39(4), 885–905 | B | Q1 | RV intraday sebagai proxy |
| `corsi2009` | Corsi (2009), JFEC 7(2), 174–196 | B (versi terbit) | Q1 | HAR-RV |
| `liu2015` | Liu, Patton & Sheppard (2015), J. Econometrics 187(1), 293–311 | B | Q1 | RV 5 menit sulit dikalahkan secara signifikan |
| `parkinson1980` | Parkinson (1980), J. Business 53(1), 61–65 | F | Q1 (historis) | Fitur range |
| `barndorff2010` | Barndorff-Nielsen, Kinnebrock & Shephard (2010), bab buku OUP, hlm. 117–136 | WP (2008) | — | Definisi RS⁻ |
| `patton2015` | Patton & Sheppard (2015), REStat 97(3), 683–697 | B | Q1 | RS⁻ sebagai prediktor |
| `amihud2002` | Amihud (2002), JFM 5(1), 31–56 | B | Q1 | Definisi Amihud |
| `brauneis2021` | Brauneis dkk. (2021), JBF 124, 106041 | B | Q1 | Amihud untuk level, Abdi-Ranaldo untuk variasi waktu |
| `abdi2017` | Abdi & Ranaldo (2017), RFS 30(12), 4437–4480 | B (WP 2017) | Q1 | Proxy likuiditas RQ2; **rumus = kode ✅** |
| `corwin2012` | Corwin & Schultz (2012), J. Finance 67(2), 719–760 | B (WP ±2009) | Q1 | Sensitivitas likuiditas; **rumus = kode ✅** |

**Model ML**

| Key | Referensi | Status | Kuartil | Dipakai untuk |
|---|---|---|---|---|
| `ke2017` | Ke dkk. (2017), LightGBM, NeurIPS 30 | **F** | CORE A\* | Definisi LightGBM, GOSS, EFB; akurasi hampir sama dengan XGBoost |
| `chen2016` | Chen & Guestrin (2016), XGBoost, KDD | B (arXiv v3) | CORE A\* | Identitas XGBoost; regularisasi L2 bobot daun (`reg_lambda`) |
| `grinsztajn2022` | Grinsztajn, Oyallon & Varoquaux (2022), NeurIPS D&B | B (arXiv v1) | CORE A\* | Model pohon > deep learning pada data tabular menengah |
| `breiman2001` | Breiman (2001), Machine Learning 45(1), 5–32 | B (TR 2001) | Q1 | Random Forest (sensitivitas) — sudah di `.bib` |
| `lightgbmfeatures` | Dokumentasi LightGBM: *Features* (Microsoft Corporation) | web | — | Leaf-wise; sumber gambar pohon — **belum di `.bib`** |
| `lightgbmtuning` | Dokumentasi LightGBM: *Parameters Tuning* | web | — | `num_leaves`, `min_data_in_leaf` — sudah di `.bib` |
| `makridakis2022` *(usulan)* | Makridakis, Spiliotis & Assimakopoulos (2022), IJF 38(4), 1346–1364 (M5) | B | belum dicek | Opsional: popularitas LightGBM di kompetisi peramalan, dengan batasan (III.4) |

**Metrik dan uji statistik**

| Key | Referensi | Status | Kuartil | Dipakai untuk |
|---|---|---|---|---|
| `patton2011` | Patton (2011), J. Econometrics 160(1), 246–256 | B | Q1 | QLIKE |
| `diebold1995` | Diebold & Mariano (1995), JBES 13(3), 253–263 | B (NBER WP 1994) | Q1 | Uji DM |
| `newey1987` | Newey & West (1987), Econometrica 55(3), 703–708 | B | Q1 | HAC |
| `andrews1991` | Andrews (1991), Econometrica 59(3), 817–858 | B (Cowles DP 877R) | Q1 | Bandwidth HAC otomatis; **rumus = kode ✅** |
| `giacomini2009` | Giacomini & Rossi (2009), REStud 76(2), 669–705 | B | Q1 | Konsep breakdown |
| `giacomini2010` | Giacomini & Rossi (2010), JAE 25(4), 595–620 | B | Q1 | Fluctuation test; syarat rolling/fixed |
| `rossi2013` | Rossi (2013), Handbook of Economic Forecasting vol. 2B, 1203–1324 | B (bab buku) | — | Survei instabilitas |
| `martins2016` | Martins & Perron (2016), JTSA | B | Q1 | Dasar UDmax pada ΔL |
| `bai1998` | Bai & Perron (1998), Econometrica 66(1), 47–78 | B | Q1 | UDmax |
| `bai2003` | Bai & Perron (2003), JAE 18(1), 1–22 | B | Q1 | UDmax lalu uji berurutan |
| `holm1979` | Holm (1979), Scand. J. Statistics 6(2), 65–70 | B | **Q2** | Koreksi uji berganda |
| `dickey1979` | Dickey & Fuller (1979), JASA 74(366a), 427–431 | B | belum dicek | Uji akar unit |
| `kwiatkowski1992` | Kwiatkowski dkk. (1992), J. Econometrics 54, 159–178 | B (Cowles DP 979) | Q1 | Uji KPSS; dasar aturan differencing |
| `pesaran2007` | Pesaran & Timmermann (2007), J. Econometrics 137(1), 134–161 | B (versi Jan 2006) | Q1 | Dasar H3 — **belum di `.bib`** |

**Evaluasi dan adaptasi model**

| Key | Referensi | Status | Kuartil | Dipakai untuk |
|---|---|---|---|---|
| `tashman2000` | Tashman (2000), IJF 16(4), 437–450 | B | Q1 | Updating vs recalibration; kelemahan satu titik awal dan satu periode uji |
| `cerqueira2020` | Cerqueira dkk. (2020), Machine Learning 109, 1997–2028 | B | Q1 | CV acak tidak cocok untuk deret waktu; *prequential in blocks* |
| `gama2014` | Gama dkk. (2014), ACM CSUR 46(4), Art. 44 | F | Q1 | Taksonomi window; rata-rata akurasi menutupi adaptasi |
| `zliobaite2015` | Žliobaitė dkk. (2015), Neurocomputing 150, 240–249 | B | Q1 | S0 sebagai pembanding |
| `morenotorres2012` | Moreno-Torres dkk. (2012), Pattern Recognition 45, 521–530 | B | Q1 | Definisi dataset shift |
| `rabanser2019` | Rabanser, Günnemann & Lipton (2019), NeurIPS 32 | B (arXiv v4) | CORE A\* | Uji KS per fitur |
| `suarez2023` | Suárez-Cetrulo dkk. (2023), ESWA 213, 118934 | F | Q1 (SJR 2024) | Recurring drift; celah dengan literatur deret waktu |
| `zanotti2025` *(usulan)* | Zanotti (2025), Machine Learning with Applications 22, 100769 | B | belum dicek | Opsional: frekuensi latih ulang (domain ritel) |

### III.2 Referensi gap (2021–2026)

**Pilar A — Evolusi pasar Bitcoin**

| Key | Referensi | Status | Kuartil | Kegunaan |
|---|---|---|---|---|
| `do2026` | Do (2026), Borsa Istanbul Review 26, 100869 | F | Q1 | Batas era; persistensi per era (seri tidak disebut eksplisit di Tabel 2) |
| `mokni2024` | Mokni dkk. (2024), Financial Innovation 10, 39 | B | Q1 | Efisiensi berubah-waktu |
| `yi2023` | Yi dkk. (2023), Scientific Reports 13, 4789 | B | Q1 | Efisiensi return (stabil antartahun) |
| `zhang2024` | Zhang dkk. (2024), Financial Innovation 10, 3 | B | Q1 | Proxy likuiditas kripto |
| `nakamoto2008` | Nakamoto (2008), white paper | web | — | Pengenalan Bitcoin |

**Pilar B — Regime**

| Key | Referensi | Status | Kuartil | Kegunaan |
|---|---|---|---|---|
| `agakishiev2025` | Agakishiev dkk. (2025), Digital Finance 7, 107–131 | B | Q2 | Manfaat regime tidak signifikan di data validasi dan uji (Tabel 6) |
| `oprea2026` | Oprea & Bâra (2026), Computational Economics | B | Q2 | Target **harga**, tanpa HAR |

**Pilar C — ML untuk volatilitas**

| Key | Referensi | Status | Kuartil | Pembanding | Kegunaan |
|---|---|---|---|---|---|
| `dudek2024` | **Dudek dkk. (2024)**, Applied Soft Computing 151, 111132 | B | Q1 | HAR | **Paper acuan** |
| `huang2024` | Huang dkk. (2024), JIFMIM 97, 102064 | B | Q1 | HAR | LSTM unggul tipis; DM signifikan hanya horizon 60 hari (Tabel 8). HAR lebih tahan saat lonjakan hanya pada horizon 1 hari, dari grafik tanpa uji |
| `wang2023` | Wang dkk. (2023), IRFA 90, 102914 | B | Q1 | **GARCH** | Determinan internal paling penting (SHAP); **bukan studi ML vs HAR** |
| `christensen2023` | Christensen, Siggaard & Veliyev (2023), JFEC 21(5), 1680–1727 | B (arXiv) | Q1 | HAR | Rujukan utama ML vs HAR |
| `feng2024ml` | Feng, Qi & Lucey (2024), IRFA 94, 103239 | B | Q1 | HAR | Tuning harian; menyarankan menguji RF, XGBoost, LightGBM dengan tuning dinamis (hlm. 13) |
| `qiu2025` | Qiu, Qu, Shi & Xie (2025), Economic Modelling 144, 106986 | B | belum terverifikasi | varian HAR | Kombinasi ramalan > model tunggal; **lag 1/7/30 untuk kripto 24/7** |
| `brauneis2026` *(usulan)* | Brauneis & Sahiner (2026), Asia-Pacific Financial Markets 33, 379–411 | B | belum dicek | HAR | Pada BTC, HAR > LightGBM (QLIKE; DM signifikan, hlm. 406) |
| `dudek2025lgbm` *(usulan)* | Dudek, Kasprzyk & Pełka (2025), arXiv:2511.20105 | B (**preprint**) | — | HAR, BMA, LASSO, RF | LightGBM untuk RV Bitcoin; DM signifikan hanya pada satu perbandingan |
| `kilic2025` *(usulan)* | Kılıç (2025), FEDS 2025-061 | B (**WP**) | — | HAR + HAR nonlinear | Evaluasi per tahun 2006–2023 (deskriptif); XGBoost terburuk di antara ML |
| `pyrlik2021` *(usulan)* | Pyrlik, Elizarov & Leonova (2021), CERGE-EI WP 713 | B (**WP**) | — | HAR | Win-rate per kuartal; GB terburuk; Lasso dan HAR terbaik |
| `nadarajah2025` *(usulan)* | Nadarajah dkk. (2025), JRFM 18(2), 52 | B | belum dicek | **GARCH** | Opsional: contoh ensemble pohon (termasuk LightGBM) untuk volatilitas kripto, satu periode uji; **bukan studi ML vs HAR** |

**Pilar D — Uji instabilitas di kripto**

| Key | Referensi | Status | Kuartil | Kegunaan |
|---|---|---|---|---|
| `trucios2023` | Trucíos & Taylor (2023), J. Forecasting 42(4), 989–1007 | B | Q2 | Fluctuation test untuk VaR/ES kripto (bukan RV) |

**Pilar E — Window training**

| Key | Referensi | Status | Kuartil | Kegunaan |
|---|---|---|---|---|
| `chassot2026` | Chassot & Audrino (2026), IJF 42(2), 330–343 | B | Q1 | Skema fitting HAR menentukan hasil |
| `akgun2025` | Akgun & Gulay (2025), Computational Economics 65, 3971–4013 | B | Q2 | Rolling vs expanding (rinci untuk GARCH; tanpa HAR, tanpa uji signifikansi) |
| `feng2024window` | Feng, Zhang & Wang (2024), J. Forecasting 43(3), 567–582 | **F** | Q2 | Dasar RQ3 |

### III.3 Tidak dipakai (di luar `.bib`)

| Referensi | Alasan |
|---|---|
| Al-Yahyaee dkk. (2020); Teller dkk. (2026) | Tidak dikutip. Teller adalah sisa topik transfer learning dan relevansinya rendah (kartu D13). Hapus dari Mendeley atau pisahkan collection |
| Berger & Koubová (2024); Arora dkk. (2024); Di-Giorgi dkk. (2025); Catania & Grassi (2022); Souto & Moradi (2024); Lima dkk. (2022); Bakirov dkk. (2021); Andrews (1993); Hansen, Lunde & Nason (2011); Inoue & Rossi (2012) | Tidak dibutuhkan argumen |
| Quiñonero-Candela dkk. (2009); preprint arXiv 2607.05291 | Hanya resensi / belum terbit |
| Paper Parlika dkk. (JOIV ×2; Sisfokom 2026, Sinta 3) | Disisihkan sampai pembimbing setuju |
| Said & Dickey (1984), Biometrika | Opsional: sumber asli versi *augmented* DF yang dipakai `adfuller(autolag="AIC")` |
| Friedman (2001) | Opsional: sumber asli persamaan GBDT di Bab II |
| Pesaran & Timmermann (2005) | Opsional: sumber asli kasus autoregresif (saat ini dikutip lewat Rossi, 2013, hlm. 1230) |

### III.4 Temuan paper

> Ringkasan untuk keputusan. Rincian dan lokasi lengkap ada di `kartu_paper.md` (kode kartu dalam kurung).

**Corsi (2009), JFEC — versi terbit (A3).**
- RV di paper ini adalah **akar** jumlah kuadrat return intraday (pers. 3, hlm. 177). Agregasi mingguan 5 hari dan bulanan 22 hari.
- HAR(3) = AR terestriksi yang meniru memori panjang. Model bisa ditulis analog untuk varians atau log-nya (hlm. 179); versi log menjamin positif (cat. kaki 9).
- OOS: estimasi ulang harian pada *moving window* 1.000 observasi (hlm. 189–191). HAR(3) mengungguli AR(1)/AR(3) dan sebanding dengan ARFIMA (hlm. 191).
- **Tidak ada** klaim bahwa koefisien HAR berubah sepanjang waktu. Satu-satunya "instability" ada di cat. kaki 15 (hlm. 188), tentang AR(22) pada T-Bond.

**Chassot & Audrino (2026), IJF (D6).**
- 1.445 saham AS, 2015 – 31 Okt 2023. HAR rolling 630 hari diestimasi ulang harian; ML memakai window statis.
- ML tidak mengungguli HAR yang di-fit dengan tepat bila input hanya RV/VIX (abstrak).
- Frekuensi estimasi ulang lebih berpengaruh daripada panjang window; window optimal sekitar 2,5–4 tahun (Gambar 1, hlm. 331–332).
- Batasan [PR]: pembandingnya ML statis vs HAR yang diperbarui harian.
- Novelty aman: bukan kripto, perlakuan window tidak simetris, tanpa analisis antarera.

**Feng, Qi & Lucey (2024), IRFA (D5).**
- BTC/USD 2017–2022, RV 5 menit. HAR-RV vs Lasso/Ridge/EN dengan tuning ulang harian dalam rolling window lebar tetap.
- Kepentingan **indikator blockchain** naik sejak Okt 2022 (abstrak). Batasan [PR]: hanya ±2,5 bulan data uji sesudahnya.
- Uji ketahanan **hanya mengubah panjang rolling window** (10% dan 30%); expanding tidak dipakai (hlm. 8).
- Penulis menyarankan menguji RF, XGBoost, dan LightGBM dengan tuning dinamis (hlm. 13).
- Novelty aman.

**Trucíos & Taylor (2023), J. Forecasting (E3).** BTC/ETH harian Binance, 17 Agu 2017 – Jul 2022; VaR/ES. Fluctuation test sebagian besar tidak signifikan (hlm. 998). Novelty aman.

**Giacomini & Rossi (2010), JAE (G2).** Fluctuation test = DM/GW bergulir, dengan H0 sama akurat di setiap titik (Proposition 1, hlm. 600). Kerangka GW mensyaratkan **rolling/fixed** (hlm. 599). LM2 adalah uji sup perubahan, bagian dari One-Time Reversal test (hlm. 602–603).

**Christensen, Siggaard & Veliyev (2023), JFEC — preprint (D1).**
- 29 saham DJIA 2001–2017; satu split 70/10/20 (hlm. PDF 13); loss MSE (tanpa QLIKE).
- Dengan input HAR saja (MHAR), RF ≈ HAR (1,020) dan GB lebih buruk (1,054) (Tabel 2). Dengan prediktor tambahan (MALL), RF 0,901 dan GB 0,962 (Tabel 3).
- Peringkat HAR vs turunannya berbalik bila data latih dipendekkan (hlm. PDF 15; Lampiran A.1).
- ⚠ Belum tercatat di kartu: preseden koreksi bias exp(ŷ + ½var), batas bawah ramalan, dan alasan "GB peka outlier". Cek lokasi di PDF sebelum dikutip.

**Ke dkk. (2017), NeurIPS — F (I1).**
- Kontribusi barunya GOSS dan EFB. Akurasinya **hampir sama** dengan XGBoost (abstrak).
- Paper ini **tidak memuat** klaim "leaf-wise rentan overfitting pada data kecil" dan tidak punya gambar leaf-wise vs level-wise. Keduanya berasal dari dokumentasi LightGBM.
- Implementasi riset ini memakai boosting standar + bagging 80% (bukan GOSS). EFB tidak berperan (9 fitur padat). Dengan `num_leaves` = 3, beda leaf-wise dan level-wise praktis hilang.

**Dudek, Kasprzyk & Pełka (2025), preprint (D8).**
- RV BTC/USD 2017–2023, **hanya Senin–Jumat**. LightGBM dilatih ulang harian dengan data yang bertambah; hiperparameter dicari sekali.
- **GOSS tidak lebih baik dari GBDT standar, sehingga dipakai GBDT** (hlm. PDF 24).
- MSE LightGBM lebih rendah dari HAR (Tabel 2), tetapi **DM hanya signifikan pada satu perbandingan** (hlm. PDF 29). Menurut Wilcoxon, LightGBM tidak lebih baik dari RF.
- Tidak memakai QLIKE.
- Batasan [PR]: penutup menyebut LightGBM "outperforms" (hlm. PDF 48), padahal uji statistiknya tidak mendukung sekuat itu. **Jangan** kutip paper ini sebagai bukti kuat LightGBM unggul atas HAR.

**Brauneis & Sahiner (2026), APFM (D9).**
- 8 kripto, Coinbase, RV **6 jam**, 21 Des 2021 – 22 Des 2022; uji ±73 hari.
- **BTC tanpa sentimen: HAR lebih baik dari LightGBM** pada MAE, RMSE, dan QLIKE (Tabel 4, hlm. 398). Dengan QLIKE, HAR signifikan mengungguli semua model ML untuk BTC (DM, hlm. 406).
- Untuk koin lain, ML umumnya lebih baik (abstrak). Abstrak tidak menyebut pengecualian BTC.
- Batasan [PR]: lag HAR 8/28 periode (2 dan 7 hari) walau teks menyebut 7/30 lebih tepat (hlm. 387); validasi silang 5 lipat; satu tahun data.

**Kılıç (2025), FEDS WP (D10).**
- RV S&P 500 (Bloomberg) 1996–2023. Evaluasi per tahun 2006–2023 dengan expanding tahunan (abstrak menyebut "rolling", tetapi desainnya expanding; hlm. PDF 22).
- THAR/STHAR paling konsisten. **XGBoost terburuk di antara ML**; pada 2008, QLIKE XGBoost 2,267 vs HAR 0,330 (Tabel 2).
- Ada MSPE/QLIKE dan MCS per tahun, tetapi **tidak ada uji formal kestabilan kinerja relatif**.

**Pyrlik dkk. (2021), CERGE-EI WP (D11).**
- 9 saham MICEX, 2016–2020; rolling per kuartal.
- Lasso dan HAR-RV terbaik; **GB terburuk**. Model terbaik berganti antarkuartal (win-rate, Tabel 2).
- Hanya RMSE; tanpa uji statistik perbandingan.

**Zanotti (2025), MLWA (F6).** M5 dan VN1 (ritel); 10 model termasuk LightGBM. Latih ulang lebih jarang mempertahankan akurasi sambil menekan biaya. Frekuensi optimal sekitar 3–4 minggu (M5) dan 8–10 minggu (VN1) (hlm. 8). **Domain ritel**, bukan keuangan.

**Makridakis dkk. (2022), M5 (I5).**
- LightGBM dipakai oleh seluruh 50 tim teratas (hlm. 1346). Semua metode teratas murni ML (*Finding 1*, hlm. 1355–1356).
- Keunggulan didukung *cross-learning* dari banyak deret dan variabel eksogen (*Finding 3*).
- Batasan: kondisinya berbeda dari riset ini (42.840 deret ritel, bukan satu deret RV).

**Nadarajah dkk. (2025), JRFM (D12).** BTC/ETH/LTC harian; GARCH vs GBM/XGBM/LightGBM (setelan bawaan) vs ANFIS; XGBM terbaik. Batasan: tanpa HAR atau RV intraday; target ML tidak didefinisikan eksplisit; tanpa uji signifikansi.

**Dokumentasi LightGBM (I6; versi "latest" 4.7.0.99; kutip versi yang sama dengan `.venv`).** *Features:* pada jumlah daun yang sama, leaf-wise umumnya mencapai loss lebih rendah tetapi dapat overfitting pada data kecil. *Parameters Tuning:* `num_leaves` dan `min_data_in_leaf` adalah parameter utama pencegah overfitting.

**Feng, Zhang & Wang (2024), J. Forecasting — F (F1).**
- RV 5 menit S&P 500 2000–2022; **HAR saja**, rolling vs expanding, strategi MoP.
- Rata-rata rolling ≈ expanding. Skema terbaik **berganti sepanjang waktu tetapi persisten** (hlm. 571). Saat resesi, expanding sedikit lebih baik (Tabel 10).
- ⚠ Angka MoP di Tabel 10 sulit dijelaskan secara aritmetika. Kutip temuan kualitatif saja.
- Novelty aman: tanpa ML, tanpa era, tanpa uji formal beda skema.

**Grinsztajn dkk. (2022), NeurIPS (I4).**
- 45 dataset. Model pohon (RF, GBT, XGBoost; **LightGBM tidak diuji**) mengungguli deep learning pada data **menengah (±10 ribu sampel)**.
- Kriteria seleksi: hanya data i.i.d. (deret waktu dibuang); **dataset dibuang bila model linear selisihnya kurang dari 5%** (hlm. PDF 3). Batas minimum 3.000 sampel dipakai di naskah; cek lokasinya karena belum tercatat di kartu.
- Implikasi: paper ini membuktikan pohon > deep learning, **bukan** pohon > model linear.

**Abdi & Ranaldo (2017), versi WP (B3).**
- Versi *two-day corrected*: nilai negatif dibatasi nol, lalu dirata-ratakan per bulan. **Kode sesuai.**
- Satu beda kecil: 27 hari bar tidak lengkap ikut masuk perhitungan likuiditas (opsional ditulis di keterbatasan).
- Jangan menyebut nomor persamaan paper (WP vs terbit bisa beda).

**Corwin & Schultz (2012), versi WP (B4).** Spread dua hari yang negatif diset nol, lalu dirata-ratakan per bulan (hlm. PDF 10). **Kode sesuai.** Penyesuaian overnight tidak perlu (BTC 24/7).

**Rabanser dkk. (2019), NeurIPS (J4).** Domain gambar. Uji KS per dimensi + Bonferroni adalah pembanding sederhana yang kompetitif, juga pada fitur asli (NoRed). Riset ini memakai **rata-rata statistik D** sebagai besaran, bukan p-value. Tulis itu sebagai pilihan desain sendiri.

**Diebold & Mariano (1995), NBER WP (H2).** H0: E[d_t] = 0. Loss tidak harus kuadratik, simetris, atau kontinu. Error boleh tidak normal, berautokorelasi, dan berkorelasi antarramalan (abstrak). Yang dibandingkan adalah **ramalan**, bukan model.

**Chen & Guestrin (2016) (I2).** Objektif teregularisasi dengan penalti jumlah daun (γ) dan L2 bobot daun (λ) (hlm. PDF 2). Tidak membandingkan dengan LightGBM.

**Breiman (2001) (I3).** Error konvergen seiring jumlah pohon, sehingga menambah pohon tidak menyebabkan overfit. Error bergantung pada kekuatan pohon dan korelasi antarpohon. **Setelan 300 pohon, minimum 20 per daun, dan 33% fitur bukan dari paper ini.** Itu keputusan desain di `config.py`.

**Pesaran & Timmermann (2007), versi Jan 2006 (F3).**
- Data pre-break menambah bias tetapi dapat menurunkan varians. Memakai sebagian data pre-break dapat optimal selama break tidak terlalu besar.
- Bila waktu dan besar break tidak diketahui, kombinasi window membantu (abstrak).
- Asumsinya regresor eksogen ketat. **Kasus autoregresif ada di Pesaran & Timmermann (2005)**, bukan paper ini.

**Kwiatkowski dkk. (1992), Cowles DP (H7).** "Terima akar unit (ADF) dan tolak stasioneritas (KPSS)" berarti ada akar unit (hlm. PDF 4). Ini persis aturan differencing di RQ2.

**Andrews (1991), Cowles DP (H4).**
- Bartlett: Ŝ_T = 1,1447 (α̂(1)T)^(1/3) (pers. 6.2). **Kode `andrews_bw` sesuai.**
- Penulis merekomendasikan kernel QS. Bartlett adalah pilihan desain.
- ⚠ Kalimat "di sampel terbatas Bartlett tidak selalu jauh tertinggal" belum tercatat di kartu.

**Dickey & Fuller (1979) (H6).** H0: ρ = 1, yang setara dengan "deret perlu di-differencing". Kode memakai versi *augmented* (Said & Dickey, 1984).

**Qiu dkk. (2025), Economic Modelling (D7).** 10 kripto Binance 5 menit; kombinasi ramalan HAR/rough volatility. **Lag HAR 1/7/30 karena kripto 24/7.** QLIKE tidak dipakai karena ada ramalan RV negatif (hlm. 6). Riset ini tidak punya masalah itu, karena model dilatih pada ln RV dan diberi batas bawah.

### III.5 Sintesis literatur

1. Karakteristik pasar Bitcoin berubah substansial (Do, 2026), tetapi tidak mulus: efisiensi berubah-waktu (Mokni dkk., 2024) dan konsep bisa berulang (Suárez-Cetrulo dkk., 2023). **Bukan kontribusi.**
2. ML vs HAR untuk volatilitas sudah banyak diteliti (Christensen dkk., 2023; Huang dkk., 2024; Dudek dkk., 2024; Feng, Qi & Lucey, 2024; Brauneis & Sahiner, 2026). Sebagian besar melaporkan hasil agregat untuk satu periode uji. Sebagian kecil melaporkan hasil per tahun atau per kuartal secara deskriptif, tanpa uji formal kestabilan (Kılıç, 2025; Pyrlik dkk., 2021). Studi ML untuk volatilitas kripto lain memakai GARCH sebagai pembanding, bukan HAR (Wang dkk., 2023; Nadarajah dkk., 2025). **Benchmarking saja bukan kontribusi.**
3. **Bukti keunggulan model pohon atas HAR tidak konsisten.**
   - Dengan input HAR saja, model pohon tidak mengalahkan HAR (Christensen dkk., 2023).
   - Model pohon terburuk di antara ML pada RV saham (Kılıç, 2025; Pyrlik dkk., 2021).
   - Pada BTC, HAR mengungguli LightGBM dengan QLIKE (Brauneis & Sahiner, 2026).
   - Keunggulan LightGBM atas HAR pada RV Bitcoin tidak signifikan menurut DM (Dudek dkk., 2025, preprint).
4. Kinerja relatif berubah antarperiode uji sudah dikenal (Tashman, 2000; Gama dkk., 2014), dan peringkat model bergantung pada periode uji (Christensen dkk., 2023; Pyrlik dkk., 2021). Alat ujinya sudah ada (Giacomini & Rossi, 2010; Martins & Perron, 2016; Rossi, 2013) dan sudah dipakai di kripto untuk VaR/ES (Trucíos & Taylor, 2023). **Menerapkan uji saja bukan kontribusi.**
5. Pilihan window dan frekuensi estimasi ulang berpengaruh (Akgun & Gulay, 2025; Chassot & Audrino, 2026). Skema terbaik berganti sepanjang waktu (Feng, Zhang & Wang, 2024). Data pre-break dapat tetap berguna (Pesaran & Timmermann, 2007). Di domain ritel, latih ulang yang lebih jarang dapat mempertahankan akurasi (Zanotti, 2025). **"Window berpengaruh" bukan kontribusi.**
6. Kepentingan fitur tidak stabil antarstudi dan antarperiode (Wang dkk., 2023 vs Feng, Qi & Lucey, 2024).
7. **Efisiensi return ≠ volatilitas tak teramalkan.** Uji efisiensi menyangkut harga/return (Yi dkk., 2023), sedangkan volatilitas sangat persisten (Corsi, 2009, hlm. 174).
8. **Rantai proxy dan loss:** Andersen & Bollerslev (1998) → QLIKE (Patton, 2011) → RV 5 menit (Liu dkk., 2015). DM sah untuk loss asimetris seperti QLIKE (Diebold & Mariano, 1995).
9. **Keunggulan model pohon pada data tabular** ditunjukkan relatif terhadap deep learning, pada dataset yang sengaja tidak bisa diselesaikan model linear (Grinsztajn dkk., 2022). Popularitas LightGBM di M5 terjadi pada puluhan ribu deret dengan *cross-learning* (Makridakis dkk., 2022). Keduanya tidak menjamin keunggulan atas HAR pada satu deret RV.
10. **Celah:** gabungan empat hal yang belum ditemukan dalam satu studi:
    - (a) uji **formal** kestabilan kinerja relatif ML terhadap HAR-RV pada RV Bitcoin lintas era;
    - (b) dekomposisi 2×2;
    - (c) asosiasi dengan karakteristik pasar dan pergeseran distribusi fitur;
    - (d) interaksi strategi pembaruan × era, dengan perlakuan window setara untuk HAR-RV.

---

## IV. Research Gap

Penelitian peramalan volatilitas Bitcoin umumnya melaporkan kinerja ML terhadap HAR sebagai satu hasil agregat untuk satu periode uji. Beberapa studi di pasar saham melaporkan hasil per periode secara deskriptif. Literatur *forecasting under instability* menunjukkan rata-rata dapat menyembunyikan perubahan kinerja relatif, dan pasar Bitcoin berubah substansial.

**Sejauh literatur yang diperiksa**, belum ditemukan penelitian yang:
1. menguji kestabilan kinerja relatif ML terhadap HAR **secara formal** pada RV Bitcoin, pada periode panjang lintas era pasar;
2. mengaitkan kinerja relatif itu dengan karakteristik pasar terukur;
3. mengevaluasi pengaruh strategi pembaruan model antarera dengan perlakuan window setara.

**Checklist novelty: selesai (semua dari PDF).**

| Paper | Hasil | Yang wajib diakui |
|---|---|---|
| Akgun & Gulay (2025) | Aman | Rolling vs expanding pada volatilitas kripto sudah ada (rinci untuk GARCH) |
| Chassot & Audrino (2026) | Aman | Skema fitting HAR menentukan hasil |
| Feng, Qi & Lucey (2024) | Aman | Variasi panjang rolling window sebagai robustness; kepentingan fitur berubah-waktu |
| Trucíos & Taylor (2023) | Aman | Fluctuation test sudah dipakai di kripto (VaR/ES) |
| Christensen dkk. (2023) | Aman | Peringkat ML vs HAR bergantung prediktor dan panjang data latih, tanpa uji kestabilan |
| Feng, Zhang & Wang (2024) | Aman | Skema terbaik HAR berganti sepanjang waktu; tanpa ML, tanpa era |
| Qiu dkk. (2025) | Aman | Kombinasi ramalan HAR/rough volatility di 10 kripto; tanpa ML pohon, tanpa uji kestabilan |
| **Dudek, Kasprzyk & Pełka (2025)** | **Aman** | **LightGBM untuk RV Bitcoin sudah ada** (preprint); satu periode uji, hiperparameter statis, satu skema expanding, data Senin–Jumat |
| **Brauneis & Sahiner (2026)** | **Aman** | **LightGBM vs HAR pada BTC sudah ada** (QLIKE, DM); satu tahun data, RV 6 jam, tanpa evaluasi sepanjang waktu |
| **Kılıç (2025)** | **Aman** | **Evaluasi ML vs HAR per tahun sudah ada** (MCS/DM per tahun, deskriptif); S&P 500, tanpa uji formal kestabilan, satu skema pembaruan |
| **Pyrlik dkk. (2021)** | **Aman** | **Model terbaik berganti antarkuartal sudah dilaporkan** (win-rate); saham Rusia, hanya RMSE, tanpa uji statistik |
| **Nadarajah dkk. (2025)** | **Aman** | Ensemble pohon untuk volatilitas kripto; pembanding GARCH, bukan HAR |

---

## V. Rancangan Penelitian (seperti diimplementasikan)

> Bagian ini mengikuti kode final (`rvlib/`, config hash `0af5b5b98c60`). **Tidak berubah dari v2.8**, kecuali catatan sitasi bertanda (v2.9).

### 1. Data

| Komponen | Keputusan |
|---|---|
| Sumber | Binance Public Data (data.binance.vision), arsip bulanan klines, checksum diverifikasi |
| Pair | BTC/USDT spot (berkas `BTCUSDT`, folder `spot`) |
| Resolusi | 5 menit (288 bar per hari UTC) |
| Periode | **17 Agu 2017 – 30 Sep 2026**: 957.865 bar, 3.332 hari (tanggal mulai Binance juga dipakai Trucíos & Taylor, 2023) |
| OOS | Mulai **1 Sep 2018** (S0/S1/S2-365): 2.914 hari (transition 829, institutional 2.085) |
| Volume dolar | *Quote asset volume* (USDT) |

**Kenapa spot:** histori sejak 2017 (perpetual ~Sep 2019); tanpa efek funding/likuidasi/basis; keterbandingan literatur.

**Kenapa 5 menit:** kompromi noise vs presisi (Andersen & Bollerslev, 1998; Liu dkk., 2015). Preseden kripto 5 menit: Dudek dkk. (2024), Feng, Qi & Lucey (2024), Qiu dkk. (2025, Binance).

**Kelebihan:** satu venue sepanjang periode. Ini juga menghindari masalah penyambungan bursa seperti di Do (2026, hlm. 3).

**Kenapa 7 hari per minggu (v2.9):** kripto diperdagangkan 24/7. Dudek dkk. (2025) membuang akhir pekan; riset ini tidak.

**Audit (sesuai kode):**
- Timestamp **mikrodetik → milidetik** (arsip sejak 1 Jan 2025).
- Hari dengan bar < 95% (< 274/288) ditandai (**27 hari**).
- Pasangan (t, t+1) dibuang bila t atau t+1 tidak lengkap atau RV = 0, tanpa interpolasi. Hari ekstrem dipertahankan.
- Bar volume nol dikecualikan dari Amihud.
- **5 penanda peristiwa:** crash Mar 2020, Terra (Mei 2022), FTX (Nov 2022), flash crash 17 Agu 2023, "10/10" (10 Okt 2025). Batas era 1 Jan 2021.

### 2. Target
`RV_t = Σ_{i=1}^{288} r²_{t,i}` (realized **variance**); target `RV_{t+1}`; model dilatih pada `ln RV`.
- **Koreksi bias:** `exp(ŷ + σ̂²/2)`. σ̂² berasal dari residual 20% akhir window latih (model dilatih di 80% awal), lalu model dilatih ulang di seluruh window. Sensitivitas: tanpa koreksi. ⚠ Preseden Christensen dkk. (2023) belum tercatat di kartu.
- **Batas bawah ramalan:** persentil ke-1 RV window latih. ⚠ Preseden Christensen dkk. (2023) belum tercatat di kartu.

### 3. Fitur

| Kelompok | Fitur | Dipakai oleh |
|---|---|---|
| HAR | `ln RV_d`, `ln RV_w`, `ln RV_m` (1, 7, 30 hari; sensitivitas 1/5/22). Preseden lag 1/7/30 untuk kripto 24/7: Qiu dkk. (2025) | Semua |
| X | Proporsi RS⁻/RV; return harian; log volume dolar; Δ log volume; log range Parkinson | HAR-X, LGBM-X |
| X | Log realized Amihud | **LGBM-X saja** (VIF window awal 19,6) |

### 4. Model: desain 2×2

| | Input HAR | Input HAR + X |
|---|---|---|
| **Linear (OLS)** | HAR (baseline) | HAR-X |
| **Non-linear (LightGBM)** | LGBM-HAR | LGBM-X |

Ditambah naive (sanity check) dan Random Forest **hanya sebagai sensitivitas**. RF mengikuti Breiman (2001), memakai input LGBM-X, dengan setelan desain sendiri: 300 pohon, minimum 20 per daun, 33% fitur.

**Implementasi LightGBM:** objective regresi kuadrat, boosting standar (gbdt) + **bagging 80% per pohon** sebagai regularisasi. **GOSS tidak dipakai**; EFB tidak berperan (9 fitur padat). Dengan `num_leaves` = 3, setiap pohon hanya punya dua pemecahan, sehingga beda leaf-wise dan level-wise praktis hilang. Pada RV Bitcoin, GOSS juga tidak lebih baik dari GBDT standar (Dudek dkk., 2025, preprint, hlm. PDF 24) (v2.9).

**Kenapa LightGBM:**
1. Model pohon mengungguli deep learning pada data tabular menengah (Grinsztajn dkk., 2022). Ini dasar pemilihan kelas model, bukan jaminan kinerja, karena data latih riset ini 365 hingga ±2.900 baris deret waktu.
2. Akurasi hampir sama dengan XGBoost (Ke dkk., 2017), yaitu GBDT dengan regularisasi L2 (Chen & Guestrin, 2016).
3. Arahan pembimbing (ML non-deep).
4. Penulis Feng, Qi & Lucey (2024, hlm. 13) menyarankan pengujian LightGBM untuk volatilitas Bitcoin.
5. *(Opsional, v2.9)* LightGBM dipakai seluruh 50 tim teratas M5 (Makridakis dkk., 2022, hlm. 1346). Wajib disertai batasan: konteksnya banyak deret dengan *cross-learning*.

Kecepatan bukan alasan.

**Antisipasi (v2.9, dirumuskan ulang agar sesuai kartu):**
- Dengan input HAR saja, GB lebih buruk dari HAR (Christensen dkk., 2023, Tabel 2).
- Model pohon terburuk saat krisis 2008 (Kılıç, 2025, Tabel 2).
- LSTM dan RF paling tidak akurat pada hari RV tertinggi, secara deskriptif (Dudek dkk., 2024, hlm. 10).

Transformasi log mengurangi masalah skala.

### 5. Tuning
- Hanya window awal (target < 1 Sep 2018; ±339 observasi), validasi berurutan waktu (*forward-chaining*) 5 fold, QLIKE pada exp(ŷ). Validasi silang acak tidak dipakai karena memutus urutan waktu (Cerqueira dkk., 2020, hlm. 1998).
- Grid:
  - num_leaves {3, 7, 15};
  - min_child_samples {10, 20, 40, 80};
  - n_estimators {50, 100, 300, 600};
  - lr 0,03;
  - reg_lambda {1, 10} (penalti L2 bobot daun; Chen & Guestrin, 2016).

  Perluasan tepi grid maksimal 2 kali; batas bawah min_child_samples 5.
- **Terkunci:**
  - LGBM-HAR: leaves 3, min_child 10, n_est 300, lr 0,03, λ 1.
  - LGBM-X: leaves 3, min_child **5 (batas bawah)**, n_est 300, lr 0,03, λ 1.
- Tidak ada scaler/standarisasi.

### 6. Strategi pembaruan (latih ulang bulanan)

| Kode | Strategi | Istilah literatur |
|---|---|---|
| S0 | Static | Updating tanpa rekalibrasi (Tashman, 2000); pembanding manfaat adaptasi (Žliobaitė dkk., 2015, hlm. 243) |
| S1 | Expanding | Landmark window (Gama dkk., 2014) |
| S2 | Rolling W ∈ {365, 730}; eksploratori 180, 1095, rolling tertunda | Sliding window |

Perlakuan setara untuk HAR (Chassot & Audrino, 2026). Uji formal di S2 (Giacomini & Rossi, 2010; Rossi, 2013; Tashman, 2000).

**Latih ulang bulanan (v2.9):** kompromi akurasi dan biaya. Di domain ritel, latih ulang periodik dapat mempertahankan akurasi (Zanotti, 2025). Tulis sebagai analogi lintas domain, bukan bukti di data keuangan.

### 7. Evaluasi
- **Loss:** QLIKE (utama), MSE (pelengkap).
- **HAC:** Bartlett (Newey & West, 1987) + bandwidth otomatis Andrews (1991), replika `sandwich::kernHAC(prewhite=FALSE)`, identik dengan R.

| Hipotesis | Uji konfirmatori |
|---|---|
| H1 | UDmax rata-rata ΔL(LGBM-X − HAR), S2-365, QLIKE, HAC, ε 0,15, M 5; nilai kritis disimulasikan (CV 5% 9,01). Bila tidak menolak → DM. Urutan UDmax lalu uji berurutan mengikuti Bai & Perron (2003, hlm. 16) |
| H2a | Uji-F bersama HAC, regresi ΔL bulanan pada 4 karakteristik (+ dummy era) |
| H2b | Dua uji-t HAC beda era kontribusi fitur X; Holm |
| H3 | Uji-t HAC dua sisi rata-rata D_t, era institutional |

**Variabel RQ2:**
- rata-rata ln RV;
- SD ln RV;
- spread Abdi–Ranaldo *two-day corrected* rata-rata bulanan (sensitivitas Corwin–Schultz);
- rata-rata D^KS (PSI deskriptif).

**Stasioneritas:** differencing bila ADF gagal menolak **dan** KPSS menolak, yaitu kombinasi "ditemukan akar unit" (Kwiatkowski dkk., 1992; Dickey & Fuller, 1979).

**Sensitivitas belum dijalankan:** RV 5 menit subsampled; retuning tahunan. Jalankan, atau tulis sebagai keterbatasan.

### 8. Kontrol leakage
- Fitur t hanya memakai data s.d. akhir t.
- Tuning hanya di window awal.
- σ̂² dan batas bawah dihitung dari window latih.
- Batas era bukan fitur.
- Pasangan konfirmatori tidak dilihat saat pilot.

---

## VI. Rumusan Masalah, Tujuan, Hipotesis (terkunci, tidak berubah)

| | Rumusan masalah | Hipotesis |
|---|---|---|
| RQ1 | Sejauh mana kinerja relatif LightGBM terhadap HAR-RV stabil sepanjang periode pengujian? | H1: rata-rata ΔL(LGBM-X − HAR) tidak konstan |
| RQ2 | Apakah variasinya berasosiasi dengan karakteristik pasar dan pergeseran distribusi fitur? | H2a: ΔL berasosiasi dengan ≥1 karakteristik. H2b: kontribusi fitur X berbeda antarera |
| RQ3 | Apakah strategi pembaruan dan panjang window memengaruhi kinerja relatif secara berbeda antarera? | H3: di era institutional, rolling > expanding bagi ML (rata-rata D_t < 0) |

**Dasar H3:**
- Trade-off bias–varians (Pesaran & Timmermann, 2007). Rolling lebih baik bila break besar dan berulang (Rossi, 2013, hlm. 1230).
- Pasar Bitcoin berubah antarera (Do, 2026).

**Hipotesis tandingan:**
- Data pre-break dapat tetap berguna (Pesaran & Timmermann, 2007).
- Untuk model autoregresif, data pre-break dapat menurunkan bias dan varians sekaligus (Pesaran & Timmermann, 2005, via Rossi, 2013, hlm. 1230).
- Konsep bisa berulang (Gama dkk., 2014; Suárez-Cetrulo dkk., 2023).

---

## VII. Status Eksekusi dan Ringkasan Hasil

> **Tidak untuk Bab I–III.** Rincian di `hasil_eksperimen_bitcoin_v2_5.md`. Angka hasil tidak berubah dari v2.8.

**Sanity (QLIKE, S2-365):** Naive 0,5293 · HAR **0,3592** · HAR-X 0,3627 · LGBM-HAR 0,3968 · LGBM-X 0,3761.

| Hipotesis | Hasil | Rumusan Bab IV |
|---|---|---|
| H1 | UDmax 4,78 (CV 9,01), p 0,37; 0 break; DM mean ΔL +0,0169, p 0,25 | Tidak didukung; tidak ada bukti perubahan; daya memadai hanya untuk pergeseran ≥ ~1–2 sd |
| H2a | F 0,81, p 0,52 (CS p 0,47) | Tidak didukung |
| H2b | p Holm 0,53 | Tidak didukung |
| H3 | Mean D +0,0241, t 2,37, p 0,018 | **Tidak didukung; arah sebaliknya signifikan (expanding lebih baik).** Jangan tulis "H3 ditolak" |

**Eksploratori kunci:**
- S0 memburuk tajam, jadi retraining wajib.
- Efek RQ3 bertahan tanpa 20 hari ekstrem, tetapi **tidak bertahan dengan MSE**.
- Kurva window monoton: makin panjang makin baik bagi LGBM-X.
- Loss HAR datar di semua window.

**Hubungan dengan literatur untuk Bab V** (v2.9: baris baru ditandai ✚):

| Temuan | Pembanding | Batasan saat menulis |
|---|---|---|
| LGBM-HAR dan LGBM-X kalah dari HAR | Christensen dkk. (2023): dengan input HAR saja RF ≈ HAR, GB lebih buruk (Tabel 2) | Saham DJIA, MSE |
| ✚ (sama) | Brauneis & Sahiner (2026): pada BTC, HAR > LightGBM dengan QLIKE, DM signifikan (hlm. 406) | RV 6 jam, satu tahun data, uji ±73 hari |
| ✚ (sama) | Kılıç (2025) dan Pyrlik dkk. (2021): model pohon (XGBoost/GB) terburuk di antara ML pada RV saham | Keduanya WP; Pyrlik hanya RMSE tanpa uji |
| ✚ (sama) | Dudek dkk. (2025): keunggulan LightGBM atas HAR pada RV Bitcoin tidak signifikan menurut DM, kecuali satu perbandingan | Preprint; MSE/MAE, tanpa QLIKE |
| (sama) | Grinsztajn dkk. (2022): bukti keunggulan pohon hanya vs deep learning, pada data yang tidak bisa diselesaikan model linear | — |
| Kekalahan LightGBM saat lonjakan | QLIKE menghukum under-forecast (Patton, 2011). ✚ XGBoost jatuh paling parah saat krisis 2008 (Kılıç, 2025, Tabel 2) | ⚠ "GB peka outlier" (Christensen) belum tercatat di kartu |
| Expanding > rolling-365 bagi LightGBM | Pesaran & Timmermann (2007): data pre-break dapat tetap berguna. Chassot & Audrino (2026): window optimal 2,5–4 tahun (untuk HAR) | Chassot: window untuk HAR, bukan ML |
| HAR tidak peka panjang window | Feng, Zhang & Wang (2024): rata-rata rolling ≈ expanding untuk HAR. Kontras linear vs non-linear bisa ditonjolkan | S&P 500 |
| S0 memburuk; latih ulang bulanan cukup | Žliobaitė dkk. (2015): S0 sebagai pembanding manfaat adaptasi. ✚ Zanotti (2025): latih ulang periodik mempertahankan akurasi | Zanotti domain ritel |
| H1 tidak menolak | Trucíos & Taylor (2023): Fluctuation test BTC sebagian besar tidak signifikan | Konteks VaR/ES, bukan RV |
| ✚ Model terbaik bisa berganti tanpa perubahan rata-rata yang signifikan | Pyrlik dkk. (2021): model terbaik berganti antarkuartal (deskriptif). Kılıç (2025): peringkat per tahun berubah | Perbedaan: riset ini memakai uji formal |

---

## VIII. Ide Tambahan

| No | Ide | Status |
|---|---|---|
| 1 | Kurva panjang window | ✅ Eksploratori |
| 2 | Rolling tertunda | ✅ Eksploratori |
| 3 | Early warning pergeseran fitur | Belum |
| 4 | Replikasi ETH/USDT spot | Belum — tambahan termurah bila paper diincar Q2. Brauneis & Sahiner (2026) menunjukkan hasil ML vs HAR berbeda antaraset |
| 5 | Horizon 5/22 hari | Belum (keunggulan ML membesar di horizon panjang: Christensen dkk., 2023, hlm. PDF 36) |
| 6 | Kombinasi ramalan rolling+expanding / switching | Belum (Feng, Zhang & Wang, 2024; Qiu dkk., 2025) |
| 7 | Dashboard pemantauan | Tergantung arahan pembimbing |
| 8 | Fluctuation μ = 0,1; HAR WLS | Opsional |
| 9 | HAR nonlinear (THAR/STHAR) sebagai pembanding tambahan | Opsional (Kılıç, 2025); di luar desain terkunci, hanya eksploratori |

---

## IX. Risiko dan Mitigasi

| Risiko | Mitigasi |
|---|---|
| "ML tidak unggul, apa kontribusinya?" | Hasil negatif valid. Kontribusinya ada pada uji kestabilan, dekomposisi, dan strategi pembaruan. Sejalan dengan Christensen dkk. (input HAR saja), Chassot & Audrino, dan Brauneis & Sahiner (BTC, QLIKE) |
| ✚ "Dudek dkk. 2025 sudah pakai LightGBM untuk Bitcoin" | Akui. Bedanya: paper itu preprint, satu periode uji, data Senin–Jumat, tanpa uji kestabilan, tanpa variasi strategi window, tanpa QLIKE |
| ✚ "Kılıç sudah evaluasi per tahun" | Akui. Bedanya: S&P 500, deskriptif per tahun (MCS/DM), tanpa uji formal perubahan rata-rata ΔL, satu skema pembaruan |
| "UDmax tidak menolak = stabil?" | Tidak. Tulis "tidak ditemukan bukti perubahan", disertai analisis daya |
| RQ3 hanya di QLIKE | Wajib disebut. QLIKE (kesalahan relatif, hari tenang) vs MSE (didominasi lonjakan) |
| "Kenapa bisa pakai QLIKE padahal Qiu dkk. tidak?" | Model dilatih pada ln RV + batas bawah, sehingga ramalan selalu positif |
| "Andrews merekomendasikan QS, kenapa Bartlett?" | Bartlett = Newey–West; kovarians dijamin *positive semi-definite*; paling umum dipakai. ⚠ Kutipan "DM menyebut Bartlett sah" dan "di sampel terbatas tidak jauh tertinggal" belum tercatat di kartu; cek PDF sebelum dikutip |
| "Kenapa bagging, bukan GOSS?" | GOSS dirancang untuk mempercepat pelatihan pada data besar (Ke dkk., 2017), sedangkan data latih riset ini hanya ratusan hingga ribuan baris. Bagging dipakai sebagai regularisasi. ✚ Pada RV Bitcoin, GOSS tidak lebih baik dari GBDT standar (Dudek dkk., 2025, preprint) |
| "Grinsztajn untuk data i.i.d., data Anda deret waktu kecil" | Dipakai sebagai dasar kelas model, bukan jaminan kinerja; ditulis eksplisit di Bab II |
| Hyperparameter terkunci (Feng, Qi & Lucey memakai tuning harian) | Kestabilan sebuah metode hanya terukur bila setelannya tetap. Dudek dkk. (2025) juga mencari hiperparameter sekali |
| min_child_samples LGBM-X di batas bawah | Keputusan desain; sebut terbuka |
| Koreksi bias mungkin merugikan LightGBM | Tanpa koreksi, ΔL turun ke +0,004. Tulis satu paragraf tentang keadilan prosedur |
| **Sumber data: tugas pembimbing cron Indodax vs arsip Binance** | **Klarifikasi di bimbingan**: cron hanya maju ke depan, tidak mencakup 2017–2026 |
| Judul belum final | Kandidat 1 dipakai sementara |

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
| Acuan | Dudek dkk. (2024); Chassot & Audrino; Christensen dkk.; Feng, Zhang & Wang |
| ✚ Beda dengan studi terdekat | Dudek dkk. (2025), Brauneis & Sahiner (2026), Kılıç (2025): apa yang sudah mereka lakukan dan apa yang belum |
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
| Verifikasi literatur & novelty | ✅ 54 referensi `.bib` + 8 paper baru dibaca (16 Okt) |
| Eksperimen | ✅ 6 Okt 2026 |
| Praskripsi Bab I–III | ✅ Draf; **revisi teks di Lampiran A** |
| Bimbingan (judul, sumber data, output sistem, pembimbing II, jadwal) | ⏳ |
| Bab IV–V | Setelah praskripsi disetujui |

**Daftar kerja:**
1. Terapkan revisi Lampiran A, lalu `make check`.
2. Tambah `pesaran2007` dan `lightgbmfeatures` ke `.bib`. Tambahkan key usulan hanya bila paper itu benar-benar dikutip di naskah (Lampiran B.1). Lengkapi `barndorff2010` (editor, DOI).
3. Rapikan Mendeley agar sama dengan `.bib` (Lampiran B.2).
4. **Klarifikasi Indodax vs Binance** di bimbingan.
5. Putuskan dua sensitivitas yang belum jalan.
6. Verifikasi:
   - tabel asli Bai–Perron (q = 1, ε = 0,15);
   - n per daun di perhitungan manual. Dugaan: bagging LightGBM memilih tiap baris dengan peluang 80%, sehingga jumlah per pohon berfluktuasi (pohon 1: 256, pohon 2: 272). Cek `leaf_count` beberapa pohon;
   - kuartil 2025 untuk ESWA, Economic Modelling, JASA, dan **7 usulan baru**;
   - versi LightGBM di `.venv` untuk URL dokumentasi;
   - ✚ **klaim ⚠** di dokumen ini (Christensen: koreksi bias, batas bawah, GB peka outlier; Andrews: Bartlett di sampel terbatas; DM: menyebut Bartlett/Andrews; Grinsztajn: batas 3.000 sampel). Cek di PDF, lalu tambahkan ke kartu.
7. Lengkapi pembimbing II, jadwal, spesifikasi perangkat.

---

## Lampiran A. Revisi teks LaTeX

> Nomor baris perkiraan (repo per 10 Okt 2026). Setelah diterapkan, hapus `% CEK:` terkait.

### A.1 `% CEK:` yang bisa diselesaikan

| Lokasi | Tindakan |
|---|---|
| Bab 2 ±204 (Corsi, koefisien berubah) | Salah kutip; ganti dengan A.2 no. 13 |
| Bab 1 ±55 (Christensen) | Status B. Perinci: perbandingan luas ML vs HAR di saham DJIA, satu periode uji, loss MSE. Hapus CEK |
| Bab 1 ±71 (GR 2010, Trucíos) | Keduanya B, kalimat sesuai. Hapus CEK |
| Bab 1 ±89 (Feng 2024 dkk.) | Semua sudah dibaca; ganti kalimat Feng, Zhang & Wang (A.2 no. 1). Hapus CEK |
| Bab 2 ±30 (Feng, Qi & Lucey; Qiu) | Revisi A.2 no. 2 dan 3. Hapus CEK |
| Bab 2 Tabel posisi ±107 | Isi sel (A.3). Hapus CEK |
| Bab 2 ±311 (Grinsztajn, Chen) | Revisi A.2 no. 4. Hapus CEK |
| Bab 2 ±400 (DM, Andrews) | Revisi A.2 no. 6. Hapus CEK |
| Bab 2 ±438 (GR 2010) | Kutip langsung; tambahkan bahwa kerangka GW mensyaratkan rolling/fixed (hlm. 599). Hapus CEK |
| Bab 2 ±590 (Rabanser) | Revisi A.2 no. 7. Hapus CEK |
| Bab 3 ±571 (n per daun) | Tetap sampai `leaf_count` dicek (Bagian XII no. 6) |
| Bab 3 ±707 (tabel Bai–Perron) | Tetap |
| Bab 3 ±787 (sensitivitas belum jalan) | Tetap sampai diputuskan |
| ✚ Bab 1/2 semua kalimat yang menyebut Wang dkk. (2023) sebagai "ML vs HAR" | Ganti menjadi "ML vs GARCH" atau "ML untuk volatilitas kripto" |
| ✚ Bab 2/3 semua kalimat "forward-chaining \cite{cerqueira2020}" | Ganti dengan A.2 no. 15 |

### A.2 Usulan kalimat

1. **Bab 1 ±82 (Feng, Zhang & Wang):**
   ```latex
   Tidak ada skema yang selalu lebih unggul. Skema yang lebih akurat berganti
   sepanjang waktu, dan keunggulan relatifnya cenderung bertahan dalam periode
   tertentu \cite{feng2024window}.
   ```
2. **Bab 2 ±20 (Feng, Qi & Lucey):** ganti "kepentingan fitur berubah sejak Oktober 2022" dengan "kepentingan **indikator blockchain** meningkat sejak Oktober 2022". Objeknya volatilitas **Bitcoin (BTC/USD) 2017–2022**. Bila menyebut robustness, tulis "dengan panjang *rolling window* yang berbeda", bukan "rolling dan expanding".
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
   \cite{grinsztajn2022}. Benchmark tersebut memakai data i.i.d., sedangkan data
   latih penelitian ini berupa fitur lag deret waktu sebanyak 365 hingga sekitar
   2.900 baris. Karena itu, temuan tersebut dipakai sebagai dasar pemilihan
   kelas model, bukan jaminan kinerja.
   ```
   Kalimat "akurasinya setara dengan XGBoost" diganti "**hampir sama**" (`\cite{ke2017,chen2016}` tetap). Bila menyebut batas 3.000 sampel, cek lokasinya dulu.
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
   sama, dengan hipotesis nol $E[\Delta L_t] = 0$. Fungsi \textit{loss} yang
   dipakai tidak harus kuadratik maupun simetris \cite{diebold1995}.
   ```
7. **Bab 2 ±585 (KS, Rabanser):**
   ```latex
   Uji KS per fitur merupakan salah satu pendekatan sederhana untuk mendeteksi
   pergeseran data dan menjadi pembanding yang kompetitif terhadap metode yang
   lebih kompleks \cite{rabanser2019}. Berbeda dari penggunaan sebagai uji
   hipotesis, penelitian ini tidak memakai \textit{p-value}-nya. Nilai
   $D^{\text{KS}}$ dirata-ratakan antarfitur sebagai ukuran besaran pergeseran
   per bulan.
   ```
8. **Bab 2 ±526 (Pesaran & Timmermann)** — v2.9: kalimat rolling/rekursif hanya dikutip ke Rossi:
   ```latex
   Pilihan strategi melibatkan \textit{trade-off} bias dan varians. Menyertakan
   data sebelum perubahan struktural menambah bias tetapi dapat mengurangi
   varians kesalahan ramalan, sehingga memakai sebagian data tersebut dapat
   optimal selama perubahannya tidak terlalu besar \cite{pesaran2007}. Secara
   umum, \textit{rolling window} cenderung lebih baik ketika perubahan besar dan
   berulang, sedangkan skema rekursif (\textit{expanding}) lebih baik ketika
   perubahan kecil atau tidak ada \cite{rossi2013}. Untuk model autoregresif
   seperti HAR, data sebelum perubahan bahkan dapat mengurangi bias dan varians
   sekaligus \cite{rossi2013}.
   ```
9. **Bab 3 ±274 (LightGBM & RF):** tambahkan setelah butir LGBM:
   ```latex
   Penelitian ini menggunakan mode \textit{boosting} standar LightGBM dengan
   \textit{bagging} sebagai regularisasi. GOSS dan EFB dirancang untuk
   mempercepat pelatihan pada data besar dan fitur jarang, sehingga tidak
   berperan pada data latih yang hanya berisi ratusan hingga ribuan baris dengan
   sembilan fitur padat. Dengan \texttt{num\_leaves} = 3, setiap pohon hanya
   memiliki dua pemecahan sehingga perbedaan pertumbuhan \textit{leaf-wise} dan
   \textit{level-wise} praktis hilang.
   ```
   Butir RF:
   ```latex
   \item \textbf{Random Forest} \cite{breiman2001}, yaitu rata-rata banyak pohon
         regresi yang masing-masing dilatih pada sampel \textit{bootstrap} dengan
         pemilihan fitur acak di setiap pemisahan. Model ini memakai masukan yang
         sama dengan LGBM-X (300 pohon, minimum 20 observasi per daun, 33\% fitur
         per pemisahan) dan digunakan hanya sebagai uji sensitivitas jenis model
         pohon.
   ```
10. **Bab 3 ±747 (Corwin–Schultz):**
    ```latex
    Sebagai uji sensitivitas, estimator Corwin--Schultz \cite{corwin2012}
    digunakan sebagai pengganti. Penyesuaian harga \textit{overnight} pada
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
12. **Opsional Bab 3 (aturan teknis ±279):** `chen2016` saat menjelaskan `reg_lambda`. Christensen dkk. (2023) sebagai preseden koreksi bias dan batas bawah **hanya setelah lokasinya diverifikasi** (⚠).
13. **Bab 2 ±203–204 (Corsi, salah kutip):** ganti "Corsi juga memperlihatkan bahwa koefisien HAR dapat berubah sepanjang waktu \cite{corsi2009}, yang menjadi ..." dengan:
    ```latex
    Dalam evaluasi \textit{out-of-sample}, Corsi mengestimasi ulang model setiap
    hari pada jendela bergerak 1000 observasi \cite{corsi2009}, sedangkan kinerja
    relatif model peramalan dapat berubah sepanjang waktu \cite{rossi2013}, yang
    menjadi salah satu alasan stabilitas kinerja perlu diuji.
    ```
14. ✚ **Opsional Bab 1/2 (literatur ML vs HAR, paper baru).** Pakai hanya bila key sudah ditambah ke `.bib`:
    ```latex
    Hasil perbandingan model berbasis pohon dengan HAR juga tidak seragam.
    Pada Bitcoin, HAR lebih akurat daripada LightGBM menurut QLIKE, dan
    perbedaannya signifikan menurut uji DM, meskipun model ML lebih baik pada
    sebagian aset kripto lain \cite{brauneis2026}. Pada RV indeks saham,
    XGBoost menjadi model ML dengan kinerja terburuk, terutama pada periode
    krisis \cite{kilic2025}.
    ```
    Bila menyebut evaluasi per periode:
    ```latex
    Sebagian penelitian telah melaporkan kinerja model per tahun atau per
    kuartal \cite{kilic2025,pyrlik2021}, tetapi perubahan kinerja relatif
    tersebut tidak diuji secara formal.
    ```
    Bila menyebut Dudek dkk. (2025), tulis status preprint dan jangan menyebutnya "membuktikan LightGBM unggul".
15. ✚ **Bab 2/3 (Cerqueira, istilah validasi):**
    ```latex
    Validasi silang acak tidak digunakan karena memutus urutan waktu
    \cite{cerqueira2020}. Tuning dilakukan dengan validasi berurutan waktu
    (\textit{forward-chaining}), yaitu setiap lipatan dilatih pada data sebelum
    lipatan validasinya.
    ```
    Kerangka S1/S2 dapat disebut sebagai bentuk *prequential in blocks* dengan window bertambah atau bergeser \cite{cerqueira2020}.

### A.3 Tabel posisi Bab 2

| Penelitian | Objek | Pembanding HAR | Evaluasi sepanjang waktu | Variasi strategi window | Asosiasi kondisi pasar |
|---|---|---|---|---|---|
| Feng, Qi & Lucey | RV BTC/USD, 2017–2022 | Ya | Kepentingan fitur antarperiode | Hanya panjang rolling window (robustness) | Tidak |
| Chassot & Audrino | RV 1.445 saham AS, 2015–2023 | Ya | Tidak (grafik selisih error kumulatif, tanpa uji) | Ya (window & frekuensi estimasi ulang HAR; ML statis) | Tidak (hanya per kapitalisasi) |
| ✚ *(opsional)* Brauneis & Sahiner | RV 6 jam 8 kripto, 2021–2022 | Ya | Tidak (agregat) | Tidak (moving window) | Tidak (sentimen sebagai fitur) |
| ✚ *(opsional)* Kılıç | RV S&P 500, uji 2006–2023 | Ya (+ HAR nonlinear) | Deskriptif per tahun (MCS/DM), tanpa uji kestabilan | Tidak (expanding tahunan) | Tidak |
| *(opsional)* Christensen dkk. | RV saham DJIA, 2001–2017 | Ya | Tidak (agregat) | Tidak | Tidak |
| *(opsional)* Feng, Zhang & Wang | RV S&P 500, 2000–2022 | Ya (HAR saja, tanpa ML) | Tidak | Ya (rolling vs expanding, switching) | Sebagian (resesi/ekspansi, deskriptif) |

---

## Lampiran B. Metadata, `.bib`, dan Mendeley

### B.1 Entri `.bib`

**Belum ada di repo (sudah dipakai di naskah):**

```bibtex
@article{pesaran2007,
  author  = {Pesaran, M. Hashem and Timmermann, Allan},
  title   = {Selection of Estimation Window in the Presence of Breaks},
  journal = {Journal of Econometrics},
  volume  = {137}, number = {1}, pages = {134--161}, year = {2007},
  doi     = {10.1016/j.jeconom.2006.03.010}
}
@online{lightgbmfeatures,
  author = {{Microsoft Corporation}}, title = {Features},
  organization = {LightGBM Documentation}, version = {4.x.x},
  url = {https://lightgbm.readthedocs.io/en/v4.x.x/Features.html},
  urldate = {2026-10-12}
}
```
Ganti `4.x.x` dengan hasil `pip show lightgbm` di `.venv` (atau pakai `/en/stable/` tanpa `version`). Samakan versinya dengan `lightgbmtuning`.

**Usulan key paper baru:** tambahkan hanya bila dikutip. Metadata diambil dari PDF yang dibaca; **verifikasi DOI lewat Crossref** sesuai aturan repo.

| Key | Jenis | Metadata dari PDF |
|---|---|---|
| `brauneis2026` | `@article` | Brauneis, Alexander; Sahiner, Mehmet. *Crypto Volatility Forecasting: Mounting a HAR, Sentiment, and Machine Learning Horserace*. Asia-Pacific Financial Markets 33, 379–411, 2026 |
| `dudek2025lgbm` | `@misc` (arXiv) | Dudek, Grzegorz; Kasprzyk, Mateusz; Pełka, Paweł. *Multivariate Forecasting of Bitcoin Volatility with Gradient Boosting: Deterministic, Probabilistic, and Feature Importance Perspectives*. arXiv:2511.20105, 2025 |
| `kilic2025` | `@techreport` | Kılıç, Rehim. *Linear and nonlinear econometric models against machine learning models: realized volatility prediction*. Finance and Economics Discussion Series 2025-061, Board of Governors of the Federal Reserve System, 2025 |
| `pyrlik2021` | `@techreport` | Pyrlik, Vladimir; Elizarov, Pavel; Leonova, Aleksandra. *Forecasting Realized Volatility Using Machine Learning and Mixed-Frequency Data (the Case of the Russian Stock Market)*. CERGE-EI Working Paper 713, 2021 |
| `nadarajah2025` | `@article` | Nadarajah, Saralees; Mba, Jules Clement; Rakotomarolahy, Patrick; Ratolojanahary, Henri T. J. E. Journal of Risk and Financial Management 18(2), 52, 2025 (judul: ambil dari PDF/Crossref) |
| `zanotti2025` | `@article` | Zanotti, Marco. *On the retraining frequency of global models in retail demand forecasting*. Machine Learning with Applications 22, 100769, 2025 |
| `makridakis2022` | `@article` | Makridakis, Spyros; Spiliotis, Evangelos; Assimakopoulos, Vassilios. *M5 accuracy competition: Results, findings, and conclusions*. International Journal of Forecasting 38(4), 1346–1364, 2022 |

`barndorff2010`: tambah `editor = {Bollerslev, Tim and Russell, Jeffrey R. and Watson, Mark W.}` dan `doi = {10.1093/acprof:oso/9780199549498.003.0007}` (cek Crossref).

### B.2 Perbaikan Mendeley

| Entri | Perbaikan |
|---|---|
| Holm (1979) | Judul → *A Simple Sequentially Rejective Multiple Test Procedure* |
| Newey & West (1987) | Penulis → Newey, Whitney K.; West, Kenneth D. |
| Andersen & Bollerslev (1998) | Penulis → Andersen, Torben G.; Bollerslev, Tim |
| Bai & Perron (1998) | Sumber → Econometrica |
| Corsi (2009) | Versi jurnal: *A Simple Approximate Long-Memory Model of Realized Volatility*, JFEC 7(2), 174–196, DOI 10.1093/jjfinec/nbp001; lampirkan PDF jurnal |
| Christensen dkk. | Tahun 2026 → **2023**, JFEC 21(5), 1680–1727 |
| Ke dkk. (2017) | Tipe → Conference Proceedings (NeurIPS 30) |
| Microsoft Corporation | Judul → **Parameters Tuning** |
| Barndorff-Nielsen (2010) | Tipe Book Section + editor |
| Al-Yahyaee (2020), Teller (2026) | Hapus/pisahkan (tidak dipakai) |
| Entri kurang | Tambah 12: Abdi & Ranaldo, Corwin & Schultz, Dickey & Fuller, KPSS, Diebold & Mariano, Andrews, Grinsztajn, Chen & Guestrin, Rabanser, Qiu, Pesaran & Timmermann, Breiman |
| ✚ Paper baru | Masukkan ke collection terpisah ("pembanding") sampai diputuskan dikutip |

Format nama: *Nama belakang, Nama depan*; urutan penulis sama persis dengan paper.

### B.3 Catatan lain
- Kutip **versi terbit** untuk semua yang dibaca versi WP/arXiv (Barndorff-Nielsen, Christensen, Abdi & Ranaldo, Corwin & Schultz, Diebold & Mariano, Andrews, KPSS, Pesaran & Timmermann, Breiman, Chen & Guestrin, Grinsztajn, Rabanser). Jangan menyebut nomor persamaan atau tabel bila versi yang dibaca berbeda.
- Dudek dkk. (2025), Kılıç (2025), dan Pyrlik dkk. (2021) **belum terbit di jurnal**. Kutip sebagai preprint/working paper dan jangan dijadikan satu-satunya dasar klaim utama.
- Rossi (2013): cek nama editor handbook. Oprea & Bâra (2026): cek volume/halaman.
- Kuartil di dokumen ini SJR 2025; tulis tahunnya bila disebut di naskah.
- Format sitasi: IEEE (biblatex).
