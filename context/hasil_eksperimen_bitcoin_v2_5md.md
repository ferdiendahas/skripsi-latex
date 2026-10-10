# Hasil Eksperimen Skripsi v2.5: Kelayakan, Source Code Final, dan Kesimpulan

> **Fungsi file ini:** konteks lengkap hasil eksekusi desain riset v2.5 (`hasil_riset_bitcoin_v2_5.md`). Berisi kronologi pilot → uji kelayakan → eksperimen penuh, hasil final yang sudah diverifikasi, kesimpulan per RQ, batasan, keputusan yang terkunci, dan **source code final lengkap** (paket `skripsi_rv`).
>
> **Status per 6 Oktober 2026:** eksperimen penuh selesai di data asli. Uji konfirmatori sudah dijalankan, sehingga **RQ, hipotesis, dan judul tidak boleh diubah mengikuti hasil** (menghindari HARKing). Perubahan apa pun setelah ini ditulis sebagai eksploratori.
>
> **Notasi:** BTC/USDT = pasar spot (yang dipakai). BTCUSDT tanpa garis miring hanya muncul sebagai nama simbol file arsip Binance.

---

## 1. Jawaban singkat

**Apakah penelitian ini bisa dilakukan? Ya.** Data lengkap dan terverifikasi, pipeline benar (lolos sanity check), semua uji konfirmatori dan eksploratori berjalan, dan hasilnya bisa dibela.

**Jawaban satu kalimat untuk pertanyaan utama:** keunggulan LightGBM atas HAR-RV dalam meramal realized variance Bitcoin **tidak terdeteksi muncul-hilang** mengikuti waktu atau kondisi pasar, dan LightGBM **tidak terbukti lebih unggul**; yang menentukan kinerja relatifnya adalah **cara model diperbarui**, yaitu pelatihan ulang wajib dan data latih yang lebih panjang (expanding) lebih menguntungkan, setidaknya menurut QLIKE.

---

## 2. Kronologi singkat

| Tahap | Isi | Hasil kunci |
|---|---|---|
| Pilot (folder `pilot/`, skrip 01–05) | HAR vs LGBM-HAR saja (pasangan eksploratori), S2-365, S1, S0, W730 | HAR unggul agregat (ΔL +0,0425, t 2,95); sup-F 1 break tidak menolak; S1 hampir setara (ΔL +0,0099); S0 rusak makin parah |
| Diagnostik pilot (05) | Ekor, ekstrapolasi, pratinjau RQ3 | Keunggulan HAR di S2-365 merata (median ΔL +0,0195), bukan dari hari ekstrem; 10 kekalahan terburuk LGBM semua *under-forecast* saat lonjakan; D institutional +0,029 (t 4,06) → expanding lebih baik |
| UDmax R (04) | Pasangan pilot | UDmax 2,98 harian, 3,99 bulanan → tidak menolak |
| Paket kelayakan (`pilot/kelayakan/`, 06–11) | VIF, tuning, kurva window, jumlah vs umur, daya, uji jalan RQ2 | Laporan: **LAYAK DENGAN PENYESUAIAN**. VIF ln_amihud 19,6 & ln_dvol 18,2; tuning terbaik di tepi grid; kesimpulan pilot bertahan setelah tuning; MDE UDmax 80% = 0,119 vs pergeseran terlihat 0,040 (daya rendah); efek jumlah data signifikan, efek umur tidak (pasangan pilot) |
| Diskusi opsi framing | A (pertahankan, laporkan MDE), B (RQ1 deskriptif, RQ3 fokus), C (geser ke kebutuhan data latih) | Diputuskan **menjalankan desain v2.5 apa adanya**. Setelah uji konfirmatori dijalankan, opsi C sebagai RQ utama baru **tidak lagi tersedia** (akan jadi HARKing); cerita "jumlah data" masuk sebagai pembahasan eksploratori |
| Eksperimen penuh (`skripsi_rv/`) | Desain 2×2, S0/S1/S2, semua uji v2.5, sensitivitas | Lihat Bagian 3 |
| Insiden data | Run kedua di folder lain menghasilkan QLIKE ~2,86, 0 hari tidak lengkap, n 2.952 | Dinyatakan **tidak sah**; hasil sah = folder pertama (27 hari tidak lengkap, n 2.914, QLIKE HAR 0,3592). Penyebab run rusak tidak teridentifikasi (kode identik; kemungkinan data/lingkungan) |
| Patch v1.1 | Butir 5–7: MSE untuk RQ3, stasioneritas ΔL, penanda peristiwa di grafik, + cek hari ekstrem D | Dijalankan di folder sehat tanpa menghitung ulang forecast; config hash tetap |
| Patch v1.2 | Penanda peristiwa 17 Agu 2023 dan 10/10 (10 Okt 2025) di grafik | Hanya `rvlib/analysis.py` (grafik); config hash dan semua uji tidak berubah |
| Verifikasi akhir | `skripsi_rv_2.zip` (hasil semua run) diperiksa | Semua 22 file kode **identik** dengan paket final + patch v1.1; data sehat (27 / 2.914 / 0,3592); config hash `0af5b5b98c60` sama saat forecast dan laporan |

**Catatan:** paper dosen pembimbing (Parlika et al.) **dikeluarkan dari pertimbangan** atas permintaan Ferdi (ditambahkan sendiri tanpa konfirmasi yang jelas). Konsekuensinya, jembatan RQ2 ke riset dosbing tidak dipakai sebagai argumen.

---

## 3. Hasil final (data asli, config hash `0af5b5b98c60`)

**Data:** BTC/USDT spot Binance, 5 menit, 957.865 bar, 3.332 hari (17 Agu 2017 – 30 Sep 2026), 27 hari bar < 95% (dibuang sesuai aturan audit), 0 hari RV = 0. OOS S2-365: 1 Sep 2018 – 30 Sep 2026, n = 2.914 hari (transition 829, institutional 2.085).

**Sanity (QLIKE rata-rata, S2-365):** NAIVE 0,5293 · HAR **0,3592** · HAR-X 0,3627 · LGBM-HAR 0,3968 · LGBM-X 0,3761. Semua model mengalahkan naive.

**Hyperparameter terkunci (window awal ~12 bulan, forward-chaining):**
- LGBM-HAR: num_leaves 3, min_child_samples 10, n_estimators 300, lr 0,03, reg_lambda 1 (CV QLIKE 0,3574)
- LGBM-X: num_leaves 3, **min_child_samples 5 (= batas bawah grid)**, n_estimators 300, lr 0,03, reg_lambda 1 (CV QLIKE 0,3187)

**Kolinearitas:** ln_amihud dibuang dari HAR-X (aturan v2.5 V.3); VIF fitur X sisa maksimum 6,9.

### 3.1 Uji konfirmatori

| RQ | Uji | Statistik | p | Kesimpulan |
|---|---|---|---|---|
| RQ1 | UDmax ΔL(LGBM-X − HAR), S2-365, QLIKE, HAC Andrews, ε 0,15, M 5 | UDmax 4,78 (CV 5% simulasi 9,01; tabel BP ~8,88) | 0,370 | H1 tidak didukung |
| RQ1 lanjutan | DM rata-rata ΔL seluruh sampel | mean +0,0169, t +1,16 | 0,246 | tidak berbeda signifikan |
| RQ2 H2a | Uji-F bersama 4 karakteristik (Abdi-Ranaldo), HAC, 97 bulan | F 0,81, R² 0,038 | 0,520 | tidak didukung (Corwin-Schultz: F 0,89, p 0,471) |
| RQ2 H2b | Beda era kontribusi X: HAR-X−HAR / LGBM-X−LGBM-HAR | t −1,12 / −0,65 | 0,526 (Holm) | tidak didukung |
| RQ3 | D = ΔL(S2-365) − ΔL(S1), institutional | mean +0,0241, t +2,37 | 0,018 | **H3 ditolak; hipotesis tandingan signifikan: expanding lebih baik** |

### 3.2 Eksploratori penting

**RQ1**
- Uji break berurutan: supF(1|0) = 1,69 (p 0,873) → **0 break**.
- **Analisis daya UDmax** (blok 30 hari, 200 ulangan; sd rata-rata ΔL tahunan = 0,0704): daya 0,02 (δ=0), 0,15 (0,5 sd), **0,58 (1 sd = 0,070)**, 0,98 (2 sd), 1,00 (3–4 sd). Daya 80% baru tercapai di antara 1–2 sd.
- Per tahun ΔL: 2018 −0,142; 2019 −0,012; 2020 +0,093; 2021 −0,033; 2022 +0,069 (p 0,002); 2023 +0,069; 2024 −0,012; 2025 +0,013; 2026 −0,008. Proporsi hari LGBM-X unggul 31–51%.
- **S0 (tanpa pelatihan ulang)**: UDmax 19–25, ΔL LGBM-X +0,093 (DM t 5,17) → model basi rusak; kontras manfaat adaptasi, bukan bukti perubahan pasar.
- S1: LGBM-X vs HAR ΔL −0,0072 (t −0,67), tidak signifikan. HAR-X vs HAR di S1: −0,0057 (p 0,008; Holm 0,52).

**RQ3**
- **Tanpa 20 hari |D| terbesar: D +0,0148, t +3,35, p Holm 0,010** → efek **tidak** digerakkan segelintir hari ekstrem (hari ekstrem menyumbang ~40% besarnya).
- Grafik kumulatif D: kenaikan terkonsentrasi di lonjakan Maret 2020, pertengahan 2022 – pertengahan 2023 (pasca-Terra/FTX), serta dua lompatan satu hari: **flash crash 17 Agustus 2023** dan **10/10 (10 Oktober 2025)**; di luar itu relatif datar. Lihat 3.4.
- **MSE: D institutional t −0,49 (p 0,625) → tidak bertahan dengan MSE.**
- Transition: D +0,024, t 1,15 (tidak signifikan).
- Dekomposisi D institutional: LGBM-HAR−HAR **+0,040 (t 4,55, Holm 8e-5)**; HAR-X−HAR ≈ 0; LGBM-X−LGBM-HAR −0,016 (ns); LGBM-X−HAR-X +0,024 (t 3,66, Holm 0,004). → **Efek strategi berasal dari komponen non-linear (LightGBM); model linear tidak peduli panjang window.**
- S2-730 vs S1: +0,020 (t 3,12, Holm 0,022) → bahkan 730 hari kalah dari expanding. S2-730 vs S2-365, S2-180 vs S2-365, S2-1095 vs S1: tidak signifikan.
- **Kurva window (periode bersama sejak Sep 2020):** ΔL S2-180 +0,020 → S2-365 +0,016 → S2-730 +0,013 → S2-1095 +0,002 → **S1 −0,006** (monoton turun). Loss HAR datar ~0,319; loss LGBM-X turun 0,352 → 0,313. HAR-X sedikit lebih baik dari HAR di semua window kecuali 180.
- **Jumlah vs umur data:** efek jumlah (S2-730 − S2-365) −0,0117, t −2,01, p 0,044 (Holm 0,40); efek umur (tertunda − S2-365) +0,0456, t +2,79, p 0,005 (Holm 0,058). → indikasi eksploratori: data lebih banyak membantu, data yang **hanya** lama merugikan. Berbeda dari pilot (LGBM-HAR: umur tidak signifikan).

**RQ2**
- Stasioneritas: level_vol di-differencing (ADF 0,49, KPSS 0,012); ΔL bulanan stasioner (ADF 0,000, KPSS 0,100).
- Tidak ada koefisien individual yang signifikan; era_inst tidak signifikan. Korelasi ΔL bulanan dengan PSI +0,10 (deskriptif).

### 3.3 Sensitivitas

| Variasi | n | mean ΔL | t DM | p UDmax | D inst. | t D |
|---|---|---|---|---|---|---|
| UTAMA | 2914 | +0,0169 | +1,16 | 0,370 | +0,0241 | +2,37 |
| tanpa 2026 | 2641 | +0,0194 | +1,21 | 0,465 | +0,0273 | +2,34 |
| hari tidak lengkap dipertahankan | 2952 | +0,0235 | +1,56 | 0,527 | +0,0335 | +2,00 |
| window awal 24 bulan | 2559 | +0,0280 | +1,64 | 0,467 | +0,0206 | +2,58 |
| lag 5/22 | 2914 | +0,0222 | +1,54 | 0,280 | +0,0144 | +1,59 |
| RF-X vs HAR | 2914 | +0,0135 | +0,84 | 0,440 | +0,0230 | +3,55 |
| RV 15 menit | 2914 | +0,0226 | +1,66 | 0,735 | +0,0303 | +2,37 |
| tanpa bias correction | 2914 | +0,0038 | +0,22 | 0,757 | +0,0257 | +1,89 |
| HAR re-estimasi harian | 2914 | +0,0155 | +1,03 | 0,441 | — | — |

Ringkas: RQ1 tidak menolak di semua variasi; arah D positif di **ketujuh** variasi yang punya D, signifikan di **5** (lag 5/22 t 1,59 dan tanpa bias correction t 1,89 tidak).

### 3.4 Peristiwa ekstrem: flash crash 17 Agustus 2023 dan 10/10

Dua lompatan terbesar di grafik kumulatif D adalah dua hari kejut, keduanya terjadi setelah periode volatilitas sangat rendah.

| Hari (UTC) | Peristiwa | RV hari itu | RV ÷ rata-rata 30 hari sebelumnya | Peringkat RV (sampel penuh / sejak 2021) | Ramalan HAR / LGBM-X S2-365 / LGBM-X S1 | D | Peringkat \|D\| institutional |
|---|---|---|---|---|---|---|---|
| 17 Agu 2023 | Flash crash: BTC turun dari dekat $29.000 ke $25.314 dalam 24 jam, likuidasi > $1 miliar; terjadi beberapa hari setelah volatilitas harian BTC terendah dalam beberapa tahun (Bloomberg; Cointelegraph) | 0,0102 | ≈ 72× | 64 / 15 | 0,000156 / 0,000126 / 0,000154 | **+16,3** | **1** dari 2.085 |
| 10 Okt 2025 | "10/10": likuidasi terbesar dalam sejarah kripto, ≈ $19 miliar pada 10–11 Okt 2025, dipicu ancaman tarif 100% AS terhadap Tiongkok (CoinGecko; FTI Consulting) | 0,0102 | ≈ 47× | 66 / 16 | 0,000364 / 0,000326 / 0,000414 | **+5,74** | **3** dari 2.085 |

**Interpretasi (eksploratori):**
- Semua model meleset jauh ke bawah (ramalan ≈ 1/30–1/65 dari RV). Karena QLIKE sangat menghukum ramalan terlalu rendah, selisih ramalan kecil antar model menjadi selisih loss besar.
- Pola sama di kedua hari: **LGBM-X rolling-365 meramal lebih rendah daripada HAR**, sedangkan **LGBM-X expanding meramal setara/lebih tinggi**. Mekanisme yang masuk akal: window 365 hari yang didominasi periode tenang membuat LightGBM "lupa" rezim volatil; expanding masih menyimpan contoh rezim volatil 2017–2022. Ini selaras dengan cerita "jumlah/cakupan data latih" di RQ3.
- Kedua hari termasuk 20 hari |D| terbesar yang dibuang di uji robustness; **tanpa hari-hari itu D tetap signifikan (t 3,35)**, jadi kesimpulan RQ3 tidak bergantung pada keduanya.
- Kedua peristiwa terutama digerakkan likuidasi **derivatif**; di pasar **spot** (yang dipakai skripsi ini) RV harinya besar tetapi bukan yang terbesar sepanjang sampel (peringkat 64 dan 66). Contoh konkret mengapa QLIKE dan MSE bisa memberi kesimpulan berbeda (Bagian 4).
- Sumber peristiwa adalah berita/laporan industri (Bloomberg, Cointelegraph, CoinGecko, FTI Consulting); untuk Bab 4 cukup sebagai konteks deskriptif, angka likuidasi tidak dipakai dalam analisis.

**Belum dijalankan (kode ada):** RV 5 menit subsampled (butuh data 1 menit), retuning tahunan, CI tanggal break (tidak relevan karena 0 break).

---

## 4. Kesimpulan per RQ (versi untuk Bab 4/5)

1. **RQ1.** Tidak ditemukan bukti bahwa kinerja relatif LightGBM-X terhadap HAR-RV berubah sepanjang Sep 2018 – Sep 2026 (UDmax p 0,37; 0 break). Secara agregat tidak ada model yang terbukti unggul (DM p 0,25). **Kalimat aman:** *"tidak ditemukan bukti perubahan kinerja relatif; uji memiliki daya memadai hanya untuk pergeseran besar (≥ sekitar 1–2 sd rata-rata ΔL tahunan)."* Jangan menulis "terbukti stabil", "ML kalah", atau "setara".
2. **RQ2.** Variasi kinerja relatif bulanan tidak berasosiasi dengan level volatilitas, vol-of-vol, likuiditas (Abdi-Ranaldo maupun Corwin-Schultz), atau pergeseran distribusi fitur; kontribusi fitur X tidak berbeda antara era transition dan institutional. Konsisten dengan RQ1.
3. **RQ3.** Strategi pembaruan berpengaruh: di era institutional, expanding memberi kinerja relatif ML yang signifikan lebih baik daripada rolling-365 (hipotesis tandingan Pesaran–Timmermann didukung). Kokoh terhadap hari ekstrem dan 5 dari 7 sensitivitas; berasal dari kebutuhan data komponen non-linear (LightGBM). **Batasan wajib disebut di bagian hasil:** tidak bertahan dengan MSE.
4. **Temuan pendukung.** Tanpa pelatihan ulang (S0), LightGBM rusak parah → retraining wajib.

**Sintesis mekanisme (pembahasan):** data lama memang kurang relevan (indikasi efek umur), tetapi menambahkannya ke data baru tetap menguntungkan karena pengurangan varians lebih besar daripada bias yang ditambahkan (trade-off bias–varians Pesaran–Timmermann via Rossi, 2013). Model linear (HAR, HAR-X) tidak sensitif terhadap panjang window; LightGBM sangat sensitif.

**Penjelasan beda QLIKE vs MSE:** QLIKE mengukur kesalahan relatif dan sensitif pada hari tenang (serta menghukum ramalan terlalu rendah); MSE pada level didominasi hari lonjakan. Jadi expanding membantu ketepatan proporsional di hari biasa, tidak di hari ekstrem. QLIKE tetap metrik utama sesuai v2.5 (Patton, 2011).

---

## 5. Batasan dan catatan penulisan

- Daya UDmax rendah untuk pergeseran realistis (lihat 3.2).
- RQ3 hanya berlaku pada QLIKE.
- Efek RQ3 terkonsentrasi dalam waktu (2022–2023 dan lompatan 17 Agu 2023 serta 10/10); tulis deskriptif (Bagian 3.4).
- LGBM-X: min_child_samples terbaik = 5 = batas bawah grid (dikunci di config untuk menjaga "regularisasi ketat" v2.5); disebut sebagai keputusan desain.
- Bias correction: tanpa koreksi, ΔL turun dari +0,017 ke +0,004 → koreksi exp(ŷ+σ̂²/2) kemungkinan lebih merugikan LightGBM; layak satu paragraf (keadilan prosedur antar model). Tidak mengubah kesimpulan konfirmatori.
- Sensitivitas RV subsampled dan retuning tahunan belum dijalankan → jalankan atau tulis sebagai keterbatasan.
- Kesimpulan terbatas pada BTC/USDT spot Binance; era niche tidak tercakup.
- Pilot (pasangan LGBM-HAR vs HAR) memengaruhi pemahaman RQ3; tulis terbuka di Bab 3 sebagai tahap uji kelayakan. Uji konfirmatori memakai pasangan LGBM-X vs HAR yang belum pernah dilihat sebelum desain dikunci.

## 6. Deviasi/keputusan implementasi terhadap v2.5

1. HAR-X tanpa ln_amihud (aturan V.3, VIF window awal); LGBM-X memakai semua 9 fitur. ln_amihud secara konstruksi ≈ ½ ln RV − ln volume dolar.
2. Nilai kritis UDmax, uji berurutan, dan Fluctuation test **disimulasikan** (CV 5% UDmax 9,01 vs tabel Bai–Perron ~8,88; tabel asli tetap perlu dicek).
3. Tuning: grid {num_leaves 3/7/15, min_child_samples 10/20/40/80 (perluasan ke bawah s.d. 5), n_estimators 50/100/300/600, lr 0,03, reg_lambda 1/10}, metrik QLIKE pada exp(ŷ), forward-chaining 5 fold, perluasan tepi grid maksimal 2 kali.
4. H2b = dua uji, dikoreksi Holm.
5. Aturan stasioneritas RQ2: differencing bila ADF gagal menolak (p > 0,05) dan KPSS menolak (p < 0,05); dummy era selalu disertakan.
6. Rolling tertunda (VII.2) dan kurva window dijalankan sebagai eksploratori.
7. HAC: Bartlett + bandwidth otomatis Andrews (1991), replika `sandwich::kernHAC(prewhite=FALSE)` — diverifikasi **identik** dengan R untuk uji DM dan regresi.
8. Hari tidak lengkap (t atau t+1) dibuang dari observasi latih/uji; sensitivitas: dipertahankan.

## 7. Langkah berikutnya

1. **Baca full text Chassot & Audrino (2026) dan Feng et al. (2024)** — penentu novelty RQ3 (risiko terbesar). Juga Trucíos & Taylor (2023).
2. **Bimbingan pertama:** bawa kesimpulan Bagian 4; tanyakan (a) output sistem (opsi: dashboard pemantauan, Bagian VII.8), (b) apakah hasil MSE yang berlawanan cukup ditulis sebagai batasan, (c) sensitivitas tersisa.
3. Verifikasi referensi ⚠, DOI \*, kuartil SCImago, tabel Bai–Perron.
4. Tulis Bab 1–5 (Bab 3 terbuka soal pilot; Bab 4 berkerangka `LAPORAN_HASIL.md`).

## 8. Lingkungan dan cara menjalankan

**Masalah lingkungan (Mac, Homebrew Python 3.12):** `pyexpat` ter-link ke `/usr/lib/libexpat.1.dylib` (macOS 26) tanpa simbol `_XML_SetAllocTrackerActivationThreshold` → plistlib/matplotlib/venv gagal. Perbaikan: salinan `pyexpat.so` di venv yang di-relink ke expat Homebrew + file `.pth` (tanpa DYLD). Alternatif sementara: `export DYLD_LIBRARY_PATH=/opt/homebrew/opt/expat/lib`. Python 3.14 juga terdampak; venv memakai 3.12.

**Menjalankan:**
```bash
python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
python 01_download.py                     # arsip 5m (checksum diverifikasi)
RV_QUICK=1 ./run_all.sh                   # uji cepat kode (hasil di results/quick, tidak bermakna)
./run_all.sh                              # run penuh -> results/final/LAPORAN_HASIL.md
DAYA=1 RETUNE=1 ./run_all.sh              # + analisis daya & retuning tahunan
python 01_download.py --interval 1m       # opsional: sensitivitas RV subsampled, lalu run ulang
```
`20_forecast.py` selalu menghitung ulang semua forecast. Hash `rvlib/config.py` dicatat di setiap output; laporan menandai bila config berubah setelah forecast dibuat (catatan: hash hanya mencakup `config.py`, bukan file kode lain).

**Setelah patch v1.2 (penanda peristiwa), cukup perbarui grafik:** `python 30_rq1.py && python 32_rq3.py` (tanpa `--daya` bila hasil daya tidak perlu dihitung ulang; perhatikan bahwa `30_rq1.py` tanpa `--daya` menimpa `30_rq1.txt` tanpa bagian daya, jadi jalankan dengan `--daya` bila ingin bagian itu tetap ada).

**Untuk menjalankan ulang analisis saja tanpa menyentuh forecast:**
```bash
python 30_rq1.py --daya && python 31_rq2.py && python 31_rq2.py --likuiditas cs && \
python 32_rq3.py && python 33_sensitivitas.py && python 40_laporan.py
```

**Cek kesehatan data/forecast (harus 27 | 2914 | 0.3592):**
```bash
python -c "
import pandas as pd, numpy as np
d=pd.read_csv('data/daily.csv',index_col=0); f=pd.read_csv('results/final/fc/S2_365.csv',index_col=0)
q=lambda a,b: a/b-np.log(a/b)-1
print(d.flag_incomplete.sum(), len(f), round(q(f.rv,f.HAR).mean(),4))"
```

---

## 9. Source code final (`skripsi_rv`, identik dengan isi `skripsi_rv_2.zip`)

Struktur:
```
skripsi_rv/
├── 01_download.py        unduh arsip Binance + checksum
├── 02_build_daily.py     audit & tabel harian (RV 5m, 15m, subsampled 1m)
├── 10_cek_fitur.py       VIF window awal
├── 11_tuning.py          tuning LGBM-HAR & LGBM-X (window awal 12 & 24 bulan)
├── 20_forecast.py        semua walk-forward (utama, opsional, sensitivitas)
├── 30_rq1.py             RQ1 konfirmatori + eksploratori + daya + grafik
├── 31_rq2.py             RQ2 H2a & H2b
├── 32_rq3.py             RQ3 konfirmatori + eksploratori + kurva window
├── 33_sensitivitas.py    tabel sensitivitas
├── 40_laporan.py         LAPORAN_HASIL.md
├── run_all.sh
├── requirements.txt
├── r/break_ci.R          CI tanggal break (opsional)
└── rvlib/
    ├── config.py         KUNCI DESAIN v2.5
    ├── data.py           muat arsip, tabel harian, matriks desain
    ├── models.py         HAR/HAR-X (OLS), LGBM, RF
    ├── walkforward.py    walk-forward bulanan
    ├── tuning.py         forward-chaining tuning
    ├── stats.py          HAC Andrews, DM, regresi HAC, UDmax, uji berurutan, Fluctuation, CV simulasi, Holm
    └── analysis.py       bantu analisis & grafik
```


### `rvlib/config.py`

```python
"""KUNCI DESAIN - mengikuti dokumen riset v2.5.
Semua keputusan desain ada di sini. Ubah file ini SEBELUM menjalankan 20_forecast.py;
hash file ini dicatat di setiap output agar terlihat bila desain berubah setelah hasil dilihat."""
import pandas as pd

DESIGN_VERSION = "v2.5"

# ---------------------------------------------------------------- data (V.1)
RAW_5M = "data/raw/5m"
RAW_1M = "data/raw/1m"              # opsional, hanya untuk sensitivitas RV subsampled
DAILY = "data/daily.csv"
BARS_PER_DAY = 288
MIN_BAR_FRAC = 0.95                 # hari dengan bar < 95% ditandai
DROP_INCOMPLETE = True              # aturan audit: hari tidak lengkap (t atau t+1) tidak dipakai sebagai
                                    # observasi latih/uji. Sensitivitas: dipertahankan.

# ---------------------------------------------------------------- target & fitur (V.2-V.3)
LAGS_MAIN = (1, 7, 30)
LAGS_SENS = (1, 5, 22)
HAR_COLS = ["ln_rv_d", "ln_rv_w", "ln_rv_m"]
X_COLS = ["neg_share", "ret", "ln_dvol", "d_ln_dvol", "ln_parkinson", "ln_amihud"]
# Aturan v2.5 V.3: "Jika [kolinearitas] ekstrem, buang dari HAR-X saja dan catat keputusannya."
# Pemeriksaan window awal (kelayakan/06): ln_amihud VIF 19,6 dan ln_dvol VIF 18,2. ln_amihud dibuang
# dari HAR-X (VIF tertinggi; secara konstruksi ~ 1/2 ln RV - ln volume). 10_cek_fitur.py memverifikasi
# bahwa VIF sisa fitur X <= 10 setelah pembuangan ini.
HARX_DROP = ["ln_amihud"]
BIAS_CORRECTION = True              # exp(yhat + s2/2), s2 dari 20% akhir window latih
BC_HOLDOUT = 0.20
FLOOR_PCT = 1                       # batas bawah forecast: persentil ke-1 RV window latih

# ---------------------------------------------------------------- model (V.4)
MODELS = ["HAR", "HARX", "LGBM_HAR", "LGBM_X"]       # + NAIVE sebagai sanity check
SEED = 42
RF_PARAMS = dict(n_estimators=300, min_samples_leaf=20, max_features=0.33, n_jobs=-1)  # robustness

# ---------------------------------------------------------------- tuning (V.5)
TUNE_SPLITS = 5                     # forward-chaining (TimeSeriesSplit), hanya window awal
TUNE_GRID = dict(num_leaves=[3, 7, 15], min_child_samples=[10, 20, 40, 80],
                 n_estimators=[50, 100, 300, 600], learning_rate=[0.03], reg_lambda=[1.0, 10.0])
TUNE_EXTEND_MAX = 2                 # bila terbaik di tepi grid (min_child_samples / n_estimators),
                                    # grid diperluas satu langkah ke arah itu, maksimal 2 kali.
TUNE_MIN_CHILD_FLOOR = 5            # batas bawah min_child_samples (v2.5: regularisasi ketat)
LGB_BASE = dict(objective="regression", subsample=0.8, subsample_freq=1,
                random_state=SEED, deterministic=True, n_jobs=1, verbose=-1)

# ---------------------------------------------------------------- strategi (V.5)
INIT_DAYS = 365                     # window awal ~12 bulan (termasuk warm-up 30 hari)
INIT_DAYS_ROBUST = 730              # robustness: window awal 24 bulan
SCHEMES = {                         # nama: (skema, W)
    "S0": ("static", None),
    "S1": ("expanding", None),
    "S2_365": ("rolling", 365),
    "S2_730": ("rolling", 730),
}
SCHEMES_OPTIONAL = {"S2_180": ("rolling", 180), "S2_1095": ("rolling", 1095),
                    "TUNDA_365": ("delayed", 365)}   # eksploratori (Bagian VII)

# ---------------------------------------------------------------- era (Do, 2026)
ERA_SPLIT = pd.Timestamp("2021-01-01")       # transition | institutional
Y2026 = pd.Timestamp("2026-01-01")           # sensitivitas tanpa 2026

# ---------------------------------------------------------------- uji (V.6)
CONF_PAIR = ("LGBM_X", "HAR")                # pasangan konfirmatori
CONF_SCHEME = "S2_365"
EPS = 0.15
EPS_SENS = 0.20
M_BREAKS = 5
ALPHA = 0.05
CV_SIM_REPS = 3000                  # nilai kritis UDmax & Fluctuation test disimulasikan (bukan dari ingatan)
FLUCT_MU = (0.3, 0.2)
POWER_REPS = 200

EXPLORATORY_PAIRS = [("LGBM_HAR", "HAR"), ("HARX", "HAR"), ("LGBM_X", "LGBM_HAR"), ("LGBM_X", "HARX")]
RQ2_REGRESSORS = ["level_vol", "volvol", "likuiditas", "ks_shift"]

RESULTS = "results/final"

# ---------------------------------------------------------------- mode uji cepat (hanya untuk cek kode)
import os
if os.environ.get("RV_QUICK"):
    RF_PARAMS = {**RF_PARAMS, "n_estimators": 30}
    CV_SIM_REPS, POWER_REPS = 300, 20
    RESULTS = "results/quick"
```


### `rvlib/data.py`

```python
"""Muat arsip Binance, bangun tabel harian, dan bentuk matriks desain (target + fitur)."""
import zipfile
from pathlib import Path
import numpy as np
import pandas as pd
from . import config as C

COLS = ["open_time", "open", "high", "low", "close", "volume", "close_time",
        "quote_volume", "trades", "taker_base", "taker_quote", "ignore"]


def load_raw(folder):
    frames = []
    for z in sorted(Path(folder).glob("*.zip")):
        with zipfile.ZipFile(z) as zf, zf.open(zf.namelist()[0]) as fh:
            df = pd.read_csv(fh, header=None)
        if not str(df.iloc[0, 0]).isdigit():
            df = df.iloc[1:]
        df.columns = COLS
        frames.append(df)
    if not frames:
        return None
    df = pd.concat(frames, ignore_index=True)
    t = df["open_time"].astype("int64").values
    t = np.where(t > 1e14, t // 1000, t)          # mikrodetik sejak 2025 -> milidetik
    df["ts"] = pd.to_datetime(t, unit="ms", utc=True)
    for c in ["open", "high", "low", "close", "volume", "quote_volume"]:
        df[c] = df[c].astype(float)
    return (df.drop_duplicates("ts").sort_values("ts").set_index("ts")
              [["open", "high", "low", "close", "volume", "quote_volume"]])


def _day(idx):
    return idx.floor("D").tz_localize(None)


def daily_from_5m(b):
    b = b.copy()
    b["r"] = np.log(b["close"]).diff()
    b["day"] = _day(b.index)
    b["r2"] = b["r"] ** 2
    b["r2neg"] = b["r2"] * (b["r"] < 0)
    b["amihud_bar"] = b["r"].abs() / b["quote_volume"].where(b["quote_volume"] > 0)
    g = b.groupby("day")
    d = pd.DataFrame({"n_bars": g.size(), "rv": g["r2"].sum(), "rs_neg": g["r2neg"].sum(),
                      "close": g["close"].last(), "high": g["high"].max(), "low": g["low"].min(),
                      "dollar_vol": g["quote_volume"].sum(), "amihud": g["amihud_bar"].mean() * 1e6})
    # RV 15 menit (sensitivitas): close terakhir tiap blok 15 menit
    c15 = b["close"].resample("15min").last().dropna()
    r15 = np.log(c15).diff()
    d["rv15"] = (r15 ** 2).groupby(_day(r15.index)).sum()
    return d


def rv_subsampled_1m(b1):
    """RV 5 menit subsampled dari data 1 menit: rata-rata RV dari 5 grid berbeda (offset 0..4 menit)."""
    c = b1["close"]
    minute = c.index.minute.values
    out = []
    for k in range(5):
        ck = c[minute % 5 == k]
        r = np.log(ck).diff()
        out.append((r ** 2).groupby(_day(r.index)).sum())
    return pd.concat(out, axis=1).mean(axis=1)


def build_daily():
    b5 = load_raw(C.RAW_5M)
    d = daily_from_5m(b5)
    b1 = load_raw(C.RAW_1M) if Path(C.RAW_1M).exists() else None
    d["rvsub"] = rv_subsampled_1m(b1) if b1 is not None else np.nan
    d = d.reindex(pd.date_range(d.index.min(), d.index.max(), freq="D"))
    d["n_bars"] = d["n_bars"].fillna(0).astype(int)
    d["flag_incomplete"] = d["n_bars"] < np.ceil(C.MIN_BAR_FRAC * C.BARS_PER_DAY)
    d["flag_zero_rv"] = ~(d["rv"] > 0)
    return d, len(b5), (0 if b1 is None else len(b1))


def design(daily, rv_col="rv", lags=C.LAGS_MAIN, drop_incomplete=C.DROP_INCOMPLETE):
    """Matriks desain: fitur hari t (data s.d. akhir hari t), target ln RV hari t+1.
    rv_col menentukan proxy target & fitur HAR; fitur X selalu dari data 5 menit."""
    d = daily.copy()
    rv = d[rv_col].where(d[rv_col] > 0)
    l1, lw, lm = lags
    d["ln_rv_d"] = np.log(rv.rolling(l1).mean())
    d["ln_rv_w"] = np.log(rv.rolling(lw).mean())
    d["ln_rv_m"] = np.log(rv.rolling(lm).mean())
    d["neg_share"] = d["rs_neg"] / d["rv"]
    d["ret"] = np.log(d["close"]).diff()
    d["ln_dvol"] = np.log(d["dollar_vol"])
    d["d_ln_dvol"] = d["ln_dvol"].diff()
    d["ln_parkinson"] = np.log((np.log(d["high"]) - np.log(d["low"])) ** 2 / (4 * np.log(2)))
    d["ln_amihud"] = np.log(d["amihud"])
    d["rv_t"] = rv
    d["rv_next"] = rv.shift(-1)
    d["y"] = np.log(d["rv_next"])
    first = d.index.min()
    feats = C.HAR_COLS + C.X_COLS
    ok = np.isfinite(d[feats + ["y"]]).all(axis=1)
    if drop_incomplete:
        bad = d["flag_incomplete"] | d["flag_zero_rv"]
        ok &= ~bad & ~bad.shift(-1, fill_value=True)
    d = d[ok].copy()
    d["target_date"] = d.index + pd.Timedelta(days=1)
    return d, first


def oos_start(first, init_days):
    s = first + pd.Timedelta(days=init_days + 1)
    m = s.to_period("M").to_timestamp()
    return m if m >= s else m + pd.offsets.MonthBegin(1)
```


### `rvlib/models.py`

```python
"""Model: HAR & HAR-X (OLS), LGBM-HAR & LGBM-X (LightGBM), RF (robustness), naive."""
import json
from pathlib import Path
import numpy as np
import lightgbm as lgb
from sklearn.ensemble import RandomForestRegressor
from . import config as C


def model_cols(name):
    if name in ("HAR", "LGBM_HAR"):
        return list(C.HAR_COLS)
    if name == "HARX":
        return C.HAR_COLS + [c for c in C.X_COLS if c not in C.HARX_DROP]
    return C.HAR_COLS + C.X_COLS            # LGBM_X, RF_X


class OLS:
    def fit(self, X, y):
        A = np.c_[np.ones(len(X)), X]
        self.b = np.linalg.lstsq(A, y, rcond=None)[0]
        return self

    def predict(self, X):
        return np.c_[np.ones(len(X)), X] @ self.b


class LGB:
    def __init__(self, params):
        self.p = params

    def fit(self, X, y):
        self.m = lgb.LGBMRegressor(**{**C.LGB_BASE, **self.p}).fit(X, y)
        return self

    def predict(self, X):
        return self.m.predict(X)


class RF:
    def fit(self, X, y):
        self.m = RandomForestRegressor(random_state=C.SEED, **C.RF_PARAMS).fit(X, y)
        return self

    def predict(self, X):
        return self.m.predict(X)


def params_path(tag):
    return Path(C.RESULTS) / f"params_{tag}.json"


def load_params(name, tag="main"):
    f = params_path(tag)
    if not f.exists():
        raise FileNotFoundError(f"{f} belum ada: jalankan 11_tuning.py dulu")
    return json.loads(f.read_text())[name]


def make(name, params=None):
    if name in ("HAR", "HARX"):
        return OLS()
    if name == "RF_X":
        return RF()
    return LGB(params)


def fit_bias_corrected(name, X, y, params, bias_correction=True):
    """Latih di 80% awal -> varians residual di 20% akhir -> latih ulang di seluruh window."""
    if not bias_correction:
        return make(name, params).fit(X, y), 0.0
    k = int(len(X) * (1 - C.BC_HOLDOUT))
    m = make(name, params).fit(X[:k], y[:k])
    s2 = float(np.var(y[k:] - m.predict(X[k:]), ddof=1))
    return make(name, params).fit(X, y), s2
```


### `rvlib/walkforward.py`

```python
"""Walk-forward bulanan: S0 static, S1 expanding, S2 rolling, rolling tertunda; HAR harian opsional."""
import numpy as np
import pandas as pd
from . import config as C
from .data import oos_start
from .models import model_cols, fit_bias_corrected


def qlike(rv, f):
    r = rv / f
    return r - np.log(r) - 1


def train_slice(d, ms, scheme, W, init_days):
    t = d["target_date"]
    if scheme == "rolling":
        return d[(t < ms) & (t >= ms - pd.Timedelta(days=W))]
    if scheme == "expanding":
        return d[t < ms]
    if scheme == "delayed":
        return d[(t < ms - pd.Timedelta(days=W)) & (t >= ms - pd.Timedelta(days=2 * W))]
    return d[(t < ms) & (t >= ms - pd.Timedelta(days=init_days))]          # static


def run(d, first, scheme, W, models, params, init_days=C.INIT_DAYS, bias_correction=C.BIAS_CORRECTION,
        har_daily=False, retune=None):
    """params: {model: dict}. retune: fungsi(train_df) -> params baru, dipanggil tiap Januari (sensitivitas)."""
    eff_init = {"rolling": max(init_days, W or 0), "delayed": max(init_days, 2 * (W or 0))}.get(scheme, init_days)
    months = pd.date_range(oos_start(first, eff_init), d["target_date"].max(), freq="MS")
    rows, frozen = [], None
    for ms in months:
        test = d[(d["target_date"] >= ms) & (d["target_date"] < ms + pd.offsets.MonthBegin(1))]
        if test.empty:
            continue
        if scheme == "static" and frozen is not None:
            fitted = frozen
        else:
            tr = train_slice(d, ms, scheme, W, init_days)
            if len(tr) < 0.8 * min(W or init_days, init_days):
                continue
            if retune is not None and ms.month == 1:
                params = retune(tr)
            y = tr["y"].values
            floor = np.percentile(tr["rv_next"], C.FLOOR_PCT)
            fitted = {}
            for m in models:
                cols = model_cols(m)
                mod, s2 = fit_bias_corrected(m, tr[cols].values, y, params.get(m), bias_correction)
                fitted[m] = (mod, s2, floor, cols)
            if scheme == "static":
                frozen = fitted
        out = pd.DataFrame({"rv": test["rv_next"].values, "NAIVE": test["rv_t"].values},
                           index=pd.DatetimeIndex(test["target_date"].values, name="target_date"))
        for m, (mod, s2, floor, cols) in fitted.items():
            out[m] = np.maximum(np.exp(mod.predict(test[cols].values) + s2 / 2), floor)
        if har_daily:
            f = []
            for td, row in zip(test["target_date"], test[C.HAR_COLS].values):
                tr = train_slice(d, td, scheme, W, init_days)
                mod, s2 = fit_bias_corrected("HAR", tr[C.HAR_COLS].values, tr["y"].values, None, bias_correction)
                f.append(max(np.exp(mod.predict(row[None, :])[0] + s2 / 2), np.percentile(tr["rv_next"], C.FLOOR_PCT)))
            out["HAR_DAILY"] = f
        rows.append(out)
    return pd.concat(rows)


def losses(fc, kind="qlike"):
    cols = [c for c in fc.columns if c != "rv"]
    if kind == "qlike":
        return pd.DataFrame({c: qlike(fc["rv"], fc[c]) for c in cols})
    return pd.DataFrame({c: (fc["rv"] - fc[c]) ** 2 for c in cols})
```


### `rvlib/tuning.py`

```python
"""Tuning forward-chaining (TimeSeriesSplit) untuk LightGBM; QLIKE pada ramalan exp(yhat)."""
import itertools
import numpy as np
from sklearn.model_selection import TimeSeriesSplit
from . import config as C
from .models import LGB, model_cols
from .walkforward import qlike

EXT = {"min_child_samples": lambda v, up: v * 2 if up else max(C.TUNE_MIN_CHILD_FLOOR, v // 2),
       "n_estimators": lambda v, up: v * 2 if up else max(10, v // 2)}


def cv_score(X, y, rv, params):
    s = []
    for tr, va in TimeSeriesSplit(n_splits=C.TUNE_SPLITS).split(X):
        m = LGB(params).fit(X[tr], y[tr])
        s.append(qlike(rv[va], np.exp(m.predict(X[va]))).mean())
    return float(np.mean(s))


def tune(train, name, verbose=False):
    X, y, rv = train[model_cols(name)].values, train["y"].values, train["rv_next"].values
    grid = {k: list(v) for k, v in C.TUNE_GRID.items()}
    log = []
    for it in range(C.TUNE_EXTEND_MAX + 1):
        res = sorted(((cv_score(X, y, rv, dict(zip(grid, v))), dict(zip(grid, v)))
                      for v in itertools.product(*grid.values())), key=lambda r: r[0])
        best = res[0][1]
        edge = False
        for k in EXT:
            if best[k] == max(grid[k]) and it < C.TUNE_EXTEND_MAX:
                grid[k].append(EXT[k](max(grid[k]), True)); edge = True
            elif best[k] == min(grid[k]) and it < C.TUNE_EXTEND_MAX and EXT[k](min(grid[k]), False) < min(grid[k]):
                grid[k].insert(0, EXT[k](min(grid[k]), False)); edge = True
        log.append(dict(iterasi=it, best=best, cv=res[0][0]))
        if verbose:
            print(f"    {name} iterasi {it}: {best}  CV QLIKE {res[0][0]:.4f}{'  -> tepi grid, diperluas' if edge else ''}")
        if not edge:
            break
    return best, res[0][0], log, res
```


### `rvlib/stats.py`

```python
"""Statistik: HAC Bartlett + bandwidth Andrews (1991) [replika sandwich::kernHAC, prewhite=FALSE],
uji tipe DM, regresi HAC, UDmax & uji break berurutan (Bai-Perron), Fluctuation test (GR 2010),
nilai kritis via simulasi, koreksi Holm."""
from pathlib import Path
import numpy as np
from scipy import stats as st
from . import config as C


# ------------------------------------------------------------------ HAC
def _ar1(u):
    z = u - u.mean()
    y, x = z[1:], z[:-1]
    A = np.c_[np.ones_like(x), x]
    b = np.linalg.lstsq(A, y, rcond=None)[0]
    e = y - A @ b
    return b[1], np.sqrt(e @ e / len(y))


def andrews_bw(U, w):
    num = den = 0.0
    for j in range(U.shape[1]):
        if w[j] == 0:
            continue
        r, s = _ar1(U[:, j])
        num += w[j] * 4 * r ** 2 * s ** 4 / ((1 - r) ** 6 * (1 + r) ** 2)
        den += w[j] * (s / (1 - r)) ** 4
    return 1.1447 * (U.shape[0] * num / den) ** (1 / 3)


def hac_vcov(X, e, intercept=None):
    """Kovarians HAC koefisien OLS. intercept: indeks kolom konstanta (bobot 0 di bandwidth, seperti sandwich)."""
    X = np.asarray(X, float); e = np.asarray(e, float)
    n, k = X.shape
    U = X * e[:, None]
    w = np.ones(k)
    if intercept is not None and k > 1:
        w[intercept] = 0
    bw = andrews_bw(U, w)
    S = 0.5 * U.T @ U
    l = 1
    while l < bw and l < n:
        S += (1 - l / bw) * U[:-l].T @ U[l:]
        l += 1
    S = S + S.T
    B = np.linalg.inv(X.T @ X)
    return B @ S @ B * n / (n - k), bw


def mean_test(x):
    """Uji tipe DM: H0 E[x] = 0. Return mean, t, p (dua sisi), n."""
    x = np.asarray(x, float); x = x[np.isfinite(x)]
    if len(x) < 30:
        return dict(mean=np.nan, t=np.nan, p=np.nan, n=len(x))
    V, _ = hac_vcov(np.ones((len(x), 1)), x - x.mean())
    t = x.mean() / np.sqrt(V[0, 0])
    return dict(mean=x.mean(), t=t, p=2 * st.norm.sf(abs(t)), n=len(x))


def ols_hac(y, X, names):
    """Regresi OLS dengan SE HAC. X tanpa konstanta; konstanta ditambahkan di kolom 0."""
    y = np.asarray(y, float); A = np.c_[np.ones(len(y)), np.asarray(X, float)]
    b = np.linalg.lstsq(A, y, rcond=None)[0]
    e = y - A @ b
    V, bw = hac_vcov(A, e, intercept=0)
    se = np.sqrt(np.diag(V))
    tab = {nm: dict(coef=b[i], se=se[i], t=b[i] / se[i], p=2 * st.norm.sf(abs(b[i] / se[i])))
           for i, nm in enumerate(["const"] + list(names))}
    return dict(b=b, V=V, tab=tab, n=len(y), k=A.shape[1], r2=1 - e @ e / ((y - y.mean()) @ (y - y.mean())))


def wald(res, idx):
    """Uji bersama koefisien idx = 0 (HAC). Return chi2, F, p_F."""
    R = np.eye(len(res["b"]))[idx]
    rb = R @ res["b"]
    chi2 = float(rb @ np.linalg.solve(R @ res["V"] @ R.T, rb))
    q = len(idx)
    return dict(chi2=chi2, F=chi2 / q, p=st.f.sf(chi2 / q, q, res["n"] - res["k"]), q=q)


# ------------------------------------------------------------------ Bai-Perron (perubahan rata-rata)
def _ssr_matrix(x, h):
    T = len(x)
    c1 = np.r_[0, np.cumsum(x)]; c2 = np.r_[0, np.cumsum(x * x)]
    n = np.arange(T + 1)[None, :] - np.arange(T + 1)[:, None]
    with np.errstate(divide="ignore", invalid="ignore"):
        Cm = (c2[None, :] - c2[:, None]) - (c1[None, :] - c1[:, None]) ** 2 / n
    Cm[n < h] = np.inf
    return Cm


def partitions(x, h, M):
    """Partisi global min-SSR untuk m = 1..M. Return {m: indeks akhir segmen (1-based)}."""
    T = len(x)
    Cm = _ssr_matrix(x, h)
    f, arg = [Cm[0].copy()], [None]
    for _ in range(2, M + 2):
        tot = f[-1][:, None] + Cm
        arg.append(np.argmin(tot, axis=0))
        f.append(tot[arg[-1], np.arange(T + 1)])
    out = {}
    for m in range(1, M + 1):
        if not np.isfinite(f[m][T]):
            break
        j, b = T, []
        for k in range(m + 1, 1, -1):
            j = arg[k - 1][j]; b.append(j)
        out[m] = sorted(b)
    return out


def wald_means(x, bps, hac=True):
    T = len(x)
    seg = np.searchsorted(np.asarray(bps), np.arange(1, T + 1), side="left")
    k = len(bps) + 1
    X = np.zeros((T, k)); X[np.arange(T), seg] = 1
    n = X.sum(0); mu = (X.T @ x) / n
    e = x - mu[seg]
    if hac:
        V, _ = hac_vcov(X, e)
    else:
        V = np.diag((e @ e / (T - k)) / n)
    R = np.eye(k)[:-1] - np.eye(k)[1:]
    dm = R @ mu
    return float(dm @ np.linalg.solve(R @ V @ R.T, dm)) / (k - 1), mu


def m_max(eps):
    return C.M_BREAKS if eps <= 0.15 else 3


def udmax(x, eps=C.EPS, hac=True):
    x = np.asarray(x, float)
    M = m_max(eps)
    parts = partitions(x, int(np.floor(eps * len(x))), M)
    supF = {m: wald_means(x, b, hac)[0] for m, b in parts.items()}
    m_star = max(supF, key=supF.get)
    return dict(udmax=max(supF.values()), supF=supF, m_star=m_star, parts=parts)


def sequential(x, l, parts, eps=C.EPS, hac=True):
    """supF(l+1|l): di tiap segmen partisi l-break, cari 1 break tambahan (min SSR), F HAC; ambil maksimum."""
    T = len(x); h = int(np.floor(eps * T))
    b = [0] + (parts.get(l, []) if l > 0 else []) + [T]
    best = 0.0
    for s, e in zip(b[:-1], b[1:]):
        seg = x[s:e]
        if len(seg) < 2 * h:
            continue
        c1 = np.cumsum(seg); n = len(seg); c2 = np.cumsum(seg * seg)
        k = np.arange(h, n - h + 1)
        ssr = (c2[k - 1] - c1[k - 1] ** 2 / k) + ((c2[-1] - c2[k - 1]) - (c1[-1] - c1[k - 1]) ** 2 / (n - k))
        kk = k[np.argmin(ssr)]
        best = max(best, wald_means(seg, [kk], hac)[0])
    return best


# ------------------------------------------------------------------ nilai kritis via simulasi
def _cache(name):
    p = Path(C.RESULTS) / "cv_sim"; p.mkdir(parents=True, exist_ok=True)
    return p / f"{name}.npy"


def sim_udmax_null(eps, reps=C.CV_SIM_REPS, T=1000, seed=1):
    f = _cache(f"udmax_eps{eps}")
    if f.exists():
        return np.load(f)
    rng = np.random.default_rng(seed)
    M = m_max(eps)
    out = np.zeros((reps, M + 1))
    for r in range(reps):
        res = udmax(rng.standard_normal(T), eps, hac=False)
        out[r, 0] = res["udmax"]
        out[r, 1:] = [res["supF"].get(m, np.nan) for m in range(1, M + 1)]
    np.save(f, out)
    return out


def sim_sequential_null(l, eps=C.EPS, reps=None, T=1000, seed=2):
    reps = reps or max(200, C.CV_SIM_REPS // 3)
    f = _cache(f"seq_l{l}_eps{eps}")
    if f.exists():
        return np.load(f)
    rng = np.random.default_rng(seed + l)
    bps = [int(T * (i + 1) / (l + 1)) for i in range(l)]
    out = np.zeros(reps)
    for r in range(reps):
        x = rng.standard_normal(T)
        for i, bp in enumerate(bps):
            x[bp:] += 10.0 * (-1) ** i                       # break besar -> partisi l-break tepat
        parts = partitions(x, int(np.floor(eps * T)), max(l, 1))
        out[r] = sequential(x, l, parts, eps, hac=False)
    np.save(f, out)
    return out


def sim_fluct_cv(mu, reps=5000, T=2000, seed=3, alpha=C.ALPHA):
    f = _cache(f"fluct_mu{mu}")
    if f.exists():
        return float(np.load(f))
    rng = np.random.default_rng(seed)
    m = int(mu * T)
    stat = np.empty(reps)
    for r in range(reps):
        B = np.r_[0, np.cumsum(rng.standard_normal(T))] / np.sqrt(T)
        stat[r] = np.max(np.abs(B[m:] - B[:-m])) / np.sqrt(mu)
    cv = float(np.quantile(stat, 1 - alpha))
    np.save(f, cv)
    return cv


def pval(sim, obs):
    sim = np.asarray(sim); sim = sim[np.isfinite(sim)]
    return float((np.sum(sim >= obs) + 1) / (len(sim) + 1))


def fluctuation(x, mu):
    """Statistik Fluctuation test GR (2010): rata-rata bergulir dL dinormalisasi sigma HAC seluruh sampel."""
    x = np.asarray(x, float); T = len(x); m = int(mu * T)
    sig = np.sqrt(hac_vcov(np.ones((T, 1)), x - x.mean())[0][0, 0] * T)
    cs = np.r_[0, np.cumsum(x)]
    return (cs[m:] - cs[:-m]) / (sig * np.sqrt(m)), m


def holm(pvals):
    p = np.asarray(pvals, float); n = len(p)
    order = np.argsort(p); adj = np.empty(n); run = 0
    for i, j in enumerate(order):
        run = max(run, min(1, (n - i) * p[j])); adj[j] = run
    return adj
```


### `rvlib/analysis.py`

```python
"""Fungsi bantu analisis: muat forecast, hitung loss & dL, label era, tabel per periode, grafik."""
import json
from pathlib import Path
import numpy as np
import pandas as pd
from . import config as C
from .walkforward import losses
from .stats import mean_test

FC = Path(C.RESULTS) / "fc"
FIG = Path(C.RESULTS) / "grafik"


def load(name, kind="qlike", drop2026=False):
    fc = pd.read_csv(FC / f"{name}.csv", index_col=0, parse_dates=True)
    if drop2026:
        fc = fc[fc.index < C.Y2026]
    return fc, losses(fc, kind)


def dL(L, pair):
    a, b = pair
    return (L[a] - L[b]).rename(f"{a}-{b}")


def era(idx):
    return pd.Series(np.where(idx < C.ERA_SPLIT, "transition", "institutional"), index=idx)


def per_period(x):
    rows = []
    groups = [("semua", x)] + list(x.groupby(era(x.index), sort=False)) + list(x.groupby(x.index.year))
    for k, g in groups:
        r = mean_test(g.values)
        rows.append(dict(periode=str(k), hari=r["n"], mean=r["mean"], t=r["t"], p=r["p"],
                         frac_unggul=(g < 0).mean()))
    return pd.DataFrame(rows)


def common(*series):
    idx = series[0].index
    for s in series[1:]:
        idx = idx.intersection(s.index)
    return [s.loc[idx] for s in series]


def write(name, text):
    Path(C.RESULTS).mkdir(parents=True, exist_ok=True)
    (Path(C.RESULTS) / name).write_text(text, encoding="utf-8")
    print(text)


def save_json(name, obj):
    (Path(C.RESULTS) / name).write_text(json.dumps(obj, indent=2, default=float, ensure_ascii=False))


def fmt(df):
    return df.to_string(index=False, float_format=lambda v: f"{v:+.4f}")


EVENTS = [("2020-03-09", "2020-03-31", "Crash Mar 2020"), ("2022-05-07", "2022-05-31", "Terra"),
          ("2022-11-06", "2022-11-30", "FTX"),
          ("2023-08-17", "2023-08-18", "Flash crash Agu 2023"),   # >$1 miliar likuidasi; RV ~72x rata-rata 30 hari
          ("2025-10-10", "2025-10-11", "10/10")]                  # likuidasi ~$19 miliar; RV ~47x rata-rata 30 hari


def mark_events(ax, label=False):
    """Penanda peristiwa (v2.5 V.1) + batas era (Do, 2026)."""
    ax.axvline(C.ERA_SPLIT, color="0.5", ls="--", lw=0.8)
    for s, e, nm in EVENTS:
        s_, e_ = pd.Timestamp(s), pd.Timestamp(e)
        if (e_ - s_).days < 7:     # peristiwa satu-dua hari: garis, agar tetap terlihat di sumbu 8 tahun
            ax.axvline(s_, color="red", lw=0.9, alpha=0.6)
        else:
            ax.axvspan(s_, e_, color="orange", alpha=0.25)
        if label:
            ax.text(pd.Timestamp(s), 1.0, nm, transform=ax.get_xaxis_transform(), fontsize=7, va="bottom")
```


### `rvlib/__init__.py`

```python
# (kosong: penanda paket)
```


### `01_download.py`

```python
"""
Tahap 1 - Unduh arsip bulanan klines BTC/USDT spot dari Binance Public Data.
Sumber: https://data.binance.vision  (folder spot, simbol file BTCUSDT)

Pakai:
    python 01_download.py                 # 5 menit, 2017-08 s.d. bulan lengkap terakhir
    python 01_download.py --interval 1m   # 1 menit (untuk sensitivitas subsampling nanti)
"""
import argparse, hashlib, io, zipfile
from datetime import date
from pathlib import Path
import requests

BASE = "https://data.binance.vision/data/spot/monthly/klines/BTCUSDT/{iv}/BTCUSDT-{iv}-{y}-{m:02d}.zip"


def months(start, end):
    y, m = start
    while (y, m) <= end:
        yield y, m
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--interval", default="5m")
    ap.add_argument("--start", default="2017-08")
    ap.add_argument("--out", default="data/raw")
    a = ap.parse_args()

    today = date.today()
    last = (today.year, today.month - 1) if today.month > 1 else (today.year - 1, 12)
    sy, sm = map(int, a.start.split("-"))
    out = Path(a.out) / a.interval
    out.mkdir(parents=True, exist_ok=True)
    log = []

    for y, m in months((sy, sm), last):
        url = BASE.format(iv=a.interval, y=y, m=m)
        f = out / url.rsplit("/", 1)[1]
        if f.exists():
            continue
        r = requests.get(url, timeout=60)
        if r.status_code == 404:
            print(f"[skip] {y}-{m:02d} belum/tidak tersedia")
            continue
        r.raise_for_status()
        # verifikasi checksum resmi
        ck = requests.get(url + ".CHECKSUM", timeout=60)
        ok = "n/a"
        if ck.ok:
            ok = ck.text.split()[0] == hashlib.sha256(r.content).hexdigest()
            if not ok:
                raise RuntimeError(f"Checksum gagal: {f.name}")
        f.write_bytes(r.content)
        log.append(f"{f.name},{hashlib.sha256(r.content).hexdigest()},{ok}")
        print(f"[ok] {f.name}  checksum={ok}")

    with open(out / "checksums.csv", "a") as fh:
        for line in log:
            fh.write(line + "\n")


if __name__ == "__main__":
    main()
```


### `02_build_daily.py`

```python
"""02 - Audit & tabel harian: RV 5 menit (utama), RV 15 menit, RV 5 menit subsampled (bila data 1m ada)."""
from pathlib import Path
from rvlib import config as C
from rvlib.data import build_daily

d, n5, n1 = build_daily()
Path("data").mkdir(exist_ok=True)
d.to_csv(C.DAILY, index_label="date")
bad = d[d["flag_incomplete"] | d["flag_zero_rv"]]
bad[["n_bars", "rv", "flag_incomplete", "flag_zero_rv"]].to_csv("data/audit.csv", index_label="date")
print(f"Bar 5m: {n5:,} | bar 1m: {n1:,}")
print(f"Hari: {len(d):,} ({d.index.min().date()} s.d. {d.index.max().date()})")
print(f"Hari bar < {C.MIN_BAR_FRAC:.0%}: {int(d['flag_incomplete'].sum())} | RV=0/NaN: {int(d['flag_zero_rv'].sum())}")
print(f"Hari dengan RV subsampled: {int(d['rvsub'].notna().sum())}")
```


### `10_cek_fitur.py`

```python
"""10 - Kolinearitas di WINDOW AWAL (aturan v2.5 V.3). Memverifikasi fitur HAR-X setelah HARX_DROP."""
from pathlib import Path
import numpy as np
import pandas as pd
from statsmodels.stats.outliers_influence import variance_inflation_factor
from rvlib import config as C
from rvlib.data import design, oos_start
from rvlib.models import model_cols

Path(C.RESULTS).mkdir(parents=True, exist_ok=True)
daily = pd.read_csv(C.DAILY, index_col="date", parse_dates=True)
d, first = design(daily)
w = d[d["target_date"] < oos_start(first, C.INIT_DAYS)]
print(f"Window awal: {w.index.min().date()} s.d. {w.index.max().date()} ({len(w)} obs)")


def vif(cols):
    A = np.c_[np.ones(len(w)), w[cols].values]
    return pd.Series([variance_inflation_factor(A, i + 1) for i in range(len(cols))], index=cols)


full = vif(C.HAR_COLS + C.X_COLS)
harx = vif(model_cols("HARX"))
tab = pd.DataFrame({"VIF_semua_fitur": full, "VIF_HARX_final": harx})
print(tab.round(2).to_string())
print("\nKorelasi fitur (window awal):")
print(w[C.HAR_COLS + C.X_COLS].corr().round(2).to_string())
tab.to_csv(Path(C.RESULTS) / "10_vif.csv")
x_after = harx.drop(C.HAR_COLS)
status = "OK" if (x_after <= 10).all() else "PERHATIAN"
msg = (f"[{status}] HAR-X tanpa {C.HARX_DROP}: VIF fitur X maksimum {x_after.max():.1f}"
       + ("" if status == "OK" else " (> 10: pertimbangkan membuang fitur lain dari HAR-X, catat keputusannya)"))
print("\n" + msg)
(Path(C.RESULTS) / "10_cek_fitur.txt").write_text(msg + "\n\n" + tab.round(2).to_string())
```


### `11_tuning.py`

```python
"""11 - Tuning LGBM-HAR dan LGBM-X di window awal (forward-chaining), lalu dikunci.
Juga window awal 24 bulan untuk robustness."""
import json
from pathlib import Path
import pandas as pd
from rvlib import config as C
from rvlib.data import design, oos_start
from rvlib.tuning import tune

out = Path(C.RESULTS); out.mkdir(parents=True, exist_ok=True)
daily = pd.read_csv(C.DAILY, index_col="date", parse_dates=True)
d, first = design(daily)
for tag, init in [("main", C.INIT_DAYS), ("init730", C.INIT_DAYS_ROBUST)]:
    w = d[d["target_date"] < oos_start(first, init)]
    print(f"[{tag}] window awal {len(w)} obs")
    P, lines = {}, []
    for name in ["LGBM_HAR", "LGBM_X"]:
        best, cv, log, _ = tune(w, name, verbose=True)
        P[name] = best
        lines.append(f"{name}: {best} | CV QLIKE {cv:.4f} | iterasi perluasan grid {len(log) - 1}")
    (out / f"params_{tag}.json").write_text(json.dumps(P, indent=2))
    (out / f"11_tuning_{tag}.txt").write_text("\n".join(lines))
    print("\n".join(lines))
```


### `20_forecast.py`

```python
"""20 - Semua walk-forward. Output: results/final/fc/<konfigurasi>.csv + manifest (hash config).
Pakai:  python 20_forecast.py                 # utama + opsional + sensitivitas (tanpa retuning tahunan)
        python 20_forecast.py --retune        # tambah sensitivitas retuning tahunan (lama, ~15-30 menit)
        python 20_forecast.py --only utama    # hanya konfigurasi utama"""
import argparse, hashlib, json, time
from pathlib import Path
import pandas as pd
from rvlib import config as C
from rvlib.data import design
from rvlib.models import load_params
from rvlib.tuning import tune
from rvlib import walkforward as WF

ap = argparse.ArgumentParser()
ap.add_argument("--retune", action="store_true")
ap.add_argument("--only", choices=["utama", "semua"], default="semua")
a = ap.parse_args()

OUT = Path(C.RESULTS) / "fc"; OUT.mkdir(parents=True, exist_ok=True)
cfg_hash = hashlib.sha256(Path("rvlib/config.py").read_bytes()).hexdigest()[:12]
daily = pd.read_csv(C.DAILY, index_col="date", parse_dates=True)
P = {m: load_params(m, "main") for m in ["LGBM_HAR", "LGBM_X"]}
M4 = C.MODELS

base = design(daily)
runs = []      # (nama, design, skema, W, model, params, kwargs)
for nm, (sch, W) in C.SCHEMES.items():
    runs.append((nm, base, sch, W, M4, P, {}))
if a.only == "semua":
    for nm, (sch, W) in C.SCHEMES_OPTIONAL.items():
        runs.append((nm, base, sch, W, M4, P, {}))
    sens = {
        "lag5_22": dict(des=design(daily, lags=C.LAGS_SENS)),
        "rv15": dict(des=design(daily, rv_col="rv15")),
        "tanpa_bc": dict(kw=dict(bias_correction=False)),
        "hari_tidak_lengkap": dict(des=design(daily, drop_incomplete=False)),
        "init730": dict(kw=dict(init_days=C.INIT_DAYS_ROBUST), params={m: load_params(m, "init730") for m in P}),
        "rf": dict(models=["HAR", "RF_X"]),
    }
    if daily["rvsub"].notna().sum() > 500:
        sens["rvsub"] = dict(des=design(daily, rv_col="rvsub"))
    else:
        print("Data 1m tidak tersedia -> sensitivitas RV subsampled dilewati")
    if a.retune:
        sens["retune"] = dict(kw=dict(retune=lambda tr: {m: tune(tr, m)[0] for m in P}))
    for tag, s in sens.items():
        for sch_nm in ["S2_365", "S1"]:
            sch, W = C.SCHEMES[sch_nm]
            runs.append((f"sens_{tag}_{sch_nm}", s.get("des", base), sch, W, s.get("models", M4),
                         s.get("params", P), s.get("kw", {})))
    runs.append(("sens_har_harian_S2_365", base, "rolling", 365, ["HAR"], P, dict(har_daily=True)))

manifest = dict(config_hash=cfg_hash, waktu=time.strftime("%Y-%m-%d %H:%M"), params=P, runs=[])
for nm, (d, first), sch, W, models, params, kw in runs:
    t0 = time.time()
    fc = WF.run(d, first, sch, W, models, params, **kw)
    fc.to_csv(OUT / f"{nm}.csv")
    manifest["runs"].append(dict(nama=nm, skema=sch, W=W, model=models, n=len(fc),
                                 mulai=str(fc.index.min().date()), selesai=str(fc.index.max().date())))
    print(f"  {nm:<34} {sch:<9} W={W}  n={len(fc):5d}  {fc.index.min().date()}..{fc.index.max().date()}  "
          f"[{time.time() - t0:.0f} dtk]", flush=True)
(Path(C.RESULTS) / "manifest.json").write_text(json.dumps(manifest, indent=2, default=str))
print(f"config hash {cfg_hash}")
```


### `30_rq1.py`

```python
"""30 - RQ1: kestabilan keunggulan relatif.
Konfirmatori (v2.5): UDmax pada rata-rata dL(LGBM-X - HAR), S2-365, QLIKE, HAC Andrews, eps 0,15, M 5.
Jika tidak menolak -> uji DM rata-rata dL seluruh sampel. Sisanya eksploratori + Holm.
Pakai: python 30_rq1.py [--daya]   (--daya: analisis daya UDmax, ~10-20 menit)"""
import argparse
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from rvlib import config as C
from rvlib import stats as S
from rvlib.analysis import load, dL, per_period, write, save_json, fmt, FIG, mark_events

ap = argparse.ArgumentParser(); ap.add_argument("--daya", action="store_true"); a = ap.parse_args()
FIG.mkdir(parents=True, exist_ok=True)
out, res = [], {}
fc, L = load(C.CONF_SCHEME)

out.append("== Sanity: rata-rata QLIKE per model (S2-365) ==")
out.append("  " + "  ".join(f"{m}={L[m].mean():.4f}" for m in ["NAIVE"] + C.MODELS))
bad = [m for m in C.MODELS if L[m].mean() >= L["NAIVE"].mean()]
out.append("  OK: semua model lebih baik dari naive" if not bad else f"  PERINGATAN: tidak lebih baik dari naive: {bad}")

# ---------------------------------------------------------------- konfirmatori
x = dL(L, C.CONF_PAIR)
sim = S.sim_udmax_null(C.EPS)
cv_sim = float(np.quantile(sim[:, 0], 1 - C.ALPHA))
u = S.udmax(x.values, C.EPS)
p_ud = S.pval(sim[:, 0], u["udmax"])
dm = S.mean_test(x.values)
reject = p_ud < C.ALPHA
res["konfirmatori"] = dict(udmax=u["udmax"], p=p_ud, cv5_sim=cv_sim, supF=u["supF"], dm=dm, tolak=reject)
out += ["", f"== KONFIRMATORI RQ1: {x.name}, {C.CONF_SCHEME}, QLIKE (T = {len(x)}) ==",
        "  " + "  ".join(f"supF({m})={v:.2f}" for m, v in u["supF"].items()),
        f"  UDmax = {u['udmax']:.2f}   p(simulasi) = {p_ud:.3f}   CV 5% simulasi = {cv_sim:.2f} "
        f"(tabel Bai-Perron 1998 q=1, eps=0,15: ~8,88 -- verifikasi)"]
if reject:
    out.append("  => TOLAK H0: rata-rata dL tidak konstan. H1 DIDUKUNG.")
else:
    out.append(f"  => Tidak menolak H0 perubahan rata-rata. Lanjut uji DM seluruh sampel:")
    out.append(f"     mean dL = {dm['mean']:+.4f}  t(HAC Andrews) = {dm['t']:+.2f}  p = {dm['p']:.4f}  "
               f"-> {'LGBM-X ' + ('unggul' if dm['mean'] < 0 else 'kalah') + ' signifikan' if dm['p'] < C.ALPHA else 'tidak berbeda signifikan'}")
    out.append("  => H1 TIDAK didukung (tidak ada bukti perubahan rata-rata dL).")
pp = per_period(x)
out += ["", "  Per periode:", fmt(pp)]
pp.to_csv(f"{C.RESULTS}/30_per_periode_konfirmatori.csv", index=False)

# ---------------------------------------------------------------- eksploratori
out += ["", "== EKSPLORATORI (p-value Holm dalam keluarga RQ1) =="]
rows = []
pairs = [C.CONF_PAIR] + C.EXPLORATORY_PAIRS
for sch in C.SCHEMES:
    _, Ls = load(sch)
    for kind in ["qlike", "mse"]:
        Lk = Ls if kind == "qlike" else load(sch, "mse")[1]
        for pr in pairs:
            if sch == C.CONF_SCHEME and kind == "qlike" and pr == C.CONF_PAIR:
                continue
            xx = dL(Lk, pr).values
            uu = S.udmax(xx, C.EPS); d2 = S.mean_test(xx)
            rows.append(dict(skema=sch, loss=kind, pasangan=f"{pr[0]}-{pr[1]}", uji="UDmax",
                             stat=uu["udmax"], p=S.pval(sim[:, 0], uu["udmax"])))
            rows.append(dict(skema=sch, loss=kind, pasangan=f"{pr[0]}-{pr[1]}", uji="DM",
                             stat=d2["t"], p=d2["p"], mean=d2["mean"]))
sim20 = S.sim_udmax_null(C.EPS_SENS)
u20 = S.udmax(x.values, C.EPS_SENS)
rows.append(dict(skema=C.CONF_SCHEME, loss="qlike", pasangan=x.name, uji="UDmax eps0.20",
                 stat=u20["udmax"], p=S.pval(sim20[:, 0], u20["udmax"])))
E = pd.DataFrame(rows)
E["p_holm"] = S.holm(E["p"].values)
E.to_csv(f"{C.RESULTS}/30_eksploratori.csv", index=False)
show = E[(E.loss == "qlike")]
out.append(show.to_string(index=False, float_format=lambda v: f"{v:.4f}"))
out.append("  (versi MSE lengkap di 30_eksploratori.csv)")

# ---------------------------------------------------------------- jumlah & tanggal break (berurutan)
out += ["", "== Uji break berurutan supF(l+1|l), pasangan konfirmatori (eksploratori) =="]
n_break = 0
for l in range(0, C.M_BREAKS):
    stat = S.sequential(x.values, l, u["parts"], C.EPS)
    simq = S.sim_sequential_null(l, C.EPS)
    p = S.pval(simq, stat)
    out.append(f"  supF({l + 1}|{l}) = {stat:.2f}  p(simulasi) = {p:.3f}")
    if p >= C.ALPHA:
        break
    n_break = l + 1
if n_break:
    dates = [x.index[i - 1].date() for i in u["parts"][n_break]]
    out.append(f"  Jumlah break terpilih: {n_break}; hari terakhir sebelum break: {dates} "
               f"(batas era Do 2026: {C.ERA_SPLIT.date()})")
else:
    out.append("  Jumlah break terpilih: 0")
res["sekuensial"] = dict(n_break=n_break)

# ---------------------------------------------------------------- grafik: dL bergulir & Fluctuation test
plot_pairs = [C.CONF_PAIR, ("LGBM_HAR", "HAR"), ("HARX", "HAR")]
fig, ax = plt.subplots(len(plot_pairs) + 1, 1, figsize=(12, 3.2 * (len(plot_pairs) + 1)), sharex=True)
ax[0].plot(fc.index, fc["rv"], lw=0.5, color="0.4"); ax[0].set_yscale("log")
ax[0].set_title("Realized variance harian (5 menit)", pad=16)
for i, pr in enumerate(plot_pairs, 1):
    xx = dL(L, pr)
    for mu, col in zip(C.FLUCT_MU, ["C0", "C3"]):
        f, m = S.fluctuation(xx.values, mu)
        cv = S.sim_fluct_cv(mu)
        ax[i].plot(xx.index[m - 1:], f, color=col, label=f"Fluctuation mu={mu} (CV 5% sim. +-{cv:.2f})")
        ax[i].axhline(cv, color=col, ls=":", lw=0.8); ax[i].axhline(-cv, color=col, ls=":", lw=0.8)
    ax[i].axhline(0, color="k", lw=0.8)
    ax[i].set_title(f"{pr[0]} - {pr[1]}  [di bawah 0 = {pr[0]} unggul]  (grafik eksploratori)")
    ax[i].legend(fontsize=8)
for i, aa in enumerate(ax):
    mark_events(aa, label=(i == 0))
fig.tight_layout(); fig.savefig(FIG / "30_fluctuation.png", dpi=130)

# ---------------------------------------------------------------- daya (opsional)
if a.daya:
    T = len(x); xv = x.values
    seg = np.searchsorted(np.asarray(u["parts"][u["m_star"]]), np.arange(1, T + 1), side="left")
    means = pd.Series(xv).groupby(seg).mean().values
    e = xv - means[seg]; rng = np.random.default_rng(2026)
    sd = x.resample("YS").mean().std()
    out += ["", f"== Analisis daya UDmax (blok 30 hari, {C.POWER_REPS} ulangan, break di tengah) =="]
    pw = []
    for k in [0, 0.5, 1, 2, 3, 4]:
        delta = k * sd; rej = 0
        for _ in range(C.POWER_REPS):
            st_ = rng.integers(0, T - 30, T // 30 + 1)
            y = np.concatenate([e[s:s + 30] for s in st_])[:T]; y[T // 2:] += delta
            rej += S.udmax(y)["udmax"] > cv_sim
        pw.append((delta, rej / C.POWER_REPS))
        out.append(f"  delta = {delta:.4f} ({k} x sd rata-rata dL tahunan)  daya = {rej / C.POWER_REPS:.2f}")
    res["daya"] = pw

save_json("30_rq1.json", res)
write("30_rq1.txt", "\n".join(out))
```


### `31_rq2.py`

```python
"""31 - RQ2.
H2a (konfirmatori): regresi dL bulanan pasangan konfirmatori (S2-365) pada 4 karakteristik pasar,
     uji-F bersama HAC.  Aturan stasioneritas (dikunci): regresor di-differencing bila ADF gagal menolak
     unit root (p > 0,05) DAN KPSS menolak stasioneritas (p < 0,05); dummy era selalu disertakan.
H2b (konfirmatori): beda rata-rata kontribusi fitur X antara era transition dan institutional, uji-t HAC,
     untuk dL(HAR-X - HAR) dan dL(LGBM-X - LGBM-HAR); dua uji -> koreksi Holm.
Pakai: python 31_rq2.py [--likuiditas cs]   (cs = Corwin-Schultz, sensitivitas)"""
import argparse, warnings
import numpy as np
import pandas as pd
from scipy.stats import ks_2samp
from statsmodels.tsa.stattools import adfuller, kpss
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from rvlib import config as C
from rvlib import stats as S
from rvlib.data import design
from rvlib.models import model_cols
from rvlib.analysis import load, dL, era, write, save_json, FIG
warnings.filterwarnings("ignore")

ap = argparse.ArgumentParser(); ap.add_argument("--likuiditas", choices=["ar", "cs"], default="ar")
a = ap.parse_args()
FIG.mkdir(parents=True, exist_ok=True)
raw = pd.read_csv(C.DAILY, index_col="date", parse_dates=True)
d, first = design(raw)
fc, L = load(C.CONF_SCHEME)
out, res = [], {}

# ---------------------------------------------------------------- likuiditas harian
lh, ll, c = np.log(raw["high"]), np.log(raw["low"]), np.log(raw["close"])
if a.likuiditas == "ar":       # Abdi & Ranaldo (2017), estimasi dua hari, negatif -> 0
    eta = (lh + ll) / 2
    liq = np.sqrt((4 * (c - eta) * (c - eta.shift(-1))).clip(lower=0))
else:                          # Corwin & Schultz (2012), negatif -> 0
    beta = (lh - ll) ** 2 + (lh.shift(-1) - ll.shift(-1)) ** 2
    gamma = (np.maximum(lh, lh.shift(-1)) - np.minimum(ll, ll.shift(-1))) ** 2
    k = 3 - 2 * np.sqrt(2)
    alpha = (np.sqrt(2 * beta) - np.sqrt(beta)) / k - np.sqrt(gamma / k)
    liq = (2 * (np.exp(alpha) - 1) / (1 + np.exp(alpha))).clip(lower=0)
lnrv = np.log(raw["rv"].where(raw["rv"] > 0))

# ---------------------------------------------------------------- variabel bulanan
feats = model_cols("LGBM_X")
W = C.SCHEMES[C.CONF_SCHEME][1]
x = dL(L, C.CONF_PAIR)
rows = []
for ms in x.resample("MS").mean().index:
    me = ms + pd.offsets.MonthBegin(1)
    t = d["target_date"]
    tr, te = d[(t < ms) & (t >= ms - pd.Timedelta(days=W))][feats], d[(t >= ms) & (t < me)][feats]
    ks = np.mean([ks_2samp(tr[f], te[f]).statistic for f in feats])
    psi = []
    for f in feats:
        q = np.unique(np.quantile(tr[f], np.linspace(0, 1, 11)))
        p1 = np.histogram(tr[f], np.r_[-np.inf, q[1:-1], np.inf])[0] / len(tr) + 1e-6
        p2 = np.histogram(te[f], np.r_[-np.inf, q[1:-1], np.inf])[0] / len(te) + 1e-6
        psi.append(np.sum((p2 - p1) * np.log(p2 / p1)))
    m = (raw.index >= ms) & (raw.index < me)
    rows.append(dict(bulan=ms, dL=x[(x.index >= ms) & (x.index < me)].mean(),
                     level_vol=lnrv[m].mean(), volvol=lnrv[m].std(), likuiditas=liq[m].mean(),
                     ks_shift=ks, psi=np.mean(psi)))
Mo = pd.DataFrame(rows).set_index("bulan").dropna()
Mo.to_csv(f"{C.RESULTS}/31_bulanan_{a.likuiditas}.csv")

out.append(f"== H2a: regresi dL bulanan {x.name} ({C.CONF_SCHEME}), likuiditas = "
           f"{'Abdi-Ranaldo' if a.likuiditas == 'ar' else 'Corwin-Schultz'}, {len(Mo)} bulan ==")
out.append("  Stasioneritas (ADF H0 unit root | KPSS H0 stasioner):")
X = pd.DataFrame(index=Mo.index); dif = []
for v in C.RQ2_REGRESSORS:
    pa, pk = adfuller(Mo[v], autolag="AIC")[1], kpss(Mo[v], regression="c", nlags="auto")[1]
    nonst = pa > 0.05 and pk < 0.05
    X[v] = Mo[v].diff() if nonst else Mo[v]
    dif += [v] if nonst else []
    out.append(f"    {v:<11} ADF p={pa:.3f}  KPSS p={pk:.3f}  -> {'differencing' if nonst else 'level'}")
pa, pk = adfuller(Mo["dL"], autolag="AIC")[1], kpss(Mo["dL"], regression="c", nlags="auto")[1]
dl_nonst = pa > 0.05 and pk < 0.05
out.append(f"    {'dL (terikat)':<11} ADF p={pa:.3f}  KPSS p={pk:.3f}  -> "
           f"{'TIDAK STASIONER (cek regresi palsu!)' if dl_nonst else 'stasioner, dipakai level'}")
X["era_inst"] = (X.index >= C.ERA_SPLIT).astype(float)
ok = X.notna().all(axis=1)
r = S.ols_hac(Mo.loc[ok, "dL"], X[ok], list(X.columns))
w = S.wald(r, [1, 2, 3, 4])
for nm, t in r["tab"].items():
    out.append(f"    {nm:<11} koef={t['coef']:+.4f}  SE={t['se']:.4f}  t={t['t']:+.2f}  p={t['p']:.3f}")
out.append(f"  Uji-F bersama 4 karakteristik (HAC): F = {w['F']:.2f}, p = {w['p']:.4f}   R2 = {r['r2']:.3f}")
h2a = w["p"] < C.ALPHA
out.append(f"  => H2a {'DIDUKUNG' if h2a else 'TIDAK didukung'} (asosiatif, bukan kausal)")
res["H2a"] = dict(F=w["F"], p=w["p"], didukung=h2a, differencing=dif, n=int(ok.sum()),
                  dL_adf_p=pa, dL_kpss_p=pk, dL_tidak_stasioner=dl_nonst,
                  koef={k: v for k, v in r["tab"].items()})
out.append(f"  Pelengkap: korelasi dL bulanan dengan PSI rata-rata = {Mo['dL'].corr(Mo['psi']):+.3f} (deskriptif)")

# ---------------------------------------------------------------- H2b
out += ["", "== H2b: kontribusi fitur X, institutional vs transition (S2-365, QLIKE) =="]
ps, h2b = [], {}
for pr in [("HARX", "HAR"), ("LGBM_X", "LGBM_HAR")]:
    cdl = dL(L, pr)
    D = (cdl.index >= C.ERA_SPLIT).astype(float)
    rr = S.ols_hac(cdl.values, D[:, None], ["era_inst"])
    t = rr["tab"]["era_inst"]
    mt, mi = cdl[cdl.index < C.ERA_SPLIT].mean(), cdl[cdl.index >= C.ERA_SPLIT].mean()
    ps.append(t["p"])
    h2b[cdl.name] = dict(mean_transition=mt, mean_institutional=mi, selisih=t["coef"], t=t["t"], p=t["p"])
ph = S.holm(ps)
for (k, v), p_adj in zip(h2b.items(), ph):
    v["p_holm"] = p_adj
    out.append(f"  {k:<18} transition {v['mean_transition']:+.4f} | institutional {v['mean_institutional']:+.4f} "
               f"| selisih {v['selisih']:+.4f}  t={v['t']:+.2f}  p={v['p']:.4f}  p_Holm={p_adj:.4f}")
sup = any(p < C.ALPHA for p in ph)
out.append(f"  => H2b {'DIDUKUNG' if sup else 'TIDAK didukung'} (minimal satu kontribusi berbeda antarera setelah Holm)")
res["H2b"] = dict(detail=h2b, didukung=sup)

fig, ax = plt.subplots(1, 4, figsize=(15, 3.5))
for i, v in enumerate(C.RQ2_REGRESSORS):
    ax[i].scatter(Mo[v], Mo["dL"], s=12, c=(Mo.index >= C.ERA_SPLIT), cmap="coolwarm")
    ax[i].axhline(0, color="k", lw=0.6); ax[i].set_xlabel(v); ax[i].set_ylabel("dL bulanan")
fig.suptitle("dL bulanan vs karakteristik pasar (biru = transition, merah = institutional)")
fig.tight_layout(); fig.savefig(FIG / f"31_rq2_{a.likuiditas}.png", dpi=120)

save_json(f"31_rq2_{a.likuiditas}.json", res)
write(f"31_rq2_{a.likuiditas}.txt", "\n".join(out))
```


### `32_rq3.py`

```python
"""32 - RQ3: strategi pembaruan & panjang window.
Konfirmatori (v2.5): rata-rata D_t = dL_t(S2-365) - dL_t(S1) di era institutional, pasangan konfirmatori,
uji-t HAC. H3 didukung bila rata-rata D_t < 0 dan signifikan. D_t > 0 signifikan = hipotesis tandingan.
Eksploratori (+Holm): era transition, strategi/W lain, S0, kurva window, efek jumlah vs umur data."""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from rvlib import config as C
from rvlib import stats as S
from rvlib.analysis import load, dL, common, write, save_json, FIG, mark_events

FIG.mkdir(parents=True, exist_ok=True)
out, res = [], {}
X = {nm: dL(load(nm)[1], C.CONF_PAIR) for nm in list(C.SCHEMES) + list(C.SCHEMES_OPTIONAL)}
Lm = {nm: load(nm)[1] for nm in list(C.SCHEMES) + list(C.SCHEMES_OPTIONAL)}

a, b = common(X["S2_365"], X["S1"])
D = a - b
Di = D[D.index >= C.ERA_SPLIT]
r = S.mean_test(Di.values)
if r["p"] < C.ALPHA and r["mean"] < 0:
    verdict = "H3 DIDUKUNG: rolling-365 memberi keunggulan relatif lebih besar daripada expanding"
elif r["p"] < C.ALPHA:
    verdict = "H3 TIDAK didukung; arah sebaliknya signifikan (hipotesis tandingan: expanding lebih baik)"
else:
    verdict = "H3 TIDAK didukung; tidak ada beda signifikan antara rolling-365 dan expanding"
res["konfirmatori"] = dict(**r, verdict=verdict)
out += [f"== KONFIRMATORI RQ3: D = dL(S2-365) - dL(S1), {C.CONF_PAIR[0]}-{C.CONF_PAIR[1]}, era institutional ==",
        f"  n = {r['n']}  mean D = {r['mean']:+.4f}  t(HAC Andrews) = {r['t']:+.2f}  p = {r['p']:.4f}",
        f"  => {verdict}"]

# ---------------------------------------------------------------- eksploratori
rows = []


def add(nama, s):
    rr = S.mean_test(s.values)
    rows.append(dict(perbandingan=nama, n=rr["n"], mean=rr["mean"], t=rr["t"], p=rr["p"]))


add("D(S2-365 vs S1) transition", D[D.index < C.ERA_SPLIT])
# apakah D digerakkan segelintir hari ekstrem?
k1 = max(1, int(0.01 * len(Di)))
add(f"D institutional tanpa {k1} hari |D| terbesar", Di.drop(Di.abs().nlargest(k1).index))
# robustness loss: MSE pada level RV (v2.5 V.6, pelengkap)
am, bm = common(dL(load("S2_365", "mse")[1], C.CONF_PAIR), dL(load("S1", "mse")[1], C.CONF_PAIR))
Dm = am - bm
rm = S.mean_test(Dm[Dm.index >= C.ERA_SPLIT].values)
res["mse_institutional"] = rm
add("MSE: D(S2-365 vs S1) institutional", Dm[Dm.index >= C.ERA_SPLIT])
add("MSE: D(S2-365 vs S1) semua", Dm)
add("D(S2-365 vs S1) semua", D)
for x1, x2 in [("S2_730", "S1"), ("S0", "S1"), ("S2_730", "S2_365"), ("S2_180", "S2_365"), ("S2_1095", "S1")]:
    p, q = common(X[x1], X[x2]); dd = p - q
    add(f"D({x1} vs {x2}) institutional", dd[dd.index >= C.ERA_SPLIT])
for pr in C.EXPLORATORY_PAIRS:
    p, q = common(dL(Lm["S2_365"], pr), dL(Lm["S1"], pr)); dd = p - q
    add(f"D(S2-365 vs S1) {pr[0]}-{pr[1]} institutional", dd[dd.index >= C.ERA_SPLIT])
# jumlah vs umur data (Bagian VII.2)
p, q = common(X["S2_730"], X["S2_365"]); add("Efek JUMLAH: S2-730 - S2-365", p - q)
p, q = common(X["TUNDA_365"], X["S2_365"]); add("Efek UMUR: tertunda - S2-365", p - q)
E = pd.DataFrame(rows); E["p_holm"] = S.holm(E["p"].values)
E.to_csv(f"{C.RESULTS}/32_eksploratori.csv", index=False)
out += ["", "== EKSPLORATORI (negatif = konfigurasi pertama lebih baik untuk ML relatif HAR) ==",
        E.to_string(index=False, float_format=lambda v: f"{v:+.4g}"),
        "  (baris MSE: satuan RV^2, bandingkan tanda dan t, bukan besarnya)"]

# ---------------------------------------------------------------- kurva window
order = ["S2_180", "S2_365", "S2_730", "S2_1095", "S1"]
st = max(X[k].index.min() for k in order)
cur = []
for k in order:
    LL = Lm[k][Lm[k].index >= st]
    rr = S.mean_test(dL(LL, C.CONF_PAIR).values)
    LM = load(k, "mse")[1]; LM = LM[LM.index >= st]
    cur.append(dict(skema=k, n=rr["n"], mean_dL=rr["mean"], t=rr["t"],
                    t_mse=S.mean_test(dL(LM, C.CONF_PAIR).values)["t"],
                    **{f"L_{m}": LL[m].mean() for m in C.MODELS}))
cur = pd.DataFrame(cur); cur.to_csv(f"{C.RESULTS}/32_kurva_window.csv", index=False)
out += ["", f"== Kurva panjang window, periode bersama mulai {st.date()} ==",
        cur.to_string(index=False, float_format=lambda v: f"{v:+.4f}")]
res["kurva"] = cur.to_dict("records")

fig, ax = plt.subplots(1, 2, figsize=(13, 4))
ax[0].plot(cur["skema"], cur["mean_dL"], "o-"); ax[0].axhline(0, color="k", lw=0.8)
ax[0].set_title(f"Rata-rata dL {C.CONF_PAIR[0]}-{C.CONF_PAIR[1]} per skema (sejak {st.date()})")
for m in C.MODELS:
    ax[1].plot(cur["skema"], cur[f"L_{m}"], "o-", label=m)
ax[1].legend(); ax[1].set_title("Rata-rata QLIKE per model")
fig.tight_layout(); fig.savefig(FIG / "32_kurva_window.png", dpi=120)
fig, ax = plt.subplots(figsize=(12, 3.5))
ax.plot(D.cumsum()); mark_events(ax, label=True); ax.axhline(0, color="k", lw=0.6)
ax.set_title("Kumulatif D = dL(S2-365) - dL(S1): naik = expanding lebih baik, turun = rolling lebih baik", pad=16)
fig.tight_layout(); fig.savefig(FIG / "32_kumulatif_D.png", dpi=120)

save_json("32_rq3.json", res)
write("32_rq3.txt", "\n".join(out))
```


### `33_sensitivitas.py`

```python
"""33 - Sensitivitas (eksploratori): apakah kesimpulan konfirmatori berubah?
Untuk tiap variasi: dL(LGBM-X - HAR) S2-365 (mean, t DM, UDmax p) dan D RQ3 institutional."""
import json
from pathlib import Path
import pandas as pd
from rvlib import config as C
from rvlib import stats as S
from rvlib.analysis import load, dL, common, write

sim = S.sim_udmax_null(C.EPS)
rows = []


def row(nama, x, D=None):
    r = S.mean_test(x.values); u = S.udmax(x.values)
    d = S.mean_test(D[D.index >= C.ERA_SPLIT].values) if D is not None else {}
    rows.append(dict(variasi=nama, n=r["n"], mean_dL=r["mean"], t_DM=r["t"], UDmax=u["udmax"],
                     p_UDmax=S.pval(sim[:, 0], u["udmax"]), D_inst=d.get("mean"), t_D=d.get("t")))


def dpair(a, b, pair=C.CONF_PAIR):
    x, y = common(dL(a, pair), dL(b, pair))
    return x - y


main = {k: load(k)[1] for k in ["S2_365", "S1"]}
row("UTAMA", dL(main["S2_365"], C.CONF_PAIR), dpair(main["S2_365"], main["S1"]))
row("tanpa 2026", dL(main["S2_365"], C.CONF_PAIR)[lambda s: s.index < C.Y2026],
    dpair(*[L[L.index < C.Y2026] for L in (main["S2_365"], main["S1"])]))
fcdir = Path(C.RESULTS) / "fc"
for f in sorted(fcdir.glob("sens_*_S2_365.csv")):
    tag = f.stem[len("sens_"):-len("_S2_365")]
    if tag == "har_harian":
        continue
    a = load(f.stem)[1]
    s1 = fcdir / f"sens_{tag}_S1.csv"
    b = load(s1.stem)[1] if s1.exists() else None
    pair = ("RF_X", "HAR") if tag == "rf" else C.CONF_PAIR
    row(tag if tag != "rf" else "rf (RF_X vs HAR)", dL(a, pair), dpair(a, b, pair) if b is not None else None)
if (fcdir / "sens_har_harian_S2_365.csv").exists():
    hd = load("sens_har_harian_S2_365")[1]
    x, y = common(main["S2_365"]["LGBM_X"], hd["HAR_DAILY"])
    row("HAR re-estimasi harian (LGBM-X vs HAR harian)", (x - y).rename("x"))
T = pd.DataFrame(rows)
T.to_csv(f"{C.RESULTS}/33_sensitivitas.csv", index=False)
for k in ["31_rq2_ar.json", "31_rq2_cs.json"]:
    p = Path(C.RESULTS) / k
    if p.exists():
        j = json.loads(p.read_text())
        T.attrs[k] = j["H2a"]["p"]
txt = ["== Sensitivitas pasangan konfirmatori (S2-365) dan D RQ3 (institutional) ==",
       T.to_string(index=False, float_format=lambda v: f"{v:+.4f}"),
       "", "H2a p-value: " + ", ".join(f"{k}: {v:.4f}" for k, v in T.attrs.items())]
write("33_sensitivitas.txt", "\n".join(txt))
```


### `40_laporan.py`

```python
"""40 - Laporan akhir: hasil konfirmatori, sensitivitas, deviasi dari v2.5, integritas (hash config)."""
import hashlib, json
from datetime import datetime
from pathlib import Path
import pandas as pd
from rvlib import config as C

R = Path(C.RESULTS)
J = lambda f: json.loads((R / f).read_text()) if (R / f).exists() else None
man = J("manifest.json")
now_hash = hashlib.sha256(Path("rvlib/config.py").read_bytes()).hexdigest()[:12]
rq1, rq2, rq3 = J("30_rq1.json"), J("31_rq2_ar.json"), J("32_rq3.json")

L = ["# Hasil Penelitian (desain " + C.DESIGN_VERSION + ")", "",
     f"Dibuat {datetime.now():%Y-%m-%d %H:%M}. Forecast dibuat {man['waktu']} dengan config hash "
     f"`{man['config_hash']}`; config sekarang `{now_hash}` "
     + ("(SAMA)." if man["config_hash"] == now_hash else "(**BERBEDA: config diubah setelah forecast dibuat**)."), ""]

L += ["## Uji konfirmatori", "", "| RQ | Uji | Statistik | p | Kesimpulan |", "|---|---|---|---|---|"]
k = rq1["konfirmatori"]
L.append(f"| RQ1 | UDmax dL({C.CONF_PAIR[0]}-{C.CONF_PAIR[1]}), {C.CONF_SCHEME} | UDmax = {k['udmax']:.2f} "
         f"(CV 5% sim. {k['cv5_sim']:.2f}) | {k['p']:.3f} | H1 {'didukung' if k['tolak'] else 'tidak didukung'} |")
if not k["tolak"]:
    L.append(f"| RQ1 (lanjutan) | DM rata-rata dL | mean {k['dm']['mean']:+.4f}, t {k['dm']['t']:+.2f} | "
             f"{k['dm']['p']:.4f} | {'beda signifikan' if k['dm']['p'] < C.ALPHA else 'tidak beda signifikan'} |")
h = rq2["H2a"]
L.append(f"| RQ2 H2a | Uji-F bersama 4 karakteristik (HAC) | F = {h['F']:.2f} | {h['p']:.4f} | "
         f"{'didukung' if h['didukung'] else 'tidak didukung'} |")
for nm, v in rq2["H2b"]["detail"].items():
    L.append(f"| RQ2 H2b | Beda era kontribusi X: {nm} | selisih {v['selisih']:+.4f}, t {v['t']:+.2f} | "
             f"{v['p_holm']:.4f} (Holm) | — |")
L.append(f"| RQ2 H2b | (gabungan) | | | {'didukung' if rq2['H2b']['didukung'] else 'tidak didukung'} |")
k3 = rq3["konfirmatori"]
L.append(f"| RQ3 | D = dL(S2-365) - dL(S1), institutional | mean {k3['mean']:+.4f}, t {k3['t']:+.2f} | "
         f"{k3['p']:.4f} | {k3['verdict']} |")
if rq3.get("mse_institutional"):
    m = rq3["mse_institutional"]
    L.append(f"\nRobustness RQ3 dengan MSE (eksploratori): t = {m['t']:+.2f}, p = {m['p']:.4f} "
             f"(arah {'sama' if (m['mean'] > 0) == (k3['mean'] > 0) else 'BERLAWANAN'} dengan QLIKE).")
if "dL_tidak_stasioner" in h:
    L.append(f"Stasioneritas dL bulanan (RQ2): ADF p = {h['dL_adf_p']:.3f}, KPSS p = {h['dL_kpss_p']:.3f} -> "
             f"{'TIDAK stasioner' if h['dL_tidak_stasioner'] else 'stasioner'}.")

if (R / "33_sensitivitas.csv").exists():
    T = pd.read_csv(R / "33_sensitivitas.csv")
    L += ["", "## Sensitivitas (eksploratori)", "",
          "| Variasi | n | mean dL | t DM | p UDmax | D inst. | t D |", "|---|---|---|---|---|---|---|"]
    f = lambda v: "—" if pd.isna(v) else f"{v:+.4f}"
    for r in T.itertuples():
        L.append(f"| {r.variasi} | {r.n} | {f(r.mean_dL)} | {f(r.t_DM)} | {r.p_UDmax:.3f} | {f(r.D_inst)} | {f(r.t_D)} |")
    cs = J("31_rq2_cs.json")
    if cs:
        L.append(f"\nH2a dengan likuiditas Corwin-Schultz: F = {cs['H2a']['F']:.2f}, p = {cs['H2a']['p']:.4f}.")

L += ["", "## Deviasi dan keputusan implementasi terhadap dokumen v2.5", "",
      f"1. HAR-X tanpa {C.HARX_DROP} (aturan v2.5 V.3, VIF window awal; lihat 10_cek_fitur.txt). LGBM-X memakai semua fitur.",
      "2. Nilai kritis UDmax, uji berurutan, dan Fluctuation test disimulasikan (bukan dikutip dari tabel); "
      "tabel Bai-Perron tetap perlu dicek sebagai pembanding.",
      "3. Tuning: grid dan aturan perluasan di config.py (QLIKE pada exp(yhat), forward-chaining 5 fold).",
      "4. H2b terdiri dari dua uji (HAR-X vs HAR, LGBM-X vs LGBM-HAR); dikoreksi Holm.",
      "5. Aturan stasioneritas RQ2: differencing bila ADF & KPSS sepakat tidak stasioner; dummy era selalu disertakan.",
      "6. Rolling tertunda (Bagian VII.2) dan kurva window dijalankan sebagai eksploratori.",
      "7. Interval kepercayaan tanggal break: r/break_ci.R (opsional, butuh R)."]
L += ["", "## File rinci", ""] + [f"- `{p.name}`" for p in sorted(R.glob("*.txt"))] + \
     [f"- `grafik/{p.name}`" for p in sorted((R / "grafik").glob("*.png"))]
(R / "LAPORAN_HASIL.md").write_text("\n".join(L), encoding="utf-8")
print("\n".join(L))
```


### `run_all.sh`

```bash
#!/usr/bin/env bash
# Pipeline lengkap. Jalankan dari folder ini. Prasyarat: data/raw/5m (01_download.py).
# Opsional: data/raw/1m (python 01_download.py --interval 1m) untuk sensitivitas RV subsampled.
# Uji cepat kode (hasil tidak bermakna): RV_QUICK=1 ./run_all.sh
set -eo pipefail
cd "$(dirname "$0")"
PY="${PYTHON:-$( [ -x .venv/bin/python ] && echo .venv/bin/python || command -v python3 || command -v python )}"
echo "Interpreter: $PY"
OUTDIR=$($PY -c "from rvlib import config as C; print(C.RESULTS)")
mkdir -p "$OUTDIR/log"
run() { echo "================ $* ================"; $PY "$@" 2>&1 | tee "$OUTDIR/log/$(basename "$1" .py).log"; }
run 02_build_daily.py
run 10_cek_fitur.py
run 11_tuning.py
run 20_forecast.py ${RETUNE:+--retune}
run 30_rq1.py ${DAYA:+--daya}
run 31_rq2.py
$PY 31_rq2.py --likuiditas cs > "$OUTDIR/log/31_rq2_cs.log" 2>&1
run 32_rq3.py
run 33_sensitivitas.py
run 40_laporan.py
echo "Selesai -> $OUTDIR/LAPORAN_HASIL.md"
```


### `r/break_ci.R`

```r
# Opsional (eksploratori): interval kepercayaan 95% tanggal break pada dL konfirmatori.
# Pakai: Rscript r/break_ci.R <jumlah_break>   (ambil dari 30_rq1.txt, "Jumlah break terpilih")
suppressPackageStartupMessages({library(strucchange); library(sandwich)})
m  <- as.integer(commandArgs(trailingOnly = TRUE)[1])
if (is.na(m) || m < 1) { cat("Jumlah break 0: tidak ada interval yang dihitung.\n"); quit() }
fc <- read.csv("results/final/fc/S2_365.csv"); fc$target_date <- as.Date(fc$target_date)
q  <- function(rv, f) rv / f - log(rv / f) - 1
dL <- q(fc$rv, fc$LGBM_X) - q(fc$rv, fc$HAR)
bp <- breakpoints(dL ~ 1, h = 0.15, breaks = 5)
ci <- confint(bp, breaks = m, het.err = TRUE)$confint
print(data.frame(bawah = fc$target_date[ci[, 1]], titik = fc$target_date[ci[, 2]], atas = fc$target_date[ci[, 3]]))
```


### `requirements.txt`

```text
pandas>=2.0
numpy>=1.24
lightgbm>=4.0
statsmodels>=0.14
matplotlib>=3.7
requests>=2.31
scikit-learn>=1.3
scipy>=1.10
```


---

## 10. Lampiran: output utama run final


### `results/final/30_rq1.txt`

```text
== Sanity: rata-rata QLIKE per model (S2-365) ==
  NAIVE=0.5293  HAR=0.3592  HARX=0.3627  LGBM_HAR=0.3968  LGBM_X=0.3761
  OK: semua model lebih baik dari naive

== KONFIRMATORI RQ1: LGBM_X-HAR, S2_365, QLIKE (T = 2914) ==
  supF(1)=1.69  supF(2)=4.78  supF(3)=3.76  supF(4)=3.65  supF(5)=4.19
  UDmax = 4.78   p(simulasi) = 0.370   CV 5% simulasi = 9.01 (tabel Bai-Perron 1998 q=1, eps=0,15: ~8,88 -- verifikasi)
  => Tidak menolak H0 perubahan rata-rata. Lanjut uji DM seluruh sampel:
     mean dL = +0.0169  t(HAC Andrews) = +1.16  p = 0.2457  -> tidak berbeda signifikan
  => H1 TIDAK didukung (tidak ada bukti perubahan rata-rata dL).

  Per periode:
      periode  hari    mean       t       p  frac_unggul
        semua  2914 +0.0169 +1.1609 +0.2457      +0.4324
   transition   829 +0.0144 +0.3546 +0.7229      +0.3860
institutional  2085 +0.0179 +1.4751 +0.1402      +0.4508
         2018   118 -0.1416 -0.6044 +0.5456      +0.3136
         2019   355 -0.0124 -0.4785 +0.6323      +0.4169
         2020   356 +0.0928 +1.7378 +0.0822      +0.3792
         2021   353 -0.0330 -0.7363 +0.4616      +0.3853
         2022   365 +0.0688 +3.0435 +0.0023      +0.3945
         2023   363 +0.0694 +1.4592 +0.1445      +0.4545
         2024   366 -0.0115 -0.9535 +0.3403      +0.4918
         2025   365 +0.0134 +0.9669 +0.3336      +0.5096
         2026   273 -0.0078 -0.9903 +0.3220      +0.4725

== EKSPLORATORI (p-value Holm dalam keluarga RQ1) ==
 skema  loss        pasangan           uji    stat      p    mean  p_holm
    S0 qlike      LGBM_X-HAR         UDmax 19.8738 0.0013     NaN  0.0946
    S0 qlike      LGBM_X-HAR            DM  5.1719 0.0000  0.0928  0.0000
    S0 qlike    LGBM_HAR-HAR         UDmax 25.3493 0.0003     NaN  0.0243
    S0 qlike    LGBM_HAR-HAR            DM  6.1486 0.0000  0.1113  0.0000
    S0 qlike        HARX-HAR         UDmax 18.9693 0.0013     NaN  0.0946
    S0 qlike        HARX-HAR            DM  0.0901 0.9282  0.0003  1.0000
    S0 qlike LGBM_X-LGBM_HAR         UDmax  7.8552 0.0870     NaN  1.0000
    S0 qlike LGBM_X-LGBM_HAR            DM -4.7783 0.0000 -0.0185  0.0001
    S0 qlike     LGBM_X-HARX         UDmax 24.8903 0.0003     NaN  0.0243
    S0 qlike     LGBM_X-HARX            DM  5.2369 0.0000  0.0926  0.0000
    S1 qlike      LGBM_X-HAR         UDmax  3.8081 0.5485     NaN  1.0000
    S1 qlike      LGBM_X-HAR            DM -0.6679 0.5042 -0.0072  1.0000
    S1 qlike    LGBM_HAR-HAR         UDmax  3.8500 0.5395     NaN  1.0000
    S1 qlike    LGBM_HAR-HAR            DM  0.1112 0.9115  0.0012  1.0000
    S1 qlike        HARX-HAR         UDmax  5.9590 0.2203     NaN  1.0000
    S1 qlike        HARX-HAR            DM -2.6648 0.0077 -0.0057  0.5161
    S1 qlike LGBM_X-LGBM_HAR         UDmax  2.9289 0.7388     NaN  1.0000
    S1 qlike LGBM_X-LGBM_HAR            DM -1.8356 0.0664 -0.0084  1.0000
    S1 qlike     LGBM_X-HARX         UDmax  2.5122 0.8441     NaN  1.0000
    S1 qlike     LGBM_X-HARX            DM -0.1473 0.8829 -0.0014  1.0000
S2_365 qlike    LGBM_HAR-HAR         UDmax  6.0854 0.2096     NaN  1.0000
S2_365 qlike    LGBM_HAR-HAR            DM  2.8729 0.0041  0.0376  0.2806
S2_365 qlike        HARX-HAR         UDmax  1.1939 0.9963     NaN  1.0000
S2_365 qlike        HARX-HAR            DM  0.2791 0.7802  0.0035  1.0000
S2_365 qlike LGBM_X-LGBM_HAR         UDmax  1.7102 0.9700     NaN  1.0000
S2_365 qlike LGBM_X-LGBM_HAR            DM -1.8623 0.0626 -0.0207  1.0000
S2_365 qlike     LGBM_X-HARX         UDmax  6.1419 0.2033     NaN  1.0000
S2_365 qlike     LGBM_X-HARX            DM  1.1996 0.2303  0.0134  1.0000
S2_730 qlike      LGBM_X-HAR         UDmax  6.9345 0.1343     NaN  1.0000
S2_730 qlike      LGBM_X-HAR            DM  2.1816 0.0291  0.0174  1.0000
S2_730 qlike    LGBM_HAR-HAR         UDmax 12.1180 0.0117     NaN  0.7697
S2_730 qlike    LGBM_HAR-HAR            DM  4.6627 0.0000  0.0272  0.0002
S2_730 qlike        HARX-HAR         UDmax  3.6600 0.5741     NaN  1.0000
S2_730 qlike        HARX-HAR            DM -0.9096 0.3630 -0.0045  1.0000
S2_730 qlike LGBM_X-LGBM_HAR         UDmax  4.0935 0.4948     NaN  1.0000
S2_730 qlike LGBM_X-LGBM_HAR            DM -1.4246 0.1543 -0.0098  1.0000
S2_730 qlike     LGBM_X-HARX         UDmax  6.5213 0.1686     NaN  1.0000
S2_730 qlike     LGBM_X-HARX            DM  3.6791 0.0002  0.0220  0.0173
S2_365 qlike      LGBM_X-HAR UDmax eps0.20  5.1579 0.2416     NaN  1.0000
  (versi MSE lengkap di 30_eksploratori.csv)

== Uji break berurutan supF(l+1|l), pasangan konfirmatori (eksploratori) ==
  supF(1|0) = 1.69  p(simulasi) = 0.873
  Jumlah break terpilih: 0

== Analisis daya UDmax (blok 30 hari, 200 ulangan, break di tengah) ==
  delta = 0.0000 (0 x sd rata-rata dL tahunan)  daya = 0.02
  delta = 0.0352 (0.5 x sd rata-rata dL tahunan)  daya = 0.15
  delta = 0.0704 (1 x sd rata-rata dL tahunan)  daya = 0.58
  delta = 0.1408 (2 x sd rata-rata dL tahunan)  daya = 0.98
  delta = 0.2112 (3 x sd rata-rata dL tahunan)  daya = 1.00
  delta = 0.2816 (4 x sd rata-rata dL tahunan)  daya = 1.00
```


### `results/final/31_rq2_ar.txt`

```text
== H2a: regresi dL bulanan LGBM_X-HAR (S2_365), likuiditas = Abdi-Ranaldo, 97 bulan ==
  Stasioneritas (ADF H0 unit root | KPSS H0 stasioner):
    level_vol   ADF p=0.488  KPSS p=0.012  -> differencing
    volvol      ADF p=0.000  KPSS p=0.100  -> level
    likuiditas  ADF p=0.000  KPSS p=0.010  -> level
    ks_shift    ADF p=0.000  KPSS p=0.051  -> level
    dL (terikat) ADF p=0.000  KPSS p=0.100  -> stasioner, dipakai level
    const       koef=-0.1382  SE=0.1555  t=-0.89  p=0.374
    level_vol   koef=+0.0022  SE=0.0266  t=+0.08  p=0.935
    volvol      koef=+0.0364  SE=0.1372  t=+0.27  p=0.791
    likuiditas  koef=+1.6425  SE=5.6571  t=+0.29  p=0.772
    ks_shift    koef=+0.2743  SE=0.2233  t=+1.23  p=0.219
    era_inst    koef=+0.0170  SE=0.0346  t=+0.49  p=0.624
  Uji-F bersama 4 karakteristik (HAC): F = 0.81, p = 0.5199   R2 = 0.038
  => H2a TIDAK didukung (asosiatif, bukan kausal)
  Pelengkap: korelasi dL bulanan dengan PSI rata-rata = +0.101 (deskriptif)

== H2b: kontribusi fitur X, institutional vs transition (S2-365, QLIKE) ==
  HARX-HAR           transition +0.0331 | institutional -0.0082 | selisih -0.0414  t=-1.12  p=0.2630  p_Holm=0.5259
  LGBM_X-LGBM_HAR    transition -0.0116 | institutional -0.0243 | selisih -0.0127  t=-0.65  p=0.5132  p_Holm=0.5259
  => H2b TIDAK didukung (minimal satu kontribusi berbeda antarera setelah Holm)
```


### `results/final/32_rq3.txt`

```text
== KONFIRMATORI RQ3: D = dL(S2-365) - dL(S1), LGBM_X-HAR, era institutional ==
  n = 2085  mean D = +0.0241  t(HAC Andrews) = +2.37  p = 0.0179
  => H3 TIDAK didukung; arah sebaliknya signifikan (hipotesis tandingan: expanding lebih baik)

== EKSPLORATORI (negatif = konfigurasi pertama lebih baik untuk ML relatif HAR) ==
                                 perbandingan    n       mean          t          p     p_holm
                   D(S2-365 vs S1) transition  829   +0.02402     +1.151    +0.2498         +1
   D institutional tanpa 20 hari |D| terbesar 2065   +0.01475     +3.351 +0.0008052   +0.01047
           MSE: D(S2-365 vs S1) institutional 2085 -4.359e-08    -0.4894    +0.6246         +1
                   MSE: D(S2-365 vs S1) semua 2914 +4.108e-07    +0.8706     +0.384         +1
                        D(S2-365 vs S1) semua 2914   +0.02406     +2.555   +0.01061    +0.1061
                D(S2_730 vs S1) institutional 2085   +0.02004      +3.12  +0.001809   +0.02171
                    D(S0 vs S1) institutional 2085    +0.1189     +6.984 +2.863e-12 +4.581e-11
            D(S2_730 vs S2_365) institutional 2085   -0.00403    -0.7047     +0.481         +1
            D(S2_180 vs S2_365) institutional 2085  +0.003682    +0.2821    +0.7779         +1
               D(S2_1095 vs S1) institutional 2085  +0.008373    +0.9843     +0.325         +1
   D(S2-365 vs S1) LGBM_HAR-HAR institutional 2085   +0.04012     +4.551  +5.33e-06 +7.994e-05
       D(S2-365 vs S1) HARX-HAR institutional 2085 -9.208e-06 -0.0009782    +0.9992         +1
D(S2-365 vs S1) LGBM_X-LGBM_HAR institutional 2085   -0.01605     -1.398     +0.162         +1
    D(S2-365 vs S1) LGBM_X-HARX institutional 2085   +0.02408     +3.662 +0.0002501  +0.003502
                 Efek JUMLAH: S2-730 - S2-365 2559   -0.01174     -2.012   +0.04426    +0.3984
                 Efek UMUR: tertunda - S2-365 2559   +0.04563     +2.788  +0.005308   +0.05839
  (baris MSE: satuan RV^2, bandingkan tanda dan t, bukan besarnya)

== Kurva panjang window, periode bersama mulai 2020-09-01 ==
  skema    n  mean_dL       t   t_mse   L_HAR  L_HARX  L_LGBM_HAR  L_LGBM_X
 S2_180 2205  +0.0201 +1.6791 +1.6094 +0.3317 +0.3342     +0.3651   +0.3519
 S2_365 2205  +0.0155 +1.3486 -0.3525 +0.3190 +0.3110     +0.3587   +0.3346
 S2_730 2205  +0.0128 +1.6288 -0.6303 +0.3203 +0.3126     +0.3436   +0.3330
S2_1095 2205  +0.0020 +0.2292 -0.6021 +0.3190 +0.3093     +0.3282   +0.3210
     S1 2205  -0.0059 -1.1515 +0.2518 +0.3193 +0.3114     +0.3214   +0.3134
```


### `results/final/33_sensitivitas.txt`

```text
== Sensitivitas pasangan konfirmatori (S2-365) dan D RQ3 (institutional) ==
                                      variasi    n  mean_dL    t_DM   UDmax  p_UDmax  D_inst     t_D
                                        UTAMA 2914  +0.0169 +1.1609 +4.7792  +0.3695 +0.0241 +2.3672
                                   tanpa 2026 2641  +0.0194 +1.2133 +4.2622  +0.4648 +0.0273 +2.3442
                           hari_tidak_lengkap 2952  +0.0235 +1.5596 +3.9266  +0.5268 +0.0335 +1.9978
                                      init730 2559  +0.0280 +1.6351 +4.2535  +0.4668 +0.0206 +2.5827
                                      lag5_22 2914  +0.0222 +1.5359 +5.4237  +0.2796 +0.0144 +1.5916
                             rf (RF_X vs HAR) 2914  +0.0135 +0.8430 +4.3811  +0.4395 +0.0230 +3.5459
                                         rv15 2914  +0.0226 +1.6634 +2.9399  +0.7351 +0.0303 +2.3704
                                     tanpa_bc 2914  +0.0038 +0.2223 +2.8531  +0.7571 +0.0257 +1.8927
HAR re-estimasi harian (LGBM-X vs HAR harian) 2914  +0.0155 +1.0261 +4.3680  +0.4412     NaN     NaN

H2a p-value: 31_rq2_ar.json: 0.5199, 31_rq2_cs.json: 0.4707
```


### `results/final/10_cek_fitur.txt`

```text
[OK] HAR-X tanpa ['ln_amihud']: VIF fitur X maksimum 6.9

              VIF_semua_fitur  VIF_HARX_final
d_ln_dvol                1.41            1.40
ln_amihud               19.59             NaN
ln_dvol                 18.21            1.35
ln_parkinson             6.91            6.88
ln_rv_d                 10.72            9.84
ln_rv_m                  4.79            4.73
ln_rv_w                  7.17            7.13
neg_share                1.46            1.46
ret                      1.64            1.62
```


### `results/final/11_tuning_main.txt`

```text
LGBM_HAR: {'num_leaves': 3, 'min_child_samples': 10, 'n_estimators': 300, 'learning_rate': 0.03, 'reg_lambda': 1.0} | CV QLIKE 0.3574 | iterasi perluasan grid 1
LGBM_X: {'num_leaves': 3, 'min_child_samples': 5, 'n_estimators': 300, 'learning_rate': 0.03, 'reg_lambda': 1.0} | CV QLIKE 0.3187 | iterasi perluasan grid 1
```


### `results/final/11_tuning_init730.txt`

```text
LGBM_HAR: {'num_leaves': 3, 'min_child_samples': 40, 'n_estimators': 100, 'learning_rate': 0.03, 'reg_lambda': 10.0} | CV QLIKE 0.4429 | iterasi perluasan grid 0
LGBM_X: {'num_leaves': 15, 'min_child_samples': 40, 'n_estimators': 100, 'learning_rate': 0.03, 'reg_lambda': 10.0} | CV QLIKE 0.4476 | iterasi perluasan grid 0
```
