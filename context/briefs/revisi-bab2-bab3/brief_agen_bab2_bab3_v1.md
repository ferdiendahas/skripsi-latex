# Brief Agen — Revisi Bab II dan III v1 (17 Okt 2026)

> Tujuan: menyelaraskan narasi Bab II–III dengan Bab I v4 dan `context/kartu_paper.md`, serta merapikan gambar TikZ.
> Revisinya **sudah disiapkan** dalam bentuk patch dan sudah lolos compile (53 halaman, tidak ada rujukan menggantung). Tugas agen hanya **menerapkan, memeriksa, dan melapor**. Jangan menulis ulang narasi sendiri.

## 0. Berkas dari Ferdi
Ferdi meletakkan berkas berikut di `context/briefs/revisi-bab2-bab3/`:
- `revisi-bab2-bab3.patch` — diff terhadap commit `fdc96e2`.
- `bab2-tinjauan-pustaka.tex`, `bab3-metodologi.tex`, `references.bib` — versi utuh hasil revisi (cadangan bila patch gagal).
- `praskripsi-preview.pdf` — tampilan acuan.

Ferdi juga menyalin `kartu_paper.md` dari Project ke `context/kartu_paper.md`.

## 1. Tugas (urut)
1. **Cek prasyarat:**
   - `context/kartu_paper.md` ada. Kalau belum ada, berhenti dan minta Ferdi menyalinnya.
   - Jalankan `git status`. Kalau ada perubahan yang belum di-commit di `chapters/bab2-*`, `chapters/bab3-*`, atau `references.bib`, berhenti dan tanya Ferdi dulu.
2. **Terapkan patch:**
   ```bash
   git apply --check context/briefs/revisi-bab2-bab3/revisi-bab2-bab3.patch
   git apply --3way context/briefs/revisi-bab2-bab3/revisi-bab2-bab3.patch
   ```
   - Kalau ada konflik karena file sudah berubah sejak `fdc96e2`, **jangan menyelesaikan konflik dengan menebak**. Laporkan bagian yang konflik ke Ferdi.
   - Kalau HEAD masih `fdc96e2` dan patch gagal karena alasan teknis (misalnya *line ending*), salin tiga file versi utuh ke `chapters/` dan `bibliography/`.
3. **Jangan ubah** isi Rumusan Masalah, hipotesis H1–H3, uji konfirmatori, judul, dan Bab I.
4. Jalankan pemeriksaan di Bagian 3, lalu `make` dan `make check`.
5. **Jangan commit/push.** Laporkan ke Ferdi dengan format di Bagian 4.

## 2. Isi revisi (untuk konteks saja, sudah ada di patch)
**Bab II**
- **Penelitian Terdahulu** ditulis ulang menjadi lima kelompok. Ada kelompok baru "Model berbasis pohon dan HAR" (`dudek2025lgbm`, `brauneis2026`, `kilic2025`, `pyrlik2021`).
- **Tabel posisi:** baris Feng–Qi–Lucey dan Chassot diperbaiki, baris Brauneis dan Kılıç ditambahkan. Kolom "Penelitian ini" sekarang menyebut Fluctuation test sebagai eksploratori.
- **Klaim yang dikoreksi sesuai kartu:**
  - Do: angka persistensi dan klaim Granger dihapus.
  - Yi: temuannya efisiensi stabil antartahun, bukan berubah-ubah.
  - Huang: perbandingan dengan CNN-LSTM, horizon 1 hari, hanya grafik.
  - Corsi: salah kutip diganti kalimat v2.9 A.2 no. 13.
  - Grinsztajn: "menengah", data i.i.d.
  - Wang: ML vs GARCH.
  - Cerqueira: *prequential in blocks*.
- **Alasan memilih LightGBM** disamakan dengan Bab I. Klaim *leaf-wise* sekarang dikutip ke `lightgbmfeatures`/`lightgbmtuning`, bukan ke `ke2017`.
- **H3:** dasar "perubahan persistensi RV" diganti "perubahan karakteristik pasar". Hipotesisnya sendiri tidak berubah. `pesaran2007` ditambahkan ke dasar H3 dan hipotesis tandingan.
- **`\sumber{}`** ditambahkan pada semua tabel dan gambar Bab II.

**Bab III**
- **Gambar 3.1 (alur penelitian)** dibuat satu kolom lurus tanpa silangan, dengan nomor langkah (1)–(7) yang sama dengan narasi.
- **Tuning:** istilahnya "validasi berurutan waktu (*forward-chaining*)", dan `cerqueira2020` hanya dikutip untuk "validasi silang acak memutus urutan waktu".
- **Sitasi Christensen** untuk koreksi bias dan batas bawah ramalan dicabut dan diganti `% CEK`, karena belum tercatat di kartu.
- **Gambar 3.3:** label ya/tidak ditambahkan pada pemecahan kedua.

**Gambar TikZ lain:** 2.1 HAR digambar ulang, 2.2 *leaf-wise* dirapatkan, 2.3 strategi dibuat hitam-putih, 2.4 kerangka tanpa silangan.

**`references.bib`:** entri `pesaran2007` ditambahkan, dengan `% CEK` untuk DOI.

## 3. Pemeriksaan
1. Semua key `\cite` di Bab I–III ada di `references.bib`, dan biber tidak melaporkan entri yang hilang.
2. Bab II dan III tidak memuat kata "GOSS" atau "EFB" sebagai alasan memilih LightGBM. Penyebutan di subbab LightGBM (definisi) dan Bab III (alasan tidak dipakai) boleh.
3. Tidak ada `\cite{christensen2023}` di Subbab Aturan Teknis Peramalan Bab III.
4. Tidak ada angka 0,697, 0,833, atau 0,723 di Bab II.
5. Tidak ada `forward-chaining` yang langsung disertai `\cite{cerqueira2020}` dalam satu klausa.
6. Tidak ada angka hasil *out-of-sample* di Bab I–III.
7. `% CEK` baru yang harus tetap ada:
   - Bab II, subbab fungsi *loss*: Patton, ramalan optimal = nilai harapan kondisional.
   - Bab II, sebelum tabel istilah: Gama, *virtual/real concept drift*.
   - Bab III, aturan teknis: dua `% CEK` Christensen.
   - `references.bib`: DOI `pesaran2007`.
8. Tampilan Gambar 2.1–2.4, 3.1, dan 3.3 di PDF sama dengan `praskripsi-preview.pdf`: tidak ada label yang menumpuk dan tidak ada panah yang bersilangan.
9. `make check`: kegagalan karena font Times New Roman/Arial di mesin tanpa font tersebut boleh diabaikan. Selain itu, tidak boleh ada *overfull box* di atas 3pt.

## 4. Format laporan ke Ferdi
```
Patch: berhasil / konflik di <file:baris>
Halaman: <n>
Overfull > 3pt: <daftar atau "tidak ada">
Rujukan menggantung / entri bib hilang: <daftar atau "tidak ada">
Pemeriksaan Bagian 3 no. 1–9: <OK / temuan>
Sisa % CEK di Bab II–III: <jumlah dan lokasi>
```

## 5. Di luar patch (opsional, hanya bila Ferdi meminta)
**Gambar 3.2** (`assets/gambar/gambar-3-2-harga-rv.pdf`) dibuat dari pipeline `skripsi_rv`, bukan TikZ. Kalau script-nya ada di workspace:
- beri jarak pada label "Terra" dan "FTX" yang berimpit di panel atas;
- pertimbangkan versi hitam-putih, misalnya arsir abu-abu untuk periode *crash* dan garis putus-putus untuk *flash crash*. Kalau warnanya diganti, ubah juga paragraf keterangan di bawah Gambar 3.2 yang menyebut "garis merah";
- jangan mengubah data, periode, atau skala log.
