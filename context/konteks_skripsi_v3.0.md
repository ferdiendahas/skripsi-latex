# Konteks Skripsi Ferdi — v3.0

Diperbarui: 24 Oktober 2026
Dokumen ini menggantikan seluruh konteks sebelumnya. Kalau ada dokumen lama yang bertentangan dengan isi di sini, ikuti dokumen ini.

---

## 1. Identitas

- Nama: Ferdi Endahas Ahmad
- Program studi: Informatika, UPN "Veteran" Jawa Timur
- Dosen pembimbing: Dr. Rizky Parlika, S.Kom, M.Kom
- Tahap: praskripsi (proposal Bab 1–3)
- Penulisan: LaTeX di VS Code, repo GitHub `ferdiendahas/skripsi-latex`. Ditulis dalam bahasa Indonesia dulu, diterjemahkan ke bahasa Inggris setelah semua bab selesai.

## 2. Arah penelitian saat ini

Topik sudah ditetapkan setelah bimbingan 23 Oktober 2026.

- **Tujuan:** mencari model terbaik untuk memprediksi harga Bitcoin (nilai numerik, regresi) dalam waktu dekat.
- **Objek:** pasangan spot BTC/IDR di Indodax. Harga dalam rupiah.
- **Model yang dibandingkan (empat):** XGBoost, LightGBM, CatBoost, AdaBoost.
- **Horizon prediksi:** tidak ditetapkan di awal. Horizon optimal dicari lewat eksperimen, misalnya 5, 15, 30, dan 60 menit.
- **Pembagian data:** tiga skenario, yaitu 80:20, 70:30, dan 60:40.
- **Optimasi:** hyperparameter tuning, dengan metode optimasi sebanyak mungkin sesuai permintaan dosen.
- **Prinsip dari dosen:** eksperimen harus banyak dan bervariasi.
- **Sudut pandang pengguna:** trader, khususnya scalper dan swing trader.

Judul final belum ditetapkan.

## 3. Data

- Sumber: API Indodax.
- Jenis data: ticker 5 menit dan candle 1 menit.
- Pengumpulan: berjalan otomatis lewat cron job dan dilanjutkan sampai Februari 2027.
- Data yang dipakai untuk eksperimen: satu minggu (arahan 23 Oktober).
- Perkiraan dataset akhir: sekitar 40.000 baris.

> Perlu dipastikan ke dosen: eksperimen utama memakai satu minggu data saja, atau seluruh data hingga Februari 2027 (sekitar 40.000 baris).

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

Dokumen project lama berikut masih membahas versi realized variance. Gunakan hanya sebagai arsip, bukan acuan:
- `hasil_riset_bitcoin_v2.9.md`
- `hasil_eksperimen_bitcoin_v2_5.md`
- `verifikasi_definisi_RV.md`
- `perhitungan_manual.md`
- `kartu_paper.md` (cek ulang, sebagian paper mungkin masih relevan)

Folder kode lama `/Users/ea/Documents/Skripsi BTC/skripsi_rv` berisi pipeline realized variance. Belum ada folder kode untuk arah baru.

## 5. Tugas yang masih terbuka

1. Mencari paper yang mengaitkan timeframe trading dengan tipe trader (scalper, swing trader).
2. Mencari paper referensi untuk keempat metode boosting.
3. Menentukan metode optimasi hyperparameter yang dipakai.
4. Menentukan fitur input dan metrik evaluasi (belum dibahas dengan dosen).
5. Menyusun ulang praskripsi Bab 1–3. Sebagian besar isi lama diganti karena penelitian kini lebih sederhana.
6. Menetapkan judul final bersama dosen.

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
- Paper untuk research gap harus dari lima tahun terakhir. Paper pendukung metode atau teori boleh tahun berapa pun.
- Setiap DOI harus dibuka dan dicek di doi.org. Indeks jurnal dicek di SCImago dan Sinta.
- Referensi hasil bantuan AI wajib diverifikasi sendiri. Referensi palsu tidak boleh masuk.
- Paper karya dosen pembimbing tidak dianggap sebagai rekomendasi dosen kecuali beliau sendiri yang meminta.

**Notasi pasar**
- Pasar spot ditulis dengan garis miring, misalnya BTC/IDR. Penulisan tanpa garis miring dianggap pasar perpetual.

**Prinsip teknis**
- Waspadai kebocoran data (data leakage), termasuk saat fitting scaler. Data uji tidak boleh ikut dipakai saat pelatihan.
- Data deret waktu dibagi berurutan sesuai waktu, tidak diacak.
