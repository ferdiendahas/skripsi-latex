# Brief Agen — Pembaruan Referensi Skripsi v3.0 (4 Nov 2026)

> Tujuan: memperbarui `bibliography/references.bib` supaya berisi semua referensi skripsi v3.0 (prediksi harga BTC/IDR dengan boosting), sesuai `context/kartu_paper_v3.md`.
> **Hanya file `.bib` dan laporan yang berubah.** Bab I–III tidak disentuh di brief ini.

## 0. Prasyarat dan larangan
1. File berikut harus ada di repo. Kalau ada yang belum, berhenti dan minta Ferdi menyalinnya:
   - `context/kartu_paper_v3.md` (sumber utama metadata)
   - `context/hasil_riset_v3.0.md`
2. Jalankan `git status`. Kalau ada perubahan yang belum di-commit di `bibliography/references.bib`, berhenti dan tanya Ferdi dulu.
3. **Jangan mengarang metadata.** DOI, volume, nomor, dan halaman hanya boleh berasal dari kartu, doi.org, atau Crossref. Kalau tidak ditemukan, kosongkan kolomnya dan beri komentar `% CEK: <apa yang kurang>`.
4. Jangan ubah isi `chapters/`, `context/kartu_paper_v3.md`, atau file lain di luar `.bib`.
5. **Jangan commit/push.**

## 1. Aturan umum entri
- Format biblatex (biber). Kolom wajib: `author` (nama lengkap seperti di kartu), `title`, `year`, dan `journaltitle` atau `booktitle`. Isi `volume`, `number`, `pages`, dan `doi` bila tersedia.
- **Key harus sama persis dengan kartu**, termasuk `barberdt`, `dudek2025lgbm`, `lightgbmfeatures`, dan `lightgbmtuning`. Supaya kartu dan `.bib` tetap sinkron.
- **Kutip versi terbit, bukan versi yang dibaca.** Contohnya B5 (versi ACM, bukan arXiv), C3 (*J. Financial Markets*, bukan WP 2012), C4 (*J. Finance*, bukan SSRN), E5 dan F3 (prosiding KDD, bukan arXiv), dan G2 (*JBES*, bukan WP NBER).
- **Preprint** (B6 `dudek2025lgbm`) memakai `@online` atau `@misc` dengan `eprint`/`eprinttype = {arxiv}`, dan diberi `% PREPRINT`.
- **Dokumentasi** (E6, E10, F7, F10) memakai `@online` dengan `url` berversi, `urldate`, dan `organization`. Versinya harus sama dengan paket di `requirements.txt` atau `.venv`. Kalau berbeda dengan versi di kartu, pakai versi yang terpasang dan laporkan.
- Judul berbahasa Inggris tetap dalam bahasa aslinya. Lindungi huruf kapital singkatan dengan kurung kurawal, misalnya `{XGBoost}`, `{LightGBM}`, `{CatBoost}`, `{AdaBoost}`, `{NSGA-II}`, dan `{Bitcoin}`.

## 2. Daftar entri yang harus ada

### 2.1 Prioritas 1 — dipakai di Latar Belakang (17 entri, urutan kemunculan)
| No | Kode | Key | Metadata dari kartu | Yang perlu dicek |
|---|---|---|---|---|
| 1 | D1 | `nakamoto2008` | White paper, 2008, https://bitcoin.org/bitcoin.pdf | `@online`, urldate 5 Okt 2026 |
| 2 | D2 | `do2026` | Kim-Oanh Do, Borsa Istanbul Review 26, 100869 | DOI |
| 3 | C1 | `muller1997` | Müller dkk., J. Empirical Finance 4, 213–239 | DOI, nomor |
| 4 | C2 | `dacorogna1995` | Dacorogna dkk., European J. Finance 1(4), 383–403, doi 10.1080/13518479500000026 | — |
| 5 | C6 | `liu2023` | Liu dkk., European J. Finance, doi 10.1080/1351847X.2023.2241883 | volume, nomor, halaman cetak |
| 6 | D4 | `yi2023` | Yi dkk., Scientific Reports 13, 4789 | DOI |
| 7 | B2 | `jaquart2021` | Jaquart dkk., J. Finance and Data Science 7, 45–66, doi 10.1016/j.jfds.2021.03.001 | — |
| 8 | B5 | `puoti2024` | Puoti dkk., AIMLSystems 2024, ACM, doi 10.1145/3703412.3703420 | judul dan halaman versi ACM |
| 9 | B1 | `bouteska2024` | Bouteska dkk., Int. Review of Financial Analysis 92, 103055, doi 10.1016/j.irfa.2023.103055 | — |
| 10 | A2 | `wei2023` | Wei dkk., J. Forecasting 42(4), 852–871, doi 10.1002/for.2922 | — |
| 11 | E7 | `grinsztajn2022` | Grinsztajn dkk., NeurIPS 35 (Datasets and Benchmarks) | halaman prosiding |
| 12 | A1 | `rodrigues2025` | Rodrigues & Machado, Information 16(4), 300, doi 10.3390/info16040300 | — |
| 13 | B7 | `nadarajah2025` | Nadarajah dkk., J. Risk and Financial Management 18(2), 52 | DOI |
| 14 | F1 | `bergstra2012` | Bergstra & Bengio, JMLR 13, 281–305 | — |
| 15 | F2 | `bergstra2011` | Bergstra dkk., NIPS 2011, 2546–2554 | nomor volume (24) |
| 16 | B3 | `akyildirim2023` | Akyildirim dkk., Annals of OR 330, 553–584, doi 10.1007/s10479-021-04205-x | — |
| 17 | G5 | `tashman2000` | Tashman, Int. J. Forecasting 16(4), 437–450 | DOI |

### 2.2 Prioritas 2 — untuk Bab II dan III
| Kode | Key | Metadata dari kartu | Yang perlu dicek |
|---|---|---|---|
| B4 | `akyildirim2021` | Annals of OR 297, 3–36, doi 10.1007/s10479-020-03575-y | — |
| B6 | `dudek2025lgbm` | arXiv:2511.20105 | `% PREPRINT` |
| B8 | `oprea2026` | Computational Economics, doi 10.1007/s10614-026-11338-3 | volume dan halaman bila sudah ada |
| C3 | `barberdt` | J. Financial Markets 18, 1–24, doi 10.1016/j.finmar.2013.05.006 | — |
| C4 | `kirilenko2017` | J. Finance 72(3), 967–998, doi 10.1111/jofi.12498 | **judul resmi** (halaman CFTC menulis judul berbeda) |
| C5 | `kakinaka2022` | Finance Research Letters 46, 102319, doi 10.1016/j.frl.2021.102319 | — |
| D3 | `mokni2024` | Financial Innovation 10, 39 | DOI |
| E1 | `friedman2001` | Annals of Statistics 29(5), 1189–1232 | DOI |
| E2 | `freund1997` | J. Computer and System Sciences 55, 119–139 | DOI, nomor |
| E3 | `prokhorenkova2018` | NeurIPS 31 | — |
| E4 | `ke2017` | NeurIPS 30 | sudah ada di `.bib` v2; cek ulang |
| E5 | `chen2016` | KDD 2016, 785–794 | DOI; sudah ada di `.bib` v2 |
| E6 | `lightgbmfeatures`, `lightgbmtuning` | Dokumentasi LightGBM | URL versi terpasang |
| E8 | `makridakis2022` | Int. J. Forecasting 38(4), 1346–1364 | DOI |
| E9 | `drucker1997` | ICML 1997, Morgan Kaufmann | **halaman prosiding** |
| E10 | `sklearnadaboost` | scikit-learn 1.9.1, AdaBoostRegressor | URL versi terpasang |
| F3 | `akiba2019` | KDD 2019, 2623–2631, doi 10.1145/3292500.3330701 | — |
| F4 | `hansen2001` | Evolutionary Computation 9(2), 159–195 | DOI |
| F5 | `deb2002` | IEEE Trans. Evolutionary Computation 6(2), 182–197 | DOI |
| F6 | `li2018` | JMLR 18, 1–52 | nomor artikel |
| F7 | `optunadocs` | Dokumentasi Optuna 5.0.0 | URL versi terpasang |
| F8 | `sobol1967` | Zh. Vychisl. Mat. Mat. Fiz. 7(4), 784–802 | kutip terbitan asli seperti di dokumentasi SciPy |
| F9 | `roy2023qmc` | JOSS 8(84), 5309, doi 10.21105/joss.05309 | — |
| F10 | `scipysobol` | SciPy v1.18.0, qmc.Sobol | URL versi terpasang |
| G1 | `harvey1997` | Int. J. Forecasting 13, 281–291 | DOI, nomor |
| G2 | `diebold1995` | J. Business & Economic Statistics 13(3), 253–263 | DOI |
| G3 | `holm1979` | Scandinavian J. Statistics 6(2), 65–70 | — |
| G4 | `cerqueira2020` | Machine Learning 109, 1997–2028 | DOI |
| H1 | `parkinson1980` | J. Business 53(1), 61–65 | DOI |

### 2.3 Tidak boleh ada di `.bib` aktif
`kharola2026`, `oyedele2023`, `qureshi2025`, `zhu2023`, `petukhina2021`, `gradojevic2023`, `karaa2024`, dan **`zhivkov2026` (kemungkinan referensi karangan)**.
- Kalau ada di `.bib` dan tidak dikutip di `chapters/`, hapus.
- Kalau masih dikutip, **jangan hapus**. Laporkan lokasinya.

## 3. Entri lama v2.9 (HAR-RV)
Bab I–III saat ini masih versi v2.9, jadi entri lamanya masih dikutip. **Jangan dihapus**, supaya `make` tidak gagal.
1. Pindahkan semua entri v2.9 yang tidak ada di Bagian 2 ke bagian bawah file, di bawah komentar:
   ```
   % ===== ARSIP v2.9 — hapus setelah Bab I–III v3.0 selesai ditulis =====
   ```
2. Entri yang key-nya ada di Bagian 2 (misalnya `ke2017`, `chen2016`, `diebold1995`, `holm1979`, `cerqueira2020`, `tashman2000`, `do2026`, `mokni2024`, `yi2023`) **dipertahankan di bagian aktif**. Metadatanya dicek ulang terhadap Bagian 2.

## 4. Urutan kerja
1. Cek prasyarat (Bagian 0).
2. Baca versi `lightgbm`, `scikit-learn`, `optuna`, dan `scipy` dari `requirements.txt` atau `.venv` (untuk entri dokumentasi).
3. Tulis atau perbarui entri Prioritas 1, lalu Prioritas 2.
4. Untuk setiap kolom "Yang perlu dicek", cari di doi.org atau Crossref (`https://api.crossref.org/works/<doi>` atau pencarian judul). **Buka setiap DOI** dan pastikan judul serta penulisnya cocok dengan kartu.
5. Rapikan sesuai Bagian 3.
6. Jalankan pemeriksaan di Bagian 5.

## 5. Pemeriksaan
1. Semua 47 key di Bagian 2.1–2.2 ada di `.bib` (17 + 30, termasuk dua key E6).
2. Tidak ada key duplikat (`biber --tool --validate-datamodel` atau `grep -c "^@"` per key).
3. Tidak ada key dari Bagian 2.3 di bagian aktif.
4. Setiap DOI di `.bib` sudah dibuka dan judulnya cocok. Kalau tidak cocok, beri `% CEK`.
5. Tidak ada kolom yang diisi dari tebakan. Kolom yang kosong harus diberi `% CEK`.
6. `make` lolos dan biber tidak melaporkan entri yang hilang. Kegagalan karena font Times New Roman/Arial boleh diabaikan.
7. `git diff --stat` hanya menunjukkan `bibliography/references.bib`.

## 6. Format laporan ke Ferdi
```
Prasyarat: lengkap / kurang <file>
Versi paket: lightgbm <v>, scikit-learn <v>, optuna <v>, scipy <v>
Entri aktif v3: <n>/47   Entri arsip v2.9: <n>
DOI dibuka dan cocok: <n>   Tidak cocok: <daftar>
Metadata baru ditemukan: <key: kolom = nilai (sumber)>
Sisa % CEK: <key: apa yang kurang>
Key terlarang (2.3): tidak ada / <key + lokasi \cite>
make / biber: <OK / temuan>
File berubah: <git diff --stat>
```
