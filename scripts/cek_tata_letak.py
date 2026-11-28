#!/usr/bin/env python3
"""cek_tata_letak.py — cek dua aturan tata letak pada PDF hasil compile.

1. Rujuk dulu, baru gambar: setiap gambar harus sudah disebut di teks
   ("ditunjukkan pada Gambar X.Y") sebelum gambarnya muncul, lalu dijelaskan
   sesudahnya. Pelanggaran = caption muncul sebelum rujukan pertamanya.
   Tabel hanya dilaporkan sebagai info.
2. Ruang kosong: tidak boleh ada ruang putih > 3 cm di area teks, kecuali di
   halaman terakhir setiap bab (diperiksa manual dari daftar yang dicetak).

Butuh: pdftotext dan pdftoppm (poppler), Pillow, numpy.
Pemakaian: python scripts/cek_tata_letak.py build/praskripsi.pdf
Kalau ada pelanggaran: pastikan lingkungan figure diletakkan sesudah paragraf
yang pertama kali merujuknya (flafter di praskripsi.tex mencegah gambar naik
ke atas rujukannya). Jangan pakai [H].
"""
import re, subprocess, sys, tempfile, glob, os
import numpy as np
from PIL import Image

pdf = sys.argv[1]
xml = subprocess.run(["pdftotext", "-bbox-layout", pdf, "-"], capture_output=True, text=True).stdout
# kata per kata, supaya "Gambar" di akhir baris dan "2.3" di baris berikutnya tetap terbaca
words = []   # (halaman, y, x, teks, awal_baris)
for pi, pg in enumerate(xml.split("<page ")[1:], 1):
    for ln in re.finditer(r'<line [^>]*>(.*?)</line>', pg, re.S):
        ws = re.findall(r'<word xMin="([\d.]+)" yMin="([\d.]+)"[^>]*>([^<]*)</word>', ln.group(1))
        for k, (x, y, t) in enumerate(ws):
            words.append((pi, float(y), float(x), t, k == 0))
# lewati halaman depan (daftar isi/tabel/gambar): mulai dari halaman "BAB I"
mulai = next((w[0] for i, w in enumerate(words[:-2])
              if w[3] == "BAB" and w[4] and words[i + 1][3] == "I" and words[i + 2][4]), 1)
caps, refs = {}, {}
for i in range(len(words) - 1):
    pi, y, x, t, awal = words[i]
    if pi < mulai or t not in ("Gambar", "Tabel"):
        continue
    m = re.match(r"(\d+\.\d+)", words[i + 1][3])
    if not m:
        continue
    key = f"{t} {m.group(1)}"
    nxt = words[i + 2][3] if i + 2 < len(words) else ""
    # caption: di awal baris, angka tanpa tanda baca, tidak diikuti kata kerja narasi
    iscap = awal and words[i + 1][3] == m.group(1) and nxt not in ("menunjukkan", "bagian")
    if iscap and key not in caps:
        caps[key] = (pi, y, x)
    else:
        refs.setdefault(key, []).append((pi, y, x))
langgar = 0
for k, pos in caps.items():
    sebelum = [r for r in refs.get(k, []) if r < pos]
    if not sebelum:
        jenis = "PELANGGARAN" if k.startswith("Gambar") else "info"
        langgar += k.startswith("Gambar")
        print(f"{jenis}: {k} (hlm. PDF {pos[0]}) muncul sebelum dirujuk di teks")
print(f"Urutan gambar: {langgar} pelanggaran dari {sum(k.startswith('Gambar') for k in caps)} gambar")

with tempfile.TemporaryDirectory() as d:
    subprocess.run(["pdftoppm", "-r", "40", "-gray", "-png", pdf, os.path.join(d, "p")], check=True)
    px = 40 / 2.54
    for f in sorted(glob.glob(os.path.join(d, "p-*.png"))):
        a = np.array(Image.open(f).convert("L")); h, w = a.shape
        top, bot = int(3 * px), h - int(3 * px)
        ink = np.where((a[top:bot, int(4 * px):w - int(3 * px)] < 200).any(axis=1))[0]
        if len(ink) == 0:
            continue
        gap = (np.diff(ink).max() if len(ink) > 1 else 0) / px
        tail = ((bot - top) - ink[-1]) / px
        if gap > 3 or tail > 3:
            n = re.search(r"p-(\d+)", f).group(1)
            print(f"Ruang kosong > 3 cm di hlm. PDF {int(n)} (celah {gap:.1f} cm, sisa bawah {tail:.1f} cm)"
                  " -> boleh hanya bila halaman terakhir bab/daftar")
