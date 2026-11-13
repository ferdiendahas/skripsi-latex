#!/usr/bin/env python3
"""contoh_manual.py — membuat subbab "Contoh Perhitungan Manual" (Bab III).

Mengambil 26 candle 1 menit BTC/IDR asli dari CSV ekspor collector, lalu
menghitung dengan tangan (numpy biasa, tanpa pustaka model):
  1. agregasi 5 candle 1 menit -> 1 bar 5 menit, harga typical
  2. return log, fitur ret_lag1, target r_{t,1}
  3. pembagian data 80/20 + purging berbasis waktu
  4. satu pohon XGBoost (kedalaman 1): g_i, q_i, gain, bobot daun
  5. satu iterasi AdaBoost.R2 (pohon kedalaman 1, loss linear)
  6. konversi ke rupiah, MAE, RMSE, MAPE, MAE vs Naive, akurasi arah
  7. uji Diebold-Mariano + HLN (h_b = 1) dan koreksi Holm

Hasil manual dicocokkan dengan xgboost dan scikit-learn bila terpasang.
Keluaran: berkas .tex siap di-\\input ke Bab III.

Pemakaian:
  python contoh_manual.py --csv btcidr_candle_1menit_XXXX.csv \\
      --mulai "2026-10-14 03:00" --out chapters/bab3-contoh-perhitungan.tex
--mulai = waktu UTC paling awal yang dicari; skrip mencari jendela 26 menit
pertama (mulai kelipatan 5 menit) yang lengkap dan layak dihitung.
"""
import argparse
import math
import sys

import numpy as np
import pandas as pd
from scipy import stats

N_CANDLE = 26          # 26 candle -> 24 baris fitur/target
LAMBDA, GAMMA, NU = 1.0, 0.0, 0.3
ALPHA = 0.05
BP = 1e4               # 1 bp = 1e-4
BULAN = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli",
         "Agustus", "September", "Oktober", "November", "Desember"]


# ---------------------------------------------------------------- format
def f(x, d=2):
    """Angka gaya Indonesia untuk mode matematika: 1.234{,}56."""
    if x is None or (isinstance(x, float) and not math.isfinite(x)):
        return r"\text{--}"
    if round(x, d) == 0:
        x = 0.0
    s = f"{x:,.{d}f}".replace(",", "#").replace(".", "{,}").replace("#", ".")
    return s


def m(x, d=2):
    return f"${f(x, d)}$"


def tgl(ts):
    return f"{ts.day} {BULAN[ts.month - 1]} {ts.year}"


def jam(ts):
    return ts.strftime("%H.%M")


# ---------------------------------------------------------------- data
def baca(path):
    df = pd.read_csv(path)
    df["waktu"] = pd.to_datetime(df["waktu_utc"]).dt.floor("1min")
    df = df.drop_duplicates("waktu").set_index("waktu").sort_index()
    return df[["open", "high", "low", "close", "volume"]].astype(float)


def hitung(win):
    """Semua perhitungan untuk satu jendela 26 candle. Mengembalikan dict."""
    R = {}
    P = ((win["high"] + win["low"] + win["close"]) / 3).to_numpy()
    R["P"] = P
    r1 = np.full(N_CANDLE, np.nan)
    r1[1:] = np.log(P[1:] / P[:-1])
    R["r1"] = r1
    # baris j = 1..24: x_j = r1[j] (ret_lag1), y_j = r1[j+1]
    j = np.arange(1, N_CANDLE - 1)
    # dibulatkan 4 desimal (bp) supaya angka di tabel = angka yang dihitung
    x = np.round(r1[j] * BP, 4)
    y = np.round(r1[j + 1] * BP, 4)
    N = len(j)
    ju = math.floor(0.8 * N) + 1                 # baris awal blok uji
    latih = j[(j + 1) < ju]                      # t + h < t_u
    purge = j[(j < ju) & ((j + 1) >= ju)]
    uji = j[j >= ju]
    R.update(j=j, x=x, y=y, N=N, ju=ju, latih=latih, purge=purge, uji=uji)
    ix = lambda arr: arr - 1                     # nomor baris -> indeks array
    xl, yl = x[ix(latih)], y[ix(latih)]
    xu, yu = x[ix(uji)], y[ix(uji)]

    # ---------------- XGBoost, satu pohon kedalaman 1
    F0 = yl.mean()
    g = F0 - yl
    q = np.ones_like(yl)
    G, Q = g.sum(), q.sum()
    ux = np.unique(xl)
    cand = []
    for a, b in zip(ux[:-1], ux[1:]):
        thr = (a + b) / 2
        kiri = xl < thr
        Gk, Qk = g[kiri].sum(), q[kiri].sum()
        Gn, Qn = G - Gk, Q - Qk
        gain = 0.5 * (Gk**2 / (Qk + LAMBDA) + Gn**2 / (Qn + LAMBDA)
                      - G**2 / (Q + LAMBDA)) - GAMMA
        cand.append(dict(thr=thr, nk=int(kiri.sum()), Gk=Gk, Qk=Qk, Gn=Gn, Qn=Qn, gain=gain))
    best = max(cand, key=lambda c: c["gain"])
    wk = -best["Gk"] / (best["Qk"] + LAMBDA)
    wn = -best["Gn"] / (best["Qn"] + LAMBDA)
    pred_x = lambda xx: F0 + NU * np.where(xx < best["thr"], wk, wn)
    R["xgb"] = dict(F0=F0, g=g, q=q, G=G, Q=Q, cand=cand, best=best, wk=wk, wn=wn,
                    fit=pred_x(xl), uji=pred_x(xu))

    # ---------------- AdaBoost.R2, satu iterasi, pohon kedalaman 1 (SSE)
    cs = []
    for a, b in zip(ux[:-1], ux[1:]):
        thr = (a + b) / 2
        kiri = xl < thr
        mk, mn = yl[kiri].mean(), yl[~kiri].mean()
        sse = ((yl[kiri] - mk) ** 2).sum() + ((yl[~kiri] - mn) ** 2).sum()
        cs.append(dict(thr=thr, mk=mk, mn=mn, sse=sse))
    sb = min(cs, key=lambda c: c["sse"])
    ada_x = lambda xx: np.where(xx < sb["thr"], sb["mk"], sb["mn"])
    yh = ada_x(xl)
    ae = np.abs(yh - yl)
    D = ae.max()
    L = ae / D
    p = np.full(len(yl), 1 / len(yl))
    Lbar = float((L * p).sum())
    beta = Lbar / (1 - Lbar)
    wbaru = 1.0 * beta ** (1 - L)
    R["ada"] = dict(stump=sb, fit=yh, ae=ae, D=D, L=L, p=p, Lbar=Lbar, beta=beta,
                    wbaru=wbaru, pbaru=wbaru / wbaru.sum(), uji=ada_x(xu))

    # ---------------- prediksi uji dalam rupiah
    Pt = P[uji]            # harga pada baris j = P[j]
    Pn = P[uji + 1]
    hasil = {}
    for nama, rhat in [("XGBoost", R["xgb"]["uji"]), ("AdaBoost.R2", R["ada"]["uji"])]:
        Ph = Pt * np.exp(rhat / BP)
        hasil[nama] = dict(rhat=rhat, Ph=Ph, e=Pn - Ph)
    hasil["Naive"] = dict(rhat=np.zeros_like(Pt), Ph=Pt.copy(), e=Pn - Pt)
    berubah = np.abs(Pn - Pt) >= 1
    for nama, h in hasil.items():
        e = h["e"]
        h["MAE"] = np.abs(e).mean()
        h["RMSE"] = math.sqrt((e**2).mean())
        h["MAPE"] = 100 * np.abs(e / Pn).mean()
        if nama != "Naive":
            arah_m = np.sign(h["Ph"] - Pt)
            arah_a = np.sign(Pn - Pt)
            c = (arah_m == arah_a) & berubah & (arah_m != 0)
            h["c"] = c
            h["n_arah"] = int(berubah.sum())
            h["arah"] = 100 * c[berubah].mean() if berubah.any() else float("nan")
    for nama in ("XGBoost", "AdaBoost.R2"):
        h = hasil[nama]
        h["vsN"] = (h["MAE"] / hasil["Naive"]["MAE"] - 1) * 100
        d = np.abs(h["e"]) - np.abs(hasil["Naive"]["e"])
        n = len(d)
        dbar = d.mean()
        c0 = ((d - dbar) ** 2).sum() / n
        dm = dbar / math.sqrt(c0 / n) if c0 > 0 else float("nan")
        hb = 1
        fk = math.sqrt((n + 1 - 2 * hb + hb * (hb - 1) / n) / n)
        dms = dm * fk
        pv = 2 * (1 - stats.t.cdf(abs(dms), n - 1)) if math.isfinite(dms) else float("nan")
        h.update(d=d, dbar=dbar, c0=c0, dm=dm, fk=fk, dms=dms, p=pv)
    R.update(Pt=Pt, Pn=Pn, berubah=berubah, hasil=hasil)

    # ---------------- Holm
    nm = ["XGBoost", "AdaBoost.R2"]
    urut = sorted(nm, key=lambda k: hasil[k]["p"])
    holm, lanjut = [], True
    for i, k in enumerate(urut, start=1):
        amb = ALPHA / (len(nm) - i + 1)
        tolak = lanjut and hasil[k]["p"] <= amb
        lanjut = lanjut and tolak
        holm.append(dict(nama=k, i=i, p=hasil[k]["p"], amb=amb, tolak=tolak))
    R["holm"] = holm
    return R


def layak(win):
    if len(win) != N_CANDLE:
        return False
    if (win.index[-1] - win.index[0]) != pd.Timedelta(minutes=N_CANDLE - 1):
        return False
    if win.isna().any().any():
        return False
    try:
        R = hitung(win)
    except (ZeroDivisionError, ValueError, FloatingPointError):
        return False
    if len(np.unique(R["x"][R["latih"] - 1])) < 6:
        return False
    gains = sorted((c["gain"] for c in R["xgb"]["cand"]), reverse=True)
    if gains[0] - gains[1] < 1e-6:                     # pemecahan terbaik harus tunggal
        return False
    sse = sorted(hitung_sse(R))
    if sse[1] - sse[0] < 1e-6:
        return False
    if R["berubah"].sum() < 3:
        return False
    if not (0 < R["ada"]["Lbar"] < 0.5):
        return False
    for k in ("XGBoost", "AdaBoost.R2"):
        if not math.isfinite(R["hasil"][k]["p"]):
            return False
    return True


def hitung_sse(R):
    xl = R["x"][R["latih"] - 1]
    yl = R["y"][R["latih"] - 1]
    ux = np.unique(xl)
    out = []
    for a, b in zip(ux[:-1], ux[1:]):
        kiri = xl < (a + b) / 2
        out.append(((yl[kiri] - yl[kiri].mean()) ** 2).sum()
                   + ((yl[~kiri] - yl[~kiri].mean()) ** 2).sum())
    return out


def cari(df, mulai):
    t = pd.Timestamp(mulai).ceil("5min")
    akhir = df.index.max()
    while t + pd.Timedelta(minutes=N_CANDLE - 1) <= akhir:
        win = df.loc[t: t + pd.Timedelta(minutes=N_CANDLE - 1)]
        if layak(win):
            return win
        t += pd.Timedelta(minutes=5)
    sys.exit("Tidak ada jendela 26 menit yang layak setelah --mulai.")


# ---------------------------------------------------------------- cek pustaka
def cocokkan(R):
    pesan = []
    xl = R["x"][R["latih"] - 1].reshape(-1, 1)
    yl = R["y"][R["latih"] - 1]
    xu = R["x"][R["uji"] - 1].reshape(-1, 1)
    try:
        import xgboost as xgb
        mdl = xgb.XGBRegressor(n_estimators=1, max_depth=1, learning_rate=NU,
                               reg_lambda=LAMBDA, gamma=GAMMA, min_child_weight=0,
                               base_score=R["xgb"]["F0"], tree_method="exact")
        mdl.fit(xl, yl)
        s = max(np.abs(mdl.predict(xl) - R["xgb"]["fit"]).max(),
                np.abs(mdl.predict(xu) - R["xgb"]["uji"]).max())
        pesan.append(f"xgboost {xgb.__version__}: selisih maks {s:.2e} bp "
                     + ("OK" if s < 1e-3 else "TIDAK COCOK"))
    except ImportError:
        pesan.append("xgboost tidak terpasang, dilewati")
    try:
        from sklearn.tree import DecisionTreeRegressor
        t = DecisionTreeRegressor(max_depth=1).fit(xl, yl)
        s = max(np.abs(t.predict(xl) - R["ada"]["fit"]).max(),
                np.abs(t.predict(xu) - R["ada"]["uji"]).max())
        pesan.append(f"sklearn pohon AdaBoost: selisih maks {s:.2e} bp "
                     + ("OK" if s < 1e-9 else "TIDAK COCOK"))
    except ImportError:
        pesan.append("scikit-learn tidak terpasang, dilewati")
    return pesan


# ---------------------------------------------------------------- LaTeX
def tabel(caption, label, kolom, header, baris, sep=4):
    out = [r"\begin{table}[htbp]", rf"  \caption{{{caption}}}", rf"  \label{{{label}}}",
           r"  \centering", r"  \begingroup", r"  \setstretch{1}\footnotesize",
           rf"  \setlength{{\tabcolsep}}{{{sep}pt}}",
           rf"  \begin{{tabular}}{{{kolom}}}", r"    \hline",
           "    " + " & ".join(header) + r" \\", r"    \hline"]
    for b in baris:
        out.append("    " + " & ".join(b) + r" \\")
    out += [r"    \hline", r"  \end{tabular}", r"  \endgroup",
            r"  \sumber{Diolah penulis}", r"\end{table}", ""]
    return "\n".join(out)


def latex(win, R):
    T = []
    w0, w1 = win.index[0], win.index[-1]
    P, x, y = R["P"], R["x"], R["y"]
    X, A, H = R["xgb"], R["ada"], R["hasil"]
    lat, uji, pur = R["latih"], R["uji"], R["purge"]

    T.append(r"""% Dibuat otomatis oleh contoh_manual.py. Jangan disunting manual;
% jalankan ulang skrip bila data berubah.
\section{Contoh Perhitungan Manual}
\label{sec:manual}
Subbab ini memberi contoh perhitungan untuk setiap tahap pada
Subbab~\ref{sec:fitur} sampai Subbab~\ref{sec:evaluasi}. Contoh memakai
26 \textit{candle} 1 menit BTC/IDR yang dikumpulkan pada """ + tgl(w0) + r""" pukul
""" + jam(w0) + "--" + jam(w1) + r""" UTC. Supaya dapat diikuti dengan tangan, contoh
memakai \textit{time frame} 1 menit, satu fitur, yaitu \texttt{ret\_lag1}, dan satu
pohon dengan kedalaman 1. Angka pada subbab ini hanya menunjukkan cara
menghitung dan bukan hasil penelitian.

\subsection{Agregasi \textit{Candle} 5 Menit dan Harga \textit{Typical}}
Tabel~\ref{tab:man-agregasi} memuat lima \textit{candle} 1 menit pertama dan
bar 5 menit yang dibentuk dengan Persamaan~\eqref{eq:agregasi}. Waktu ditulis
dalam UTC, harga dalam rupiah, dan volume dalam BTC.
""")
    rows = []
    for t, r in win.iloc[:5].iterrows():
        rows.append([jam(t), m(r.open, 0), m(r.high, 0), m(r.low, 0), m(r.close, 0), m(r.volume, 6)])
    b5 = win.iloc[:5]
    o5, h5, l5, c5, v5 = b5.open.iloc[0], b5.high.max(), b5.low.min(), b5.close.iloc[-1], b5.volume.sum()
    rows.append([r"\textbf{Bar 5 menit}", m(o5, 0), m(h5, 0), m(l5, 0), m(c5, 0), m(v5, 6)])
    T.append(tabel(r"Contoh Agregasi \textit{Candle} 1 Menit menjadi 5 Menit", "tab:man-agregasi",
                   "|l|r|r|r|r|r|", ["Waktu", "Open", "High", "Low", "Close", "Volume"],
                   rows, sep=2))
    p5 = (h5 + l5 + c5) / 3
    T.append(r"""Harga \textit{open} bar 5 menit diambil dari menit pertama, \textit{high}
merupakan nilai terbesar, \textit{low} nilai terkecil, \textit{close} diambil dari
menit terakhir, dan volume merupakan jumlah kelima menit. Harga \textit{typical}
bar tersebut menurut Persamaan~\eqref{eq:typical} merupakan
\begin{equation*}
  P = \frac{""" + f(h5, 0) + " + " + f(l5, 0) + " + " + f(c5, 0) + r"""}{3}
    = """ + f(p5) + r""" .
\end{equation*}
Contoh selanjutnya memakai dataset \textit{candle} 1 menit. Harga
\textit{typical} setiap menit dihitung dengan cara yang sama dan dimuat pada
Tabel~\ref{tab:man-harga}.

\subsection{\textit{Return}, Fitur, dan Target}
\textit{Return} satu bar dihitung dengan Persamaan~\eqref{eq:return} untuk
$h = 1$. Supaya angkanya mudah dibaca, \textit{return} ditulis dalam basis poin
(bp), dengan 1~bp $= 10^{-4}$. Sebagai contoh, \textit{return} pada
menit ke-$1$ merupakan
\begin{equation*}
  r = \ln\!\left(\frac{""" + f(P[1]) + "}{" + f(P[0]) + r"""}\right) \times 10^{4}
    = """ + f(R["r1"][1] * BP, 4) + r"""~\text{bp}.
\end{equation*}
""")
    rows = []
    for i, (t, r) in enumerate(win.iterrows()):
        rr = "--" if i == 0 else m(R["r1"][i] * BP, 4)
        rows.append([str(i), m(r.high, 0), m(r.low, 0), m(r.close, 0), m(P[i]), rr])
    T.append(tabel(r"Harga \textit{Typical} dan \textit{Return} 1 Menit", "tab:man-harga",
                   "|c|r|r|r|r|r|", ["$i$", "High", "Low", "Close", "$P$", "$r$ (bp)"],
                   rows, sep=3))
    T.append(r"""Pada baris ke-$j$, fitur \texttt{ret\_lag1} merupakan \textit{return} menit
ke-$j$, sedangkan targetnya merupakan \textit{return} menit ke-$(j+1)$. Fitur
hanya memakai harga sampai menit ke-$j$, sedangkan target memakai harga satu
menit sesudahnya. Dengan 26 menit, terbentuk $N = """ + str(R["N"]) + r"""$ baris, yaitu
$j = 1, \ldots, """ + str(R["N"]) + r"""$.

\subsection{Pembagian Data dan \textit{Purging}}
Menurut Persamaan~\eqref{eq:split}, blok uji final dimulai pada baris ke-$(\lfloor
0{,}8 \times """ + str(R["N"]) + r""" \rfloor + 1) = """ + str(R["ju"]) + r"""$, sehingga
blok uji berisi baris """ + str(uji[0]) + "--" + str(uji[-1]) + r""" ("""
             + str(len(uji)) + r""" baris). Baris """ + ", ".join(map(str, pur))
             + r""" memiliki target pada menit ke-""" + str(R["ju"]) + r""", yaitu tepat pada awal
blok uji, sehingga baris tersebut dibuang. Data latih berisi baris
""" + str(lat[0]) + "--" + str(lat[-1]) + " (" + str(len(lat)) + r""" baris).

\subsection{Satu Iterasi XGBoost}
Contoh ini memakai $\lambda = """ + f(LAMBDA, 0) + r"""$, $\gamma = """ + f(GAMMA, 0)
             + r"""$, dan $\nu = """ + f(NU, 1) + r"""$. Nilai awal $F_0$ diambil
dari rata-rata target data latih, yaitu $F_0 = """ + f(X["F0"], 4) + r"""$~bp. Karena
\textit{loss} kuadrat, $g_i = F_0 - y_i$ dan $q_i = 1$.
Tabel~\ref{tab:man-gq} memuat nilai tersebut.
""")
    rows = []
    for k, jj in enumerate(lat):
        rows.append([str(jj), m(x[jj - 1], 4), m(y[jj - 1], 4), m(X["g"][k], 4), m(1, 0)])
    rows.append([r"\textbf{Jumlah}", "", "", m(X["G"], 4), m(X["Q"], 0)])
    T.append(tabel(r"Gradien dan \textit{Hessian} Data Latih", "tab:man-gq",
                   "|c|r|r|r|r|", ["$j$", r"$x$ (bp)", r"$y$ (bp)", "$g_i$", "$q_i$"], rows))
    T.append(r"""Setiap nilai tengah antara dua nilai $x$ berurutan diuji sebagai titik
pemecahan. Data dengan $x$ lebih kecil dari titik pemecahan masuk ke daun kiri.
\textit{Gain} setiap titik dihitung dengan Persamaan~\eqref{eq:xgbgain} dan
dimuat pada Tabel~\ref{tab:man-gain}.
""")
    rows = []
    for c in X["cand"]:
        tanda = r"\textbf{" if c is X["best"] else ""
        tutup = "}" if tanda else ""
        rows.append([m(c["thr"], 4), str(c["nk"]), m(c["Gk"], 4), m(c["Qk"], 0),
                     m(c["Gn"], 4), m(c["Qn"], 0), tanda + m(c["gain"], 4) + tutup])
    T.append(tabel(r"\textit{Gain} Setiap Titik Pemecahan", "tab:man-gain", "|r|c|r|r|r|r|r|",
                   ["Titik (bp)", r"$n_{\text{kiri}}$", r"$G_{\text{kiri}}$", r"$Q_{\text{kiri}}$",
                    r"$G_{\text{kanan}}$", r"$Q_{\text{kanan}}$", "\\textit{Gain}"], rows))
    b = X["best"]
    T.append(r"""\textit{Gain} terbesar diperoleh pada titik $x < """ + f(b["thr"], 4) + r"""$~bp, yaitu
\begin{equation*}
  \textit{Gain} = \frac{1}{2}\left[
    \frac{(""" + f(b["Gk"], 4) + r""")^2}{""" + f(b["Qk"], 0) + r""" + 1}
  + \frac{(""" + f(b["Gn"], 4) + r""")^2}{""" + f(b["Qn"], 0) + r""" + 1}
  - \frac{(""" + f(X["G"], 4) + r""")^2}{""" + f(X["Q"], 0) + r""" + 1}
  \right] - 0 = """ + f(b["gain"], 4) + r""" .
\end{equation*}
Bobot kedua daun menurut Persamaan~\eqref{eq:xgbbobot} merupakan
\begin{equation*}
  w^{*}_{\text{kiri}} = -\frac{""" + f(b["Gk"], 4) + r"""}{""" + f(b["Qk"], 0)
             + r""" + 1} = """ + f(X["wk"], 4) + r""", \qquad
  w^{*}_{\text{kanan}} = -\frac{""" + f(b["Gn"], 4) + r"""}{""" + f(b["Qn"], 0)
             + r""" + 1} = """ + f(X["wn"], 4) + r""" .
\end{equation*}
Ramalan setelah satu pohon dihitung dengan Persamaan~\eqref{eq:boosting},
\begin{equation*}
  F_1 = """ + f(X["F0"], 4) + r""" + """ + f(NU, 1) + r""" \times w^{*} =
  \begin{cases}
    """ + f(X["F0"] + NU * X["wk"], 4) + r"""~\text{bp}, & x < """ + f(b["thr"], 4) + r"""~\text{bp},\\
    """ + f(X["F0"] + NU * X["wn"], 4) + r"""~\text{bp}, & \text{lainnya}.
  \end{cases}
\end{equation*}
LightGBM dan CatBoost juga menambahkan pohon secara bertahap seperti
Persamaan~\eqref{eq:boosting}. Perbedaannya terletak pada cara pohon
ditumbuhkan (Gambar~\ref{fig:leafwise}) dan bentuk pohonnya
(Gambar~\ref{fig:pohon-simetris}), yang baru tampak pada pohon dengan
kedalaman lebih dari 1.

\subsection{Satu Iterasi AdaBoost.R2}
Pohon AdaBoost.R2 dipilih dengan jumlah kuadrat galat terkecil. Supaya mudah
diikuti, contoh ini memakai seluruh data latih tanpa pengambilan sampel ulang,
sehingga $p_i = 1/""" + str(len(lat)) + r"""$. Titik pemecahan terbaik merupakan
$x < """ + f(A["stump"]["thr"], 4) + r"""$~bp, dengan ramalan """ + m(A["stump"]["mk"], 4)
             + r"""~bp di daun kiri dan """ + m(A["stump"]["mn"], 4) + r"""~bp di daun kanan.
Galat absolut terbesar merupakan $D = """ + f(A["D"], 4) + r"""$~bp. \textit{Loss}
linear tiap contoh dihitung dengan Persamaan~\eqref{eq:adaloss} dan dimuat pada
Tabel~\ref{tab:man-ada}.
""")
    rows = []
    for k, jj in enumerate(lat):
        rows.append([str(jj), m(y[jj - 1], 4), m(A["fit"][k], 4), m(A["ae"][k], 4),
                     m(A["L"][k], 4), m(A["wbaru"][k], 4)])
    T.append(tabel(r"Satu Iterasi AdaBoost.R2", "tab:man-ada", "|c|r|r|r|r|r|",
                   ["$j$", r"$y$ (bp)", r"$\hat{y}$ (bp)", r"$|\hat{y}-y|$", "$L_i$",
                    r"$w_i$ baru"], rows))
    T.append(r"""Rata-rata \textit{loss} dan rasio $\beta$ menurut
Persamaan~\eqref{eq:adabeta} merupakan
\begin{equation*}
  \bar{L} = \sum_i L_i p_i = """ + f(A["Lbar"], 4) + r""", \qquad
  \beta_1 = \frac{""" + f(A["Lbar"], 4) + r"""}{1 - """ + f(A["Lbar"], 4) + r"""} = """
             + f(A["beta"], 4) + r""" .
\end{equation*}
Karena $\bar{L} < 0{,}5$, pelatihan dapat dilanjutkan. Dengan bobot awal
$w_i = 1$, bobot baru dihitung dengan Persamaan~\eqref{eq:adabobot}, misalnya
untuk baris """ + str(lat[0]) + r""",
$w = 1 \times """ + f(A["beta"], 4) + "^{1 - " + f(A["L"][0], 4) + "} = " + f(A["wbaru"][0], 4)
             + r"""$. Contoh dengan galat kecil mendapat bobot yang lebih kecil, sehingga
pohon berikutnya lebih banyak belajar dari contoh yang sulit. Bobot pohon ini
pada ramalan akhir merupakan $\log(1/\beta_1) = """ + f(math.log(1 / A["beta"]), 4) + r"""$.
Dengan satu pohon, ramalan AdaBoost.R2 sama dengan ramalan pohon tersebut.

\subsection{Prediksi dan Konversi ke Rupiah}
Ramalan \textit{return} pada blok uji dikembalikan ke rupiah dengan
Persamaan~\eqref{eq:konversi}. Sebagai contoh, pada baris """ + str(uji[0]) + r""",
ramalan XGBoost merupakan
\begin{equation*}
  \hat{P} = """ + f(R["Pt"][0]) + r""" \times \exp\!\left(""" + f(H["XGBoost"]["rhat"][0], 4)
             + r""" \times 10^{-4}\right) = """ + f(H["XGBoost"]["Ph"][0]) + r""" .
\end{equation*}
Naive meramalkan harga terakhir, yaitu """ + m(R["Pt"][0]) + r""".
Tabel~\ref{tab:man-uji} memuat ramalan dan galat pada seluruh blok uji.
""")
    rows = []
    for k, jj in enumerate(uji):
        rows.append([str(jj), m(R["Pt"][k]), m(R["Pn"][k]),
                     m(H["XGBoost"]["Ph"][k]), m(H["AdaBoost.R2"]["Ph"][k])])
    T.append(tabel("Ramalan pada Blok Uji", "tab:man-uji", "|c|r|r|r|r|",
                   ["$j$", "$P_t$", "$P_{t+1}$", r"$\hat{P}$ XGBoost", r"$\hat{P}$ AdaBoost.R2"],
                   rows))
    T.append(r"""Galat $e_t = P_{t+1} - \hat{P}$ setiap ramalan dimuat pada
Tabel~\ref{tab:man-galat}, bersama selisih \textit{loss} absolut
$d_t = |e_{\text{model}}| - |e_{\text{Naive}}|$ yang dipakai pada uji
Diebold-Mariano.
""")
    rows = []
    for k, jj in enumerate(uji):
        rows.append([str(jj), m(H["Naive"]["e"][k]), m(H["XGBoost"]["e"][k]),
                     m(H["AdaBoost.R2"]["e"][k]), m(H["XGBoost"]["d"][k]),
                     m(H["AdaBoost.R2"]["d"][k])])
    T.append(tabel("Galat dan Selisih \\textit{Loss} pada Blok Uji", "tab:man-galat",
                   "|c|r|r|r|r|r|",
                   ["$j$", r"$e$ Naive", r"$e$ XGBoost", r"$e$ AdaBoost.R2",
                    r"$d_t$ XGBoost", r"$d_t$ AdaBoost.R2"], rows))
    nN = H["Naive"]
    ab = [f(abs(v)) for v in nN["e"]]
    absN = " + ".join(ab[:3]) + r" \\ &\qquad + " + " + ".join(ab[3:])
    T.append(r"""\subsection{Perhitungan Metrik Evaluasi}
MAE Naive menurut Persamaan~\eqref{eq:mae} merupakan
\begin{equation*}
  \begin{aligned}
  \text{MAE}_{\text{Naive}} &= \frac{1}{""" + str(len(uji)) + r"""}\bigl(""" + absN + r"""\bigr) \\
  &= """ + f(nN["MAE"]) + r""" .
  \end{aligned}
\end{equation*}
MAE vs Naive untuk XGBoost menurut Persamaan~\eqref{eq:maenaive} merupakan
\begin{equation*}
  \left(\frac{""" + f(H["XGBoost"]["MAE"]) + "}{" + f(nN["MAE"]) + r"""} - 1\right)
  \times 100\% = """ + f(H["XGBoost"]["vsN"]) + r"""\% .
\end{equation*}
Untuk akurasi arah, """ + str(H["XGBoost"]["n_arah"]) + r""" dari """ + str(len(uji))
             + r""" baris uji memiliki harga yang berubah, sehingga $n = """
             + str(H["XGBoost"]["n_arah"]) + r"""$ pada Persamaan~\eqref{eq:arah}.
Tabel~\ref{tab:man-metrik} merangkum seluruh metrik.
""")
    def arah(k):
        h = H[k]
        return m(h["arah"], 2) if math.isfinite(h["arah"]) else "--"
    rows = [
        ["MAE (Rp)", m(nN["MAE"]), m(H["XGBoost"]["MAE"]), m(H["AdaBoost.R2"]["MAE"])],
        ["RMSE (Rp)", m(nN["RMSE"]), m(H["XGBoost"]["RMSE"]), m(H["AdaBoost.R2"]["RMSE"])],
        [r"MAPE (\%)", m(nN["MAPE"], 6), m(H["XGBoost"]["MAPE"], 6), m(H["AdaBoost.R2"]["MAPE"], 6)],
        [r"MAE vs Naive (\%)", "--", m(H["XGBoost"]["vsN"]), m(H["AdaBoost.R2"]["vsN"])],
        [r"Akurasi arah (\%)", "--", arah("XGBoost"), arah("AdaBoost.R2")],
    ]
    T.append(tabel("Rangkuman Metrik pada Contoh", "tab:man-metrik", "|l|r|r|r|",
                   ["Metrik", "Naive", "XGBoost", "AdaBoost.R2"], rows))
    hx = H["XGBoost"]
    T.append(r"""\subsection{Uji Diebold-Mariano dan Koreksi Holm}
Uji dihitung dengan \textit{loss} absolut. Dari nilai $d_t$ XGBoost pada
Tabel~\ref{tab:man-galat}, diperoleh $\bar{d} = """ + f(hx["dbar"]) + r"""$ dan
$\hat{\phi}_0 = """ + f(hx["c0"]) + r"""$. Karena $h_b = 1$, tidak ada autokovarians
lag lain, sehingga menurut Persamaan~\eqref{eq:dm}
\begin{equation*}
  \text{DM} = \frac{""" + f(hx["dbar"]) + r"""}{\sqrt{""" + f(hx["c0"]) + "/" + str(len(uji))
             + r"""}} = """ + f(hx["dm"], 4) + r""" .
\end{equation*}
Faktor koreksi HLN pada Persamaan~\eqref{eq:hln} dengan $n = """ + str(len(uji))
             + r"""$ dan $h_b = 1$ merupakan $\sqrt{(""" + str(len(uji)) + r""" + 1 - 2)/"""
             + str(len(uji)) + r"""} = """ + f(hx["fk"], 4) + r"""$, sehingga statistik
terkoreksinya """ + m(hx["dms"], 4) + r""". Nilai $p$ dua sisi dari distribusi $t$
berderajat bebas """ + str(len(uji) - 1) + r""" merupakan """ + m(hx["p"], 4) + r""".
Tabel~\ref{tab:man-dm} memuat hasil kedua model.
""")
    rows = []
    for k in ("XGBoost", "AdaBoost.R2"):
        h = H[k]
        rows.append([k, m(h["dbar"]), m(h["c0"]), m(h["dm"], 4), m(h["dms"], 4), m(h["p"], 4)])
    T.append(tabel("Uji Diebold-Mariano pada Contoh", "tab:man-dm", "|l|r|r|r|r|r|",
                   ["Model", r"$\bar{d}$", r"$\hat{\phi}_0$", "DM", r"DM$^{*}$", "$p$"], rows))
    hl = R["holm"]
    kal = []
    for e in hl:
        kal.append(rf"$p_{{({e['i']})}} = {f(e['p'], 4)}$ ({e['nama']}) dibandingkan dengan "
                   rf"$0{{,}}05/{len(hl) - e['i'] + 1} = {f(e['amb'], 4)}$")
    n_tolak = sum(e["tolak"] for e in hl)
    if n_tolak == 0:
        simpul = (r"Nilai $p$ terkecil sudah lebih besar daripada ambangnya, sehingga tidak ada "
                  r"hipotesis yang ditolak dan pengujian berhenti. Kedua model dinyatakan "
                  r"tidak berbeda secara signifikan dari Naive.")
    else:
        simpul = (rf"Sebanyak {n_tolak} hipotesis ditolak. Status setiap model lalu ditentukan "
                  r"dari tanda MAE vs Naive dan statistik DM sesuai aturan pada "
                  r"Subbab~\ref{sec:evaluasi}.")
    T.append(r"""Koreksi Holm diterapkan pada kedua nilai $p$ dengan
Persamaan~\eqref{eq:holm} dan $q = 2$. Setelah diurutkan, """ + "; lalu ".join(kal) + ". "
             + simpul + r""" Dengan hanya """ + str(len(uji)) + r""" data uji, hasil ini wajar dan
tidak menggambarkan hasil penelitian, yang memakai seluruh blok uji final.
""")
    return "\n".join(T)


def main():
    a = argparse.ArgumentParser()
    a.add_argument("--csv", required=True)
    a.add_argument("--mulai", required=True, help="waktu UTC, mis. '2026-10-14 03:00'")
    a.add_argument("--out", default="bab3-contoh-perhitungan.tex")
    a = a.parse_args()
    df = baca(a.csv)
    win = cari(df, a.mulai)
    R = hitung(win)
    for s in cocokkan(R):
        print(s)
    with open(a.out, "w", encoding="utf-8") as fh:
        fh.write(latex(win, R))
    h = R["hasil"]
    print(f"Jendela: {win.index[0]} -- {win.index[-1]} UTC")
    print(f"Latih {len(R['latih'])} baris, purging {list(R['purge'])}, uji {list(R['uji'])}")
    print(f"MAE Naive {h['Naive']['MAE']:.2f}, XGB {h['XGBoost']['MAE']:.2f}, "
          f"Ada {h['AdaBoost.R2']['MAE']:.2f}")
    print(f"Tersimpan: {a.out}")


if __name__ == "__main__":
    main()
