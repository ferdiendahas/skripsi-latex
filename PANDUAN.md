# Panduan Perintah

Semua yang perlu dijalankan sendiri di Terminal, tanpa bantuan agen.

Semua perintah di bawah dijalankan dari folder proyek:

```bash
cd ~/skripsi-latex
```

Kalau lupa sedang di folder mana, ketik `pwd`.

---

## Alur harian

Lima langkah ini urut. Sisanya di dokumen ini hanya rincian dari kelimanya.

1. Edit berkas `.tex` di editor.
2. `make` — bangun PDF.
3. `make check` — pastikan formatnya lolos Pedoman.
4. `git add -A && git commit -m "pesan"` — simpan ke riwayat.
5. `git push origin main` — kirim ke GitHub.

---

## Membangun PDF

```bash
make
```
Mengompilasi `praskripsi.tex` menjadi `build/praskripsi.pdf`. Jalankan XeLaTeX
berulang sampai daftar isi, nomor gambar, dan sitasi stabil, lalu Biber untuk
daftar pustaka. Aman dijalankan berkali-kali.

```bash
make watch
```
Mode pantau: setiap kali berkas `.tex` disimpan, PDF langsung dibangun ulang.
Berguna saat menulis. Hentikan dengan `Ctrl-C`.

```bash
open build/praskripsi.pdf
```
Membuka hasilnya di Preview. Preview otomatis memuat ulang kalau PDF-nya
berubah, jadi biarkan terbuka sambil `make watch` jalan.

```bash
make clean
```
Menghapus seluruh folder `build/`. Dipakai kalau hasil build terasa aneh dan
dicurigai ada berkas sisa yang basi. Setelah ini, `make` berikutnya akan lebih
lama karena membangun dari nol.

---

## Memeriksa format

```bash
make check
```
Membangun PDF lalu memeriksanya terhadap aturan Pedoman Skripsi Fasilkom UPN
Jatim 2025. Keluaran yang diharapkan satu baris: `LULUS build/praskripsi.pdf`.

Yang diperiksa:

| Aspek | Aturan |
|---|---|
| Ukuran halaman | A4 |
| Font | Times New Roman, Arial, Courier New tertanam di PDF |
| Font pengganti | Memperingatkan kalau TeX Gyre yang terpakai |
| Margin | Teks isi di dalam margin kiri 4 cm dan kanan 3 cm |
| Teks wajib | Frasa seperti `DOSEN PEMBIMBING` ada di sampul |
| Rujukan | Tidak ada `??` atau sitasi tak terdefinisi |
| Baris kebablasan | Tidak ada `Overfull \hbox` 3 pt atau lebih |

Kalau gagal, pesannya menyebutkan halaman dan kata yang bermasalah.

---

## Ekspor ke Word

```bash
make docx
```
Menghasilkan `build/praskripsi.docx` lengkap dengan sampul, daftar isi, daftar
gambar, daftar tabel, dan nomor halaman.

Menyimpan ke nama lain:

```bash
python3 scripts/build_docx.py --keluaran ~/Desktop/draf-bab1.docx
```

### Dua pertanyaan Word saat file dibuka

**"This document contains fields that may refer to other files. Do you want to
update the fields in this document?"** — jawab **Yes**.

Daftar isi dan daftar tabel disimpan sebagai *field*, bukan teks mati. Word yang
menghitung isinya saat file dibuka. Ini memang disengaja supaya nomor halamannya
selalu ikut isi dokumen.

**"Creating a table of contents? Start by applying a heading style..."** —
muncul kalau pertanyaan di atas dijawab **No**, sehingga field-nya tetap kosong.
Perbaikannya tanpa perlu menutup file: klik kanan di area daftar isi, pilih
**Update Field**, lalu **Update entire table**.

### Gambar tidak muncul di Word

Gambar 2.1 sampai 2.4 digambar dengan TikZ, yaitu kode yang hanya dimengerti
LaTeX. Pandoc tidak bisa menerjemahkannya ke Word, jadi keempatnya hilang dalam
ekspor. Karena tidak ada satu pun gambar yang tersisa, halaman Daftar Gambar
juga tidak dibuat di berkas `.docx` — ini disengaja, supaya tidak ada daftar
kosong.

Versi PDF tetap memuat seluruh gambar. Untuk keperluan yang butuh gambar di
Word, gambarnya perlu dirender lebih dulu menjadi PNG.

### Kalau muncul lagi `ImportError ... pyexpat`

Homebrew mengemas `python@3.14` dengan `pyexpat` yang dikompilasi memakai header
expat versi baru, tetapi ditautkan ke `libexpat` bawaan macOS yang lebih lama.
Akibatnya modul itu gagal dimuat. Perbaikannya mengarahkan ulang tautan tersebut
ke expat milik Homebrew:

```bash
SO=$(python3 -c "import sysconfig,glob,os; print(glob.glob(os.path.join(sysconfig.get_paths()['stdlib'],'lib-dynload','pyexpat*.so'))[0])")
install_name_tool -change /usr/lib/libexpat.1.dylib \
  /opt/homebrew/opt/expat/lib/libexpat.1.dylib "$SO"
codesign --force --sign - "$SO"
python3 -c "import pyexpat; print('OK', pyexpat.version_info)"
```

Perlu diulang setiap kali `brew upgrade` memasang ulang `python@3.14`, karena
berkas yang ditambal ikut tertimpa.

Alternatif tanpa menambal apa pun: pakai Python bawaan macOS, yang tidak
terpengaruh masalah ini.

```bash
/usr/bin/python3 scripts/build_docx.py
```

Berkas `.docx` masuk `.gitignore`, jadi tidak ikut ter-commit. Yang disimpan di
Git hanya sumber `.tex`-nya.

---

## Sampul dan metadata

Seluruh isi sampul diatur dari satu berkas: `metadata.tex`. Setelah diubah,
jalankan `make` lagi.

```latex
\upnsetup{
  judul={...},
  nama={...},
  npm={...},
  pembimbing-satu={...},
  pembimbing-dua={...},
  program-studi={Informatika},
  tahun={2026}
}
```

Kunci `judul`, `nama`, `npm`, dan `pembimbing-satu` wajib diisi — kalau kosong,
build berhenti dengan pesan error yang menyebut nama kuncinya.

Kunci lain yang tersedia kalau perlu diubah: `fakultas`, `universitas`,
`kementerian`, `kota`, dan `logo`.

### Opsi kelas

Diatur di baris pertama `praskripsi.tex`:

```latex
\documentclass[jenis=praskripsi]{upnjatim-skripsi}
```

| Opsi | Nilai | Arti |
|---|---|---|
| `jenis` | `praskripsi` / `skripsi` | Label di sampul. `skripsi` baru menyediakan sampul saja |
| `sampul` | `putih` / `oranye` | Latar sampul. Bawaan `putih` |
| `ketat` | — | Build gagal kalau Times New Roman / Arial / Courier New tidak terpasang, bukan diganti diam-diam |
| `pemenggalan` | — | Mengizinkan kata dipenggal di ujung baris. Bawaan mati, mengikuti template Word |

Contoh memakai dua opsi sekaligus:

```latex
\documentclass[jenis=praskripsi,sampul=oranye]{upnjatim-skripsi}
```

---

## Mengganti gambar

Gambar 1.1 dibangkitkan dari pipeline `skripsi_rv`. Untuk memperbaruinya, timpa
berkasnya dengan nama yang sama lalu build ulang:

```bash
cp ~/Downloads/skripsi_rv/figures/gambar_1_1_harga_rv.pdf \
   assets/gambar/gambar-1-1-harga-rv.pdf
make
```

Nama `gambar-1-1-harga-rv.pdf` harus dipertahankan karena itu yang diacu di
`chapters/bab1-pendahuluan.tex`. Pakai versi PDF, bukan PNG — PDF dari
matplotlib berupa vektor sehingga tetap tajam saat dicetak.

Gambar 2.1 sampai 2.4 digambar dengan TikZ langsung di dalam
`chapters/bab2-tinjauan-pustaka.tex`, jadi tidak ada berkas gambar terpisah
untuk diganti.

---

## Git

### Menyimpan pekerjaan

```bash
git status              # berkas apa saja yang berubah
git diff                # lihat perubahannya baris per baris
git add -A              # tandai semua perubahan untuk disimpan
git commit -m "feat: isi Bab I dan Bab II"
git push origin main    # kirim ke GitHub
```

`git push` adalah satu-satunya perintah yang benar-benar mengirim ke internet.
Sebelum itu, semuanya masih lokal.

### Mengambil update dari template

Repo ini adalah fork dari `fikrahdamar/skripsi-fasilkom-latex`.

```bash
git fetch upstream                       # ambil versi terbaru template
git log --oneline main..upstream/main    # lihat apa yang baru
git merge upstream/main                  # gabungkan ke pekerjaan sendiri
make check                               # pastikan masih lolos setelah digabung
```

Kalau muncul konflik, Git menandai berkasnya dan `git status` menyebutkan mana
saja. Edit bagian bertanda `<<<<<<<` sampai `>>>>>>>`, lalu `git add` berkas itu
dan `git commit`.

### Membatalkan

```bash
git restore <berkas>    # buang perubahan pada satu berkas yang belum di-commit
git restore .           # buang semua perubahan yang belum di-commit
```

Keduanya tidak bisa dibatalkan. Pastikan memang ingin membuangnya.

---

## Kalau error

| Pesan | Sebab | Tindakan |
|---|---|---|
| `ImportError: No module named expat` | `pyexpat` Homebrew salah taut ke `libexpat` bawaan macOS | Jalankan ulang tambalan di bagian Ekspor ke Word |
| `Metadata judul belum diisi` | Kunci wajib kosong di `metadata.tex` | Isi kunci yang disebut di pesan error |
| `Logo tidak ditemukan` | Berkas logo hilang atau path salah | Periksa `assets/logo-upnjatim.png` |
| `Overfull \hbox ... too wide` | Tabel atau kata terlalu lebar untuk margin | Persempit kolom tabel, atau kecilkan font tabel |
| `Reference ... undefined` | `\ref` menunjuk label yang belum ada | Periksa ejaan `\label` dan `\ref` |
| `Citation ... undefined` | Key sitasi tidak ada di `references.bib` | Tambahkan entri, atau perbaiki ejaan key |
| `Font pengganti TeX Gyre dipakai` | Times New Roman tidak terpasang | Pasang fontnya untuk hasil akhir |
| Hasil build aneh tanpa sebab jelas | Berkas sementara basi | `make clean` lalu `make` |

Pesan error LaTeX yang panjang biasanya hanya baris pertama yang penting. Cari
baris yang diawali tanda `!`:

```bash
grep -n "^!" build/praskripsi.log
```

---

## Struktur folder

```
skripsi-latex/
├── praskripsi.tex           # berkas utama, mengatur urutan bab
├── metadata.tex             # judul, nama, NPM, pembimbing
├── upnjatim-skripsi.cls     # kelas dokumen, jangan diubah tanpa perlu
├── chapters/                # isi bab
├── frontmatter/             # daftar notasi
├── appendices/              # lampiran
├── bibliography/            # references.bib
├── assets/                  # logo dan gambar
├── scripts/                 # build_docx.py, check_pdf.py
└── build/                   # hasil build, tidak masuk Git
```

---

## Perintah LaTeX khusus template

Dipakai di dalam berkas `.tex`, bukan di Terminal.

| Perintah | Kegunaan |
|---|---|
| `\buatsampul` | Membuat halaman sampul |
| `\daftarisi` `\daftargambar` `\daftartabel` | Membangkitkan ketiga daftar |
| `\bagianutama` | Menandai mulai penomoran halaman angka |
| `\daftarpustaka` | Mencetak daftar pustaka |
| `\lampiran{Judul}` | Memulai satu lampiran baru |
| `\sumber{...}` | Baris "Sumber:" di bawah gambar atau tabel |
