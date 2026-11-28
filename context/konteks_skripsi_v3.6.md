# Konteks Skripsi Ferdi — v3.6

Diperbarui: 28 November 2026 (v3.5: 27 November 2026; v3.4: 26 November 2026; v3.3: 23 November 2026; v3.2: 17 November 2026; v3.1: 16 November 2026; v3.0: 24 Oktober 2026)
Dokumen ini menggantikan seluruh konteks sebelumnya. Kalau ada dokumen lama yang bertentangan dengan isi di sini, ikuti dokumen ini.

> **Perubahan v3.6 (28 November 2026):** pembimbing 2 ditambahkan; catatan folder kode diperbarui (`prediksi_btc`); rujukan tabel *research gap* diganti ke Tabel 2.3. **Menggantikan:** `konteks_skripsi_v3.5.md` (arsip).
>
> **Perubahan v3.5 (27 November 2026):** Tugas 5 disesuaikan: CatBoost diputuskan memakai mode Plain, `has_time` ditutup, perbaikan review v5 dan panduan format masuk Bab I–III. **Menggantikan:** `konteks_skripsi_v3.4.md` (arsip).
>
> **Perubahan v3.4 (26 November 2026):** Bagian 3 dan 5 disesuaikan: periode data sudah pasti, sumber *scalper* sudah ada, istilah data primer sudah diputuskan. **Menggantikan:** `konteks_skripsi_v3.3.md` (arsip).
>
> **Perubahan v3.3 (23 November 2026):** istilah diganti ke istilah umum (keputusan Ferdi): **horizon prediksi** = berapa menit ke depan; ***time frame*** = lama satu *candle*; **data latih**, **data uji**, **metode optimasi**, **MAE validasi**. Judul sementara diganti. **Menggantikan:** `konteks_skripsi_v3.2.md` (arsip).
>
> **Perubahan v3.2 (17 November 2026):** status Tugas Terbuka (Bagian 5) disesuaikan dengan kondisi 17 Nov; kode final di `prediksi_btc` `main` = `8524462`.
>
> **Perubahan v3.1 (16 November 2026):** Bagian 2 dan 3 disesuaikan dengan desain v4 hasil review dosen 11 November 2026. Tiga rasio *split* 80:20/70:30/60:40, data *ticker* 5 menit sebagai sumber eksperimen, dan "data satu minggu" sudah **tidak dipakai**; ketiganya dipindah ke Bagian 4. Ringkasan desain v4 mengikuti `CLAUDE.md` bagian Fakta kunci. **Menggantikan:** `konteks_skripsi_v3.0.md` (arsip).

---

## 1. Identitas

- Nama: Ferdi Endahas Ahmad
- Program studi: Informatika, UPN "Veteran" Jawa Timur
- Dosen pembimbing 1: Dr. Rizky Parlika, S.Kom., M.Kom.
- Dosen pembimbing 2: Angga Lisdiyanto, S.Kom., M.Kom.
- Tahap: praskripsi (proposal Bab 1–3)
- Penulisan: LaTeX di VS Code, repo GitHub `ferdiendahas/skripsi-latex`. Ditulis dalam bahasa Indonesia dulu, diterjemahkan ke bahasa Inggris setelah semua bab selesai.

## 2. Arah penelitian saat ini

Topik sudah ditetapkan setelah bimbingan 23 Oktober 2026.

- **Tujuan:** mencari model terbaik untuk memprediksi harga Bitcoin (nilai numerik, regresi) dalam waktu dekat.
- **Objek:** harga Bitcoin dalam rupiah (BTC/IDR). Data diambil dari API publik Indodax sebagai sumber data; penelitian tidak membuat prediksi untuk platform tertentu (keputusan Ferdi, 22 Nov 2026).
- **Model yang dibandingkan (empat):** XGBoost, LightGBM, CatBoost, AdaBoost.
- **Horizon prediksi:** 1, 5, 15, 30, dan 60 menit; 1 menit hanya untuk *candle* 1 menit. Horizon prediksi = jarak waktu prediksi (berapa menit ke depan). *Time frame* = lama satu *candle* (1 dan 5 menit), sesuai istilah umum trader.
- **Pembagian data:** data latih ±80% data awal + data uji 20% data akhir, berurutan waktu, dengan *purging* berbasis waktu. Tahap 3 memvariasikan **panjang data latih** (100%, 75%, 50% data latih), bukan memindah data uji.
- **Optimasi:** 7 metode optimasi — *default*, Grid (27 kombinasi), Random, TPE, CMA-ES, GA (NSGA-II), QMC (masing-masing 30 *trial*) — ditambah 4 teknik tambahan (*early stopping*, top-15 fitur, *loss* L1, *pruner* median).
- **Validasi dan evaluasi:** *walk-forward* 5 *fold* di data latih dengan *purging* berbasis waktu; objektif *tuning* = MAE harga (rupiah). Metrik MAE, RMSE, MAPE, akurasi arah; uji Diebold-Mariano dengan koreksi HLN dan koreksi Holm per keluarga uji.
- **Aturan pemilihan:** Tahap 1 dan 2 memilih dari median MAE validasi vs Naive keempat model (rata-rata dua nilai tengah), hanya memakai MAE validasi di data latih. Data uji baru dibuka setelah pilihan dikunci.
- **Prinsip dari dosen:** eksperimen harus banyak dan bervariasi.
- **Sudut pandang pengguna:** trader jangka pendek, khususnya scalper.

Judul sementara: "Prediksi Harga BTC/IDR Jangka Pendek dengan Model Boosting dan Optimasi Hyperparameter" (23 Nov 2026). Judul final belum ditetapkan bersama dosen.

## 3. Data

- Sumber: API publik Indodax.
- Jenis data eksperimen: **candle 1 menit** (dari `tradingview/history_v2`, `tf=1`) dan **candle 5 menit** hasil agregasi candle 1 menit. Indodax tidak menyediakan candle 5 menit.
- Snapshot ticker tetap disimpan, tetapi **tidak dipakai sebagai fitur**. Data ticker hanya dipakai untuk menghitung selisih harga jual-beli pada deskripsi data.
- Pengumpulan: berjalan otomatis lewat cron job tiap 1 menit di VPS (UTC) dan dilanjutkan sampai Februari 2027.
- Menit tanpa transaksi tetap menghasilkan candle dengan volume 0 (H=L=C=close menit sebelumnya), sekitar 6,6% menit. Pada data penelitian, harga bar seperti itu dianggap tetap ($P_t = P_{t-1}$).
- Data yang dipakai untuk eksperimen final: **10 Oktober 2026 – 10 Februari 2027** (bukan satu minggu), diputuskan 17 Nov 2026. `START_UTC`/`END_UTC` di `config.py` diisi sebelum Tahap 1.

## 4. Yang sudah TIDAK dipakai

Bagian ini penting supaya tidak tercampur dengan versi lama.

| Versi lama | Status |
|---|---|
| Transfer learning LSTM pada token HYPE (Hyperliquid) | Ditolak dosen, ditinggalkan |
| LightGBM vs HAR-RV untuk realized variance Bitcoin | Diganti, sudah tidak dipakai |
| Realized variance / volatilitas sebagai target | Dibuang. Dosen menilai istilah ini membingungkan |
| HAR-RV sebagai pembanding | Dibuang, tidak cocok untuk prediksi harga |
| Data Binance dan Hyperliquid | Tidak dipakai. Sekarang hanya Indodax |
| Horizon tetap 5 menit saja | Diganti. Horizon dicari lewat eksperimen |
| Horizon 1 jam saja | Dibuang. Diuji sebagai salah satu variasi horizon |
| Tiga rasio *split* 80:20, 70:30, 60:40 | **Usang** sejak review dosen 11 Nov 2026. Diganti data uji tetap + Tahap 3 = panjang data latih |
| Dataset ticker 5 menit sebagai sumber eksperimen | **Usang.** Dataset 5 menit sekarang dari agregasi candle 1 menit; ticker hanya untuk deskripsi spread |
| Eksperimen memakai data satu minggu | **Usang.** Eksperimen final memakai data Okt 2026 – Feb 2027. Data satu minggu hanya dipakai pada uji coba P1 |

Dokumen project lama berikut masih membahas versi realized variance. Gunakan hanya sebagai arsip, bukan acuan:
- `hasil_riset_bitcoin_v2.9.md`
- `hasil_eksperimen_bitcoin_v2_5.md`
- `verifikasi_definisi_RV.md`
- `perhitungan_manual.md`
- `kartu_paper.md` (cek ulang, sebagian paper mungkin masih relevan)

Folder kode lama `/Users/ea/Documents/Skripsi BTC/skripsi_rv` berisi pipeline realized variance. Kode arah baru ada di repo `ferdiendahas/prediksi_btc` (lihat `hasil_eksperimen_v3.8.md` Lampiran B).

## 5. Tugas yang masih terbuka

1. Mencari paper yang mengaitkan horizon trading dengan tipe trader (scalper, swing trader). — selesai untuk kebutuhan praskripsi: teori pasar heterogen (C1, C2), tipe trader Bitcoin (C6), dan definisi *scalper* Silber 1984 (C7). Pemetaan horizon menit ke tipe trader kripto tetap ditulis sebagai asumsi.
2. ~~Mencari paper referensi untuk keempat metode boosting~~ — selesai (kartu E1–E10).
3. ~~Menentukan metode optimasi hyperparameter yang dipakai~~ — selesai: 7 metode optimasi + 4 teknik tambahan (Bab III).
4. ~~Menentukan fitur input dan metrik evaluasi~~ — selesai, lihat Bab III 3.5 dan 3.8.
5. Menyusun ulang praskripsi Bab 1–3. — draft lengkap (commit `ae379bd`, 28 Nov 2026). Data primer sudah diputuskan 17 Nov. Perbaikan review v5 dan penyesuaian panduan format penulisan sudah masuk (27 Nov 2026); hal yang perlu keputusan pembimbing dicatat di `hasil_riset_v3.9.md` Bagian IX no. 9. Masih menunggu dosen: aturan model terbaik RM3, QMC 30/32, multi-*seed*. CatBoost diputuskan memakai mode Plain (27 Nov 2026), sehingga `has_time` tidak diperlukan.
6. Menetapkan judul final bersama dosen.
7. ~~Menetapkan tanggal pasti periode data~~ — selesai 17 Nov 2026 (10 Okt 2026 – 10 Feb 2027). Ada/tidaknya aplikasi web masih menunggu dosen.
8. ~~Memutuskan skor Tahap 1–2: rata-rata atau median 4 model~~ — selesai 16 Nov 2026: **median** (Bab III Skenario Pengujian; `ringkas.py` di `main` commit `8524462`).

## 6. Kewajiban log harian

Mulai 24 Oktober 2026, dosen meminta log penelitian harian.
- Satu entri per hari, Senin sampai Sabtu.
- Minimal dua kalimat tentang kegiatan yang mendukung penelitian.
- Kolom: No, Hari, Tanggal, Waktu, Pembahasan.
- Isi harus sesuai kegiatan yang benar-benar dikerjakan.

## 7. Aturan penulisan dan referensi

**Narasi skripsi**
- Kalimat sederhana dan pendek, kosakata sehari-hari, gaya mahasiswa S1.
- Tidak boleh melebih-lebihkan klaim. Klaim harus sesuai paper yang benar-benar dibaca.
- Tidak memakai titik dua di tengah kalimat.
- Lebih memilih "merupakan" daripada "adalah" dalam definisi.
- Sitasi cukup nomor, misalnya [1], tanpa menyebut nama penulis kalau tidak perlu.
- Hindari mengulang sitasi yang sama kecuali benar-benar perlu.
- Sitasi kelompok seperti [11]–[13] boleh kalau setiap sumber memang cocok.
- Paragraf yang sudah sederhana dan mudah dipahami tidak perlu diubah.

**Referensi**
- Paper untuk research gap (Tabel 2.3) harus dari lima tahun terakhir, yaitu terbit 2022–2026. Paper pendukung metode atau teori boleh tahun berapa pun.
- Metadata setiap referensi dicocokkan dengan Crossref atau doi.org. Indeks jurnal dicek di SCImago dan Sinta.
- Referensi hasil bantuan AI wajib diverifikasi sendiri. Referensi palsu tidak boleh masuk.
- Paper karya dosen pembimbing tidak dianggap sebagai rekomendasi dosen kecuali beliau sendiri yang meminta.

**Notasi pasar**
- Pasar spot ditulis dengan garis miring, misalnya BTC/IDR. Penulisan tanpa garis miring dianggap pasar perpetual.

**Prinsip teknis**
- Waspadai kebocoran data (data leakage), termasuk saat fitting scaler. Data uji tidak boleh ikut dipakai saat pelatihan.
- Data deret waktu dibagi berurutan sesuai waktu, tidak diacak.
