# Hasil Eksperimen Skripsi v3.0: Prediksi Harga BTC/IDR dengan Model Boosting

> **Fungsi file ini:** konteks lengkap hasil eksperimen arah penelitian baru (setelah bimbingan 23 Oktober 2026). Berisi desain yang dikunci, kronologi, hasil Tahap 1–4 dalam bentuk tabel, temuan utama, kalimat yang aman ditulis, batasan, catatan lingkungan, dan **source code final** paket `prediksi_btc`.
>
> **Status per 28 Oktober 2026:** Tahap 1–4 selesai (92 run, 0 gagal) pada **data satu minggu (14–20 Oktober 2026 UTC)**. Aturan pemilihan dikunci 27 Oktober 2026 pukul 10:08:33 WIB, sebelum Tahap 1 dijalankan. Desain dan aturan **tidak boleh diubah mengikuti hasil**. Analisis tambahan apa pun setelah ini ditulis sebagai eksploratif.
>
> **Hubungan dengan dokumen lain:** menggantikan `hasil_eksperimen_bitcoin_v2_5.md` (versi realized variance, sekarang arsip). Konteks umum ada di `konteks_skripsi_v3.0.md`.
>
> **Notasi:** BTC/IDR = pasar spot Indodax. Angka "MAE vs Naive (%)" negatif berarti model lebih akurat dari Naive.

---

## 1. Jawaban singkat

**Apakah eksperimen bisa dijalankan? Ya.** Data lengkap (0 bar hilang), seluruh 92 run selesai, hasil deterministik (run yang sama di tahap berbeda memberi angka identik), dan semua pemilihan mengikuti aturan yang dikunci.

**Jawaban satu kalimat:** pada data satu minggu, keempat model boosting **hampir tidak bisa mengalahkan Naive** (tebakan "harga tidak berubah"). Keunggulan tipis hanya muncul di **horizon 1 menit**, dan hanya **satu dari 92 run** yang signifikan lebih baik dari Naive menurut MAE, yaitu **LightGBM + Bayesian (TPE) + loss L1** (MAE −0,723%, p = 0,033). Optimasi hyperparameter sangat berpengaruh dibanding setting default, dan metode Bayesian (TPE) memberi rata-rata terbaik.

---

## 2. Kronologi singkat

| Tahap | Isi | Hasil kunci |
|---|---|---|
| Pilot (20–22 Okt, kode lama `btc5m`, bukan paket ini) | Ticker 5 menit, horizon 5 menit, 4 model, Optuna TPE, uji rentang lama/lebar, kelompok fitur, loss L1, split 60/70/80 | Tuning menurunkan error 20–37% dari default; semua model sedikit di belakang Naive; CatBoost dan XGBoost bergantian teratas, AdaBoost terlemah |
| Bimbingan 23 Okt | Arah ditetapkan: harga BTC/IDR, 4 model, split 80:20/70:30/60:40, optimasi sebanyak mungkin, TF dicari lewat eksperimen | Paket `prediksi_btc` dibuat |
| Persiapan 27 Okt | venv Python 3.14.8; perbaikan bug `--tag` di `run_id`; fallback Optuna; metadata, checksum data | `KEPUTUSAN_TERKUNCI.md` dibuat 10:08:33 WIB |
| Tahap 1 (27 Okt) | 2 dataset × horizon × 4 model, TPE, 80:20 | Terpilih `candle_1m`, horizon 1 menit (Aturan 2, tidak ada yang signifikan) |
| Tahap 2 | 7 metode optimasi × 4 model | Terpilih Bayesian (TPE) |
| Tahap 3 | 3 split × 4 model | Tidak ada pemilihan |
| Tahap 4 | 4 teknik tambahan × 4 model | Tidak ada pemilihan; satu run signifikan (LightGBM + loss L1) |

Total 92 run model + 17 baris Naive, durasi 73 menit 22 detik di Apple M5 (10 core, 16 GB).

---

## 3. Desain yang dikunci

| Komponen | Nilai |
|---|---|
| Data | Indodax BTC/IDR, dikumpulkan sendiri lewat collector di VPS |
| Periode | 2026-10-14 00:00 s.d. 2026-10-20 23:59 UTC (7 hari) |
| Dataset | `candle_1m` (candle 1 menit, ±10.080 bar), `ticker_5m` (ticker 5 menit, ±2.016 bar) |
| Definisi harga | candle: `typical` = (high+low+close)/3; ticker: `mid` = (bid+ask)/2 |
| Horizon (TF prediksi) | 1, 5, 15, 30, 60 menit (1 menit hanya untuk candle) |
| Target | Log return h menit ke depan, dikonversi ke rupiah: harga_prediksi = harga_sekarang × exp(return_prediksi) |
| Fitur | 42 fitur (candle) / 32 fitur (ticker): lag return, statistik bergulir 5–240 menit, range dan volume (candle), spread dan posisi 24 jam (ticker), jam (sin/cos) |
| Model | XGBoost, LightGBM, CatBoost, AdaBoost (AdaBoost.R2); pembanding Naive |
| Tuning | 30 trial (Grid 27), walk-forward CV 5 fold di data latih (`TimeSeriesSplit`, jeda = horizon), objektif MAE return, seed 42 |
| Split | Berurutan waktu; h bar terakhir data latih dibuang (*purging*) |
| Metrik utama | MAE vs Naive (%) |
| Metrik pendukung | RMSE vs Naive (%), MAPE, akurasi arah, uji Diebold-Mariano (koreksi HLN, autokovarians lag h−1) |
| **Signifikan lebih baik dari Naive** | MAE vs Naive < 0 **dan** DM_MAE < 0 **dan** p_MAE < 0,05 |

**Aturan pemilihan:** Tahap 1 memilih pasangan (dataset, horizon) dengan skor terkecil (skor = MAE vs Naive terkecil di antara 4 model), diutamakan pasangan yang punya model signifikan; seri → horizon lebih pendek, lalu `candle_1m`. Tahap 2 memilih metode dengan rata-rata MAE vs Naive 4 model terkecil (`default` tidak boleh dipilih; seri → waktu tuning terpendek). Tahap 3 dan 4 tanpa pemilihan.

---

## 4. Hasil per tahap

Tanda: **✓** = signifikan lebih baik dari Naive · **✗** = signifikan lebih buruk dari Naive (DM_MAE > 0, p_MAE < 0,05). Angka = MAE vs Naive (%).

### 4.1 Tahap 1 — Time frame (Bayesian/TPE, split 80:20)

| Dataset | Horizon (menit) | XGBoost | LightGBM | CatBoost | AdaBoost | Rata-rata |
|---|---|---|---|---|---|---|
| candle_1m | 1 | -0,291 | -0,321 | -0,347 | -0,066 | -0,256 |
| candle_1m | 5 | +0,069 | +0,093 ✗ | +0,060 | +1,089 ✗ | +0,328 |
| candle_1m | 15 | +0,133 | +0,084 | +0,183 | +0,350 | +0,187 |
| candle_1m | 30 | +0,010 | +0,059 | +0,469 | +0,439 | +0,244 |
| candle_1m | 60 | +0,207 | -0,159 | +0,411 | +0,104 | +0,141 |
| ticker_5m | 5 | +0,160 ✗ | +0,366 ✗ | +1,043 ✗ | +0,541 ✗ | +0,527 |
| ticker_5m | 15 | +0,269 | +0,132 | +0,792 | +2,554 | +0,937 |
| ticker_5m | 30 | +0,034 | +0,049 | +0,069 | +0,447 | +0,150 |
| ticker_5m | 60 | +0,077 | +0,016 | +0,017 | +0,333 | +0,111 |

MAE Naive per pasangan (Rp): candle_1m h1 = 349.278, candle_1m h5 = 764.151, candle_1m h15 = 1.406.890, candle_1m h30 = 2.019.749, candle_1m h60 = 3.006.141, ticker_5m h5 = 635.172, ticker_5m h15 = 1.309.648, ticker_5m h30 = 1.940.612, ticker_5m h60 = 2.980.794.

**Penerapan aturan:** 0 run signifikan lebih baik dari Naive → Aturan 2. Skor terkecil `candle_1m` horizon 1 menit (−0,347, CatBoost), tidak seri. **Terpilih: `candle_1m`, horizon 1 menit.** Pasangan terbaik kedua: `candle_1m` horizon 60 menit (−0,159, LightGBM).

### 4.2 Tahap 2 — Metode optimasi (`candle_1m`, horizon 1 menit, 80:20)

| Metode | XGBoost | LightGBM | CatBoost | AdaBoost | Rata-rata |
|---|---|---|---|---|---|
| Bayesian (TPE) | -0,291 | -0,321 | -0,347 | -0,066 | -0,256 |
| Random Search | +0,069 | -0,489 | -0,226 | -0,066 | -0,178 |
| Grid Search | +0,059 | -0,041 | -0,301 | +0,420 ✗ | +0,035 |
| CMA-ES | +0,255 | +0,048 | -0,341 | +0,736 ✗ | +0,175 |
| Genetic Algorithm | -0,140 | +0,020 | -0,226 | -0,066 | -0,103 |
| Quasi-Monte Carlo | -0,358 | -0,354 | -0,230 | +0,452 ✗ | -0,122 |
| Default (tanpa tuning) | +4,291 ✗ | +6,586 ✗ | +10,815 ✗ | +14,205 ✗ | +8,974 |

Waktu tuning total (4 model): Bayesian (TPE) 229,3 s, Random Search 118,7 s, Grid Search 227,6 s, CMA-ES 129,9 s, Genetic Algorithm 140,0 s, Quasi-Monte Carlo 157,4 s, Default (tanpa tuning) 9,2 s.

**Penerapan aturan:** rata-rata terkecil Bayesian (TPE) −0,256 (peringkat 2 Random Search −0,178), tidak seri. **Terpilih: Bayesian (TPE).** Setting default rata-rata +8,97% (semua model signifikan lebih buruk dari Naive), jadi tuning hyperparameter sangat menentukan.

### 4.3 Tahap 3 — Rasio split (`candle_1m`, horizon 1 menit, TPE)

| Split | XGBoost | LightGBM | CatBoost | AdaBoost | Rata-rata |
|---|---|---|---|---|---|
| 80:20 | -0,291 | -0,321 | -0,347 | -0,066 | -0,256 |
| 70:30 | +0,205 | +0,186 | +0,207 | +0,241 | +0,210 |
| 60:40 | -0,175 | +0,128 | -0,153 | +0,165 ✗ | -0,009 |

MAE Naive (Rp): 80:20 = 349.278, 70:30 = 317.826, 60:40 = 304.163. MAE rupiah antar-split tidak sebanding karena periode ujinya berbeda. Hanya split 80:20 yang rata-ratanya di bawah Naive; di 70:30 keempat model di atas Naive.

### 4.4 Tahap 4 — Teknik tambahan (`candle_1m`, horizon 1 menit, TPE, 80:20)

| Teknik | XGBoost | LightGBM | CatBoost | AdaBoost | Rata-rata |
|---|---|---|---|---|---|
| Tanpa (Tahap 2, TPE) | -0,291 | -0,321 | -0,347 | -0,066 | -0,256 |
| Early stopping | -0,103 | +0,061 ✗ | +0,045 | -0,066 | -0,016 |
| Top-15 fitur | +0,315 | -0,212 | +0,392 | +0,230 ✗ | +0,181 |
| Loss L1 | +0,232 ✗ | -0,723 ✓ | -0,462 | -0,066 | -0,255 |
| Pruner median | -0,375 | -0,121 | -0,347 | -0,066 | -0,227 |

Waktu total 4 model: Tanpa (Tahap 2, TPE) 232,6 s, Early stopping 654,5 s, Top-15 fitur 1113,2 s, Loss L1 163,5 s, Pruner median 148,4 s. Pruner median memangkas rata-rata 14 dari 30 trial dan menghemat ±36% waktu dengan rata-rata hampir sama. Top-15 fitur justru paling lambat dan paling buruk. AdaBoost tidak terpengaruh loss L1 dan early stopping (AdaBoost.R2 punya parameter `loss` sendiri), jadi angkanya identik.

### 4.5 Rekap per model (seluruh 92 run)

| Model | Run | Rata-rata MAE vs Naive (%) | Terbaik (%) | Rata-rata akurasi arah (%) | Lebih baik sig. | Lebih buruk sig. |
|---|---|---|---|---|---|---|
| XGBoost | 23 | +0,190 | -0,375 | 54,18 | 0 | 3 |
| LightGBM | 23 | +0,207 | -0,723 | 53,61 | 1 | 4 |
| CatBoost | 23 | +0,486 | -0,462 | 54,02 | 0 | 2 |
| AdaBoost | 23 | +0,947 | -0,066 | 52,40 | 0 | 8 |

### 4.6 Ringkasan uji Diebold-Mariano (92 run)

| Kategori | Jumlah |
|---|---|
| Signifikan lebih baik dari Naive (MAE) | 1 |
| Signifikan lebih buruk dari Naive (MAE) | 17 (4 di antaranya setting default) |
| Tidak signifikan | 74 |
| MAE vs Naive < 0 (tanpa syarat signifikan) | 37 |
| RMSE vs Naive < 0 | 65 |
| Akurasi arah > 50% | 71 |

### 4.7 Konfigurasi terbaik

| Komponen | Nilai |
|---|---|
| Konfigurasi | `candle_1m`, harga typical, horizon 1 menit, split 80:20 |
| Model / optimasi / teknik | **LightGBM**, Bayesian (TPE) 30 trial 5 fold, **loss L1**, 42 fitur |
| MAE | Rp346.752 (Naive Rp349.278) |
| MAE vs Naive | **-0,723%**, DM_MAE -2,133, p_MAE 0,0331 |
| RMSE vs Naive | -1,628%, p_RMSE 1.13e-07 |
| Akurasi arah | 58,73% (tertinggi di seluruh eksperimen) |
| Hyperparameter | `n_estimators` 38, `num_leaves` 23, `max_depth` 8, `learning_rate` 0.056086, `min_child_samples` 112, `subsample` 0.942933, `colsample_bytree` 0.87423, `reg_lambda` 0.006908, `reg_alpha` 0.012795, `subsample_freq` 1 |

---

## 5. Temuan utama dan kalimat yang aman ditulis

1. **Time frame.** Hanya horizon 1 menit (data candle) yang rata-rata keempat modelnya di bawah Naive. Di horizon 5–60 menit, hampir semua model sedikit di atas Naive (0,01–2,6%), dan tidak ada yang signifikan lebih baik.
   *Aman:* "Pada data satu minggu, keunggulan model atas Naive hanya terlihat pada horizon 1 menit dan nilainya kecil (kurang dari 1%)."
2. **Optimasi.** Tanpa tuning, keempat model jauh lebih buruk dari Naive (+4,3% sampai +14,2%). Setelah tuning, selisihnya tinggal sekitar −0,5% sampai +0,7%. Bayesian (TPE) rata-ratanya terbaik, disusul Random Search.
   *Aman:* "Optimasi hyperparameter berpengaruh besar terhadap akurasi. Di antara enam metode optimasi, Bayesian Optimization (TPE) memberi rata-rata kesalahan terkecil pada eksperimen ini."
3. **Model.** XGBoost dan LightGBM rata-ratanya paling dekat ke Naive; CatBoost di tengah; AdaBoost paling lemah dan paling sering signifikan lebih buruk. Selisih antar tiga model gradient boosting kecil.
   *Aman:* "AdaBoost konsisten paling lemah. Perbedaan XGBoost, LightGBM, dan CatBoost kecil dan peringkatnya berubah antar konfigurasi."
4. **Satu-satunya hasil signifikan:** LightGBM + TPE + loss L1 (MAE −0,723%, p = 0,033). Ini 1 dari 92 uji; dengan koreksi Bonferroni (α/92 ≈ 0,00054) tidak signifikan.
   *Aman:* "Satu konfigurasi (LightGBM dengan loss L1) lebih akurat dari Naive secara signifikan pada α = 0,05, tetapi hasil ini tidak bertahan setelah koreksi pengujian berganda."
5. **MAE vs RMSE berbeda arah.** 65 dari 92 run lebih baik dari Naive menurut RMSE (di horizon 1 menit hampir semua signifikan), tetapi hanya 37 menurut MAE dan 1 yang signifikan. Artinya model membantu mengurangi kesalahan besar, tetapi tidak menurunkan kesalahan rata-rata.
6. **Prediksi mendekati konstan.** 8 run menghasilkan prediksi return (hampir) konstan, yaitu model "memilih" untuk menebak hampir sama dengan Naive. Ini konsisten dengan pola harga jangka pendek yang sangat lemah.
7. **Split.** Hasil tidak stabil antar split: 80:20 rata-rata di bawah Naive, 70:30 di atas Naive, 60:40 hampir sama dengan Naive.

**Jangan ditulis:** "model X terbukti paling akurat untuk trader", "ML mengalahkan Naive", "horizon 1 menit optimal untuk scalper", atau kesimpulan umum tentang pasar BTC/IDR.

---

## 6. Batasan dan catatan penulisan

- **Data satu minggu.** Semua angka berlaku untuk 14–20 Oktober 2026 saja. Status data (satu minggu vs seluruh data sampai Februari 2027, ±40.000 baris) **belum dikonfirmasi ke dosen**. Mengulang Tahap 1–4 pada data lebih panjang diperkirakan ±5 jam.
- **Horizon 1 menit dan kegunaan bagi trader.** Rata-rata gerakan harga 1 menit (MAE Naive ±0,024% dari harga) kira-kira sama dengan median spread Indodax minggu itu (0,024%) dan lebih kecil dari rata-ratanya (0,043%). Keunggulan kurang dari 1% atas Naive belum cukup untuk menutup biaya spread. Tulis di keterbatasan, bukan sebagai alasan mengubah pilihan.
- **Sisa efek bid-ask.** Harga `typical` dipakai untuk mengurangi loncatan bid-ask (autokorelasi return 1 menit minggu itu: close −0,273, typical −0,073). Sisa efek ini mungkin ikut menjelaskan mengapa keunggulan hanya muncul di horizon 1 menit.
- **Pengujian berganda.** 92 uji pada data yang sama; tanpa efek apa pun, ±4–5 hasil p < 0,05 diharapkan muncul kebetulan.
- **Run berulang.** Konfigurasi TPE yang sama muncul di beberapa tahap (identik sampai digit terakhir). Itu bukti reproduksibilitas, bukan bukti tambahan.
- **Perbandingan metode optimasi terbatas.** Random, TPE, CMA-ES, dan GA memakai seed sama sehingga beberapa trial awal identik (pada AdaBoost hasil Random = TPE = GA). Grid hanya 27 kombinasi, metode lain 30 trial.
- **AdaBoost** tidak terpengaruh pengaturan loss dan early stopping.
- **Satu bursa, satu pasangan** (BTC/IDR Indodax), satu periode uji per split.

---

## 7. Deviasi dan perubahan kode

1. `run.py`: `--tag` dimasukkan ke `run_id` dan id baris Naive (27 Okt, sebelum Tahap 1). Sebelumnya run dengan tag berbeda ikut dilewati.
2. `btcpred/optim.py`: fallback ke parameter default bila semua trial Optuna gagal/dipangkas (tidak pernah aktif dalam eksperimen).
3. Tidak ada perubahan kode setelah Tahap 1 dimulai (`LOG_PERUBAHAN.md`: "belum ada").
4. Tahap 4: satu kegagalan perintah shell (variabel tak terkutip di zsh) tidak menghasilkan baris apa pun dan sudah dijalankan ulang.

---

## 8. Langkah berikutnya

1. **Bimbingan:** bawa tabel Bagian 4 dan temuan Bagian 5. Tanyakan (a) data satu minggu atau seluruh data sampai Februari, (b) apakah horizon 1 menit dapat diterima mengingat batasan spread, atau perlu dilaporkan juga horizon yang lebih relevan bagi trader sebagai eksploratif, (c) metrik utama tetap MAE atau RMSE ikut dibahas.
2. Bila data diperpanjang: jalankan ulang Tahap 1–4 dengan aturan yang sama dan tag baru.
3. Cari paper: CatBoost (Prokhorenkova dkk., 2018), AdaBoost.R2 (Drucker, 1997), Optuna/TPE, Heterogeneous Market Hypothesis (timeframe vs tipe trader), perbandingan boosting untuk harga kripto intraday. Verifikasi semua DOI.
4. Susun ulang Bab 1–3 sesuai desain ini.

---

## 9. Lingkungan dan cara menjalankan

- Folder: `/Users/ea/Documents/Prediksi BTC SKRIPSI/prediksi_btc`
- Python 3.14.8 (venv). Python 3.12 Homebrew rusak (`pyexpat`/libexpat), perbaikan: `brew reinstall python@3.12`.
- Paket utama: pandas 3.1, numpy 2.5, scikit-learn 1.9, xgboost 3.4, lightgbm 4.7, catboost 1.2.10, optuna 5.0, cmaes 0.13 (daftar lengkap: `hasil/metadata/versi_paket.txt`).
- Perangkat: Apple M5, 10 core, 16 GB RAM, macOS 26.2.
- Checksum data (SHA-256):
  - `btcidr_candle_1menit.csv` f1c9b82c1c29e0d594970a43dd8f73fe2ee803d74685732e98bff7cdfc70d8f6 (17.258 baris, 9–21 Okt 2026)
  - `btcidr_ticker_5menit.csv` 5aa8d449f1af3702783a73715da0e358cf9af82799bbe3d99efe66697d405298 (3.451 baris, 9–21 Okt 2026)

```bash
source .venv/bin/activate
caffeinate -i python run.py --optimizers tpe --splits 0.8 --tag tahap1
python run.py --datasets candle_1m --horizons 1 --splits 0.8 --optimizers default grid random tpe cmaes ga qmc --tag tahap2
python run.py --datasets candle_1m --horizons 1 --optimizers tpe --splits 0.8 0.7 0.6 --tag tahap3
python run.py --datasets candle_1m --horizons 1 --optimizers tpe --splits 0.8 --early-stop    --tag tahap4_earlystop
python run.py --datasets candle_1m --horizons 1 --optimizers tpe --splits 0.8 --top-k 15      --tag tahap4_topk15
python run.py --datasets candle_1m --horizons 1 --optimizers tpe --splits 0.8 --loss l1       --tag tahap4_lossl1
python run.py --datasets candle_1m --horizons 1 --optimizers tpe --splits 0.8 --pruner median --tag tahap4_prunermedian
python ringkas.py --tag tahap1      # dst. per tag
```

Cek kesehatan hasil (harus `109 1 17`):
```bash
python -c "
import pandas as pd; t=pd.read_csv('hasil/hasil_semua.csv'); m=t[t.model!='Naive']
print(len(t), ((m.MAE_vs_naive_pct<0)&(m.DM_MAE<0)&(m.p_MAE<0.05)).sum(), ((m.DM_MAE>0)&(m.p_MAE<0.05)).sum())"
```

---

## 10. Lampiran A: tabel lengkap per tahap

### A.1 Tahap 1
| Dataset | Horizon | Split | Model | Optimasi | MAE (Rp) | RMSE (Rp) | Akurasi arah (%) | MAE vs Naive (%) | RMSE vs Naive (%) | DM MAE | p MAE | p RMSE |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| candle_1m | 1 | 80:20 | **Naive** | — | 349.278 | 636.540 | — | 0 | 0 | — | — | — |
| candle_1m | 1 | 80:20 | AdaBoost | Bayesian (TPE) | 349.047 | 623.438 | 54,43 | -0,066 | -2,058 | -0,130 | 0,8966 | 0,0000 |
| candle_1m | 1 | 80:20 | CatBoost | Bayesian (TPE) | 348.066 | 622.845 | 56,82 | -0,347 | -2,151 | -0,850 | 0,3952 | 0,0000 |
| candle_1m | 1 | 80:20 | LightGBM | Bayesian (TPE) | 348.157 | 625.799 | 56,70 | -0,321 | -1,687 | -1,044 | 0,2964 | 0,0000 |
| candle_1m | 1 | 80:20 | XGBoost | Bayesian (TPE) | 348.262 | 618.940 | 57,48 | -0,291 | -2,765 | -0,546 | 0,5848 | 0,0000 |
| candle_1m | 5 | 80:20 | **Naive** | — | 764.151 | 1.356.121 | — | 0 | 0 | — | — | — |
| candle_1m | 5 | 80:20 | AdaBoost | Bayesian (TPE) | 772.473 | 1.359.292 | 50,66 | +1,089 ✗ | +0,234 | +2,147 | 0,0319 | 0,1928 |
| candle_1m | 5 | 80:20 | CatBoost | Bayesian (TPE) | 764.611 | 1.355.656 | 51,13 | +0,060 | -0,034 | +0,952 | 0,3410 | 0,5375 |
| candle_1m | 5 | 80:20 | LightGBM | Bayesian (TPE) | 764.858 | 1.356.212 | 50,66 | +0,093 ✗ | +0,007 | +3,490 | 0,0005 | 0,7084 |
| candle_1m | 5 | 80:20 | XGBoost | Bayesian (TPE) | 764.678 | 1.356.361 | 52,24 | +0,069 | +0,018 | +0,660 | 0,5092 | 0,8364 |
| candle_1m | 15 | 80:20 | **Naive** | — | 1.406.890 | 2.389.920 | — | 0 | 0 | — | — | — |
| candle_1m | 15 | 80:20 | AdaBoost | Bayesian (TPE) | 1.411.819 | 2.391.727 | 49,04 | +0,350 | +0,076 | +1,681 | 0,0929 | 0,6410 |
| candle_1m | 15 | 80:20 | CatBoost | Bayesian (TPE) | 1.409.464 | 2.389.233 | 48,78 | +0,183 | -0,029 | +1,171 | 0,2418 | 0,8734 |
| candle_1m | 15 | 80:20 | LightGBM | Bayesian (TPE) | 1.408.067 | 2.390.167 | 50,51 | +0,084 | +0,010 | +0,508 | 0,6118 | 0,9610 |
| candle_1m | 15 | 80:20 | XGBoost | Bayesian (TPE) | 1.408.759 | 2.390.834 | 49,04 | +0,133 | +0,038 | +1,392 | 0,1642 | 0,6842 |
| candle_1m | 30 | 80:20 | **Naive** | — | 2.019.749 | 3.399.424 | — | 0 | 0 | — | — | — |
| candle_1m | 30 | 80:20 | AdaBoost | Bayesian (TPE) | 2.028.617 | 3.407.769 | 49,37 | +0,439 | +0,245 | +0,820 | 0,4123 | 0,6510 |
| candle_1m | 30 | 80:20 | CatBoost | Bayesian (TPE) | 2.029.219 | 3.390.982 | 48,47 | +0,469 | -0,248 | +0,481 | 0,6305 | 0,8334 |
| candle_1m | 30 | 80:20 | LightGBM | Bayesian (TPE) | 2.020.945 | 3.400.423 | 49,02 | +0,059 | +0,029 | +0,759 | 0,4478 | 0,6839 |
| candle_1m | 30 | 80:20 | XGBoost | Bayesian (TPE) | 2.019.946 | 3.396.990 | 53,13 | +0,010 | -0,072 | +0,029 | 0,9772 | 0,8188 |
| candle_1m | 60 | 80:20 | **Naive** | — | 3.006.141 | 4.834.244 | — | 0 | 0 | — | — | — |
| candle_1m | 60 | 80:20 | AdaBoost | Bayesian (TPE) | 3.009.270 | 4.841.380 | 49,65 | +0,104 | +0,148 | +0,207 | 0,8360 | 0,6877 |
| candle_1m | 60 | 80:20 | CatBoost | Bayesian (TPE) | 3.018.493 | 4.870.407 | 44,14 | +0,411 | +0,748 | +0,742 | 0,4580 | 0,3883 |
| candle_1m | 60 | 80:20 | LightGBM | Bayesian (TPE) | 3.001.349 | 4.835.678 | 50,15 | -0,159 | +0,030 | -0,292 | 0,7700 | 0,9520 |
| candle_1m | 60 | 80:20 | XGBoost | Bayesian (TPE) | 3.012.358 | 4.848.611 | 47,25 | +0,207 | +0,297 | +0,234 | 0,8148 | 0,7673 |
| ticker_5m | 5 | 80:20 | **Naive** | — | 635.172 | 1.270.250 | — | 0 | 0 | — | — | — |
| ticker_5m | 5 | 80:20 | AdaBoost | Bayesian (TPE) | 638.607 | 1.265.698 | 51,83 | +0,541 ✗ | -0,358 | +2,578 | 0,0103 | 0,0564 |
| ticker_5m | 5 | 80:20 | CatBoost | Bayesian (TPE) | 641.795 | 1.263.277 | 52,11 | +1,043 ✗ | -0,549 | +3,009 | 0,0028 | 0,0221 |
| ticker_5m | 5 | 80:20 | LightGBM | Bayesian (TPE) | 637.497 | 1.267.941 | 49,86 | +0,366 ✗ | -0,182 | +3,241 | 0,0013 | 0,0082 |
| ticker_5m | 5 | 80:20 | XGBoost | Bayesian (TPE) | 636.191 | 1.269.149 | 52,68 | +0,160 ✗ | -0,087 | +2,611 | 0,0094 | 0,0387 |
| ticker_5m | 15 | 80:20 | **Naive** | — | 1.309.648 | 2.328.251 | — | 0 | 0 | — | — | — |
| ticker_5m | 15 | 80:20 | AdaBoost | Bayesian (TPE) | 1.343.102 | 2.385.663 | 49,23 | +2,554 | +2,466 | +1,337 | 0,1819 | 0,2145 |
| ticker_5m | 15 | 80:20 | CatBoost | Bayesian (TPE) | 1.320.016 | 2.342.865 | 51,28 | +0,792 | +0,628 | +1,422 | 0,1557 | 0,1585 |
| ticker_5m | 15 | 80:20 | LightGBM | Bayesian (TPE) | 1.311.375 | 2.329.055 | 46,94 | +0,132 | +0,035 | +1,693 | 0,0912 | 0,4697 |
| ticker_5m | 15 | 80:20 | XGBoost | Bayesian (TPE) | 1.313.167 | 2.330.877 | 45,41 | +0,269 | +0,113 | +1,966 | 0,0500 | 0,2309 |
| ticker_5m | 30 | 80:20 | **Naive** | — | 1.940.612 | 3.389.026 | — | 0 | 0 | — | — | — |
| ticker_5m | 30 | 80:20 | AdaBoost | Bayesian (TPE) | 1.949.283 | 3.409.246 | 49,75 | +0,447 | +0,597 | +0,902 | 0,3675 | 0,5001 |
| ticker_5m | 30 | 80:20 | CatBoost | Bayesian (TPE) | 1.941.960 | 3.393.938 | 48,74 | +0,069 | +0,145 | +0,709 | 0,4790 | 0,4896 |
| ticker_5m | 30 | 80:20 | LightGBM | Bayesian (TPE) | 1.941.556 | 3.390.532 | 51,01 | +0,049 | +0,044 | +0,870 | 0,3849 | 0,4736 |
| ticker_5m | 30 | 80:20 | XGBoost | Bayesian (TPE) | 1.941.262 | 3.389.729 | 48,74 | +0,034 | +0,021 | +0,490 | 0,6241 | 0,7033 |
| ticker_5m | 60 | 80:20 | **Naive** | — | 2.980.794 | 4.825.316 | — | 0 | 0 | — | — | — |
| ticker_5m | 60 | 80:20 | AdaBoost | Bayesian (TPE) | 2.990.733 | 4.849.904 | 48,38 | +0,333 | +0,510 | +0,527 | 0,5986 | 0,2279 |
| ticker_5m | 60 | 80:20 | CatBoost | Bayesian (TPE) | 2.981.290 | 4.829.706 | 51,62 | +0,017 | +0,091 | +0,149 | 0,8815 | 0,4701 |
| ticker_5m | 60 | 80:20 | LightGBM | Bayesian (TPE) | 2.981.272 | 4.825.899 | 47,88 | +0,016 | +0,012 | +0,281 | 0,7791 | 0,7571 |
| ticker_5m | 60 | 80:20 | XGBoost | Bayesian (TPE) | 2.983.097 | 4.829.723 | 48,38 | +0,077 | +0,091 | +0,716 | 0,4744 | 0,4798 |

### A.2 Tahap 2
| Dataset | Horizon | Split | Model | Optimasi | MAE (Rp) | RMSE (Rp) | Akurasi arah (%) | MAE vs Naive (%) | RMSE vs Naive (%) | DM MAE | p MAE | p RMSE |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| candle_1m | 1 | 80:20 | **Naive** | — | 349.278 | 636.540 | — | 0 | 0 | — | — | — |
| candle_1m | 1 | 80:20 | AdaBoost | CMA-ES | 351.849 | 631.538 | 53,23 | +0,736 ✗ | -0,786 | +3,754 | 0,0002 | 0,0000 |
| candle_1m | 1 | 80:20 | CatBoost | CMA-ES | 348.088 | 624.490 | 55,92 | -0,341 | -1,893 | -0,935 | 0,3499 | 0,0000 |
| candle_1m | 1 | 80:20 | LightGBM | CMA-ES | 349.445 | 634.710 | 56,52 | +0,048 | -0,288 | +0,893 | 0,3721 | 0,0000 |
| candle_1m | 1 | 80:20 | XGBoost | CMA-ES | 350.170 | 615.488 | 58,01 | +0,255 | -3,307 | +0,313 | 0,7544 | 0,0000 |
| candle_1m | 1 | 80:20 | AdaBoost | Default (tanpa tuning) | 398.893 | 653.471 | 51,85 | +14,205 ✗ | +2,660 | +13,533 | 0,0000 | 0,0000 |
| candle_1m | 1 | 80:20 | CatBoost | Default (tanpa tuning) | 387.051 | 631.596 | 55,80 | +10,815 ✗ | -0,777 | +7,386 | 0,0000 | 0,5130 |
| candle_1m | 1 | 80:20 | LightGBM | Default (tanpa tuning) | 372.283 | 621.637 | 57,06 | +6,586 ✗ | -2,341 | +4,733 | 0,0000 | 0,0662 |
| candle_1m | 1 | 80:20 | XGBoost | Default (tanpa tuning) | 364.264 | 625.121 | 56,46 | +4,291 ✗ | -1,794 | +3,817 | 0,0001 | 0,0758 |
| candle_1m | 1 | 80:20 | AdaBoost | Genetic Algorithm | 349.047 | 623.438 | 54,43 | -0,066 | -2,058 | -0,130 | 0,8966 | 0,0000 |
| candle_1m | 1 | 80:20 | CatBoost | Genetic Algorithm | 348.489 | 627.695 | 55,38 | -0,226 | -1,390 | -0,891 | 0,3733 | 0,0000 |
| candle_1m | 1 | 80:20 | LightGBM | Genetic Algorithm | 349.348 | 633.926 | 55,80 | +0,020 | -0,411 | +0,249 | 0,8037 | 0,0000 |
| candle_1m | 1 | 80:20 | XGBoost | Genetic Algorithm | 348.788 | 622.190 | 57,72 | -0,140 | -2,254 | -0,334 | 0,7382 | 0,0000 |
| candle_1m | 1 | 80:20 | AdaBoost | Grid Search | 350.746 | 632.446 | 53,41 | +0,420 ✗ | -0,643 | +2,751 | 0,0060 | 0,0000 |
| candle_1m | 1 | 80:20 | CatBoost | Grid Search | 348.228 | 625.438 | 56,40 | -0,301 | -1,744 | -0,950 | 0,3422 | 0,0000 |
| candle_1m | 1 | 80:20 | LightGBM | Grid Search | 349.137 | 634.318 | 55,20 | -0,041 | -0,349 | -0,657 | 0,5115 | 0,0000 |
| candle_1m | 1 | 80:20 | XGBoost | Grid Search | 349.486 | 635.509 | 55,32 | +0,059 | -0,162 | +1,894 | 0,0583 | 0,0000 |
| candle_1m | 1 | 80:20 | AdaBoost | Quasi-Monte Carlo | 350.857 | 635.663 | 53,41 | +0,452 ✗ | -0,138 | +7,706 | 0,0000 | 0,0009 |
| candle_1m | 1 | 80:20 | CatBoost | Quasi-Monte Carlo | 348.476 | 627.140 | 58,31 | -0,230 | -1,477 | -0,906 | 0,3649 | 0,0000 |
| candle_1m | 1 | 80:20 | LightGBM | Quasi-Monte Carlo | 348.041 | 624.770 | 56,28 | -0,354 | -1,849 | -1,005 | 0,3148 | 0,0000 |
| candle_1m | 1 | 80:20 | XGBoost | Quasi-Monte Carlo | 348.029 | 628.544 | 57,24 | -0,358 | -1,256 | -1,726 | 0,0845 | 0,0000 |
| candle_1m | 1 | 80:20 | AdaBoost | Random Search | 349.047 | 623.438 | 54,43 | -0,066 | -2,058 | -0,130 | 0,8966 | 0,0000 |
| candle_1m | 1 | 80:20 | CatBoost | Random Search | 348.489 | 627.695 | 55,38 | -0,226 | -1,390 | -0,891 | 0,3733 | 0,0000 |
| candle_1m | 1 | 80:20 | LightGBM | Random Search | 347.570 | 618.852 | 57,12 | -0,489 | -2,779 | -0,859 | 0,3902 | 0,0000 |
| candle_1m | 1 | 80:20 | XGBoost | Random Search | 349.520 | 617.572 | 56,16 | +0,069 | -2,980 | +0,102 | 0,9190 | 0,0000 |
| candle_1m | 1 | 80:20 | AdaBoost | Bayesian (TPE) | 349.047 | 623.438 | 54,43 | -0,066 | -2,058 | -0,130 | 0,8966 | 0,0000 |
| candle_1m | 1 | 80:20 | CatBoost | Bayesian (TPE) | 348.066 | 622.845 | 56,82 | -0,347 | -2,151 | -0,850 | 0,3952 | 0,0000 |
| candle_1m | 1 | 80:20 | LightGBM | Bayesian (TPE) | 348.157 | 625.799 | 56,70 | -0,321 | -1,687 | -1,044 | 0,2964 | 0,0000 |
| candle_1m | 1 | 80:20 | XGBoost | Bayesian (TPE) | 348.262 | 618.940 | 57,48 | -0,291 | -2,765 | -0,546 | 0,5848 | 0,0000 |

### A.3 Tahap 3
| Dataset | Horizon | Split | Model | Optimasi | MAE (Rp) | RMSE (Rp) | Akurasi arah (%) | MAE vs Naive (%) | RMSE vs Naive (%) | DM MAE | p MAE | p RMSE |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| candle_1m | 1 | 60:40 | **Naive** | — | 304.163 | 562.309 | — | 0 | 0 | — | — | — |
| candle_1m | 1 | 60:40 | AdaBoost | Bayesian (TPE) | 304.665 | 561.831 | 51,95 | +0,165 ✗ | -0,085 | +6,928 | 0,0000 | 0,0000 |
| candle_1m | 1 | 60:40 | CatBoost | Bayesian (TPE) | 303.699 | 553.402 | 56,25 | -0,153 | -1,584 | -0,811 | 0,4174 | 0,0000 |
| candle_1m | 1 | 60:40 | LightGBM | Bayesian (TPE) | 304.553 | 558.439 | 55,04 | +0,128 | -0,688 | +1,406 | 0,1599 | 0,0000 |
| candle_1m | 1 | 60:40 | XGBoost | Bayesian (TPE) | 303.630 | 546.134 | 56,90 | -0,175 | -2,877 | -0,458 | 0,6466 | 0,0000 |
| candle_1m | 1 | 70:30 | **Naive** | — | 317.826 | 588.901 | — | 0 | 0 | — | — | — |
| candle_1m | 1 | 70:30 | AdaBoost | Bayesian (TPE) | 318.591 | 575.770 | 54,16 | +0,241 | -2,230 | +0,356 | 0,7218 | 0,0003 |
| candle_1m | 1 | 70:30 | CatBoost | Bayesian (TPE) | 318.485 | 575.104 | 54,40 | +0,207 | -2,343 | +0,473 | 0,6366 | 0,0000 |
| candle_1m | 1 | 70:30 | LightGBM | Bayesian (TPE) | 318.417 | 584.890 | 53,77 | +0,186 | -0,681 | +1,534 | 0,1251 | 0,0000 |
| candle_1m | 1 | 70:30 | XGBoost | Bayesian (TPE) | 318.478 | 573.215 | 56,17 | +0,205 | -2,664 | +0,435 | 0,6633 | 0,0000 |
| candle_1m | 1 | 80:20 | **Naive** | — | 349.278 | 636.540 | — | 0 | 0 | — | — | — |
| candle_1m | 1 | 80:20 | AdaBoost | Bayesian (TPE) | 349.047 | 623.438 | 54,43 | -0,066 | -2,058 | -0,130 | 0,8966 | 0,0000 |
| candle_1m | 1 | 80:20 | CatBoost | Bayesian (TPE) | 348.066 | 622.845 | 56,82 | -0,347 | -2,151 | -0,850 | 0,3952 | 0,0000 |
| candle_1m | 1 | 80:20 | LightGBM | Bayesian (TPE) | 348.157 | 625.799 | 56,70 | -0,321 | -1,687 | -1,044 | 0,2964 | 0,0000 |
| candle_1m | 1 | 80:20 | XGBoost | Bayesian (TPE) | 348.262 | 618.940 | 57,48 | -0,291 | -2,765 | -0,546 | 0,5848 | 0,0000 |

### A.4 Tahap 4
**Early stopping**

| Dataset | Horizon | Split | Model | Optimasi | MAE (Rp) | RMSE (Rp) | Akurasi arah (%) | MAE vs Naive (%) | RMSE vs Naive (%) | DM MAE | p MAE | p RMSE |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| candle_1m | 1 | 80:20 | **Naive** | — | 349.278 | 636.540 | — | 0 | 0 | — | — | — |
| candle_1m | 1 | 80:20 | AdaBoost | Bayesian (TPE) | 349.047 | 623.438 | 54,43 | -0,066 | -2,058 | -0,130 | 0,8966 | 0,0000 |
| candle_1m | 1 | 80:20 | CatBoost | Bayesian (TPE) | 349.435 | 615.764 | 57,06 | +0,045 | -3,264 | +0,060 | 0,9525 | 0,0000 |
| candle_1m | 1 | 80:20 | LightGBM | Bayesian (TPE) | 349.492 | 636.547 | 49,52 | +0,061 ✗ | +0,001 | +11,090 | 0,0000 | 0,7403 |
| candle_1m | 1 | 80:20 | XGBoost | Bayesian (TPE) | 348.918 | 616.306 | 57,00 | -0,103 | -3,179 | -0,148 | 0,8827 | 0,0000 |

**Top-15 fitur**

| Dataset | Horizon | Split | Model | Optimasi | MAE (Rp) | RMSE (Rp) | Akurasi arah (%) | MAE vs Naive (%) | RMSE vs Naive (%) | DM MAE | p MAE | p RMSE |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| candle_1m | 1 | 80:20 | **Naive** | — | 349.278 | 636.540 | — | 0 | 0 | — | — | — |
| candle_1m | 1 | 80:20 | AdaBoost | Bayesian (TPE) | 350.082 | 636.008 | 53,83 | +0,230 ✗ | -0,084 | +6,510 | 0,0000 | 0,0013 |
| candle_1m | 1 | 80:20 | CatBoost | Bayesian (TPE) | 350.646 | 617.967 | 56,82 | +0,392 | -2,918 | +0,454 | 0,6498 | 0,0002 |
| candle_1m | 1 | 80:20 | LightGBM | Bayesian (TPE) | 348.538 | 626.476 | 57,00 | -0,212 | -1,581 | -0,586 | 0,5577 | 0,0000 |
| candle_1m | 1 | 80:20 | XGBoost | Bayesian (TPE) | 350.377 | 615.828 | 57,95 | +0,315 | -3,254 | +0,393 | 0,6942 | 0,0000 |

**Loss L1**

| Dataset | Horizon | Split | Model | Optimasi | MAE (Rp) | RMSE (Rp) | Akurasi arah (%) | MAE vs Naive (%) | RMSE vs Naive (%) | DM MAE | p MAE | p RMSE |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| candle_1m | 1 | 80:20 | **Naive** | — | 349.278 | 636.540 | — | 0 | 0 | — | — | — |
| candle_1m | 1 | 80:20 | AdaBoost | Bayesian (TPE) | 349.047 | 623.438 | 54,43 | -0,066 | -2,058 | -0,130 | 0,8966 | 0,0000 |
| candle_1m | 1 | 80:20 | CatBoost | Bayesian (TPE) | 347.665 | 627.691 | 57,12 | -0,462 | -1,390 | -1,541 | 0,1235 | 0,0000 |
| candle_1m | 1 | 80:20 | LightGBM | Bayesian (TPE) | 346.752 | 626.176 | 58,73 | -0,723 ✓ | -1,628 | -2,133 | 0,0331 | 0,0000 |
| candle_1m | 1 | 80:20 | XGBoost | Bayesian (TPE) | 350.090 | 636.565 | 49,52 | +0,232 ✗ | +0,004 | +13,867 | 0,0000 | 0,6904 |

**Pruner median**

| Dataset | Horizon | Split | Model | Optimasi | MAE (Rp) | RMSE (Rp) | Akurasi arah (%) | MAE vs Naive (%) | RMSE vs Naive (%) | DM MAE | p MAE | p RMSE |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| candle_1m | 1 | 80:20 | **Naive** | — | 349.278 | 636.540 | — | 0 | 0 | — | — | — |
| candle_1m | 1 | 80:20 | AdaBoost | Bayesian (TPE) | 349.047 | 623.438 | 54,43 | -0,066 | -2,058 | -0,130 | 0,8966 | 0,0000 |
| candle_1m | 1 | 80:20 | CatBoost | Bayesian (TPE) | 348.066 | 622.845 | 56,82 | -0,347 | -2,151 | -0,850 | 0,3952 | 0,0000 |
| candle_1m | 1 | 80:20 | LightGBM | Bayesian (TPE) | 348.857 | 629.179 | 54,90 | -0,121 | -1,156 | -0,576 | 0,5645 | 0,0000 |
| candle_1m | 1 | 80:20 | XGBoost | Bayesian (TPE) | 347.969 | 625.011 | 58,37 | -0,375 | -1,811 | -1,221 | 0,2222 | 0,0000 |

---

## 11. Lampiran B: source code final (`prediksi_btc`)

Hash SHA-256 kode yang dipakai (diambil dari salinan 28 Okt 2026, tidak berubah sejak Tahap 1):

```text
f8f47bf0285180b3688dd26dbb4a5fc8ef5404b6995052b4680288a4eee0ff11  config.py
f8b662e3788bcd287391b9dd087a0b74e1b47ddceaf8322b68b4da94feb92b87  run.py
5bc3c05b587757ae14e6ae34782d155fc7edb90d45caefc3a5e2828ba8a16ac7  ringkas.py
c0ab46f18aa40fda36f9673080c736be1b640a828c6fed9741a5f7a8c1669f86  btcpred/data.py
d9602204d678acebe7cff0e2e6468e5a85bd10a60e6f997708b2ba80b937a192  btcpred/models.py
03717e82130255fd7bb929cbb748a7e5e2454dd72c201f8dab5a7099abfa7eff  btcpred/optim.py
76c38e4ea54dbe0c5218b0722ef044bc632199f3b9e28e0534b765319f5e3a8b  btcpred/evaluate.py
```

Struktur:
```
prediksi_btc/
├── config.py            pengaturan percobaan
├── run.py               menjalankan semua kombinasi, mencatat ke hasil/hasil_semua.csv
├── ringkas.py           tabel perbandingan per tag
├── requirements.txt
└── btcpred/
    ├── data.py          baca CSV, definisi harga, fitur, target
    ├── models.py        4 model, ruang hyperparameter, grid
    ├── optim.py         metode optimasi (default, grid, random, tpe, cmaes, ga, qmc), pruner, early stopping
    └── evaluate.py      metrik, uji Diebold-Mariano, seleksi fitur
```

### `config.py`

```python
"""
KONFIGURASI PERCOBAAN
=====================
Ubah daftar di bawah untuk menentukan variasi percobaan. run.py akan menjalankan
SEMUA kombinasi (dataset x horizon x split x model x optimasi).
Semua daftar juga bisa ditimpa lewat argumen command line, contoh:
    python run.py --datasets candle_1m --horizons 5 15 --optimizers tpe random
Lihat DAFTAR_PERCOBAAN.md untuk penjelasan tiap pilihan.
"""

# ---------------------------------------------------------------------------
# 1. DATA
# ---------------------------------------------------------------------------
DATA = {
    # nama_dataset: path, jenis (candle/ticker), resolusi asli dalam menit
    "candle_1m": {"path": "data/btcidr_candle_1menit.csv", "jenis": "candle", "tf_menit": 1},
    "ticker_5m": {"path": "data/btcidr_ticker_5menit.csv", "jenis": "ticker", "tf_menit": 5},
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
DATASETS   = ["candle_1m", "ticker_5m"]

# Horizon prediksi dalam MENIT (berapa menit ke depan harga diprediksi).
# Horizon yang bukan kelipatan resolusi data otomatis dilewati
# (mis. horizon 1 menit tidak bisa untuk ticker_5m).
HORIZONS   = [1, 5, 15, 30, 60]

# Porsi data latih (sisanya data uji): 0.8 = 80:20, 0.7 = 70:30, 0.6 = 60:40
SPLITS     = [0.8, 0.7, 0.6]

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

### `btcpred/data.py`

```python
"""Memuat data Indodax dan membangun fitur + target untuk horizon tertentu."""
import numpy as np
import pandas as pd


def load(path, jenis, tf_menit, harga, start=None, end=None):
    """Baca CSV, rapikan timestamp ke grid TF, isi kolom 'harga'.
    Bar yang hilang dibiarkan NaN (tidak diisi), supaya fitur/target yang
    melewati gap otomatis terbuang."""
    df = pd.read_csv(path)
    df["waktu"] = pd.to_datetime(df["waktu_utc"]).dt.floor(f"{tf_menit}min")
    df = df.drop_duplicates("waktu").sort_values("waktu").set_index("waktu")

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
    n_gap = len(full) - len(df)
    df = df.reindex(full)
    if start or end:
        # ambil sedikit data sebelum START untuk pemanasan fitur (hanya data masa lalu)
        buf = pd.Timedelta(minutes=300)
        s = pd.Timestamp(start) - buf if start else None
        df = df.loc[s:end]
    return df, n_gap


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
Semua metode memakai fungsi objektif yang sama: rata-rata MAE return pada
walk-forward CV (TimeSeriesSplit) di data latih saja."""
import time
import warnings
import numpy as np
import optuna
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_absolute_error

from . import models as M

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


def cv_score(name, params, X, y, n_folds, gap, loss, seed, early_stop, trial=None):
    """Walk-forward CV. Return (MAE rata-rata, jumlah pohon terbaik rata-rata/None)."""
    tscv = TimeSeriesSplit(n_splits=n_folds, gap=gap)
    if name == "AdaBoost":
        # AdaBoost (scikit-learn) hanya memakai 1 core, jadi fold dijalankan paralel.
        from joblib import Parallel, delayed

        def one(tr, va):
            m = M.make(name, params, loss, seed)
            m.fit(X.iloc[tr], y.iloc[tr])
            return mean_absolute_error(y.iloc[va], m.predict(X.iloc[va]))
        errs = Parallel(n_jobs=-1)(delayed(one)(tr, va) for tr, va in tscv.split(X))
        if trial is not None:
            for i in range(len(errs)):
                trial.report(float(np.mean(errs[: i + 1])), i)
            if trial.should_prune():
                raise optuna.TrialPruned()
        return float(np.mean(errs)), None
    errs, best_n = [], []
    for i, (tr, va) in enumerate(tscv.split(X)):
        m = M.make(name, params, loss, seed, early_stop and name != "AdaBoost")
        bn = M.fit(name, m, X.iloc[tr], y.iloc[tr], X.iloc[va], y.iloc[va], early_stop)
        if bn is not None:
            best_n.append(bn)
        errs.append(mean_absolute_error(y.iloc[va], m.predict(X.iloc[va])))
        if trial is not None:
            trial.report(float(np.mean(errs)), i)
            if trial.should_prune():
                raise optuna.TrialPruned()
    return float(np.mean(errs)), (int(np.mean(best_n)) if best_n else None)


def tune(name, X, y, method, cfg, gap):
    """Return dict: params final, cv_mae, n_trials, n_pruned, detik."""
    t0 = time.time()
    es = cfg["EARLY_STOP"]
    kw = dict(n_folds=cfg["N_FOLDS"], gap=gap, loss=cfg["LOSS"], seed=cfg["SEED"], early_stop=es)

    if method == "default":
        params = dict(M.DEFAULT[name])
        if es and name != "AdaBoost":
            params[M.N_TREES_KEY[name]] = M.ES_MAX_TREES
        cv, bn = cv_score(name, params, X, y, **kw)
        n_tr, n_pr = 1, 0
    else:
        best_n = {}

        def objective(t):
            p = M.grid_params(name, t, es) if method == "grid" else M.space(name, t, es)
            score, bn = cv_score(name, p, X, y, trial=t, **kw)
            best_n[t.number] = bn
            return score

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
        if not any(t.state == optuna.trial.TrialState.COMPLETE for t in study.trials):
            # semua trial gagal/dipangkas -> pakai setelan bawaan supaya run tidak batal
            params = dict(M.DEFAULT[name])
            if es and name != "AdaBoost":
                params[M.N_TREES_KEY[name]] = M.ES_MAX_TREES
            cv, bn = cv_score(name, params, X, y, **kw)
            return dict(params=params, cv_mae=cv, n_trials=len(study.trials),
                        n_pruned=sum(t.state == optuna.trial.TrialState.PRUNED
                                     for t in study.trials),
                        detik_tuning=time.time() - t0)
        bt = study.best_trial
        params = dict(bt.params)
        if name == "LightGBM":
            params["subsample_freq"] = 1
        if es and name != "AdaBoost":
            params[M.N_TREES_KEY[name]] = M.ES_MAX_TREES
        cv, bn = bt.value, best_n.get(bt.number)
        n_tr = len(study.trials)
        n_pr = sum(t.state == optuna.trial.TrialState.PRUNED for t in study.trials)

    # Early stopping: model final memakai rata-rata jumlah pohon terbaik dari CV
    if es and name != "AdaBoost" and bn is not None:
        params[M.N_TREES_KEY[name]] = max(1, bn)
    return dict(params=params, cv_mae=cv, n_trials=n_tr, n_pruned=n_pr,
                detik_tuning=time.time() - t0)
```

### `btcpred/evaluate.py`

```python
"""Metrik evaluasi, uji Diebold-Mariano, dan seleksi fitur."""
import numpy as np
import pandas as pd
from scipy import stats

from . import models as M


def metrics(h_true, h_pred, r_true, r_pred):
    e = h_true - h_pred
    gerak = r_true != 0          # bar tanpa perubahan harga tidak dihitung arahnya
    arah = (np.sign(r_pred[gerak]) == np.sign(r_true[gerak])).mean() * 100 if gerak.any() else np.nan
    return dict(MAE_Rp=float(np.abs(e).mean()),
                RMSE_Rp=float(np.sqrt((e ** 2).mean())),
                MAPE_pct=float((np.abs(e) / h_true).mean() * 100),
                Akurasi_arah_pct=float(arah))


def dm_test(e_model, e_naive, h, power=1):
    """Diebold-Mariano dengan koreksi Harvey-Leybourne-Newbold.
    power=1: loss absolut (MAE), power=2: loss kuadrat (RMSE).
    Autokovarians sampai lag h-1 karena target horizon h saling tumpang tindih.
    DM < 0 berarti model lebih akurat daripada Naive."""
    d = np.abs(e_model) ** power - np.abs(e_naive) ** power
    n = len(d)
    dc = d - d.mean()
    gamma0 = np.dot(dc, dc) / n
    var = gamma0
    for k in range(1, h):
        var += 2 * np.dot(dc[k:], dc[:-k]) / n
    if var <= 0:
        var = gamma0
    if var == 0:
        return np.nan, np.nan
    dm = d.mean() / np.sqrt(var / n)
    koreksi = np.sqrt(max((n + 1 - 2 * h + h * (h - 1) / n) / n, 1e-12))
    dm *= koreksi
    p = 2 * (1 - stats.t.cdf(abs(dm), df=n - 1))
    return float(dm), float(p)


def select_top_k(name, X, y, k, loss, seed):
    """Seleksi fitur: latih model bawaan di data latih, ambil K fitur dengan
    importance tertinggi. Hanya memakai data latih."""
    m = M.make(name, M.DEFAULT[name], loss, seed)
    m.fit(X, y)
    imp = pd.Series(m.feature_importances_, index=X.columns).sort_values(ascending=False)
    return list(imp.index[:k])
```

### `run.py`

```python
"""
Menjalankan semua kombinasi percobaan dari config.py (bisa ditimpa lewat argumen).

Contoh:
    python run.py                                   # semua kombinasi di config.py
    python run.py --datasets candle_1m --horizons 5 15 30 60 --optimizers tpe --splits 0.8
    python run.py --models CatBoost --optimizers default grid random tpe cmaes ga --trials 50
    python run.py --early-stop --top-k 15 --loss l1 --pruner median

Hasil setiap run langsung ditambahkan ke hasil/hasil_semua.csv.
Run yang sudah pernah selesai (konfigurasi sama persis, termasuk --tag) otomatis
dilewati, jadi script aman dihentikan lalu dijalankan lagi. Karena --tag ikut masuk
run_id, konfigurasi yang sama dengan tag berbeda tetap dicatat ulang (perlu supaya
tahap 2/3/4 tidak kehilangan baris yang kebetulan sudah dijalankan di tahap 1).
"""
import argparse
import itertools
import json
import time
import warnings
warnings.filterwarnings("ignore")
from pathlib import Path

import numpy as np
import pandas as pd

import config as C
from btcpred import data as D, models as M, optim as O, evaluate as E


def parse():
    a = argparse.ArgumentParser()
    a.add_argument("--datasets", nargs="+")
    a.add_argument("--horizons", nargs="+", type=int)
    a.add_argument("--splits", nargs="+", type=float)
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


def main():
    a = parse()
    cfg = dict(
        DATASETS=a.datasets or C.DATASETS, HORIZONS=a.horizons or C.HORIZONS,
        SPLITS=a.splits or C.SPLITS, MODELS=a.models or C.MODELS,
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
    fres = out / "hasil_semua.csv"
    done = set(pd.read_csv(fres)["run_id"]) if fres.exists() else set()

    total = (len(cfg["DATASETS"]) * len(cfg["HORIZONS"]) * len(cfg["SPLITS"])
             * len(cfg["MODELS"]) * len(cfg["OPTIMIZERS"]))
    print(f"Maksimum {total} run (kombinasi tidak valid dilewati). Hasil: {fres}")
    t_all, ke = time.time(), 0

    for ds in cfg["DATASETS"]:
        info = C.DATA[ds]
        jenis, tf = info["jenis"], info["tf_menit"]
        harga = cfg["HARGA"][jenis]
        raw, n_gap = D.load(info["path"], jenis, tf, harga, cfg["START"], cfg["END"])
        print(f"\n=== {ds} | harga={harga} | bar hilang di file: {n_gap}")

        for hz in cfg["HORIZONS"]:
            if hz % tf != 0:
                print(f"  lewati horizon {hz} menit (bukan kelipatan TF {tf} menit)")
                continue
            data, feats, hb = D.build(raw, jenis, tf, hz, C.N_LAG, C.WINDOWS_MNT, cfg["START"])
            n = len(data)

            for sp in cfg["SPLITS"]:
                cut = int(n * sp)
                train = data.iloc[: cut - hb]          # purge: buang hb baris terakhir
                test = data.iloc[cut:]                 # agar target latih tidak masuk periode uji
                ytr, yte = train["target"], test["target"]
                h_now, h_true = test["harga_now"].values, test["harga_next"].values
                naive = h_now.copy()
                e_naive = h_true - naive
                m_naive = E.metrics(h_true, naive, yte.values, np.zeros(len(yte)))
                split_lbl = f"{int(round(sp*100))}:{int(round((1-sp)*100))}"

                base = dict(dataset=ds, harga=harga, tf_data_menit=tf, horizon_menit=hz,
                            horizon_bar=hb, split=split_lbl, n_latih=len(train),
                            n_uji=len(test), latih_mulai=str(train.index.min()),
                            uji_mulai=str(test.index.min()), uji_akhir=str(test.index.max()),
                            loss=cfg["LOSS"], early_stop=cfg["EARLY_STOP"],
                            top_k=cfg["TOP_K"] or 0, pruner=cfg["PRUNER"] or "none",
                            n_trials_cfg=cfg["N_TRIALS"], n_folds=cfg["N_FOLDS"],
                            periode=f"{cfg['START']}..{cfg['END']}", tag=a.tag)

                # baris Naive (sekali per dataset x horizon x split)
                nid = f"{ds}|{harga}|h{hz}|{split_lbl}|Naive|{cfg['START']}|{cfg['END']}|{a.tag}"
                if nid not in done:
                    row = dict(run_id=nid, model="Naive", optimasi="-", **base, **m_naive,
                               MAE_vs_naive_pct=0.0, RMSE_vs_naive_pct=0.0)
                    row["Akurasi_arah_pct"] = np.nan
                    _append(fres, row)
                    done.add(nid)

                for model, opt in itertools.product(cfg["MODELS"], cfg["OPTIMIZERS"]):
                    ke += 1
                    rid = (f"{ds}|{harga}|h{hz}|{split_lbl}|{model}|{opt}|{cfg['LOSS']}|"
                           f"es{int(cfg['EARLY_STOP'])}|k{cfg['TOP_K'] or 0}|"
                           f"pr{cfg['PRUNER'] or 'none'}|t{cfg['N_TRIALS']}|f{cfg['N_FOLDS']}|"
                           f"{cfg['START']}|{cfg['END']}|{a.tag}")
                    if rid in done:
                        continue
                    t0 = time.time()
                    cols = feats
                    if cfg["TOP_K"]:
                        cols = E.select_top_k(model, train[feats], ytr, cfg["TOP_K"],
                                              cfg["LOSS"], cfg["SEED"])
                    Xtr, Xte = train[cols], test[cols]

                    tuned = O.tune(model, Xtr, ytr, opt, cfg, gap=hb)
                    mdl = M.make(model, tuned["params"], cfg["LOSS"], cfg["SEED"])
                    mdl.fit(Xtr, ytr)
                    r_pred = mdl.predict(Xte)
                    h_pred = h_now * np.exp(r_pred)
                    met = E.metrics(h_true, h_pred, yte.values, r_pred)
                    e_m = h_true - h_pred
                    dm1, p1 = E.dm_test(e_m, e_naive, hb, power=1)
                    dm2, p2 = E.dm_test(e_m, e_naive, hb, power=2)

                    row = dict(run_id=rid, model=model, optimasi=opt, **base, **met,
                               MAE_vs_naive_pct=(met["MAE_Rp"] / m_naive["MAE_Rp"] - 1) * 100,
                               RMSE_vs_naive_pct=(met["RMSE_Rp"] / m_naive["RMSE_Rp"] - 1) * 100,
                               DM_MAE=dm1, p_MAE=p1, DM_RMSE=dm2, p_RMSE=p2,
                               cv_mae_return=tuned["cv_mae"], n_trials=tuned["n_trials"],
                               n_pruned=tuned["n_pruned"], n_fitur=len(cols),
                               std_pred_return=float(np.std(r_pred)),
                               detik_tuning=tuned["detik_tuning"],
                               detik_total=time.time() - t0)
                    _append(fres, row)
                    done.add(rid)

                    safe = rid.replace("|", "__").replace(":", "-").replace(" ", "_")
                    json.dump(dict(params=tuned["params"], fitur=cols), open(
                        out / "params" / f"{safe}.json", "w"), indent=2, default=str)
                    if C.SIMPAN_PREDIKSI:
                        pd.DataFrame({"waktu_target": test.index + pd.Timedelta(minutes=hz),
                                      "harga_now": h_now, "harga_aktual": h_true,
                                      "prediksi": h_pred, "naive": naive}).to_csv(
                            out / "prediksi" / f"{safe}.csv", index=False)

                    print(f"  [{ke}] {ds} h{hz} {split_lbl} {model:8s} {opt:7s} | "
                          f"MAE Rp{met['MAE_Rp']:,.0f} ({row['MAE_vs_naive_pct']:+.2f}% vs Naive) "
                          f"| RMSE {row['RMSE_vs_naive_pct']:+.2f}% | arah {met['Akurasi_arah_pct']:.1f}% "
                          f"| {row['detik_total']:.0f}s", flush=True)

    print(f"\nSelesai dalam {(time.time()-t_all)/60:.1f} menit.")


KOLOM = ["run_id", "dataset", "harga", "tf_data_menit", "horizon_menit", "horizon_bar",
         "split", "model", "optimasi", "loss", "early_stop", "top_k", "pruner",
         "n_trials_cfg", "n_folds", "MAE_Rp", "RMSE_Rp", "MAPE_pct", "Akurasi_arah_pct",
         "MAE_vs_naive_pct", "RMSE_vs_naive_pct", "DM_MAE", "p_MAE", "DM_RMSE", "p_RMSE",
         "cv_mae_return", "n_trials", "n_pruned", "n_fitur", "std_pred_return",
         "detik_tuning", "detik_total", "n_latih", "n_uji", "latih_mulai", "uji_mulai",
         "uji_akhir", "periode", "tag"]


def _append(path, row):
    df = pd.DataFrame([{k: row.get(k, np.nan) for k in KOLOM}])
    df.to_csv(path, mode="a", header=not path.exists(), index=False)


if __name__ == "__main__":
    main()
```

### `ringkas.py`

```python
"""
Meringkas hasil/hasil_semua.csv menjadi tabel perbandingan.

Contoh:
    python ringkas.py                                  # semua tabel, semua run
    python ringkas.py --dataset candle_1m --split 80:20 --optimasi tpe
    python ringkas.py --tag tahap1

Tabel yang dibuat (juga disimpan ke hasil/ringkasan/):
  1. horizon_x_model   : MAE vs Naive (%) per horizon dan model  -> cari TF optimal
  2. optimasi_x_model  : MAE vs Naive (%) per metode optimasi dan model
  3. split_x_model     : MAE vs Naive (%) per rasio split dan model
  4. peringkat         : 15 konfigurasi terbaik
Angka negatif = lebih akurat dari Naive. Bintang (*) = DM signifikan p < 0,05.
"""
import argparse
from pathlib import Path
import pandas as pd

import config as C


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--dataset"); a.add_argument("--split"); a.add_argument("--optimasi")
    a.add_argument("--horizon", type=int); a.add_argument("--tag")
    a.add_argument("--metrik", default="MAE_vs_naive_pct",
                   choices=["MAE_vs_naive_pct", "RMSE_vs_naive_pct", "Akurasi_arah_pct"])
    a = a.parse_args()

    t = pd.read_csv(Path(C.OUT_DIR) / "hasil_semua.csv")
    t = t[t["model"] != "Naive"]
    for col, val in [("dataset", a.dataset), ("split", a.split), ("optimasi", a.optimasi),
                     ("horizon_menit", a.horizon), ("tag", a.tag)]:
        if val is not None:
            t = t[t[col] == val]
    if t.empty:
        print("Tidak ada run yang cocok dengan filter."); return

    out = Path(C.OUT_DIR) / "ringkasan"; out.mkdir(exist_ok=True)
    m = a.metrik
    pcol = "p_RMSE" if m == "RMSE_vs_naive_pct" else "p_MAE"
    pd.set_option("display.width", 200)

    def pivot(idx, nama):
        pv = t.pivot_table(index=idx, columns="model", values=m, aggfunc="mean")
        sig = t.pivot_table(index=idx, columns="model", values=pcol, aggfunc="max")
        print(f"\n=== {nama} ({m}, rata-rata bila ada beberapa run) ===")
        print(pv.round(3).to_string())
        if m != "Akurasi_arah_pct":
            print("  p-value DM terbesar per sel (signifikan bila < 0,05):")
            print(sig.round(3).to_string())
        pv.to_csv(out / f"{nama}.csv")

    pivot(["dataset", "horizon_menit"], "horizon_x_model")
    pivot("optimasi", "optimasi_x_model")
    pivot("split", "split_x_model")

    asc = m != "Akurasi_arah_pct"
    top = t.sort_values(m, ascending=asc).head(15)
    kol = ["dataset", "horizon_menit", "split", "model", "optimasi", "MAE_Rp",
           "MAE_vs_naive_pct", "RMSE_vs_naive_pct", "Akurasi_arah_pct", "p_MAE", "p_RMSE"]
    print("\n=== 15 konfigurasi terbaik ===")
    print(top[kol].round(3).to_string(index=False))
    top[kol].to_csv(out / "peringkat.csv", index=False)
    print(f"\nTabel disimpan di {out}/")


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
```
