# Hasil Eksperimen Skripsi v3.3 — Uji Coba P1 & P2, Desain Final v4, dan Source Code

> **Fungsi file ini:** konteks lengkap eksperimen untuk skripsi v3 (prediksi harga BTC/IDR dengan model boosting). Isinya: kronologi, **desain final v4** (hasil review dosen 11 Nov 2026) yang akan dipakai pada eksperimen Februari 2027, hasil **dua uji coba** (P1: satu minggu, P2: ±31,7 hari), temuan uji coba, kalimat yang aman ditulis, hal yang masih terbuka, cara menjalankan, dan **source code final v4**.
>
> **Status per 13 November 2026:**
> - P1 (14–20 Okt 2026, 92 run) dan P2 (10 Okt – 10 Nov 2026, 120 run) **selesai**. Keduanya **uji coba**, bukan hasil skripsi.
> - Kode direvisi menjadi **v4** sesuai review dosen 11 Nov 2026 (K1–K10). Repo `ferdiendahas/prediksi_btc`, branch `main` = `revisi-dosen-v4` = commit `ed8b735`. Uji cepat lolos; v4 **belum** dipakai untuk eksperimen penuh. SHA-256 di Lampiran B dicocokkan ulang dengan repo pada 13 Nov 2026 (semua sama).
> - Eksperimen final dijalankan **Februari 2027** dengan kode v4 dan data Okt 2026 – Feb 2027.
>
> **Perubahan v3.3 (13 Nov 2026):** daftar run yang lolos Holm sebagai lebih buruk diperjelas (Bagian 4.3); dasar angka spread diberi keterangan (Bagian 4.5); rekomendasi aturan duplikat Holm (Bagian 7 poin 8); catatan keterbatasan blok uji tunggal (Bagian 5 poin 11). Angka dan kode tidak berubah.
>
> **Menggantikan:** `hasil_eksperimen_v3.2.md`, `hasil_eksperimen_v3.1.md`, dan `hasil_eksperimen_v3.0.md`. Ketiganya jadi arsip.
>
> **Aturan Bab I–III:** angka dan peringkat di dokumen ini **tidak boleh** masuk Bab I–III. Bab I–III hanya memuat desain (Bagian 3), data, alasan metode, dan literatur.
>
> **Notasi:** BTC/IDR = spot Indodax. "MAE vs Naive (%)" negatif = model lebih akurat dari Naive. ✓ = signifikan lebih baik (MAE vs Naive < 0, DM_MAE < 0, p_MAE < 0,05); ✗ = signifikan lebih buruk (DM_MAE > 0, p_MAE < 0,05). Di P1/P2, ✓/✗ memakai p tanpa koreksi kecuali disebut Holm. *corr* = korelasi return prediksi dengan return aktual di data uji.

---

## 1. Jawaban singkat

**Apa yang sudah diketahui dari dua uji coba?**
1. Keempat model boosting **tidak bisa mengalahkan Naive secara berarti**. Masing-masing percobaan hanya punya 1 run signifikan lebih baik (p < 0,05), dan **tidak ada yang lolos koreksi Holm** (0 dari 92 dan 0 dari 120).
2. **Tanpa tuning, model jauh lebih buruk** dari Naive (+9% di P1, +12% di P2). Tuning membawanya kembali ke sekitar Naive. Ini konsisten di kedua percobaan.
3. Di antara metode tuning bedanya kecil. **TPE paling baik untuk XGBoost, LightGBM, dan CatBoost di kedua percobaan.**
4. **AdaBoost paling lemah dan paling tidak stabil** di kedua percobaan.
5. **Time frame terpilih tidak stabil** (P1 candle 1 menit h1, P2 ticker 5 menit h60). Penyebab utamanya kondisi pasar di periode uji (P1 datar/naik, P2 turun 6,3%).
6. **Sinyal nyata hanya ada di horizon 1 menit**, dan muncul di kedua percobaan. Keunggulan di h60 pada P2 berasal dari tren turun, bukan dari kemampuan prediksi.

**Apa yang berubah untuk eksperimen final?** Pemilihan Tahap 1–2 kini memakai **skor validasi saja**, blok uji final **tetap 20% terakhir** untuk semua skenario, Tahap 3 memvariasikan **panjang data latih** (bukan rasio split), objektif tuning **MAE rupiah**, seleksi fitur **di dalam fold**, dan signifikansi memakai **koreksi Holm**. Dataset kedua diganti **candle 5 menit** (agregasi candle 1 menit). Karena itu angka P1/P2 **tidak bisa dibandingkan langsung** dengan hasil final.

---

## 2. Kronologi

| Tanggal | Kejadian | Hasil kunci |
|---|---|---|
| 20–22 Okt 2026 | Pilot kode lama `btc5m` (ticker 5 menit, h5) | Tuning menurunkan error 20–37% dari default; semua model sedikit di belakang Naive |
| 23 Okt | Bimbingan: harga BTC/IDR, 4 model, split 80:20/70:30/60:40, optimasi sebanyak mungkin, TF dicari lewat eksperimen | Paket `prediksi_btc` dibuat |
| 27 Okt 10:08 WIB | Aturan pemilihan P1 dikunci (`KEPUTUSAN_TERKUNCI.md`) | — |
| 27–28 Okt | **P1**: Tahap 1–4, data 14–20 Okt, 92 run, 73 menit (Apple M5) | candle_1m h1 → TPE; 1 run ✓ (LightGBM+TPE+L1) |
| 4 Nov | Dipastikan Indodax tidak menyediakan candle 5 menit (`tf` = 1, 15, 30, 60, 240, 1D, 3D, 1W) | Dataset kedua diusulkan diganti candle 5 menit |
| 6 Nov | RM direvisi (lihat Bagian 8) | Uji coba seminggu dinyatakan sementara |
| 10–11 Nov | **P2**: kode sama, data 10 Okt – 10 Nov, 120 run, ±96 menit | ticker_5m h60 → CMA-ES; 1 run ✓ (LightGBM+CMA-ES+L1, datar) |
| 11 Nov | Review dosen → brief kode K1–K12 | — |
| 12 Nov | **Kode v4** (commit `ed8b735`), uji cepat lolos, `main` disamakan dengan `revisi-dosen-v4` | Siap untuk eksperimen final |
| 13 Nov | Holm per tahap dihitung ulang untuk P1/P2 (analisis tambahan, tidak mengubah pilihan) | 0 run lolos Holm sebagai lebih baik |
| Feb 2027 | Eksperimen final dengan kode v4 | ⏳ |

---

## 3. Desain final v4 (untuk eksperimen Februari 2027)

Bagian ini sudah sejalan dengan Bab III di repo `skripsi-latex` (perbaikan v1.9), kecuali aturan duplikat Holm (Bagian 7 poin 8).

| Komponen | Desain v4 | Beda dengan P1/P2 |
|---|---|---|
| Data | API publik Indodax, BTC/IDR spot; collector cron tiap 1 menit di VPS (UTC), SQLite | sama |
| Dataset | `candle_1m` (asli) dan `candle_5m` (agregasi candle 1 menit: open pertama, high maks, low min, close terakhir, volume jumlah; waktu = awal bar; `n_parsial` dicatat) | P1/P2 memakai `ticker_5m` |
| Periode | Data Okt 2026 – Feb 2027 (batas pasti ⏳; Bab I menulis 10 Okt 2026 – 10 Feb 2027) | P1 7 hari; P2 31,7 hari |
| Harga | *typical* = (high+low+close)/3 | sama (ticker *mid* tidak dipakai lagi) |
| Target | log return h menit ke depan; prediksi rupiah = harga_now × exp(return_pred) | sama |
| *Time frame* | 1, 5, 15, 30, 60 menit (1 menit hanya candle_1m) → 9 pasangan; satu pasangan dipilih di Tahap 1 | sama jumlahnya |
| Fitur | 42 fitur: lag return 1–12, statistik bergulir 5–240 menit, range, posisi bar, volume, jam sin/cos | sama (candle_5m memakai jendela minimal 2 bar, sehingga jendela 5 menit menjadi 10 menit) |
| Model | XGBoost, LightGBM, CatBoost, AdaBoost (AdaBoost.R2) + Naive | sama |
| Pembagian data | **Blok uji final = 20% bar terakhir mulai t_u** (tetap untuk semua skenario per dataset × horizon). Data pengembangan = baris dengan **t + h < t_u** (purging berbasis waktu), jadi sedikit kurang dari 80% | P1/P2: split baris 80:20/70:30/60:40, buang h baris terakhir |
| Validasi | Walk-forward 5 fold (`TimeSeriesSplit` tanpa gap) + purging berbasis waktu per fold (t + h < awal validasi) | P1/P2: gap = h baris |
| Objektif tuning | **MAE harga (rupiah)** rata-rata fold; skor Naive di fold yang sama dicatat → `cv_vs_naive_pct` | P1/P2: MAE return |
| Optimasi | default, Grid (27), Random, TPE, CMA-ES, GA (NSGA-II), QMC (30 trial); seed 42 | sama |
| Teknik tambahan | early stopping (maks 2.000 pohon, sabar 50), top-15 fitur **di dalam fold**, loss L1, pruner median. AdaBoost + early stop/L1 = `tidak_berlaku` | P1/P2: top-15 di luar fold; AdaBoost tetap dijalankan |
| Tahap 1 | Pilih (dataset, h) dengan `cv_vs_naive_pct` terkecil di antara 4 model; seri → h lebih pendek → candle_1m. **Tanpa syarat signifikansi** | P1/P2: dari data uji, diutamakan yang signifikan |
| Tahap 2 | Pilih strategi dengan rata-rata `cv_vs_naive_pct` 4 model terkecil; **default boleh terpilih**; seri → waktu tuning terpendek | P1/P2: dari data uji; default dilarang |
| Tahap 3 | Panjang data latih 100% / 75% / 50% (bagian akhir data pengembangan); blok uji tetap. Tanpa pemilihan | P1/P2: rasio split (blok uji ikut berubah) |
| Tahap 4 | 4 teknik tambahan. Tanpa pemilihan | sama |
| Penguncian | `ringkas.py --tahap 2` menulis `keputusan_terkunci.json` (pilihan + hash). Blok uji baru dibuka lewat `ringkas.py --uji-final` | P1/P2: `KEPUTUSAN_TERKUNCI.md` manual |
| Metrik | MAE (utama), MAE vs Naive (%), RMSE, MAPE, akurasi arah (harga tetap bila selisih < Rp1; baseline = tanda return bar terakhir; dilaporkan juga % tetap/naik/turun) | akurasi arah tanpa baseline |
| Uji | DM dua sisi + koreksi HLN, autokovarians lag h_b−1 **pada grid waktu rapat**, t(n−1). **Holm per tahap** pada p_MAE: satu keluarga = semua baris model vs Naive dalam satu tahap; tag `tahap4_*` digabung jadi satu keluarga; duplikat dibuang hanya di dalam satu tahap | P1/P2: tanpa Holm, DM tanpa grid waktu |
| Model terbaik (RM3) | MAE vs Naive terkecil pada blok uji final; RMSE dan MAPE pendukung; "lebih baik dari Naive" hanya bila lolos Holm (Bab III) | ⏳ dikonfirmasi dosen |
| Jumlah skenario | Tahap 1: 36, Tahap 2: 28, Tahap 3: 12, Tahap 4: ≤16 | P2: 120 (Tahap 3–4 dengan 2 metode) |

---

## 4. Hasil uji coba P1 dan P2

### 4.1 Perbedaan kedua uji coba

| | P1 | P2 |
|---|---|---|
| Periode | 14–20 Okt 2026 (7 hari) | 10 Okt – 10 Nov 2026 16:00 (±31,7 hari) |
| Bar candle_1m / ticker_5m | ±10.080 / ±2.016 | ±45.600 / ±9.120 |
| Data uji 80:20 | 19 Okt 14:23 – 20 Okt 23:58 (±1,4 hari) | 4 Nov 07:15 – 10 Nov 15:59 (±6,3 hari) |
| Tren harga di data uji 80:20 | **+0,6%** (datar) | **−6,3%** (turun) |
| Bar hilang | 0 | 0 |
| Run | 92, aturan terkunci penuh | 120; Tahap 3–4 pakai `cmaes` (resmi) **dan** `tpe` (eksploratif) |
| Kode | hash Lampiran B v3.0 | sama, kecuali path data dan tabel `sebaran_prediksi` di `ringkas.py` |
| Perangkat | Apple M5, 10 core, 16 GB, Python 3.14.8 | sama |

P2 bukan sampel independen: minggu P1 berada di dalam data latih P2. Yang benar-benar baru adalah periode uji P2 (4–10 Nov).

### 4.2 Tahap 1 — time frame (TPE, 80:20)

| dataset | h | P1 XGB | P1 LGBM | P1 Cat | P1 Ada | P2 XGB | P2 LGBM | P2 Cat | P2 Ada |
|---|---|---|---|---|---|---|---|---|---|
| candle_1m | 1 | −0,291 | −0,321 | −0,347 | −0,066 | +0,837 ✗ | +0,095 ✗ | +0,632 ✗ | +0,621 ✗ |
| candle_1m | 5 | +0,069 | +0,093 ✗ | +0,060 | +1,089 ✗ | +0,181 | +0,122 | +0,311 ✗ | +0,640 |
| candle_1m | 15 | +0,133 | +0,084 | +0,183 | +0,350 | +0,067 | +0,078 | +0,028 | +0,030 |
| candle_1m | 30 | +0,010 | +0,059 | +0,469 | +0,439 | +0,042 | +0,042 | +0,040 | +0,012 |
| candle_1m | 60 | +0,207 | −0,159 | +0,411 | +0,104 | −0,231 | −0,137 | −0,181 | −0,166 |
| ticker_5m | 5 | +0,160 ✗ | +0,366 ✗ | +1,043 ✗ | +0,541 ✗ | +0,241 ✗ | +0,240 ✗ | +0,238 ✗ | +0,551 ✗ |
| ticker_5m | 15 | +0,269 | +0,132 | +0,792 | +2,554 | +0,133 | +0,099 | +0,090 | +0,272 |
| ticker_5m | 30 | +0,034 | +0,049 | +0,069 | +0,447 | +0,031 | +0,053 | −0,003 | +2,578 |
| ticker_5m | 60 | +0,077 | +0,016 | +0,017 | +0,333 | −0,284 | −0,221 | −0,330 | +1,186 |

**Pilihan menurut aturan P1/P2:** P1 → candle_1m h1 (tidak ada yang signifikan, skor terkecil). P2 → ticker_5m h60.

### 4.3 Tahap 2–4

#### Hasil P1 per tahap (MAE vs Naive %, ✓ signifikan lebih baik, ✗ signifikan lebih buruk; p_MAE < 0,05 tanpa koreksi)

**Tahap 2 — metode optimasi** (candle_1m, h1, 80:20)

| optimasi | XGBoost | LightGBM | CatBoost | AdaBoost | Rata-rata |
|---|---|---|---|---|---|
| default | +4,291 ✗ | +6,586 ✗ | +10,815 ✗ | +14,205 ✗ | +8,974 |
| grid | +0,059 | -0,041 | -0,301 | +0,420 ✗ | +0,035 |
| random | +0,069 | -0,489 | -0,226 | -0,066 | -0,178 |
| tpe | -0,291 | -0,321 | -0,347 | -0,066 | -0,256 |
| cmaes | +0,255 | +0,048 | -0,341 | +0,736 ✗ | +0,175 |
| ga | -0,140 | +0,020 | -0,226 | -0,066 | -0,103 |
| qmc | -0,358 | -0,354 | -0,230 | +0,452 ✗ | -0,122 |

**Tahap 3 — split**

| optimasi | split | XGBoost | LightGBM | CatBoost | AdaBoost | Rata-rata |
|---|---|---|---|---|---|---|
| tpe | 60:40 | -0,175 | +0,128 | -0,153 | +0,165 ✗ | -0,009 |
| tpe | 70:30 | +0,205 | +0,186 | +0,207 | +0,241 | +0,210 |
| tpe | 80:20 | -0,291 | -0,321 | -0,347 | -0,066 | -0,256 |

**Tahap 4 — teknik tambahan** (split 80:20)

| optimasi | teknik | XGBoost | LightGBM | CatBoost | AdaBoost | Rata-rata |
|---|---|---|---|---|---|---|
| tpe | earlystop | -0,103 | +0,061 ✗ | +0,045 | -0,066 | -0,016 |
| tpe | lossl1 | +0,232 ✗ | -0,723 ✓ | -0,462 | -0,066 | -0,255 |
| tpe | prunermedian | -0,375 | -0,121 | -0,347 | -0,066 | -0,227 |
| tpe | topk15 | +0,315 | -0,212 | +0,392 | +0,230 ✗ | +0,181 |

#### Hasil P2 per tahap (MAE vs Naive %, ✓ signifikan lebih baik, ✗ signifikan lebih buruk; p_MAE < 0,05 tanpa koreksi)

**Tahap 2 — metode optimasi** (ticker_5m, h60, 80:20)

| optimasi | XGBoost | LightGBM | CatBoost | AdaBoost | Rata-rata |
|---|---|---|---|---|---|
| default | +16,915 ✗ | +10,804 ✗ | +10,235 ✗ | +8,310 ✗ | +11,566 |
| grid | -0,117 | -0,251 | -0,199 | +2,994 | +0,607 |
| random | -0,150 | -0,278 | -0,290 | +5,079 ✗ | +1,090 |
| tpe | -0,284 | -0,221 | -0,330 | +1,186 | +0,088 |
| cmaes | -0,251 | -0,140 | -0,284 | -0,749 | -0,356 |
| ga | -0,289 | -0,140 | -0,260 | +1,754 | +0,266 |
| qmc | -0,235 | -0,325 | -0,259 | +1,215 | +0,099 |

**Tahap 3 — split**

| optimasi | split | XGBoost | LightGBM | CatBoost | AdaBoost | Rata-rata |
|---|---|---|---|---|---|---|
| cmaes | 60:40 | -0,006 | -0,006 | +0,011 | +5,863 ✗ | +1,466 |
| cmaes | 70:30 | -0,068 | -0,161 | -0,167 | +2,072 | +0,419 |
| cmaes | 80:20 | -0,251 | -0,140 | -0,284 | -0,749 | -0,356 |
| tpe | 60:40 | -0,006 | -0,008 | -0,001 | +2,476 | +0,615 |
| tpe | 70:30 | +0,008 | -0,070 | -0,201 | -0,628 | -0,223 |
| tpe | 80:20 | -0,284 | -0,221 | -0,330 | +1,186 | +0,088 |

**Tahap 4 — teknik tambahan** (split 80:20)

| optimasi | teknik | XGBoost | LightGBM | CatBoost | AdaBoost | Rata-rata |
|---|---|---|---|---|---|---|
| cmaes | earlystop | -0,528 | -0,490 | +0,105 | -0,749 | -0,416 |
| cmaes | lossl1 | -0,117 | -0,111 ✓ | -0,087 | -0,749 | -0,266 |
| cmaes | prunermedian | -0,140 | -0,140 | -0,291 | +1,157 | +0,146 |
| cmaes | topk15 | -0,151 | -0,302 | -0,333 | -0,418 | -0,301 |
| tpe | earlystop | -0,461 | -0,268 | -0,249 | +1,186 | +0,052 |
| tpe | lossl1 | -0,117 | -0,132 | -0,105 | +1,186 | +0,208 |
| tpe | prunermedian | -0,284 | -0,221 | -0,330 | +1,186 | +0,088 |
| tpe | topk15 | -0,210 | -0,282 | -0,271 | +2,203 | +0,360 |

#### Ringkasan signifikansi, dengan koreksi Holm per tahap (dihitung ulang 13 Nov 2026)

Holm di P1/P2 merupakan **analisis tambahan** setelah aturan uji coba dikunci (27 Okt). Holm hanya bisa menghapus status signifikan, sehingga pilihan Tahap 1–2 P1/P2 tidak berubah.

| Percobaan | Tahap | Run | Lebih baik (p<0,05) | Lebih buruk (p<0,05) | Lebih baik (Holm) | Lebih buruk (Holm) |
|---|---|---|---|---|---|---|
| P1 | tahap1 | 36 | 0 | 6 | 0 | 2 |
| P1 | tahap2 | 28 | 0 | 7 | 0 | 6 |
| P1 | tahap3 | 12 | 0 | 1 | 0 | 1 |
| P1 | tahap4 | 16 | 1 | 3 | 0 | 3 |
| P2 | tahap1 | 36 | 0 | 9 | 0 | 7 |
| P2 | tahap2 | 28 | 0 | 5 | 0 | 3 |
| P2 | tahap3 | 24 | 0 | 1 | 0 | 0 |
| P2 | tahap4 | 32 | 1 | 0 | 0 | 0 |
| **P1** | **total** | **92** | **1** | **17** | **0** | **12** |
| **P2** | **total** | **120** | **1** | **15** | **0** | **10** |

Run yang lolos Holm sebagai **lebih buruk**:

| Percobaan | Tahap | Run |
|---|---|---|
| P1 | tahap1 (2) | LightGBM candle_1m h5; LightGBM ticker_5m h5 |
| P1 | tahap2 (6) | default (XGB, LGBM, Cat, Ada); AdaBoost + CMA-ES; AdaBoost + QMC |
| P1 | tahap3 (1) | AdaBoost TPE 60:40 |
| P1 | tahap4 (3) | LightGBM + early stop; XGBoost + loss L1; AdaBoost + top-15 |
| P2 | tahap1 (7) | ticker_5m h5 (XGB, LGBM, Cat, Ada); candle_1m h1 (XGB, LGBM, Cat) |
| P2 | tahap2 (3) | default (XGB, Cat, Ada) |

### 4.4 Apakah model punya informasi? (rata-rata 4 model, Tahap 1)

| dataset | h | corr P1 | corr P2 | akurasi arah P1 (baseline) | akurasi arah P2 (baseline) |
|---|---|---|---|---|---|
| candle_1m | 1 | **0,251** | **0,066** (XGB 0,155; Cat 0,110) | **56,3%** (49,5%) | 53,2% (51,8%); XGB **55,8%**, Cat **56,1%** |
| candle_1m | 5–30 | 0,03–0,04 | −0,01 s.d. 0,01 | ≈ baseline | ≈ baseline |
| candle_1m | 60 | −0,042 | −0,004 | 47,8% (49,6%) | 55,3% (55,2%) |
| ticker_5m | 5 | 0,177 | −0,021 | 51,4% (48,5%) | 49,6% (49,5%) |
| ticker_5m | 60 | −0,094 | −0,013 | 49,1% (47,9%) | 56,4% (55,1%) |

Baseline di tabel ini = proporsi arah mayoritas di data uji (bukan baseline v4). Uji binomial satu sisi: candle_1m h1 P1 semua model p < 0,001; P2 XGBoost p ≈ 8e−13, CatBoost p ≈ 1e−14. Di h60, P2 CatBoost p = 0,011, tetapi target 60 menit saling tumpang tindih sehingga p terlalu optimistis.

### 4.5 Konfigurasi terbaik

| | P1 | P2 |
|---|---|---|
| Konfigurasi | candle_1m h1, LightGBM, TPE, L1 | ticker_5m h60, LightGBM, CMA-ES, L1 |
| MAE vs Naive | −0,723% (p = 0,033; Holm tidak lolos) | −0,111% (p = 0,036; Holm tidak lolos) |
| RMSE vs Naive | −1,628% (p < 0,001) | −0,002% (p = 0,96) |
| corr prediksi–aktual | 0,233 | 0,003 |
| Rasio sebaran prediksi | 0,085 | 0,006 (datar) |

Angka MAE terkecil P2 sebenarnya AdaBoost + CMA-ES ticker_5m h60 (−0,749%), tetapi tidak signifikan (p = 0,38), RMSE-nya lebih buruk (+0,54%), corr ≈ 0, dan konfigurasi yang sama di split lain melonjak sampai +5,86%. Jadi run terbaik secara substansi tetap **run P1**.

Keunggulan run P1 ±Rp2.500 per prediksi (0,723% × MAE Naive candle_1m h1 Rp349.278). Angka ini jauh di bawah spread bid-ask minggu P1: median 0,024% dan rata-rata 0,043% dari harga. Dengan harga rata-rata ±Rp1,46 miliar (diturunkan dari MAE Naive ≈ 0,024% harga), spread itu setara ±Rp350 ribu (median) dan ±Rp600 ribu (rata-rata). ⚠ Hitung ulang spread langsung dari data ticker sebelum angka rupiah dipakai di skripsi.

---

## 5. Temuan uji coba

1. **Naive sulit dikalahkan.** 0 run lolos Holm di kedua percobaan. Yang lolos Holm justru run yang lebih buruk (12 di P1, 10 di P2), terutama `default` dan AdaBoost.
2. **Sinyal hanya di 1 menit, di kedua periode** (Bagian 4.4). Hati-hati: return 1 menit harga *typical* cenderung berbalik arah (efek loncatan bid-ask pada high/low), jadi sebagian sinyal bisa berupa pola mekanis dari definisi harga, bukan peluang trading.
3. **MAE dan RMSE berlawanan di h1** karena 14–17% menit uji harganya tidak berubah. Naive tepat sempurna di menit-menit itu, sehingga MAE menghukum model, sedangkan RMSE hampir tidak. P1: 57 run ✓ di RMSE; P2: 2 run.
4. **Keunggulan h60 di P2 berasal dari tren turun.** corr ≈ 0 dan akurasi arah ≈ "selalu tebak turun". Pasangan yang sama kalah di P1. Memeringkat selisih yang tidak signifikan ternyata tidak stabil antarperiode — alasan kuat untuk aturan v4 (pemilihan dari validasi, keputusan signifikansi lewat Holm).
5. **Optimasi berpengaruh besar, tetapi sebagian karena "meredam" model.**

   | | P1 default | P1 tuning | P2 default | P2 tuning |
   |---|---|---|---|---|
   | MAE vs Naive (rata-rata metode) | +8,97% | −0,26 s.d. +0,18% | +11,57% | −0,36 s.d. +1,09% |
   | Rasio sebaran (median) | 0,330 | 0,078 | 0,352 | 0,018 |
   | corr (median) | 0,213 | 0,250 | −0,051 | −0,032 |
   | Run datar | 0% | 8% | 0% | 25% |

   Di P1 (h1) tuning mengecilkan amplitudo sambil mempertahankan korelasi. Di P2 (h60) tuning mengecilkan amplitudo sampai mendekati nol tanpa korelasi.
6. **TPE terbaik untuk 3 model utama di kedua periode** (rata-rata XGB/LGBM/Cat: P1 −0,320, P2 −0,279). Pemenang 4 model di P2 (CMA-ES) hanya karena satu angka AdaBoost.
7. **Model:** XGBoost, LightGBM, CatBoost tidak terbedakan secara berarti; AdaBoost terburuk dan tidak stabil (P2 Tahap 3: −0,749 → +5,863 hanya karena split/metode berubah).
8. **Split:** P1 tidak beraturan; P2 80:20 > 70:30 > 60:40, tetapi tren periode ujinya berbeda (60:40 −10,2%, 70:30 −5,8%, 80:20 −6,3%). Ini alasan v4 menetapkan blok uji tetap dan mengganti Tahap 3 dengan panjang data latih.
9. **Satu-satunya run ✓ di kedua percobaan = LightGBM + loss L1.** Hanya run P1 yang punya informasi; run P2 menang karena loss L1 = metrik MAE sehingga model menebak median ≈ 0.
10. **Teknik tambahan (P1):** pruner median hemat ±36% waktu dengan akurasi hampir sama; top-15 fitur (di luar fold) paling buruk. Di v4, top-15 dihitung di dalam fold, jadi hasil P1 tidak berlaku lagi.
11. **Blok uji final v4 tetap satu periode.** Perbedaan P1 dan P2 menunjukkan bahwa satu periode uji rentan terhadap kondisi pasar saat itu (sejalan dengan kartu G5). Desain v4 mengurangi risiko ini lewat pemilihan di validasi *walk-forward*, tetapi evaluasi akhir tetap satu blok. Tulis sebagai keterbatasan.

---

## 6. Kalimat yang aman ditulis (untuk Bab IV–V, setelah eksperimen final)

> Uji coba awal pada dua periode data (satu minggu dan sekitar satu bulan) menunjukkan bahwa keempat model boosting tidak mampu mengungguli Naive secara signifikan setelah koreksi uji berganda. Optimasi *hyperparameter* secara konsisten menurunkan error dibanding setelan bawaan, dan TPE memberikan rata-rata terbaik untuk XGBoost, LightGBM, dan CatBoost. *Time frame* terbaik tidak stabil antarperiode, dan keunggulan tipis pada horizon 60 menit di periode kedua berasal dari tren turun di periode uji. Temuan ini menjadi dasar desain eksperimen final yang memilih konfigurasi hanya dari skor validasi dan memakai koreksi Holm.

**Jangan ditulis:** "LightGBM terbukti lebih akurat dari Naive", "horizon 60 menit adalah time frame terbaik", "CMA-ES metode optimasi terbaik", "akurasi arah 57% menunjukkan model dapat dipakai trading", atau angka P1/P2 sebagai hasil skripsi.

**Di Bab I–III:** tidak ada angka dari dokumen ini. Boleh menyebut bahwa uji coba awal dipakai untuk menyempurnakan desain (tanpa angka).

---

## 7. Catatan untuk eksperimen final (Februari 2027)

1. **Pull kode terbaru** (`main` = `ed8b735`) dan `pip install -r requirements.txt` (tambahan `statsmodels`).
2. **Ekspor CSV candle 1 menit terbaru** dari VPS (`indodax ekspor`) dan arahkan `CANDLE_1M` di `config.py` ke file itu. Ticker tidak perlu.
3. **Atur periode** `START_UTC`/`END_UTC` di `config.py` (saat ini masih 14–20 Okt 2026) atau beri `--start`/`--end` di setiap perintah. Periode harus sama di semua tahap.
4. **Pakai folder `hasil/` baru.** Jangan campur dengan hasil P1/P2 (format kolomnya berbeda).
5. **Perkiraan waktu** (data ±4,5× P2): LightGBM ±1–2 menit/run; AdaBoost candle_1m ±50 menit/run; total Tahap 1–4 **±7–8 jam** di Apple M5. Satu run LightGBM data 1 menit penuh P2 (45.601 bar, TPE 30 trial) = 25 detik di mesin 2 core.
6. **Cek `hasil/deskripsi_data.csv`** setelah Tahap 1 (celah, `n_parsial`, `t_u`) untuk Tabel data di Bab III.
7. **Jangan mengubah aturan setelah melihat hasil.** `--uji-final` menolak jalan bila baris validasi Tahap 1–2 berubah setelah dikunci.
8. **Aturan duplikat Holm (perlu diputuskan sebelum Februari).** Bab III menulis "konfigurasi yang sama persis dan muncul di lebih dari satu tahap dihitung satu kali", sedangkan kode v4 membentuk keluarga per tahap dan membuang duplikat **hanya di dalam** satu tahap (kunci = run_id tanpa tag). Di dalam satu tahap duplikat praktis tidak terjadi, jadi konfigurasi yang muncul lagi di tahap lain tetap diuji di keluarga tahap itu.
   - **Rekomendasi:** ubah Bab III supaya mengikuti kode: *"Satu keluarga uji berisi seluruh perbandingan model terhadap Naive dalam satu tahap. Keempat teknik pada Tahap 4 digabung menjadi satu keluarga."* Aturan lintas tahap ambigu karena tidak jelas konfigurasi masuk keluarga tahap mana.
   - ⚠ Keputusan Ferdi. Bila Bab III dipertahankan, kode `holm()` di `ringkas.py` perlu diubah.
9. **Belum diputuskan (sengaja belum dikerjakan):** QMC 30 atau 32 trial; `has_time=True` CatBoost; beberapa seed untuk Tahap 2.

---

## 8. Kaitan dengan rumusan masalah (versi 6 Nov 2026, sesuai Bab I)

| RM | Rumusan | Bagian eksperimen | Gambaran dari uji coba (bukan hasil skripsi) |
|---|---|---|---|
| RM1 | Bagaimana membangun model XGBoost, LightGBM, CatBoost, dan AdaBoost untuk memprediksi harga BTC/IDR pada berbagai *time frame*? | Tahap 1 + pipeline (fitur, target, pembagian data, tuning) | Pipeline berjalan pada 212 run tanpa gagal. Hanya h1 yang memuat sinyal; horizon lebih panjang cenderung datar |
| RM2 | Bagaimana pengaruh optimasi *hyperparameter* terhadap akurasi keempat model tersebut? | Tahap 2 dan 4 | Default +9 s.d. +12%; tuning sekitar Naive; antar metode kecil; TPE terbaik untuk 3 model utama |
| RM3 | Model mana yang memiliki performa terbaik berdasarkan nilai MAE, RMSE, dan MAPE dibandingkan dengan Naive? | Evaluasi blok uji final + Holm | Tidak ada model yang lolos Holm; XGB/LGBM/Cat setara; AdaBoost terlemah |

Tahap 3 tidak dipetakan ke RM tertentu; dipakai untuk melihat ketahanan hasil terhadap panjang data latih.

---

## 9. Lingkungan dan cara menjalankan (v4)

- Repo: `https://github.com/ferdiendahas/prediksi_btc` (public), branch `main`, commit `ed8b735`. Folder Mac: `/Users/ea/Documents/Prediksi BTC SKRIPSI/prediksi_btc`.
- Python 3.14.8 (venv). Paket: pandas 3.1, numpy 2.5, scipy 1.18.1, scikit-learn 1.9, xgboost 3.4, lightgbm 4.7, catboost 1.2.10, optuna 5.0, cmaes 0.13, statsmodels (baru). `hasil/lingkungan.txt` dibuat otomatis.
- Perangkat: Apple M5, 10 core, 16 GB, macOS 26.2.

```bash
source .venv/bin/activate
python run.py --optimizers tpe --tag tahap1                       # 9 pasangan x 4 model
python ringkas.py --tahap 1                                       # -> DS, H (dari validasi)
python run.py --datasets <DS> --horizons <H> \
  --optimizers default grid random tpe cmaes ga qmc --tag tahap2
python ringkas.py --tahap 2                                       # -> OPT, tulis keputusan_terkunci.json
python run.py --datasets <DS> --horizons <H> --optimizers <OPT> --train-fracs 1.0 0.75 0.5 --tag tahap3
for t in "--early-stop" "--top-k 15" "--loss l1" "--pruner median"; do
  python run.py --datasets <DS> --horizons <H> --optimizers <OPT> $t --tag "tahap4_$(echo $t | tr -d ' -')"
done
python ringkas.py --uji-final                                     # baru membuka hasil_uji_final.csv
```

Uji cepat (beberapa detik):
```bash
python run.py --datasets candle_1m candle_5m --horizons 5 --models LightGBM \
  --optimizers tpe --trials 3 --start "2026-10-14 00:00" --end "2026-10-16 23:59" --tag uji_cepat
```

Keluaran v4: `hasil/hasil_validasi.csv`, `hasil/hasil_uji_final.csv`, `hasil/deskripsi_data.csv`, `hasil/keputusan_terkunci.json`, `hasil/lingkungan.txt`, `hasil/ringkasan/*.csv`, `hasil/params/`, `hasil/prediksi/`.

---

## Lampiran A — Perubahan kode v4 (ringkas dari `CHANGELOG.md`)

| Bagian | Perubahan |
|---|---|
| K1 | `agregasi_5m()`; dataset `candle_5m` dari candle 1 menit; `ticker_5m` keluar dari default |
| K2 | `hasil/deskripsi_data.csv`: tanggal, baris mentah, bar, celah, celah terpanjang, `n_parsial`, `n_pengembangan`, `n_uji_final`, `t_u` |
| K3 | `FINAL_TEST_FRAC = 0.2`, `TRAIN_FRACS = [1.0, 0.75, 0.5]`; purging berbasis waktu + `assert`; `--splits` → `--train-fracs`; kolom `frac_latih`, `t_u` |
| K4 | Purging per fold berbasis waktu (`_folds()`) |
| K5 | Objektif = MAE rupiah; `cv_mae_rp`, `cv_naive_rp`, `cv_vs_naive_pct` |
| K6 | Top-k di dalam fold (cache per fold); top-k final sekali di seluruh data pengembangan; `fitur_final` dicatat |
| K7 | `hasil_validasi.csv` vs `hasil_uji_final.csv`; `ringkas.py --tahap 1/2`, `keputusan_terkunci.json` (hash file + hash baris Tahap 1–2), `--uji-final` |
| K8 | DM pada grid waktu rapat; Holm per tahap (`statsmodels`); `p_MAE_holm`, `status_uji`, `beda_arah_rmse` |
| K9 | `hasil/lingkungan.txt` otomatis |
| K10 | Akurasi arah dengan ambang Rp1, `n_arah`, `pct_tetap/naik/turun`, `arah_baseline_pct`; AdaBoost + early stop/L1 = `tidak_berlaku`; rekap skenario dan konfigurasi unik |

Ruang pencarian, seed, jumlah trial, fold, model, dan fitur tidak berubah.

---

## Lampiran B — Source code final v4 (`prediksi_btc`, commit `ed8b735`)

SHA-256 (dicocokkan dengan repo 13 Nov 2026):
```text
88b93f6ef373bdda42605ddbacda392a4b23eb8c3870d7fc60fe246daeb70d71  config.py
b1e9f17a22ffb0e964a37cd1ca70809c463beac82a6ffa5bac8c578fe7f68856  run.py
bf329e6f5df41cc4bb45fa280301fd67e48e86aa9410bf3eef122bab3b06cfbb  ringkas.py
d3eb736e266e52cdf4b593595e850ae2cab7ad1a60aa3a6b9e7256be3a774b3a  requirements.txt
ea3a707f8e972e8497b620fbd7107133edfdb2b461cd25458abda3a548e61554  btcpred/data.py
d9602204d678acebe7cff0e2e6468e5a85bd10a60e6f997708b2ba80b937a192  btcpred/models.py
2ef5a0d9e0283d11a1728752c297b03938afc12daf37d10bda34481047464e31  btcpred/optim.py
70d51a0f1b2e3afdd0fadd8cbe84c6bcc565f73a6b57b72c8a50666785a92e04  btcpred/evaluate.py
```

Struktur:
```
prediksi_btc/
├── config.py            pengaturan percobaan
├── run.py               menjalankan semua kombinasi; tulis hasil_validasi.csv dan hasil_uji_final.csv
├── ringkas.py           aturan pemilihan Tahap 1-2, penguncian, uji final + Holm
├── requirements.txt
├── CHANGELOG.md, README.md, DAFTAR_PERCOBAAN.md
└── btcpred/
    ├── data.py          baca CSV, agregasi 5 menit, definisi harga, fitur, target, deskripsi data
    ├── models.py        4 model, ruang hyperparameter, grid
    ├── optim.py         fold berbasis waktu, objektif MAE rupiah, metode optimasi, pruner, early stopping, top-k per fold
    └── evaluate.py      metrik, uji Diebold-Mariano (grid waktu), seleksi fitur
```


### `config.py`

```python
"""
KONFIGURASI PERCOBAAN
=====================
Ubah daftar di bawah untuk menentukan variasi percobaan. run.py akan menjalankan
SEMUA kombinasi (dataset x horizon x frac_latih x model x optimasi).
Semua daftar juga bisa ditimpa lewat argumen command line, contoh:
    python run.py --datasets candle_1m --horizons 5 15 --optimizers tpe random
Lihat DAFTAR_PERCOBAAN.md untuk penjelasan tiap pilihan.
"""

# ---------------------------------------------------------------------------
# 1. DATA
# ---------------------------------------------------------------------------
CANDLE_1M = "data/btcidr_candle_1menit_20261110_1642.csv"
DATA = {
    # nama_dataset: path, jenis (candle/ticker), resolusi dalam menit,
    # sumber_tf = resolusi file sumber bila bar dibentuk lewat agregasi
    "candle_1m": {"path": CANDLE_1M, "jenis": "candle", "tf_menit": 1},
    # candle 5 menit = agregasi candle 1 menit (Indodax tidak menyediakan tf=5).
    # Waktu bar = AWAL bar (UTC). Bar dengan < 5 menit data dicatat sebagai n_parsial.
    "candle_5m": {"path": CANDLE_1M, "jenis": "candle", "tf_menit": 5, "sumber_tf": 1},
    # ticker_5m tidak lagi dipakai (review dosen 11-11-2026); definisi disimpan
    # supaya hasil lama tetap bisa direproduksi bila file CSV-nya tersedia.
    "ticker_5m": {"path": "data/btcidr_ticker_5menit_20261110_1642.csv", "jenis": "ticker", "tf_menit": 5},
}

# Rentang data yang dipakai (UTC). Seminggu penuh = 7 x 24 jam.
START_UTC = "2026-10-14 00:00"
END_UTC   = "2026-10-20 23:59"

# Definisi "harga" per jenis data
#   candle: "typical" = (high+low+close)/3  | "close" | "ohlc4" = (open+high+low+close)/4
#   ticker: "mid" = (bid+ask)/2            | "last" = last_price
HARGA = {"candle": "typical", "ticker": "mid"}

# ---------------------------------------------------------------------------
# 2. VARIASI PERCOBAAN
# ---------------------------------------------------------------------------
DATASETS   = ["candle_1m", "candle_5m"]

# Horizon prediksi dalam MENIT (berapa menit ke depan harga diprediksi).
# Horizon yang bukan kelipatan resolusi data otomatis dilewati
# (mis. horizon 1 menit tidak bisa untuk candle_5m).
HORIZONS   = [1, 5, 15, 30, 60]

# Pembagian data berbasis waktu (review dosen 11-11-2026):
#   blok uji final = FINAL_TEST_FRAC bar terakhir (sama untuk semua run per dataset x horizon).
#   Tahap 3 memvariasikan PANJANG data latih: porsi akhir data pengembangan yang dipakai.
#   run.py memakai --train-fracs (default 1.0); daftar di bawah dipakai untuk Tahap 3.
FINAL_TEST_FRAC = 0.2
TRAIN_FRACS     = [1.0, 0.75, 0.5]

MODELS     = ["XGBoost", "LightGBM", "CatBoost", "AdaBoost"]

# Metode optimasi hyperparameter:
#   default : tanpa tuning (setelan bawaan library)
#   grid    : Grid Search (kombinasi tetap, lihat GRID di btcpred/models.py)
#   random  : Random Search
#   tpe     : Bayesian Optimization (Tree-structured Parzen Estimator)
#   cmaes   : CMA-ES (Evolution Strategy)
#   ga      : Genetic Algorithm (NSGA-II)
#   qmc     : Quasi-Monte Carlo (Sobol)
OPTIMIZERS = ["default", "grid", "random", "tpe", "cmaes", "ga"]

# ---------------------------------------------------------------------------
# 3. PENGATURAN OPTIMASI TAMBAHAN (berlaku untuk semua run)
# ---------------------------------------------------------------------------
N_TRIALS   = 30        # jatah percobaan tuning per model (sama untuk semua metode, kecuali grid)
N_FOLDS    = 5         # fold walk-forward (TimeSeriesSplit) saat tuning
PRUNER     = None      # None | "median" | "hyperband"  -> hentikan trial jelek lebih awal
EARLY_STOP = False     # True = early stopping (XGBoost, LightGBM, CatBoost)
TOP_K      = None      # None = semua fitur | angka = seleksi K fitur terpenting
LOSS       = "l2"      # "l2" = squared error | "l1" = absolute error (MAE)

# ---------------------------------------------------------------------------
# 4. FITUR
# ---------------------------------------------------------------------------
N_LAG       = 12                      # jumlah lag return (dalam bar)
WINDOWS_MNT = [5, 15, 30, 60, 240]    # jendela statistik bergulir (menit)

# ---------------------------------------------------------------------------
# 5. LAIN-LAIN
# ---------------------------------------------------------------------------
SEED           = 42
OUT_DIR        = "hasil"
SIMPAN_PREDIKSI = True                # simpan prediksi data uji per run
```

### `run.py`

```python
"""
Menjalankan semua kombinasi percobaan dari config.py (bisa ditimpa lewat argumen).

Contoh:
    python run.py --optimizers tpe --tag tahap1
    python run.py --datasets candle_1m --horizons 5 --optimizers default grid random tpe cmaes ga qmc --tag tahap2
    python run.py --datasets candle_1m --horizons 5 --optimizers tpe --train-fracs 1.0 0.75 0.5 --tag tahap3
    python run.py --datasets candle_1m --horizons 5 --optimizers tpe --top-k 15 --tag tahap4_topk15

Pembagian data (berbasis waktu, revisi dosen 11-11-2026):
  - Blok uji final = 20% bar terakhir, mulai waktu t_u. Sama untuk semua run
    dengan (dataset, horizon) yang sama.
  - Data pengembangan = semua baris yang waktu targetnya (t + horizon) < t_u.
  - --train-fracs 0.75 / 0.5 memakai hanya bagian akhir data pengembangan
    (Tahap 3: panjang data latih). Blok uji tidak berubah.

Keluaran:
  hasil/hasil_validasi.csv   : identitas run + skor validasi (dipakai untuk memilih)
  hasil/hasil_uji_final.csv  : identitas run + metrik blok uji (dibuka setelah dikunci)
  hasil/deskripsi_data.csv   : satu baris per (dataset, horizon, periode)
  hasil/lingkungan.txt       : versi Python, paket, CPU, RAM, OS
  hasil/params/, hasil/prediksi/

Run yang sudah selesai (run_id sama, termasuk --tag) otomatis dilewati, jadi
script aman dihentikan lalu dijalankan lagi.
"""
import argparse
import itertools
import json
import os
import platform
import subprocess
import sys
import time
import warnings
warnings.filterwarnings("ignore")
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

import config as C
from btcpred import data as D, models as M, optim as O, evaluate as E


def parse():
    a = argparse.ArgumentParser()
    a.add_argument("--datasets", nargs="+")
    a.add_argument("--horizons", nargs="+", type=int)
    a.add_argument("--train-fracs", nargs="+", type=float, default=[1.0],
                   help="porsi akhir data pengembangan yang dipakai melatih (Tahap 3)")
    a.add_argument("--models", nargs="+")
    a.add_argument("--optimizers", nargs="+")
    a.add_argument("--trials", type=int)
    a.add_argument("--folds", type=int)
    a.add_argument("--pruner", choices=["median", "hyperband", "none"])
    a.add_argument("--early-stop", action="store_true")
    a.add_argument("--top-k", type=int)
    a.add_argument("--loss", choices=["l1", "l2"])
    a.add_argument("--harga-candle", choices=["typical", "close", "ohlc4"])
    a.add_argument("--harga-ticker", choices=["mid", "last"])
    a.add_argument("--start")
    a.add_argument("--end")
    a.add_argument("--tag", default="", help="label bebas untuk menandai run")
    return a.parse_args()


# ---------------------------------------------------------------------------
# kolom keluaran
# ---------------------------------------------------------------------------
ID = ["run_id", "status", "dataset", "harga", "tf_data_menit", "horizon_menit", "horizon_bar",
      "frac_latih", "model", "optimasi", "loss", "early_stop", "top_k", "pruner",
      "n_trials_cfg", "n_folds", "periode", "t_u", "n_latih", "latih_mulai", "latih_akhir", "tag"]
KOLOM_VALIDASI = ID + ["cv_mae_rp", "cv_naive_rp", "cv_vs_naive_pct", "n_trials", "n_pruned",
                       "n_fitur", "fitur_final", "detik_tuning", "detik_total"]
KOLOM_UJI = ID + ["n_uji", "uji_mulai", "uji_akhir", "MAE_Rp", "RMSE_Rp", "MAPE_pct",
                  "Akurasi_arah_pct", "n_arah", "pct_tetap", "pct_naik", "pct_turun",
                  "arah_baseline_pct", "MAE_vs_naive_pct", "RMSE_vs_naive_pct",
                  "DM_MAE", "p_MAE", "DM_RMSE", "p_RMSE", "std_pred_return"]
KOLOM_DESKRIPSI = ["dataset", "horizon_menit", "periode", "tanggal_awal", "tanggal_akhir",
                   "n_baris_mentah", "n_bar", "n_bar_grid", "n_hilang", "n_celah",
                   "celah_terpanjang_mnt", "n_parsial", "n_setelah_fitur", "n_pengembangan",
                   "n_uji_final", "t_u"]


def _append(path, row, kolom):
    df = pd.DataFrame([{k: row.get(k, np.nan) for k in kolom}])
    df.to_csv(path, mode="a", header=not path.exists(), index=False)


def _upsert_deskripsi(path, row):
    new = pd.DataFrame([{k: row.get(k, np.nan) for k in KOLOM_DESKRIPSI}])
    if path.exists():
        old = pd.read_csv(path)
        key = (old.dataset == row["dataset"]) & (old.horizon_menit == row["horizon_menit"]) \
            & (old.periode == row["periode"])
        new = pd.concat([old[~key], new], ignore_index=True)
    new.to_csv(path, index=False)


def tulis_lingkungan(path):
    """K9: catat lingkungan sekali (kalau file belum ada)."""
    if path.exists():
        return

    def sh(cmd):
        try:
            return subprocess.run(cmd, capture_output=True, text=True, timeout=60).stdout.strip()
        except Exception as e:
            return f"(gagal: {e})"

    cpu, ram = platform.processor(), ""
    if sys.platform == "darwin":
        cpu = sh(["sysctl", "-n", "machdep.cpu.brand_string"]) or cpu
        try:
            ram = f"{int(sh(['sysctl', '-n', 'hw.memsize'])) / 2**30:.1f} GB"
        except ValueError:
            ram = ""
    elif Path("/proc/cpuinfo").exists():
        for line in open("/proc/cpuinfo"):
            if line.startswith("model name"):
                cpu = line.split(":", 1)[1].strip(); break
        for line in open("/proc/meminfo"):
            if line.startswith("MemTotal"):
                ram = f"{int(line.split()[1]) / 2**20:.1f} GB"; break
    teks = [f"tanggal : {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
            f"python  : {sys.version.split()[0]} ({sys.executable})",
            f"OS      : {platform.platform()}",
            f"CPU     : {cpu} | {os.cpu_count()} core logis",
            f"RAM     : {ram}", "", "== pip freeze ==",
            sh([sys.executable, "-m", "pip", "freeze"])]
    path.write_text("\n".join(teks) + "\n")


def main():
    a = parse()
    cfg = dict(
        DATASETS=a.datasets or C.DATASETS, HORIZONS=a.horizons or C.HORIZONS,
        TRAIN_FRACS=a.train_fracs, MODELS=a.models or C.MODELS,
        OPTIMIZERS=a.optimizers or C.OPTIMIZERS, N_TRIALS=a.trials or C.N_TRIALS,
        N_FOLDS=a.folds or C.N_FOLDS,
        PRUNER=(None if a.pruner == "none" else a.pruner) if a.pruner else C.PRUNER,
        EARLY_STOP=a.early_stop or C.EARLY_STOP, TOP_K=a.top_k or C.TOP_K,
        LOSS=a.loss or C.LOSS, SEED=C.SEED,
        HARGA={"candle": a.harga_candle or C.HARGA["candle"],
               "ticker": a.harga_ticker or C.HARGA["ticker"]},
        START=a.start or C.START_UTC, END=a.end or C.END_UTC,
    )
    out = Path(C.OUT_DIR)
    (out / "params").mkdir(parents=True, exist_ok=True)
    (out / "prediksi").mkdir(parents=True, exist_ok=True)
    tulis_lingkungan(out / "lingkungan.txt")
    fval, fuji, fdes = out / "hasil_validasi.csv", out / "hasil_uji_final.csv", out / "deskripsi_data.csv"
    done = set(pd.read_csv(fuji)["run_id"]) if fuji.exists() else set()
    periode = f"{cfg['START']}..{cfg['END']}"

    total = (len(cfg["DATASETS"]) * len(cfg["HORIZONS"]) * len(cfg["TRAIN_FRACS"])
             * len(cfg["MODELS"]) * len(cfg["OPTIMIZERS"]))
    print(f"Maksimum {total} run (kombinasi tidak valid dilewati). Hasil: {fval}, {fuji}")
    t_all, ke = time.time(), 0

    for ds in cfg["DATASETS"]:
        info = C.DATA[ds]
        jenis, tf = info["jenis"], info["tf_menit"]
        harga = cfg["HARGA"][jenis]
        raw, dinfo = D.load(info["path"], jenis, tf, harga, cfg["START"], cfg["END"],
                            sumber_tf=info.get("sumber_tf"))
        print(f"\n=== {ds} | harga={harga} | n_bar={dinfo['n_bar']} | n_parsial={dinfo['n_parsial']}"
              f" | n_hilang={dinfo['n_hilang']} (celah {dinfo['n_celah']}, terpanjang "
              f"{dinfo['celah_terpanjang_mnt']} menit)")

        for hz in cfg["HORIZONS"]:
            if hz % tf != 0:
                print(f"  lewati horizon {hz} menit (bukan kelipatan TF {tf} menit)")
                continue
            data, feats, hb = D.build(raw, jenis, tf, hz, C.N_LAG, C.WINDOWS_MNT, cfg["START"])
            n = len(data)

            # ---- K3: blok uji final + purging berbasis waktu ----
            t_u = data.index[int(np.floor((1 - C.FINAL_TEST_FRAC) * n))]
            t_target = data.index + pd.Timedelta(minutes=hz)
            dev_full = data[t_target < t_u]
            test = data[data.index >= t_u]
            assert (dev_full.index + pd.Timedelta(minutes=hz) < t_u).all(), "purging gagal"

            _upsert_deskripsi(fdes, dict(dataset=ds, horizon_menit=hz, periode=periode,
                                         n_setelah_fitur=n, n_pengembangan=len(dev_full),
                                         n_uji_final=len(test), t_u=str(t_u), **dinfo))

            yte = test["target"]
            h_now, h_true = test["harga_now"].values, test["harga_next"].values
            naive = h_now.copy()
            m_naive = E.metrics(h_true, naive, np.zeros(len(yte)), h_now, test["ret_lag1"].values)
            e_naive = pd.Series(h_true - naive, index=test.index)

            for frac in cfg["TRAIN_FRACS"]:
                dev = dev_full
                if frac < 1.0:
                    t0f = dev.index.max() - (dev.index.max() - dev.index.min()) * frac
                    dev = dev[dev.index >= t0f]
                ydev = dev["target"]

                base = dict(dataset=ds, harga=harga, tf_data_menit=tf, horizon_menit=hz,
                            horizon_bar=hb, frac_latih=frac, loss=cfg["LOSS"],
                            early_stop=cfg["EARLY_STOP"], top_k=cfg["TOP_K"] or 0,
                            pruner=cfg["PRUNER"] or "none", n_trials_cfg=cfg["N_TRIALS"],
                            n_folds=cfg["N_FOLDS"], periode=periode, t_u=str(t_u),
                            n_latih=len(dev), latih_mulai=str(dev.index.min()),
                            latih_akhir=str(dev.index.max()), tag=a.tag)
                uji_id = dict(n_uji=len(test), uji_mulai=str(test.index.min()),
                              uji_akhir=str(test.index.max()))

                # baris Naive (sekali per dataset x horizon x frac x tag), hanya di uji final
                nid = f"{ds}|{harga}|h{hz}|fl{frac}|Naive|{cfg['START']}|{cfg['END']}|{a.tag}"
                if nid not in done:
                    row = dict(run_id=nid, status="ok", model="Naive", optimasi="-", **base,
                               **uji_id, **m_naive, MAE_vs_naive_pct=0.0, RMSE_vs_naive_pct=0.0)
                    row["Akurasi_arah_pct"] = np.nan
                    _append(fuji, row, KOLOM_UJI)
                    done.add(nid)

                for model, opt in itertools.product(cfg["MODELS"], cfg["OPTIMIZERS"]):
                    ke += 1
                    rid = (f"{ds}|{harga}|h{hz}|fl{frac}|{model}|{opt}|{cfg['LOSS']}|"
                           f"es{int(cfg['EARLY_STOP'])}|k{cfg['TOP_K'] or 0}|"
                           f"pr{cfg['PRUNER'] or 'none'}|t{cfg['N_TRIALS']}|f{cfg['N_FOLDS']}|"
                           f"{cfg['START']}|{cfg['END']}|{a.tag}")
                    if rid in done:
                        continue

                    # ---- K10: teknik yang tidak berlaku untuk AdaBoost ----
                    if model == "AdaBoost" and (cfg["EARLY_STOP"] or cfg["LOSS"] == "l1"):
                        row = dict(run_id=rid, status="tidak_berlaku", model=model,
                                   optimasi=opt, **base)
                        _append(fval, row, KOLOM_VALIDASI)
                        _append(fuji, {**row, **uji_id}, KOLOM_UJI)
                        done.add(rid)
                        print(f"  [{ke}] {ds} h{hz} fl{frac} {model:8s} {opt:7s} | tidak_berlaku")
                        continue

                    t0 = time.time()
                    Xdev = dev[feats]
                    tuned = O.tune(model, Xdev, ydev, opt, cfg, horizon_menit=hz,
                                   harga_now=dev["harga_now"], harga_next=dev["harga_next"])

                    # ---- K6: seleksi top-k final pada seluruh data pengembangan ----
                    cols = feats
                    if cfg["TOP_K"]:
                        cols = E.select_top_k(model, Xdev, ydev, cfg["TOP_K"], cfg["LOSS"], cfg["SEED"])
                    mdl = M.make(model, tuned["params"], cfg["LOSS"], cfg["SEED"])
                    mdl.fit(dev[cols], ydev)
                    t_total = time.time() - t0

                    vrow = dict(run_id=rid, status="ok", model=model, optimasi=opt, **base,
                                cv_mae_rp=tuned["cv_mae_rp"], cv_naive_rp=tuned["cv_naive_rp"],
                                cv_vs_naive_pct=tuned["cv_vs_naive_pct"],
                                n_trials=tuned["n_trials"], n_pruned=tuned["n_pruned"],
                                n_fitur=len(cols),
                                fitur_final=";".join(cols) if cfg["TOP_K"] else "",
                                detik_tuning=tuned["detik_tuning"], detik_total=t_total)
                    _append(fval, vrow, KOLOM_VALIDASI)

                    # ---- blok uji final ----
                    r_pred = mdl.predict(test[cols])
                    h_pred = h_now * np.exp(r_pred)
                    met = E.metrics(h_true, h_pred, r_pred, h_now, test["ret_lag1"].values)
                    e_m = pd.Series(h_true - h_pred, index=test.index)
                    dm1, p1 = E.dm_test(e_m.abs() - e_naive.abs(), hb, tf)
                    dm2, p2 = E.dm_test(e_m ** 2 - e_naive ** 2, hb, tf)
                    urow = dict(run_id=rid, status="ok", model=model, optimasi=opt, **base,
                                **uji_id, **met,
                                MAE_vs_naive_pct=(met["MAE_Rp"] / m_naive["MAE_Rp"] - 1) * 100,
                                RMSE_vs_naive_pct=(met["RMSE_Rp"] / m_naive["RMSE_Rp"] - 1) * 100,
                                DM_MAE=dm1, p_MAE=p1, DM_RMSE=dm2, p_RMSE=p2,
                                std_pred_return=float(np.std(r_pred)))
                    _append(fuji, urow, KOLOM_UJI)
                    done.add(rid)

                    safe = rid.replace("|", "__").replace(":", "-").replace(" ", "_")
                    json.dump(dict(params=tuned["params"], fitur_final=cols,
                                   fitur_fold=tuned["fitur_fold"]),
                              open(out / "params" / f"{safe}.json", "w"), indent=2, default=str)
                    if C.SIMPAN_PREDIKSI:
                        pd.DataFrame({"waktu_target": test.index + pd.Timedelta(minutes=hz),
                                      "harga_now": h_now, "harga_aktual": h_true,
                                      "prediksi": h_pred, "naive": naive}).to_csv(
                            out / "prediksi" / f"{safe}.csv", index=False)

                    # log hanya menampilkan skor validasi (blok uji dibuka lewat ringkas.py)
                    print(f"  [{ke}] {ds} h{hz} fl{frac} {model:8s} {opt:7s} | "
                          f"CV MAE Rp{tuned['cv_mae_rp']:,.0f} ({tuned['cv_vs_naive_pct']:+.3f}% vs Naive"
                          f" validasi) | {t_total:.0f}s", flush=True)

    print(f"\nSelesai dalam {(time.time()-t_all)/60:.1f} menit.")


if __name__ == "__main__":
    main()
```

### `ringkas.py`

```python
"""
Meringkas hasil percobaan dan menerapkan aturan pemilihan (review dosen 11-11-2026).

Urutan pemakaian:
    python ringkas.py                      # rekap jumlah skenario (hanya hasil_validasi.csv)
    python ringkas.py --tahap 1            # pilih (dataset, horizon) dari VALIDASI
    python ringkas.py --tahap 2            # pilih strategi optimasi dari VALIDASI,
                                           #   lalu tulis hasil/keputusan_terkunci.json
    python ringkas.py --uji-final          # baru membuka hasil_uji_final.csv (+ Holm)

Aturan:
  Tahap 1 : pasangan (dataset, horizon) dengan cv_vs_naive_pct terkecil di antara
            4 model. Seri -> horizon lebih pendek -> candle_1m. Tanpa syarat signifikansi.
  Tahap 2 : strategi dengan rata-rata cv_vs_naive_pct 4 model terkecil. 'default'
            boleh terpilih. Seri -> total waktu tuning terpendek.
  Uji final: satu keluarga Holm = semua baris model-vs-Naive dalam satu tahap
            (tag tahap4_* digabung jadi satu keluarga 'tahap4'). Konfigurasi duplikat
            (run_id tanpa tag) dihitung sekali.
"""
import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

import config as C

OUT = Path(C.OUT_DIR)
F_VAL, F_UJI = OUT / "hasil_validasi.csv", OUT / "hasil_uji_final.csv"
F_KUNCI = OUT / "keputusan_terkunci.json"
URUT_DATASET = {"candle_1m": 0, "candle_5m": 1}
pd.set_option("display.width", 220)


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def sha256_baris(df):
    """Hash isi baris tertentu (urut run_id), supaya bisa dicek ulang walaupun
    hasil_validasi.csv bertambah baris Tahap 3-4 setelah dikunci."""
    kol = ["run_id", "dataset", "horizon_menit", "model", "optimasi",
           "cv_mae_rp", "cv_naive_rp", "cv_vs_naive_pct", "detik_tuning"]
    d = df[kol].sort_values("run_id").copy()
    d["horizon_menit"] = d["horizon_menit"].astype(int)
    for c in kol[5:]:
        d[c] = d[c].map(lambda x: f"{float(x):.10e}")   # format tetap, tidak bergantung dtype kolom
    return hashlib.sha256(d.to_csv(index=False).encode()).hexdigest()


def baca_validasi():
    v = pd.read_csv(F_VAL)
    return v.drop_duplicates("run_id", keep="last")


def keluarga(tag):
    m = re.match(r"^(tahap\d)", str(tag))
    return m.group(1) if m else str(tag)


def kunci_tanpa_tag(run_id):
    return str(run_id).rsplit("|", 1)[0]


# ---------------------------------------------------------------------------
# rekap (K10)
# ---------------------------------------------------------------------------
def rekap(v):
    v = v[v.model != "Naive"].copy()
    v["tahap"] = v.tag.map(keluarga)
    v["kunci"] = v.run_id.map(kunci_tanpa_tag)
    r = v.groupby("tahap").agg(skenario=("run_id", "size"),
                               konfigurasi_unik=("kunci", "nunique"),
                               ok=("status", lambda s: (s == "ok").sum()),
                               tidak_berlaku=("status", lambda s: (s == "tidak_berlaku").sum()))
    print("\n=== Rekap skenario (dari hasil_validasi.csv) ===")
    print(r.to_string())
    print(f"  total skenario: {len(v)} | konfigurasi unik lintas tahap: {v.kunci.nunique()}")


# ---------------------------------------------------------------------------
# Tahap 1 dan 2 (hanya validasi)
# ---------------------------------------------------------------------------
def pilih_tahap1(v, tag):
    t = v[(v.tag == tag) & (v.status == "ok") & (v.model != "Naive")]
    if t.empty:
        raise SystemExit(f"Tidak ada baris validasi dengan tag '{tag}'.")
    n_model = t.groupby(["dataset", "horizon_menit"]).model.nunique()
    kurang = n_model[n_model < 4]
    if len(kurang):
        print("PERINGATAN: pasangan berikut belum lengkap 4 model:\n", kurang.to_string())
    pv = t.pivot_table(index=["dataset", "horizon_menit"], columns="model",
                       values="cv_vs_naive_pct", aggfunc="mean")
    s = t.groupby(["dataset", "horizon_menit"]).cv_vs_naive_pct.min().rename("skor").reset_index()
    s["urut_ds"] = s.dataset.map(URUT_DATASET).fillna(9)
    s = s.sort_values(["skor", "horizon_menit", "urut_ds"]).drop(columns="urut_ds")
    print(f"\n=== Tahap 1 (validasi, tag={tag}): cv_vs_naive_pct per model ===")
    print(pv.round(3).to_string())
    print("\nSkor pasangan = cv_vs_naive_pct terkecil di antara model:")
    print(s.round(3).to_string(index=False))
    best = s.iloc[0]
    print(f"\n-> Terpilih: dataset={best.dataset}, horizon={int(best.horizon_menit)} menit "
          f"(skor {best.skor:+.3f}%)")
    (OUT / "ringkasan").mkdir(exist_ok=True)
    s.to_csv(OUT / "ringkasan" / "tahap1_validasi.csv", index=False)
    return dict(dataset=best.dataset, horizon_menit=int(best.horizon_menit),
                skor_cv_vs_naive_pct=float(best.skor)), t


def pilih_tahap2(v, tag):
    t = v[(v.tag == tag) & (v.status == "ok") & (v.model != "Naive")]
    if t.empty:
        raise SystemExit(f"Tidak ada baris validasi dengan tag '{tag}'.")
    pv = t.pivot_table(index="optimasi", columns="model", values="cv_vs_naive_pct", aggfunc="mean")
    n_model = t.groupby("optimasi").model.nunique()
    r = t.groupby("optimasi").agg(rata2=("cv_vs_naive_pct", "mean"),
                                  detik_tuning=("detik_tuning", "sum")).reset_index()
    r["n_model"] = r.optimasi.map(n_model)
    r = r.sort_values(["rata2", "detik_tuning"])
    print(f"\n=== Tahap 2 (validasi, tag={tag}): cv_vs_naive_pct per model ===")
    print(pv.round(3).to_string())
    print("\nRata-rata 4 model (seri -> waktu tuning terpendek):")
    print(r.round(3).to_string(index=False))
    if "default" in pv.index:
        print("\nSelisih tiap strategi terhadap 'default' per model (poin persen; negatif = lebih baik):")
        print((pv - pv.loc["default"]).round(3).to_string())
    if (r.n_model < 4).any():
        print("PERINGATAN: ada strategi yang belum lengkap 4 model.")
    best = r.iloc[0]
    print(f"\n-> Terpilih: optimasi={best.optimasi} (rata-rata {best.rata2:+.3f}%)")
    (OUT / "ringkasan").mkdir(exist_ok=True)
    r.to_csv(OUT / "ringkasan" / "tahap2_validasi.csv", index=False)
    return dict(optimasi=best.optimasi, rata2_cv_vs_naive_pct=float(best.rata2)), t


def kunci(v, tag1, tag2, paksa):
    if F_KUNCI.exists() and not paksa:
        print(f"\n{F_KUNCI} sudah ada; tidak ditimpa (pakai --paksa bila memang perlu).")
        print(F_KUNCI.read_text())
        return
    p1, t1 = pilih_tahap1(v, tag1)
    p2, t2 = pilih_tahap2(v, tag2)
    if not ((t2.dataset == p1["dataset"]) & (t2.horizon_menit == p1["horizon_menit"])).all():
        print("PERINGATAN: baris Tahap 2 tidak semuanya memakai pasangan terpilih Tahap 1.")
    isi = dict(dibuat_utc=datetime.now(timezone.utc).isoformat(timespec="seconds"),
               tag_tahap1=tag1, tag_tahap2=tag2, tahap1=p1, tahap2=p2,
               sha256_hasil_validasi=sha256(F_VAL),
               sha256_baris_tahap1_2=sha256_baris(pd.concat([t1, t2])),
               n_baris_tahap1=len(t1), n_baris_tahap2=len(t2))
    F_KUNCI.write_text(json.dumps(isi, indent=2))
    print(f"\nKeputusan dikunci -> {F_KUNCI}")
    print(json.dumps(isi, indent=2))


# ---------------------------------------------------------------------------
# Uji final (K8)
# ---------------------------------------------------------------------------
def cek_kunci(v):
    if not F_KUNCI.exists():
        raise SystemExit("Belum ada hasil/keputusan_terkunci.json. Jalankan "
                         "'python ringkas.py --tahap 2' dulu.")
    k = json.loads(F_KUNCI.read_text())
    t = v[v.tag.isin([k["tag_tahap1"], k["tag_tahap2"]]) & (v.status == "ok") & (v.model != "Naive")]
    if sha256_baris(t) != k["sha256_baris_tahap1_2"]:
        raise SystemExit("Baris validasi Tahap 1/2 berubah sejak dikunci. Uji final dibatalkan.")
    status_file = "sama" if sha256(F_VAL) == k["sha256_hasil_validasi"] else \
        "berbeda (wajar bila Tahap 3-4 sudah menambah baris)"
    print(f"Keputusan terkunci {k['dibuat_utc']}: {k['tahap1']} | {k['tahap2']}")
    print(f"  baris Tahap 1-2 tidak berubah (hash cocok); hash file validasi: {status_file}")
    return k


def holm(u):
    from statsmodels.stats.multitest import multipletests
    u = u[(u.model != "Naive") & (u.status == "ok")].copy()
    u["tahap"] = u.tag.map(keluarga)
    u["kunci"] = u.run_id.map(kunci_tanpa_tag)
    u["duplikat"] = u.duplicated(["tahap", "kunci"])
    u["p_MAE_holm"] = np.nan
    for _, g in u[~u.duplikat & u.p_MAE.notna()].groupby("tahap"):
        u.loc[g.index, "p_MAE_holm"] = multipletests(g.p_MAE.values, method="holm")[1]
    # duplikat mengikuti nilai baris pertamanya
    first = u[~u.duplikat].set_index(["tahap", "kunci"])["p_MAE_holm"]
    dup = u.duplikat
    u.loc[dup, "p_MAE_holm"] = [first.get((a, b), np.nan) for a, b in zip(u.loc[dup, "tahap"], u.loc[dup, "kunci"])]
    sig = u.p_MAE_holm < 0.05
    u["status_uji"] = np.select(
        [(u.MAE_vs_naive_pct < 0) & (u.DM_MAE < 0) & sig, (u.DM_MAE > 0) & sig],
        ["lebih_baik", "lebih_buruk"], "tidak_berbeda")
    u["beda_arah_rmse"] = np.sign(u.DM_RMSE) != np.sign(u.DM_MAE)
    return u


def sebaran(u):
    """Uji model datar dari file prediksi (lihat LOG_PERUBAHAN P2)."""
    dirp = OUT / "prediksi"
    baris = []
    for _, r in u.iterrows():
        safe = str(r["run_id"]).replace("|", "__").replace(":", "-").replace(" ", "_")
        f = dirp / f"{safe}.csv"
        if not f.exists():
            continue
        d = pd.read_csv(f)
        pr = np.log(d["prediksi"] / d["harga_now"])
        ak = np.log(d["harga_aktual"] / d["harga_now"])
        sd = ak.std()
        baris.append(dict(run_id=r["run_id"], n_unik=pr.round(12).nunique(),
                          rasio_sebaran=pr.std() / sd if sd > 0 else np.nan,
                          korelasi=np.corrcoef(pr, ak)[0, 1] if pr.std() > 0 else np.nan,
                          geser_rata2=pr.mean()))
    if not baris:
        return u.assign(n_unik=np.nan, rasio_sebaran=np.nan, korelasi=np.nan, geser_rata2=np.nan,
                        datar=np.nan)
    s = pd.DataFrame(baris)
    s["datar"] = (s.n_unik <= 3) | (s.rasio_sebaran < 0.01)
    return u.merge(s, on="run_id", how="left")


def uji_final(v):
    cek_kunci(v)
    u = pd.read_csv(F_UJI).drop_duplicates("run_id", keep="last")
    h = sebaran(holm(u))
    kol = ["tahap", "tag", "dataset", "horizon_menit", "frac_latih", "model", "optimasi", "loss",
           "early_stop", "top_k", "pruner", "MAE_vs_naive_pct", "RMSE_vs_naive_pct", "DM_MAE",
           "p_MAE", "p_MAE_holm", "status_uji", "beda_arah_rmse", "Akurasi_arah_pct",
           "arah_baseline_pct", "pct_tetap", "korelasi", "rasio_sebaran", "datar", "duplikat"]
    print("\n=== Uji final per tahap (Holm per tahap pada p_MAE) ===")
    for tahap, g in h.groupby("tahap"):
        print(f"\n--- {tahap}: {len(g)} baris ({(~g.duplikat).sum()} unik dalam keluarga Holm) ---")
        print(g[kol[1:]].drop(columns=["duplikat"]).round(4).to_string(index=False))
        print("  status:", g[~g.duplikat].status_uji.value_counts().to_dict())
    tb = pd.read_csv(F_UJI)
    tb = tb[tb.status == "tidak_berlaku"]
    if len(tb):
        print(f"\nTidak berlaku (tidak dijalankan): {len(tb)} baris, mis. AdaBoost dengan --early-stop/--loss l1")
    (OUT / "ringkasan").mkdir(exist_ok=True)
    h[kol + ["run_id"]].to_csv(OUT / "ringkasan" / "uji_final_holm.csv", index=False)
    print(f"\nTersimpan: {OUT / 'ringkasan' / 'uji_final_holm.csv'}")


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--tahap", type=int, choices=[1, 2])
    a.add_argument("--uji-final", action="store_true")
    a.add_argument("--tag1", default="tahap1")
    a.add_argument("--tag2", default="tahap2")
    a.add_argument("--paksa", action="store_true", help="timpa keputusan_terkunci.json")
    a = a.parse_args()

    v = baca_validasi()
    rekap(v)
    if a.tahap == 1:
        pilih_tahap1(v, a.tag1)
    elif a.tahap == 2:
        kunci(v, a.tag1, a.tag2, a.paksa)
    if a.uji_final:
        uji_final(v)


if __name__ == "__main__":
    main()
```

### `requirements.txt`

```text
pandas>=2.0
numpy>=1.24
scipy>=1.10
scikit-learn>=1.3
xgboost>=2.0
lightgbm>=4.0
catboost>=1.2
optuna>=3.6
cmaes>=0.10
statsmodels>=0.14
```

### `btcpred/data.py`

```python
"""Memuat data Indodax dan membangun fitur + target untuk horizon tertentu."""
import numpy as np
import pandas as pd


def agregasi_5m(df1):
    """df1: index waktu awal candle 1 menit (UTC), kolom open, high, low, close, volume.
    Hasil: candle 5 menit, waktu = AWAL bar (UTC). n_menit < 5 = bar parsial."""
    g = df1.resample("5min", label="left", closed="left", origin="epoch")
    out = pd.DataFrame({
        "open": g["open"].first(), "high": g["high"].max(),
        "low": g["low"].min(), "close": g["close"].last(),
        "volume": g["volume"].sum(min_count=1),
        "n_menit": g["close"].count(),
    })
    out = out[out["n_menit"] > 0]
    return out


def _celah(idx, tf_menit, start, end):
    """Statistik bar hilang pada grid TF di dalam [start, end]."""
    s = pd.Timestamp(start).floor(f"{tf_menit}min") if start else idx.min()
    e = pd.Timestamp(end).floor(f"{tf_menit}min") if end else idx.max()
    grid = pd.date_range(s, e, freq=f"{tf_menit}min")
    ada = grid.isin(idx)
    hilang = ~ada
    n_hilang = int(hilang.sum())
    if n_hilang == 0:
        return dict(n_bar_grid=len(grid), n_hilang=0, n_celah=0, celah_terpanjang_mnt=0)
    blok = pd.Series(hilang).ne(pd.Series(hilang).shift()).cumsum()
    panjang = pd.Series(hilang)[hilang].groupby(blok[hilang]).size()
    return dict(n_bar_grid=len(grid), n_hilang=n_hilang, n_celah=int(len(panjang)),
                celah_terpanjang_mnt=int(panjang.max() * tf_menit))


def load(path, jenis, tf_menit, harga, start=None, end=None, sumber_tf=None):
    """Baca CSV, rapikan timestamp ke grid TF, isi kolom 'harga'.
    Bar yang hilang dibiarkan NaN (tidak diisi), supaya fitur/target yang
    melewati gap otomatis terbuang.

    sumber_tf=1 dengan tf_menit=5 (jenis candle): candle 5 menit dibentuk dari
    candle 1 menit lewat agregasi_5m().

    Mengembalikan (df, info). info memuat deskripsi data di dalam [start, end]:
    tanggal awal/akhir, n_baris_mentah, n_bar, n_parsial, n_hilang, n_celah,
    celah_terpanjang_mnt."""
    df = pd.read_csv(path)
    agregasi = sumber_tf is not None and sumber_tf != tf_menit
    floor_tf = sumber_tf if agregasi else tf_menit
    df["waktu"] = pd.to_datetime(df["waktu_utc"]).dt.floor(f"{floor_tf}min")
    df = df.drop_duplicates("waktu").sort_values("waktu").set_index("waktu")

    dalam = slice(start, end)
    n_mentah = int(len(df.loc[dalam]))
    if agregasi:
        if jenis != "candle" or sumber_tf != 1 or tf_menit != 5:
            raise ValueError("agregasi hanya didukung untuk candle 1 menit -> 5 menit")
        df = agregasi_5m(df[["open", "high", "low", "close", "volume"]])
    else:
        df["n_menit"] = tf_menit if jenis == "candle" else np.nan

    info = dict(tanggal_awal=str(df.loc[dalam].index.min()),
                tanggal_akhir=str(df.loc[dalam].index.max()),
                n_baris_mentah=n_mentah, n_bar=int(len(df.loc[dalam])),
                n_parsial=int((df.loc[dalam, "n_menit"] < tf_menit).sum()) if jenis == "candle" else 0)
    info.update(_celah(df.index, tf_menit, start, end))

    if jenis == "candle":
        if harga == "typical":
            df["harga"] = (df["high"] + df["low"] + df["close"]) / 3
        elif harga == "ohlc4":
            df["harga"] = (df["open"] + df["high"] + df["low"] + df["close"]) / 4
        elif harga == "close":
            df["harga"] = df["close"]
        else:
            raise ValueError(f"harga candle tidak dikenal: {harga}")
    elif jenis == "ticker":
        df["mid"] = (df["buy"] + df["sell"]) / 2          # buy = bid, sell = ask
        if harga == "mid":
            df["harga"] = df["mid"]
        elif harga == "last":
            df["harga"] = df["last_price"]
        else:
            raise ValueError(f"harga ticker tidak dikenal: {harga}")
    else:
        raise ValueError(jenis)

    full = pd.date_range(df.index.min(), df.index.max(), freq=f"{tf_menit}min")
    df = df.reindex(full)
    if start or end:
        # ambil sedikit data sebelum START untuk pemanasan fitur (hanya data masa lalu)
        buf = pd.Timedelta(minutes=300)
        s = pd.Timestamp(start) - buf if start else None
        df = df.loc[s:end]
    return df, info


def build(df, jenis, tf_menit, horizon_menit, n_lag, windows_mnt, start=None):
    """Kembalikan DataFrame berisi fitur, 'target' (log return h ke depan),
    'harga_now', 'harga_next'. Semua fitur hanya memakai data sampai waktu t."""
    h = horizon_menit // tf_menit                     # horizon dalam bar
    p = df["harga"]
    r = np.log(p).diff()                              # return bar t-1 -> t
    X = pd.DataFrame(index=df.index)

    for k in range(1, n_lag + 1):
        X[f"ret_lag{k}"] = r.shift(k - 1)

    wins = sorted({max(2, w // tf_menit) for w in windows_mnt})
    for w in wins:
        m = w * tf_menit
        X[f"ret_sum_{m}m"] = r.rolling(w).sum()
        X[f"ret_std_{m}m"] = r.rolling(w).std()
        X[f"nol_{m}m"] = (r == 0).astype(float).where(r.notna()).rolling(w).mean()

    if jenis == "candle":
        rng = (df["high"] - df["low"]) / df["close"]
        X["range_rel"] = rng
        hl = (df["high"] - df["low"]).replace(0, np.nan)
        X["posisi_bar"] = ((df["close"] - df["low"]) / hl).fillna(0.5).where(df["close"].notna())
        lv = np.log1p(df["volume"])
        X["log_vol"] = lv
        for w in wins:
            m = w * tf_menit
            X[f"range_mean_{m}m"] = rng.rolling(w).mean()
            X[f"vol_rasio_{m}m"] = lv - lv.rolling(w).mean()
    else:
        X["spread_rel"] = (df["sell"] - df["buy"]) / df["mid"]
        r24 = (df["high_24h"] - df["low_24h"]).replace(0, np.nan)
        X["posisi_24h"] = (p - df["low_24h"]) / r24
        X["dvol_24h"] = np.log(df["vol_btc_24h"]).diff()

    jam = df.index.hour + df.index.minute / 60
    X["jam_sin"] = np.sin(2 * np.pi * jam / 24)
    X["jam_cos"] = np.cos(2 * np.pi * jam / 24)

    out = X.copy()
    out["target"] = np.log(p.shift(-h) / p)
    out["harga_now"] = p
    out["harga_next"] = p.shift(-h)
    out = out.replace([np.inf, -np.inf], np.nan).dropna()
    if start:
        out = out.loc[start:]
    return out, list(X.columns), h
```

### `btcpred/models.py`

```python
"""Definisi model, ruang pencarian hyperparameter, dan grid."""
from sklearn.ensemble import AdaBoostRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
from catboost import CatBoostRegressor

ES_ROUNDS = 50          # kesabaran early stopping
ES_MAX_TREES = 2000     # jumlah pohon maksimum saat early stopping aktif

# Nama parameter "jumlah pohon" per model
N_TREES_KEY = {"XGBoost": "n_estimators", "LightGBM": "n_estimators",
               "CatBoost": "iterations", "AdaBoost": "n_estimators"}

DEFAULT = {"XGBoost": {}, "LightGBM": {}, "CatBoost": {}, "AdaBoost": {"max_depth": 3}}

# Grid Search: 3 x 3 x 3 = 27 kombinasi per model
GRID = {
    "XGBoost":  {"n_estimators": [50, 200, 500], "max_depth": [2, 4, 6],
                 "learning_rate": [0.001, 0.01, 0.1]},
    "LightGBM": {"n_estimators": [50, 200, 500], "num_leaves": [4, 15, 31],
                 "learning_rate": [0.001, 0.01, 0.1]},
    "CatBoost": {"iterations": [50, 200, 500], "depth": [2, 4, 6],
                 "learning_rate": [0.001, 0.01, 0.1]},
    "AdaBoost": {"n_estimators": [50, 150, 300], "max_depth": [2, 3, 5],
                 "learning_rate": [0.01, 0.1, 1.0]},
}


def space(name, t, early_stop=False):
    """Ruang pencarian untuk random/tpe/cmaes/ga/qmc."""
    if name == "XGBoost":
        p = dict(
            n_estimators=t.suggest_int("n_estimators", 10, 1000, log=True),
            max_depth=t.suggest_int("max_depth", 1, 8),
            learning_rate=t.suggest_float("learning_rate", 1e-3, 0.3, log=True),
            min_child_weight=t.suggest_int("min_child_weight", 1, 100, log=True),
            subsample=t.suggest_float("subsample", 0.5, 1.0),
            colsample_bytree=t.suggest_float("colsample_bytree", 0.3, 1.0),
            reg_lambda=t.suggest_float("reg_lambda", 1e-3, 100, log=True),
            reg_alpha=t.suggest_float("reg_alpha", 1e-3, 10, log=True),
        )
    elif name == "LightGBM":
        p = dict(
            n_estimators=t.suggest_int("n_estimators", 10, 1000, log=True),
            num_leaves=t.suggest_int("num_leaves", 2, 63, log=True),
            max_depth=t.suggest_int("max_depth", 1, 8),
            learning_rate=t.suggest_float("learning_rate", 1e-3, 0.3, log=True),
            min_child_samples=t.suggest_int("min_child_samples", 5, 300, log=True),
            subsample=t.suggest_float("subsample", 0.5, 1.0),
            colsample_bytree=t.suggest_float("colsample_bytree", 0.3, 1.0),
            reg_lambda=t.suggest_float("reg_lambda", 1e-3, 100, log=True),
            reg_alpha=t.suggest_float("reg_alpha", 1e-3, 10, log=True),
        )
        p["subsample_freq"] = 1
    elif name == "CatBoost":
        p = dict(
            iterations=t.suggest_int("iterations", 10, 1000, log=True),
            depth=t.suggest_int("depth", 1, 8),
            learning_rate=t.suggest_float("learning_rate", 1e-3, 0.3, log=True),
            l2_leaf_reg=t.suggest_float("l2_leaf_reg", 0.1, 100, log=True),
            random_strength=t.suggest_float("random_strength", 1e-3, 10, log=True),
            bagging_temperature=t.suggest_float("bagging_temperature", 0.0, 1.0),
        )
    elif name == "AdaBoost":
        p = dict(
            n_estimators=t.suggest_int("n_estimators", 10, 500, log=True),
            learning_rate=t.suggest_float("learning_rate", 1e-3, 1.0, log=True),
            loss=t.suggest_categorical("loss", ["linear", "square", "exponential"]),
            max_depth=t.suggest_int("max_depth", 1, 6),
        )
    else:
        raise ValueError(name)
    if early_stop and name != "AdaBoost":
        p[N_TREES_KEY[name]] = ES_MAX_TREES
    return p


def grid_params(name, t, early_stop=False):
    g = GRID[name]
    p = {k: t.suggest_categorical(k, v) for k, v in g.items()
         if not (early_stop and name != "AdaBoost" and k == N_TREES_KEY[name])}
    if name == "LightGBM":
        p["subsample_freq"] = 1
    if early_stop and name != "AdaBoost":
        p[N_TREES_KEY[name]] = ES_MAX_TREES
    return p


def grid_space(name, early_stop=False):
    g = dict(GRID[name])
    if early_stop and name != "AdaBoost":
        g.pop(N_TREES_KEY[name])
    return g


def make(name, params, loss="l2", seed=42, early_stop=False):
    prm = dict(params)
    if name == "XGBoost":
        if loss == "l1":
            prm["objective"] = "reg:absoluteerror"
        if early_stop:
            prm["early_stopping_rounds"] = ES_ROUNDS
        return XGBRegressor(**prm, random_state=seed, n_jobs=-1, verbosity=0)
    if name == "LightGBM":
        if loss == "l1":
            prm["objective"] = "l1"
        return LGBMRegressor(**prm, random_state=seed, n_jobs=-1, verbose=-1)
    if name == "CatBoost":
        if loss == "l1":
            prm["loss_function"] = "MAE"
        return CatBoostRegressor(**prm, random_seed=seed, verbose=0, thread_count=-1,
                                 allow_writing_files=False)
    if name == "AdaBoost":
        # AdaBoost.R2 punya parameter 'loss' sendiri (linear/square/exponential);
        # pengaturan LOSS l1/l2 tidak berlaku untuk AdaBoost.
        depth = prm.pop("max_depth", 3)
        return AdaBoostRegressor(estimator=DecisionTreeRegressor(max_depth=depth),
                                 **prm, random_state=seed)
    raise ValueError(name)


def fit(name, model, Xtr, ytr, Xva=None, yva=None, early_stop=False):
    """Latih model; bila early stopping aktif, pakai (Xva, yva) sebagai data validasi.
    Mengembalikan jumlah pohon terbaik (atau None)."""
    if not early_stop or name == "AdaBoost" or Xva is None:
        model.fit(Xtr, ytr)
        return None
    if name == "XGBoost":
        model.fit(Xtr, ytr, eval_set=[(Xva, yva)], verbose=False)
        return int(model.best_iteration) + 1
    if name == "LightGBM":
        import lightgbm as lgb
        model.fit(Xtr, ytr, eval_set=[(Xva, yva)],
                  callbacks=[lgb.early_stopping(ES_ROUNDS, verbose=False)])
        return int(model.best_iteration_ or model.n_estimators)
    if name == "CatBoost":
        model.fit(Xtr, ytr, eval_set=(Xva, yva), early_stopping_rounds=ES_ROUNDS)
        return int(model.get_best_iteration()) + 1
```

### `btcpred/optim.py`

```python
"""Optimasi hyperparameter: default, grid, random, tpe, cmaes, ga, qmc.
Semua metode memakai fungsi objektif yang sama: rata-rata MAE harga (rupiah)
pada walk-forward CV (TimeSeriesSplit + purging berbasis waktu) di data
pengembangan saja."""
import time
import warnings
import numpy as np
import pandas as pd
import optuna
from sklearn.model_selection import TimeSeriesSplit

from . import models as M
from .evaluate import select_top_k

optuna.logging.set_verbosity(optuna.logging.WARNING)
warnings.filterwarnings("ignore", category=optuna.exceptions.ExperimentalWarning)


def make_sampler(method, seed):
    s = optuna.samplers
    if method == "random":
        return s.RandomSampler(seed=seed)
    if method == "tpe":
        return s.TPESampler(seed=seed, n_startup_trials=10)
    if method == "cmaes":
        return s.CmaEsSampler(seed=seed, n_startup_trials=5, warn_independent_sampling=False)
    if method == "ga":
        return s.NSGAIISampler(seed=seed, population_size=10)
    if method == "qmc":
        return s.QMCSampler(qmc_type="sobol", scramble=True, seed=seed,
                            warn_independent_sampling=False)
    raise ValueError(f"metode optimasi tidak dikenal: {method}")


def make_pruner(pruner):
    if pruner is None:
        return optuna.pruners.NopPruner()
    if pruner == "median":
        return optuna.pruners.MedianPruner(n_startup_trials=5, n_warmup_steps=1)
    if pruner == "hyperband":
        return optuna.pruners.HyperbandPruner()
    raise ValueError(pruner)


def _folds(X, n_folds, horizon_menit):
    """TimeSeriesSplit tanpa gap, lalu purging berbasis waktu: baris latih fold
    dibuang bila waktu target (t + horizon) tidak lebih awal dari awal validasi."""
    hz = pd.Timedelta(minutes=horizon_menit)
    out = []
    for tr, va in TimeSeriesSplit(n_splits=n_folds).split(X):
        t_val0 = X.index[va[0]]
        tr = tr[(X.index[tr] + hz) < t_val0]
        if len(tr) == 0:
            raise ValueError("fold tanpa data latih setelah purging; kurangi n_folds")
        out.append((tr, va))
    return out


def cv_score(name, params, X, y, harga_now, harga_next, folds, loss, seed, early_stop,
             fitur_fold=None, trial=None):
    """Walk-forward CV. Objektif = MAE harga (rupiah) rata-rata fold.

    folds      : daftar (idx_latih, idx_validasi) dari _folds().
    fitur_fold : None (semua kolom) atau daftar kolom per fold (seleksi top-k di
                 dalam fold).
    Return dict: mae_rp, naive_rp, best_n."""
    hn, hx = harga_now.to_numpy(), harga_next.to_numpy()

    def one(i, tr, va):
        cols = fitur_fold[i] if fitur_fold is not None else list(X.columns)
        Xtr, Xva = X.iloc[tr][cols], X.iloc[va][cols]
        m = M.make(name, params, loss, seed, early_stop and name != "AdaBoost")
        bn = M.fit(name, m, Xtr, y.iloc[tr], Xva, y.iloc[va], early_stop)
        p_hat = hn[va] * np.exp(m.predict(Xva))
        mae_m = float(np.mean(np.abs(hx[va] - p_hat)))
        mae_n = float(np.mean(np.abs(hx[va] - hn[va])))
        return mae_m, mae_n, bn

    if name == "AdaBoost":
        # AdaBoost (scikit-learn) hanya memakai 1 core, jadi fold dijalankan paralel.
        from joblib import Parallel, delayed
        res = Parallel(n_jobs=-1)(delayed(one)(i, tr, va) for i, (tr, va) in enumerate(folds))
        if trial is not None:
            for i in range(len(res)):
                trial.report(float(np.mean([r[0] for r in res[: i + 1]])), i)
            if trial.should_prune():
                raise optuna.TrialPruned()
    else:
        res = []
        for i, (tr, va) in enumerate(folds):
            res.append(one(i, tr, va))
            if trial is not None:
                trial.report(float(np.mean([r[0] for r in res])), i)
                if trial.should_prune():
                    raise optuna.TrialPruned()
    best_n = [r[2] for r in res if r[2] is not None]
    return dict(mae_rp=float(np.mean([r[0] for r in res])),
                naive_rp=float(np.mean([r[1] for r in res])),
                best_n=int(np.mean(best_n)) if best_n else None)


def tune(name, X, y, method, cfg, horizon_menit, harga_now, harga_next):
    """Tuning pada data pengembangan saja.

    Return dict: params, cv_mae_rp, cv_naive_rp, cv_vs_naive_pct, n_trials,
    n_pruned, detik_tuning, fitur_fold (daftar kolom per fold bila top-k)."""
    t0 = time.time()
    es = cfg["EARLY_STOP"]
    folds = _folds(X, cfg["N_FOLDS"], horizon_menit)
    fitur_fold = None
    if cfg["TOP_K"]:
        # importance dihitung dengan model bawaan pada data latih tiap fold.
        # Tidak bergantung pada hyperparameter trial, jadi cukup sekali per fold.
        fitur_fold = [select_top_k(name, X.iloc[tr], y.iloc[tr], cfg["TOP_K"],
                                   cfg["LOSS"], cfg["SEED"]) for tr, _ in folds]
    kw = dict(harga_now=harga_now, harga_next=harga_next, folds=folds, loss=cfg["LOSS"],
              seed=cfg["SEED"], early_stop=es, fitur_fold=fitur_fold)

    def default_params():
        p = dict(M.DEFAULT[name])
        if es and name != "AdaBoost":
            p[M.N_TREES_KEY[name]] = M.ES_MAX_TREES
        return p

    if method == "default":
        params = default_params()
        sc = cv_score(name, params, X, y, **kw)
        n_tr, n_pr = 1, 0
    else:
        hasil = {}

        def objective(t):
            p = M.grid_params(name, t, es) if method == "grid" else M.space(name, t, es)
            sc_t = cv_score(name, p, X, y, trial=t, **kw)
            hasil[t.number] = sc_t
            return sc_t["mae_rp"]

        if method == "grid":
            g = M.grid_space(name, es)
            sampler = optuna.samplers.GridSampler(g, seed=cfg["SEED"])
            n_trials = int(np.prod([len(v) for v in g.values()]))
        else:
            sampler = make_sampler(method, cfg["SEED"])
            n_trials = cfg["N_TRIALS"]
        study = optuna.create_study(direction="minimize", sampler=sampler,
                                    pruner=make_pruner(cfg["PRUNER"]))
        study.optimize(objective, n_trials=n_trials)
        n_tr = len(study.trials)
        n_pr = sum(t.state == optuna.trial.TrialState.PRUNED for t in study.trials)
        if not any(t.state == optuna.trial.TrialState.COMPLETE for t in study.trials):
            # semua trial gagal/dipangkas -> pakai setelan bawaan supaya run tidak batal
            params = default_params()
            sc = cv_score(name, params, X, y, **kw)
        else:
            bt = study.best_trial
            params = dict(bt.params)
            if name == "LightGBM":
                params["subsample_freq"] = 1
            if es and name != "AdaBoost":
                params[M.N_TREES_KEY[name]] = M.ES_MAX_TREES
            sc = hasil[bt.number]

    # Early stopping: model final memakai rata-rata jumlah pohon terbaik dari CV
    if es and name != "AdaBoost" and sc["best_n"] is not None:
        params[M.N_TREES_KEY[name]] = max(1, sc["best_n"])
    return dict(params=params, cv_mae_rp=sc["mae_rp"], cv_naive_rp=sc["naive_rp"],
                cv_vs_naive_pct=(sc["mae_rp"] / sc["naive_rp"] - 1) * 100,
                n_trials=n_tr, n_pruned=n_pr, detik_tuning=time.time() - t0,
                fitur_fold=fitur_fold)
```

### `btcpred/evaluate.py`

```python
"""Metrik evaluasi, uji Diebold-Mariano, dan seleksi fitur."""
import numpy as np
import pandas as pd
from scipy import stats

from . import models as M

AMBANG_TETAP_RP = 1.0     # harga dianggap tetap bila |harga_next - harga_now| < 1 rupiah


def metrics(h_true, h_pred, r_pred, h_now, ret_lag1=None):
    """Metrik harga + akurasi arah.

    Akurasi arah hanya dihitung pada bar yang harganya berubah
    (|harga_next - harga_now| >= 1 rupiah). arah_baseline_pct = akurasi arah
    bila arah ditebak dengan sign(ret_lag1) (arah return bar terakhir)."""
    h_true, h_pred, h_now = map(np.asarray, (h_true, h_pred, h_now))
    e = h_true - h_pred
    dh = h_true - h_now
    gerak = np.abs(dh) >= AMBANG_TETAP_RP
    arah_aktual = np.sign(dh[gerak])
    arah = (np.sign(np.asarray(r_pred)[gerak]) == arah_aktual).mean() * 100 if gerak.any() else np.nan
    out = dict(MAE_Rp=float(np.abs(e).mean()),
               RMSE_Rp=float(np.sqrt((e ** 2).mean())),
               MAPE_pct=float((np.abs(e) / h_true).mean() * 100),
               Akurasi_arah_pct=float(arah),
               n_arah=int(gerak.sum()),
               pct_tetap=float((~gerak).mean() * 100),
               pct_naik=float((dh >= AMBANG_TETAP_RP).mean() * 100),
               pct_turun=float((dh <= -AMBANG_TETAP_RP).mean() * 100))
    if ret_lag1 is not None and gerak.any():
        b = np.sign(np.asarray(ret_lag1)[gerak])
        out["arah_baseline_pct"] = float((b == arah_aktual).mean() * 100)
    else:
        out["arah_baseline_pct"] = np.nan
    return out


def dm_test(d, h, freq_menit):
    """Diebold-Mariano dengan koreksi Harvey-Leybourne-Newbold.

    d          : pd.Series selisih loss (loss_model - loss_naive), index = waktu.
    h          : horizon dalam bar (autokovarians lag 1 .. h-1).
    freq_menit : resolusi grid (1 atau 5 menit).

    Seri di-reindex ke grid waktu rapat, sehingga bar yang hilang menjadi NaN dan
    jarak lag tetap benar walaupun ada celah. Autokovarians lag k memakai hanya
    pasangan yang keduanya tidak NaN, lalu dibagi n = jumlah d yang tidak NaN.
    DM < 0 berarti model lebih akurat daripada Naive."""
    d = d.sort_index()
    grid = pd.date_range(d.index.min(), d.index.max(), freq=f"{freq_menit}min")
    x = d.reindex(grid).to_numpy(dtype=float)
    ok = ~np.isnan(x)
    n = int(ok.sum())
    if n < 2:
        return np.nan, np.nan
    mean = np.nanmean(x)
    dc = np.where(ok, x - mean, 0.0)          # NaN -> 0 supaya pasangan berisi NaN tidak ikut
    gamma0 = np.dot(dc, dc) / n
    var = gamma0
    for k in range(1, h):
        if k >= len(dc):
            break
        var += 2 * np.dot(dc[k:], dc[:-k]) / n
    if var <= 0:
        var = gamma0
    if var == 0:
        return np.nan, np.nan
    dm = mean / np.sqrt(var / n)
    koreksi = np.sqrt(max((n + 1 - 2 * h + h * (h - 1) / n) / n, 1e-12))
    dm *= koreksi
    p = 2 * (1 - stats.t.cdf(abs(dm), df=n - 1))
    return float(dm), float(p)


def select_top_k(name, X, y, k, loss, seed):
    """Seleksi fitur: latih model bawaan pada (X, y), ambil K fitur dengan
    importance tertinggi. Dipanggil di dalam tiap fold CV (data latih fold saja)
    dan sekali pada seluruh data pengembangan untuk model akhir."""
    m = M.make(name, M.DEFAULT[name], loss, seed)
    m.fit(X, y)
    imp = pd.Series(m.feature_importances_, index=X.columns).sort_values(ascending=False)
    return list(imp.index[:k])
```
