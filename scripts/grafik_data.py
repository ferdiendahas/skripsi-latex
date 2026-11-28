#!/usr/bin/env python3
"""grafik_data.py — data untuk Gambar 3.x (grafik statistik data, Bab III).

Membaca CSV candle 1 menit hasil ekspor collector lewat btcpred.data.load
(repo prediksi_btc), sehingga harga typical dan aturan candle volume nol sama
persis dengan pipeline eksperimen. Keluaran (dibaca pgfplots):
  assets/data/harga_per_jam.dat   jam ke-, harga typical (juta Rp) tiap awal jam
  assets/data/hist_return_1m.dat  tengah bin (bp), persentase return; bin tepi memuat semua nilai di luarnya
  assets/data/ringkasan_data.txt  angka deskriptif untuk narasi (cek manual)

Pemakaian:
  python scripts/grafik_data.py --csv <btcidr_candle_1menit_XXXX.csv> \
      --prediksi-btc ../prediksi_btc --start "2026-10-10 00:00" --end "2026-11-12 23:59"
Untuk eksperimen final: --end "2027-02-10 23:59" dengan CSV ekspor terbaru.
"""
import argparse, sys
from pathlib import Path
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("--csv", required=True)
ap.add_argument("--prediksi-btc", required=True)
ap.add_argument("--start", required=True)
ap.add_argument("--end", required=True)
ap.add_argument("--out", default="assets/data")
ap.add_argument("--batas-bp", type=float, default=20.0)
ap.add_argument("--lebar-bin-bp", type=float, default=1.0)
a = ap.parse_args()

sys.path.insert(0, str(Path(a.prediksi_btc).resolve()))
from btcpred.data import load  # noqa: E402

df, info = load(a.csv, "candle", 1, "typical", start=a.start, end=a.end)
df = df.loc[a.start:a.end]
harga = df["harga"]
out = Path(a.out); out.mkdir(parents=True, exist_ok=True)

# (a) harga tiap awal jam, sumbu x = hari sejak awal periode
jam = harga[harga.index.minute == 0].dropna()
hari = (jam.index - jam.index[0]).total_seconds() / 86400
with open(out / "harga_per_jam.dat", "w") as f:
    f.write("hari harga_juta\n")
    for x, y in zip(hari, jam.values / 1e6):
        f.write(f"{x:.4f} {y:.3f}\n")

# (b) sebaran return logaritmik 1 menit (bp); di luar batas dijumlah ke bin tepi
r = (np.log(harga).diff() * 1e4).dropna()
b = a.batas_bp; w = a.lebar_bin_bp
edges = np.arange(-b - w / 2, b + w / 2 + 1e-9, w)   # bin berpusat di kelipatan w
rc = r.clip(edges[0] + 1e-9, edges[-1] - 1e-9)
cnt, _ = np.histogram(rc, bins=edges)
pct = cnt / len(r) * 100
with open(out / "hist_return_1m.dat", "w") as f:
    f.write("tengah persen\n")
    for e, p in zip(edges[:-1] + w / 2, pct):
        f.write(f"{e:.2f} {p:.4f}\n")

ret_nol = float((r == 0).mean() * 100)
with open(out / "ringkasan_data.txt", "w") as f:
    f.write(f"periode={a.start} s.d. {a.end}\n")
    for k, v in info.items():
        f.write(f"{k}={v}\n")
    f.write(f"harga_min_juta={harga.min()/1e6:.1f}\nharga_maks_juta={harga.max()/1e6:.1f}\n")
    f.write(f"n_return={len(r)}\nreturn_nol_pct={ret_nol:.1f}\n")
    f.write(f"return_std_bp={r.std():.2f}\nreturn_luar_batas_pct={(r.abs() > b + w / 2).mean()*100:.2f}\n")
    f.write(f"kurtosis_berlebih={r.kurt():.1f}\n")
print((out / "ringkasan_data.txt").read_text())
