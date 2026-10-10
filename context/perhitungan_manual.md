# Perhitungan Manual (ilustrasi Bab 3)

Window awal: target_date < 2018-09-01. Hari contoh **t\* = 2018-08-30**, diramal untuk **t\*+1 = 2018-08-31**. Data latih ilustrasi: 339 observasi (target 2017-09-16 s.d. 2018-08-30). Angka 6 digit bermakna. Config hash `0af5b5b98c60`.

Semua angka berasal dari window awal; tidak ada hasil out-of-sample.

## 1. Realized variance hari t*

Return bar pertama memakai close bar terakhir hari 2018-08-29 (C = 7031.22).

| Timestamp (UTC) | Close | r = ln(C_i/C_{i-1}) | r² | r < 0 |
|---|---|---|---|---|
| 2018-08-30 00:00 | 7038.22 | 0.000995065 | 9.90153e-07 | tidak |
| 2018-08-30 00:05 | 7036.24 | -0.000281361 | 7.91638e-08 | ya |
| 2018-08-30 00:10 | 7031.41 | -0.000686682 | 4.71532e-07 | ya |
| 2018-08-30 00:15 | 7039.17 | 0.00110301 | 1.21663e-06 | tidak |
| 2018-08-30 00:20 | 7039.01 | -2.27302e-05 | 5.16662e-10 | ya |

- Jumlah bar: 288
- RV_t\* = Σr² = 0.000537199
- RS⁻ = Σr²·1(r<0) = 0.000267476 (154 bar negatif)
- Proporsi RS⁻/RV = 0.497908

## 2. Komponen HAR

RV 7 hari untuk rata-rata mingguan:

| Tanggal | RV |
|---|---|
| 2018-08-24 | 0.000628396 |
| 2018-08-25 | 0.000350138 |
| 2018-08-26 | 0.000482313 |
| 2018-08-27 | 0.000499351 |
| 2018-08-28 | 0.000454143 |
| 2018-08-29 | 0.000440669 |
| 2018-08-30 | 0.000537199 |

- Rata-rata mingguan = 0.000484601
- Rata-rata bulanan (30 nilai, 2018-08-01 s.d. 2018-08-30): min 0.000350138, maks 0.0038063, rata-rata 0.00127306
- ln RV_d = ln(0.000537199) = -7.52914
- ln RV_w = ln(0.000484601) = -7.63218
- ln RV_m = ln(0.00127306) = -6.66633

## 3. Fitur X hari t*

| Fitur | Input mentah | Hasil |
|---|---|---|
| ret | close t\* = 6984.84, close t\*−1 = 7031.22 | ln(6984.84/7031.22) = -0.00661815 |
| ln_dvol | volume dolar t\* = 3.09357e+08 | 19.55 |
| d_ln_dvol | volume dolar t\*−1 = 3.04565e+08 | 19.55 − 19.5344 = 0.0156107 |
| ln_parkinson | H = 7063.63, L = 6784.81 | ln[(ln H − ln L)²/(4 ln 2)] = -7.44394 |
| ln_amihud | 10⁶ × rata-rata \|r\|/quote volume (288 bar) = 0.00116494 | -6.75508 |
| neg_share | lihat Bagian 1 | 0.497908 |

HAR-X tidak memakai ln_amihud; LGBM-X memakai kesembilan fitur.

## 4. HAR (OLS)

| Koefisien | Nilai |
|---|---|
| β0 | -0.56989 |
| βd | 0.478542 |
| βw | 0.0689003 |
| βm | 0.384379 |

ŷ = (-0.56989)(1) + (0.478542)(-7.52914) + (0.0689003)(-7.63218) + (0.384379)(-6.66633)
  = (-0.56989) + (-3.60301) + (-0.525859) + (-2.5624) = **-7.26116**

- σ̂² (fit di 271 observasi awal, residual 68 observasi akhir, ddof 1) = 0.497938
- exp(ŷ + σ̂²/2) = exp(-7.26116 + 0.248969) = 0.000900836
- Batas bawah (persentil ke-1 rv_next data latih) = 0.000290955
- **F_HAR = maks(0.000900836, 0.000290955) = 0.000900836**

## 5. LGBM-HAR

Hyperparameter (`params_main.json`): num_leaves = 3, min_child_samples = 10, n_estimators = 300, learning_rate = 0.03, reg_lambda = 1.0.

Init score (boost_from_average) = rata-rata ln RV_t+1 data latih = -6.03756; LightGBM meleburkannya ke nilai daun pohon ke-1, sehingga ŷ = jumlah nilai daun seluruh pohon.

Catatan: n daun dijumlah < 339 karena subsample 0,8 (bagging) — tiap pohon dilatih pada sampel acak 80% data latih (seed tetap, deterministik).

### Pohon ke-1

- jika ln_rv_m <= -5.80353:
  - daun 0: nilai -6.06517 (n = 108)
- jika ln_rv_m > -5.80353:
  - jika ln_rv_d <= -5.05151:
    - daun 1: nilai -6.02747 (n = 101)
  - jika ln_rv_d > -5.05151:
    - daun 2: nilai -5.99638 (n = 47)

Lintasan hari t\*: ln_rv_m = -6.66633 <= -5.80353 → daun 0 (nilai -6.06517)

### Pohon ke-2

- jika ln_rv_m <= -5.80353:
  - daun 0: nilai -0.0260821 (n = 111)
- jika ln_rv_m > -5.80353:
  - jika ln_rv_d <= -4.88302:
    - daun 1: nilai 0.00821454 (n = 126)
  - jika ln_rv_d > -4.88302:
    - daun 2: nilai 0.0432716 (n = 35)

Lintasan hari t\*: ln_rv_m = -6.66633 <= -5.80353 → daun 0 (nilai -0.0260821)

- Pohon ke-1: -6.06517 (≈ init -6.03756 + -0.0276166)
- Pohon ke-2: -0.0260821
- Pohon ke-3 s.d. ke-300: jumlah -1.22919
- ŷ = Σ nilai daun 300 pohon = **-7.32044**
- σ̂² (holdout 20%) = 0.511547
- exp(ŷ + σ̂²/2) = exp(-7.32044 + 0.255773) = 0.000854778
- Batas bawah = 0.000290955
- **F_LGBM = maks(0.000854778, 0.000290955) = 0.000854778**

## 6. Evaluasi hari t*+1

RV aktual 2018-08-31 = 0.00041419

| Model | Ramalan F | RV/F | QLIKE = RV/F − ln(RV/F) − 1 | MSE = (RV − F)² |
|---|---|---|---|---|
| HAR | 0.000900836 | 0.459784 | 0.236783 | 2.36825e-07 |
| LGBM-HAR | 0.000854778 | 0.484558 | 0.209076 | 1.94118e-07 |

**ΔL = QLIKE(LGBM-HAR) − QLIKE(HAR) = 0.209076 − 0.236783 = -0.0277067** (negatif: LGBM unggul pada hari ini; satu hari, bukan kesimpulan).

## Verifikasi

Semua 25 pemeriksaan lolos (toleransi relatif 1e-9; β dan σ̂² HAR 1e-8 karena persamaan normal vs lstsq).

| Pemeriksaan | Selisih maks |
|---|---|
| r bar pertama memakai close hari t*-1 | 1.58e-15 |
| RV_t* = Σr² vs daily.csv | 9.53e-17 |
| RS⁻_t* vs daily.csv | 9.88e-17 |
| RS⁻/RV vs design (neg_share) | 9.56e-14 |
| ln_rv_d vs design | 0.00e+00 |
| ln_rv_w vs design | 8.88e-16 |
| ln_rv_m vs design | 0.00e+00 |
| close t* = close bar terakhir | 0.00e+00 |
| volume dolar = Σ quote volume | 0.00e+00 |
| H = maks high bar | 0.00e+00 |
| L = min low bar | 0.00e+00 |
| ret vs design | 5.52e-16 |
| ln_dvol vs design | 0.00e+00 |
| d_ln_dvol vs design | 0.00e+00 |
| ln_parkinson vs design | 0.00e+00 |
| ln_amihud vs design | 1.78e-15 |
| β OLS (persamaan normal) vs rvlib | 6.18e-14 |
| ŷ_HAR = β·x vs predict | 4.80e-14 |
| σ̂² HAR (holdout 20%) vs fit_bias_corrected | 5.55e-16 |
| daun traversal manual = pred_leaf (300 pohon) | 0.00e+00 |
| ŷ_LGBM = Σ nilai daun vs predict | 3.55e-15 |
| σ̂² LGBM (holdout 20%) vs fit_bias_corrected | 0.00e+00 |
| RV_t*+1 vs daily.csv | 0.00e+00 |
| QLIKE HAR vs rvlib.qlike | 0.00e+00 |
| QLIKE LGBM vs rvlib.qlike | 0.00e+00 |
