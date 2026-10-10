# Brief 2: Koreksi Klaim Referensi, Bentrok Notasi, dan Verifikasi Sisa `references.bib`

**Aturan umum** (sama dengan brief 1): ubah hanya yang tercantum, pertahankan `% CEK:` kecuali yang disebut dihapus, jangan mengarang. Selesai: `make` lalu `make check`, kirim laporan per butir.

---

## A. Klaim yang harus ditulis ulang

### A1. Akgun & Gulay (`akgun2025`) — diverifikasi dari full text
Fakta dari full text: BTC, ETH, dan BNB (BTC: 18 Agu 2017 – 31 Des 2021, data Binance); sebelas model tipe GARCH dalam enam distribusi serta ANN, LSTM, dan CNN; rasio latih-uji 70:30/80:20/90:10; tidak ada HAR; tidak ada uji signifikansi (perbandingan berdasarkan nilai *loss* terkecil). Perbandingan *rolling* dan *expanding window* (ukuran 3–45) dilaporkan rinci hanya untuk model tipe GARCH (Bagian 3.6, Bagian 4, Tabel 14–22, Kesimpulan). Temuan: *rolling* umumnya lebih baik daripada *expanding*, dan rasio latih yang lebih besar meningkatkan akurasi.

**Bab I**, paragraf "Persoalan berikutnya adalah cara model diperbarui ...". Ganti kalimat dari "Pilihan antara \textit{rolling window} ..." sampai "... bukan panjang data latih \cite{feng2024ml}." menjadi:

```latex
Pilihan antara \textit{rolling window} dan \textit{expanding window}
berpengaruh terhadap akurasi peramalan volatilitas \cite{feng2024window},
termasuk pada aset kripto \cite{akgun2025}. Namun, Akgun dan Gulay
melaporkan perbandingan kedua skema tersebut secara rinci hanya untuk model
tipe GARCH, tanpa HAR sebagai pembanding dan tanpa uji signifikansi
\cite{akgun2025}, sedangkan Feng, Qi, dan Lucey memvariasikan
\textit{hyperparameter} model ML, bukan panjang data latih
\cite{feng2024ml}.
```

**Bab II**, 2.1 paragraf "Pengaruh \textit{window} data latih". Ganti kalimat Akgun menjadi:

```latex
Akgun dan Gulay membandingkan sebelas model tipe GARCH dan tiga model
\textit{deep learning} untuk peramalan volatilitas Bitcoin, Ethereum, dan
Binance Coin hingga akhir 2021 \cite{akgun2025}. Perbandingan
\textit{rolling} dan \textit{expanding window} dilaporkan secara rinci untuk
model tipe GARCH, dengan hasil bahwa \textit{rolling window} umumnya lebih
akurat; perbandingan tersebut tidak menyertakan HAR dan tidak disertai uji
signifikansi.
```

**Tabel 2.1**, baris Akgun & Gulay:
- Kolom "Objek": `Volatilitas BTC, ETH, BNB s.d. 2021`
- Kolom "Pembanding HAR": `Tidak (GARCH dan \textit{deep learning})`
- Kolom "Variasi strategi window": `Ya (rolling vs expanding, dilaporkan untuk GARCH)`

Hapus komentar `% CEK:` tentang `akgun2025` yang dipasang agen pada brief 1 dan jangan memasang yang baru; klaim ini sudah diverifikasi dari full text.

### A2. Zhang dkk. (`zhang2024`)
Judul sebenarnya: "Relationships among return and liquidity of cryptocurrencies". Di 2.2.12, ganti kalimat "Zhang dkk. juga membahas penggunaan proksi likuiditas harian pada pasar kripto \cite{zhang2024}." menjadi:

```latex
Proksi likuiditas harian juga dipakai Zhang dkk. untuk mengkaji hubungan
antara \textit{return} dan likuiditas aset kripto \cite{zhang2024}.
```

Hapus `% CEK:` agen untuk `zhang2024`.

### A3. `feng2024window` dan `agakishiev2025`
- `feng2024window`: tidak ada nama penulis di prosa, jadi kalimat tidak perlu diubah. Hapus `% CEK:` agen bila isinya hanya soal jumlah penulis.
- `agakishiev2025`: judul Crossref ("Regime switching forecasting for cryptocurrencies") sesuai dengan klaim di 2.1. Hapus `% CEK:` agen untuk entri ini; kalimat tidak diubah.

---

## B. Bentrok notasi (Bab II + Daftar Notasi)

### B1. Harga tertinggi/terendah vs loss
$L_t$ dipakai untuk harga terendah (Parkinson) dan *loss*. Ganti notasi harga di persamaan `eq:parkinson`, blok keterangannya, dan prosa sekitarnya:
- $H_t$ → $P^{H}_t$ (harga tertinggi hari $t$)
- $L_t$ → $P^{L}_t$ (harga terendah hari $t$)

Notasi *loss* ($L_t(\cdot)$, $L^{\text{QLIKE}}_t$, $L^{\text{MSE}}_t$) tetap.

### B2. Tiga makna $m$
- Persamaan GBDT `eq:gbdt` dan keterangannya: ganti indeks iterasi $m$ menjadi $b$ ($F_b$, $F_{b-1}$, $h_b$; "pohon ke-$b$", "setelah $b$ iterasi").
- Fluctuation test (2.2.9): ganti "jendela berukuran $m = \mu n$" menjadi "jendela berukuran $n_F = \mu n$".
- $m$ pada UDmax ($\sup F_T(m)$, jumlah titik patah) **tetap**, karena itu notasi baku Bai–Perron.

### B3. Statistik KS
Ganti $D$ pada persamaan `eq:ks`, keterangannya, dan prosa 2.2.11 menjadi $D^{\text{KS}}$. $D_t$ (selisih antarstrategi) tetap.

### B4. Daftar Notasi
Perbarui `frontmatter/daftar-notasi.tex` sesuai B1–B3: $P^{H}_t$, $P^{L}_t$, $b$, $n_F$, $D^{\text{KS}}$. Hapus entri $H_t$, $L_t$ (harga), dan $D$ yang lama. $m$ kini hanya berarti jumlah titik patah.

---

## C. Verifikasi sisa `references.bib`

1. Jalankan verifikasi Crossref yang sama untuk **semua** entri ber-DOI yang belum diverifikasi (termasuk `andersen1998`, `corsi2009`, `liu2015`, `parkinson1980`, `patton2015`, `amihud2002`, `brauneis2021`, `chen2016`, `patton2011`, `diebold1995`, `newey1987`, `giacomini2009`, `giacomini2010`, `rossi2013`, `martins2016`, `bai1998`, `bai2003`, `tashman2000`, `cerqueira2020`, `gama2014`, `zliobaite2015`, `morenotorres2012`, `suarez2023`, `mokni2024`, `yi2023`).
2. Entri tanpa DOI (`ke2017`, `holm1979`, `barndorff2010`, `grinsztajn2022`, `rabanser2019`, `nakamoto2008`): jangan diubah. Beri `% CEK: tanpa DOI, verifikasi manual` di atas masing-masing.
3. Untuk setiap judul yang ternyata berbeda **substansi** (bukan sekadar huruf besar/kecil), laporkan key, judul lama, dan judul baru, lalu tandai kalimat di Bab I/II yang mengutipnya dengan `% CEK:`. Jangan menulis ulang kalimatnya.
4. Normalkan karakter non-ASCII yang tidak ada di Times New Roman (seperti U+2010) seperti pada brief 1.

---

## D. Laporan balik
- Ringkasan per butir A1–A3, B1–B4, C.
- Untuk C: tabel field yang berubah (key, field, lama, baru), daftar judul yang berbeda substansi, dan entri yang masih `% CEK`.
- Output `make check`.
