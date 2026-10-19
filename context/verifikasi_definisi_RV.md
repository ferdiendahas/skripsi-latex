# Verifikasi Definisi "RV" di Paper yang Dikutip

> Diperiksa 18 Okt 2026 langsung dari teks PDF yang dikirim, dengan naskah repo `skripsi-latex` commit `3bf3e07` (18 Okt 2026 20.37).
> **"hlm."** = halaman cetak jurnal. **"hlm. PDF"** = urutan halaman berkas, dipakai untuk preprint dan working paper.
> File `.tex`, `.bib`, dan `kartu_paper.md` **tidak diubah**.

---

## 1. Tabel ringkas

| Key | Istilah di paper | Rumus definisi (salin) | Skala yang diramal | Skala loss | Lokasi | Kesimpulan |
|---|---|---|---|---|---|---|
| corsi2009 | *realized volatility* (judul dan teks). *Integrated volatility* = akar dari *integrated variance* | RV_t^(d) = √( Σ_{j=0}^{M−1} r²_{t−j·Δ} ) (pers. 3). Di data empiris memakai estimator *two scales* (Zhang dkk., 2005) dari data tik | Akar (volatilitas). Semua besaran return dan volatilitas **disetahunkan** ("intended to be annualized") | RMSE, MAE, R² Mincer–Zarnowitz. Skalanya tidak disebut terpisah | Pers. 2–3, hlm. 177; disetahunkan hlm. 178; data dan estimator hlm. 186; Tabel 4 hlm. 189 | **Volatilitas** (akar, disetahunkan) |
| andersen1998 | *volatility factor* σ²; *cumulative sum of squared intraday returns* | plim (Σ r²_{(m),t+j/m} − ∫σ² dτ) = 0. Proksi = jumlah kuadrat return intrahari | Varians harian (ramalan GARCH σ²). Return dalam **persen** ("scaled to reflect daily percentage returns") | R² regresi kuadrat return pada ramalan volatilitas (pers. 15) | Persen hlm. 888; proksi hlm. 897; Tabel 5 (m = 288, yaitu 5 menit) hlm. 900 | **Varians** (return dalam persen) |
| liu2015 | *standard realized variance (RV)* | RV_{t+1} = Σ_{j=1}^{n} r²_{t+j/n} (pers. 3) | Varians (QV dan *realized measure*) | QLIKE dan MSE pada θ = QV atau proksinya | Pers. 3 hlm. 294; definisi RV hlm. 295; QLIKE hlm. 297 | **Varians** |
| dudek2024 | *realized variance* (konsisten di seluruh paper) | r²_t = (ln(C_t/C_{t−1}))² (pers. 1); RV_{d,t} = Σ_{k=1}^{K} r²_{k,t} (pers. 2); rata-rata mingguan/bulanan (pers. 3–4) | Model dilatih pada **ln RV** (pers. 5, "to ensure positive forecasts"). Ramalan mingguan = jumlah tujuh ramalan harian | MSE dan MAE. Skala (level atau log) tidak disebut eksplisit | Pers. 1–2 hlm. 2; pers. 3–5 hlm. 3–4; catatan Tabel 1 ("sum of squared of 5-minute returns") hlm. 7; mingguan hlm. 8 | **Varians** |
| huang2024 | *realised volatility* (RV) | RV_{t,N} = Σ_{j=1}^{N} r²_{t,j} dari return log yang di-*pre-averaging* (pers. 3) | Level RV dalam **basis poin** sebagai input ("we employ the basis point of the RV as inputs"). Tabel 4 menyajikan RV **disetahunkan** (×144·365 dan ×365), **hanya untuk statistik deskriptif** | RMSE, MAE, MSLE pada y (pers. 6–8). Skala y tidak disebut terpisah | Pers. 3 dan basis poin hlm. 6; Tabel 4 hlm. 5; pers. 6–8 hlm. 8; HAR dengan "sum of squared returns" hlm. 10 | **Varians** (input dalam basis poin) |
| christensen2023 | *realized variance* | RV_t = Σ |Δ^n_{t−1,j} X|² (pers. 2), dari return log 5 menit (TAQ) | Level RV (HAR pers. 5; tujuan estimasi pers. 13 pada RV_{t+1}). LogHAR (pers. 6) hanya salah satu pembanding. Gambar pohon ditampilkan sebagai simpangan baku tahunan dalam persen, hanya untuk ilustrasi | MSE relatif terhadap HAR | Pers. 2 hlm. PDF 4; HAR hlm. PDF 4–5; data 5 menit hlm. PDF 13; ilustrasi Gambar hlm. PDF 8 (preprint) | **Varians** |
| feng2024ml | Judul *volatility*; teks menyebut RV_{t−1} "realized volatility" | RV_t = Σ_{i=1}^{M} r²_{t,i} (pers. 1), dengan r_{t,i} = **100 ×** (log P_{t,i} − log P_{t,i−1}) | Level RV (HAR-RV pers. 2). Return dalam **persen** | RMSE, R²_oos, Clark–West. Skala tidak disebut terpisah | Pers. 1–2 dan definisi return hlm. 3 | **Varians** (return dalam persen) |
| qiu2025 | RV; Gambar 1 *realized variance* | RV_t ≡ Σ_{j=1}^{S} r²_{t,j} (pers. 1) | Level RV (HAR pers. 2) | RMSFE | Pers. 1–2 hlm. 3; Gambar 1 hlm. 4 | **Varians** |
| dudek2025lgbm | Judul *volatility*; teks *daily realized variance* (Bitcoin RV) | RV_{d,t} = Σ_{k=1}^{K} r²_{k,t}, r_{k,t} = ln P_{k,t} − ln P_{k−1,t} (pers. 1), K = 288 untuk 5 menit | Target utama RV. Dataset menyediakan ln RV, dan model disebut umumnya bekerja pada target log | MSE, MAE, sMAPE, R². Skala tidak ditemukan eksplisit | Pers. 1 hlm. PDF 8; ln RV hlm. PDF 8–9 (preprint) | **Varians** |
| brauneis2026 | *realized volatility* (RV) | RV_t = Σ_{i=2}^{72} (log(P_{t_i}/P_{t_{i−1}}))² (pers. 1); data 5 menit, interval **6 jam** | Level RV 6 jam (HAR pers. 2) | MAE, RMSE, QLIKE. Rumus QLIKE **tidak ditemukan**. Tabel 2 menyatakan nilai deskriptif "in percent" | Pers. 1 hlm. 386; Tabel 2 dan pers. 2 hlm. 387; loss hlm. 394–395; Tabel 4 hlm. 398 | **Varians** (6 jam) |
| kilic2025 | Judul *realized volatility*; teks "daily realized variance, RV_t" | RV_t = Σ_{s=1}^{n} r²_s, r_s = log(P_s/P_{s−1}) (pers. 2); dibentuk penulis dari harga 5 menit S&P 500 dari Bloomberg | Level RV (ARFIMA dan HAR pers. 3–7). Transformasi log tidak ditemukan | MSPE (pers. 22) dan QLIKE (pers. 23). **QLIKE ditulis dengan exp(RV_t)/exp(RV̂_t) − (RV_t − RV̂_t) − 1**, bentuk yang lazim bila RV dalam log, padahal transformasi log tidak disebut | Pers. 2 hlm. PDF 9 (cetak 8); pers. 22–23 hlm. PDF 53 (WP) | **Varians** (catatan: rumus QLIKE tidak konsisten dengan definisi) |
| pyrlik2021 | *realized volatility* (RV) | **Tidak ada rumus.** Hanya definisi verbal di pendahuluan: RV "is defined as the sum of squared intraday stock returns" (dirujuk ke Andersen & Bollerslev, 1998). Di bagian data hanya tertulis "calculate daily, weekly and monthly stock realized volatility" dari data 5 menit FINAM | **ln RV** sebagai variabel dependen | RMSE pada **log-RV** | Definisi verbal hlm. PDF 4; data 5 menit hlm. PDF 13–14; log hlm. PDF 15; RMSE log-RV hlm. PDF 19 (WP) | **Tidak jelas** (lihat bagian 2) |
| chassot2026 | RV; teks "logarithmic RV estimator" | RV_t = **log**( Σ_{i=0}^{m−1} r²_{t−Δi} ) (pers. 1), Δ = 5 menit | **Log** dari Σr² (HAR pers. 2–3 pada besaran ini) | MSE, QLIKE, MCS. Skala tidak disebut eksplisit. *Realized utility* (pers. 7) memakai exp(RV) | Pers. 1 hlm. 333; pers. 7 hlm. 337 | **Varians** (dalam log; "RV" di paper = log Σr²) |
| feng2024window | RV | RV_t = Σ_{i=1}^{N} r²_{i,t} (pers. 1); data jadi RV 5 menit dari Oxford-Man Realized Library | Level RV (HAR-RV) | QLIKE (pers. 6) dan MSE pada RV | Pers. 1 hlm. 569; Oxford-Man dan loss hlm. 570 | **Varians** |

**Ringkasan:** 12 paper memakai skala varians (Σr²). Satu paper memakai volatilitas berupa akar yang disetahunkan (Corsi), dan satu paper tidak jelas (Pyrlik). Tiga hal kecil perlu dicatat walaupun kesimpulannya varians:
- Andersen dan Feng–Qi–Lucey memakai return dalam persen.
- Huang memakai basis poin sebagai input.
- Chassot mendefinisikan RV sebagai log dari Σr².

---

## 2. Usulan perbaikan kalimat

### corsi2009 — Volatilitas

**bab1 baris 40–42 (P3)**
- Lama: "Salah satu model untuk meramalkan RV merupakan \textit{Heterogeneous Autoregressive model of Realized Volatility} (HAR-RV), yang meramalkan RV hari berikutnya dari rata-rata RV harian, mingguan, dan bulanan."
- Usulan:
  ```latex
  Salah satu model untuk meramalkan volatilitas merupakan \textit{Heterogeneous
  Autoregressive model of Realized Volatility} (HAR-RV). Model ini meramalkan
  volatilitas hari berikutnya dari rata-rata volatilitas harian, mingguan, dan
  bulanan.
  ```
- Catatan: perbaikan ini opsional. Corsi menyebut model dapat ditulis analog untuk varians (hlm. 179), jadi kalimat lama tidak salah besar. Versi usulan lebih aman karena Corsi sendiri meramalkan akarnya.

**bab2 baris 224–226 (subbab RV)**
- Kalimat "Corsi mendefinisikan \textit{realized volatility} sebagai akar dari besaran tersebut" **sudah benar** (pers. 3, hlm. 177).
- Opsional, bila ingin lengkap: "...sebagai akar dari besaran tersebut dan menyajikannya dalam bentuk tahunan \cite{corsi2009}."

**bab2 baris 242–245 dan 264–266:** tidak perlu diubah. Kalimatnya membahas gagasan horizon dan lag 5/22 hari, bukan skala RV.

### pyrlik2021 — Tidak jelas

**Kenapa tidak jelas:**
- Paper tidak memuat rumus RV.
- Definisi "sum of squared intraday stock returns" hanya muncul di pendahuluan sebagai rujukan ke Andersen & Bollerslev, bukan sebagai prosedur penulis.
- Bagian data hanya menyebut "realized volatility" dari data 5 menit, tanpa keterangan diakarkan atau tidak.
- Model dan RMSE memakai log RV.

**bab2 baris 55**
- Lama: "Pada RV saham Rusia, Pyrlik, Elizarov, dan Leonova menemukan bahwa..."
- Usulan:
  ```latex
  Pada volatilitas saham Rusia, Pyrlik, Elizarov, dan Leonova menemukan bahwa
  ```

**bab1 baris 82–83 (P5)**
- Lama: "Pada RV saham, model berbasis pohon bahkan termasuk yang paling buruk di antara model ML \cite{kilic2025,pyrlik2021}."
- Usulan:
  ```latex
  Pada volatilitas saham, model berbasis pohon bahkan termasuk yang paling
  buruk di antara model ML \cite{kilic2025,pyrlik2021}.
  ```
- Kılıç memakai varians, jadi "RV" benar untuknya. Namun kalimat ini juga mengutip Pyrlik, sehingga istilah umum "volatilitas" lebih aman untuk keduanya.

**Tabel 2.1:** Pyrlik tidak ada di tabel, jadi tidak ada sel yang perlu diubah.

### Paper lain

Tidak perlu diubah. Kalimat "RV …" di naskah untuk paper berkesimpulan **Varians** sudah sesuai, termasuk sel kolom "Objek" Tabel 2.1 (baris 120, 123, 126, 130, 133, 143).

Satu catatan opsional untuk Chassot (Tabel 2.1 baris 143): RV di paper itu berupa log Σr². Sel "RV 1.445 saham AS, 2015--2023" tetap benar karena besaran dasarnya varians, jadi tidak perlu diubah.

---

## 3. Tambahan untuk kartu paper

Tempel di butir 3 (**Bentuk data & sumber**) masing-masing kartu:

- **A3 corsi2009:** `- **Definisi RV:** RV_t = √(Σ r²) (akar, *realized volatility*), semua besaran disetahunkan; data empiris memakai estimator *two scales* dari data tik, pers. 3 hlm. 177, hlm. 178 dan 186.`
- **A1 andersen1998:** `- **Definisi RV:** proksi = jumlah kuadrat return intrahari (Σr², varians), return dalam persen harian, hlm. 888 dan 897; Tabel 5 hlm. 900.`
- **A2 liu2015:** `- **Definisi RV:** RV = Σ r² (*realized variance*, varians), pers. 3 hlm. 294 dan hlm. 295.`
- **D3 dudek2024:** `- **Definisi RV:** RV_{d,t} = Σ r²_{k,t} dari return 5 menit (varians), model pada ln RV, pers. 1–2 hlm. 2, pers. 5 hlm. 3–4, catatan Tabel 1 hlm. 7.`
- **D2 huang2024:** `- **Definisi RV:** RV_{t,N} = Σ r²_{t,j} dari return *pre-averaging* (varians), input dalam basis poin; Tabel 4 disetahunkan hanya untuk deskripsi, pers. 3 hlm. 6, Tabel 4 hlm. 5.`
- **D1 christensen2023:** `- **Definisi RV:** RV_t = Σ |ΔX|² dari return log 5 menit TAQ (varians), model utama pada level RV, pers. 2 hlm. PDF 4, data hlm. PDF 13.`
- **D5 feng2024ml:** `- **Definisi RV:** RV_t = Σ r²_{t,i} dengan r = 100 × selisih log harga (varians, return dalam persen), pers. 1 hlm. 3.`
- **D7 qiu2025:** `- **Definisi RV:** RV_t = Σ r²_{t,j} (varians), pers. 1 hlm. 3; Gambar 1 hlm. 4.`
- **D8 dudek2025lgbm:** `- **Definisi RV:** RV_{d,t} = Σ r²_{k,t}, K = 288 untuk 5 menit (varians), model umumnya pada ln RV, pers. 1 hlm. PDF 8–9.`
- **D9 brauneis2026:** `- **Definisi RV:** RV_t = Σ_{i=2}^{72} (log P_{t_i}/P_{t_{i−1}})² dari harga 5 menit dalam interval 6 jam (varians); rumus QLIKE tidak ditulis, pers. 1 hlm. 386.`
- **D10 kilic2025:** `- **Definisi RV:** RV_t = Σ r²_s dari return log 5 menit S&P 500 yang dihitung penulis dari harga Bloomberg (varians); rumus QLIKE memakai exp(RV) walau transformasi log tidak disebut, pers. 2 hlm. PDF 9, pers. 23 hlm. PDF 53.`
  - **Koreksi kartu D10:** butir 3 sekarang menulis "data sudah berbentuk RV (Bloomberg)". Yang benar, penulis **membentuk** RV harian dari harga 5 menit yang diambil dari Bloomberg (hlm. PDF 9).
- **D11 pyrlik2021:** `- **Definisi RV:** tidak ada rumus; hanya definisi verbal "sum of squared intraday stock returns" di pendahuluan; model dan RMSE pada log RV dari data 5 menit FINAM, hlm. PDF 4, 13, 15, 19.`
- **D6 chassot2026:** `- **Definisi RV:** RV_t = log(Σ r²) dari return 5 menit (log varians), pers. 1 hlm. 333.`
- **F1 feng2024window:** `- **Definisi RV:** RV_t = Σ r²_{i,t} (varians), data jadi RV 5 menit Oxford-Man, pers. 1 hlm. 569, hlm. 570.`
