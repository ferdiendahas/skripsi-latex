# Konteks Sistem Pengumpulan Data (Collector) — v3.0

> **Fungsi file ini:** konteks lengkap sistem yang mengumpulkan data BTC/IDR dari Indodax untuk skripsi v3.0: cara kerja, struktur database, asal "ticker 5 menit" dan "candle 1 menit", keterbatasan, kalimat aman untuk Bab 3, dan **source code lengkap** keempat file collector.
>
> **Dibuat:** 4 November 2026. **Pasangan dokumen:** source code eksperimen (`prediksi_btc`) ada di Lampiran B `hasil_eksperimen_v3.0.md`. Konteks umum ada di `konteks_skripsi_v3.0.md`.
>
> **Notasi:** BTC/IDR = pasar spot Indodax. Semua timestamp di database dalam UTC. WIB = UTC+7.

---

## 1. Ringkasan satu paragraf

Data dikumpulkan sendiri (data primer) dari **API publik Indodax**, tanpa API key, login, atau akses saldo. Sebuah VPS Ubuntu menjalankan `collector.py --once` lewat **cron tiap 1 menit**. Setiap kali jalan, collector menyimpan (1) satu **snapshot ticker** ke tabel `ticker_snapshots` dan (2) **candle 1 menit** ke tabel `ohlc_1m` di SQLite. Ekspor CSV untuk eksperimen dilakukan dengan perintah `indodax ekspor`, yang menghasilkan **ticker 5 menit** (snapshot per menit disaring hanya yang menit-nya kelipatan 5) dan **candle 1 menit**. Pengumpulan berjalan sampai Februari 2027.

## 2. File

| File | Tempat | Fungsi |
|---|---|---|
| `collector.py` | `/opt/indodax/` di VPS | Mengambil ticker + candle 1 menit, menyimpan ke SQLite. Mode `--once` (cron) atau loop |
| `cek_status.py` | `/opt/indodax/` | Ringkasan jumlah data, keterlambatan, celah candle, candle per hari; `export` = CSV mentah semua baris |
| `setup_vps.sh` | dijalankan sekali | Instal paket, user `collector` tanpa hak admin, venv, zona waktu UTC, cron + `flock`, firewall hanya SSH |
| `indodax` | perintah shell di VPS | `indodax cek` (cek cepat dalam WIB) dan `indodax ekspor` (CSV untuk eksperimen ke `~/ekspor/`) |
| `data/indodax_btcidr.db` | `/opt/indodax/data/` | Database SQLite (mode WAL) |
| `data/collector.log` | `/opt/indodax/data/` | Log berputar 5 MB × 3 cadangan, waktu UTC |

SHA-256 file yang didokumentasikan di sini (salinan 4 Nov 2026):
```text
2ac123eee0130f1532aea2012c1917b7dd9c7ca19935ffd0ba63037af1ab36da  collector.py
6225bceeeee3d75814d1365baf465bc604b68d5c990288c599d9610a250cde9c  cek_status.py
55851f4c8e1cf646c6776491a3e6aac651eb475b506de0d6f303136c1a91ace5  setup_vps.sh
63fd099c56f778514aa2cfbffaafebb20c948212c5738caffeac474c988e6593  indodax
```

## 3. Sumber API

| Endpoint | Isi | Dipakai untuk |
|---|---|---|
| `https://indodax.com/api/btc_idr/ticker` | Snapshot saat itu: `last`, `buy` (bid), `sell` (ask), `high`/`low` 24 jam, `vol_btc`/`vol_idr` 24 jam, `server_time` | `ticker_snapshots` |
| `https://indodax.com/tradingview/history_v2?symbol=BTCIDR&tf=1&from=..&to=..` | Candle OHLCV | `ohlc_1m` |

**Time frame candle yang disediakan Indodax** (parameter `tf`, dokumentasi resmi Public RestAPI `btcid/indodax-official-api-docs`): `1`, `15`, `30`, `60`, `240`, `1D`, `3D`, `1W`. **Tidak ada candle 5 menit.** Karena itu collector mengambil `tf=1`, resolusi terkecil, dan time frame lain dapat dibentuk dengan resample.

**Arti "ticker":** di sini bukan kode aset (ticker symbol, mis. BTCIDR), melainkan nama endpoint yang memberi ringkasan harga terkini sebuah pasangan. `btc_idr` di URL = kode pasangan; `/ticker` = jenis data. Di skripsi sebut "data snapshot ticker".

## 4. Struktur database

**`ticker_snapshots`** (satu baris per pengambilan, ±1 per menit)

| Kolom | Arti |
|---|---|
| `id` | Auto increment |
| `fetched_at_ms` | Jam VPS saat diambil (UTC, milidetik) |
| `server_time` | Jam server Indodax (detik) |
| `last_price` | Harga transaksi terakhir |
| `buy`, `sell` | Bid tertinggi, ask terendah |
| `high_24h`, `low_24h` | Tertinggi/terendah 24 jam bergulir |
| `vol_btc_24h`, `vol_idr_24h` | Volume 24 jam bergulir |

**`ohlc_1m`** (satu baris per menit, kunci = awal menit)

| Kolom | Arti |
|---|---|
| `t` | Awal candle (unix detik, UTC). Candle `t`=10:04 mencakup 10:04:00–10:04:59 |
| `open_p`, `high_p`, `low_p`, `close_p` | OHLC menit itu |
| `volume` | Volume BTC menit itu |
| `updated_at_ms` | Kapan baris terakhir ditulis ulang |

## 5. Cara kerja per menit

1. Cron memanggil `collector.py --once` di detik ~0 setiap menit. `flock` dan kunci port `47821` mencegah dua proses berjalan bersamaan.
2. **Ticker** diambil lalu langsung di-*insert*.
3. **Candle** diambil untuk rentang `MAX(t) − 5 menit` sampai sekarang (maks. 6 jam ke belakang), lalu di-*upsert*. Artinya 5 menit terakhir selalu ditulis ulang, sehingga candle yang masih terbentuk saat diambil akan dikoreksi ke nilai finalnya pada menit-menit berikutnya. Kalau VPS sempat mati ≤ 6 jam, menit yang terlewat ditambal otomatis.
4. Ticker dan candle diproses terpisah: kalau salah satu gagal, yang lain tetap tersimpan.
5. Tiap request dicoba sampai 3 kali (jeda 5 dan 15 detik; 60 detik kalau kena 429).

## 6. Dari mana "ticker 5 menit" dan "candle 1 menit"

| Data | Di database | Di CSV eksperimen | Penyebab |
|---|---|---|---|
| Ticker | **per 1 menit** | **per 5 menit** | Disaring saat ekspor: `strftime('%M', fetched_at) % 5 = 0` (hanya menit :00, :05, :10, ...) |
| Candle | per 1 menit | per 1 menit | Indodax tidak menyediakan candle 5 menit; 1 menit = resolusi terkecil |

Konsekuensi:
- **Ticker 1 menit tersedia** di database (4 dari 5 snapshot hanya dibuang saat ekspor). Bisa diekspor dengan `cek_status.py export` atau menghapus filter `% 5 = 0` di `indodax`.
- **Candle 5 menit** (dan TF lain) dapat dibentuk sah dari candle 1 menit: open = open menit pertama, high = maks, low = min, close = close menit terakhir, volume = jumlah.
- Data yang sudah dipakai (eksperimen 92 run): `btcidr_candle_1menit.csv` 17.258 baris dan `btcidr_ticker_5menit.csv` 3.451 baris, rentang 9–21 Okt 2026; periode eksperimen 14–20 Okt 2026 UTC, 0 bar hilang.

Format CSV ekspor:
- Ticker: `waktu_utc, waktu_wib, last_price, buy, sell, high_24h, low_24h, vol_btc_24h, vol_idr_24h`
- Candle: `waktu_utc, waktu_wib, open, high, low, close, volume`

## 7. Keterbatasan dan catatan (untuk Bab 3 / batasan)

1. **Ticker tidak bisa ditambal.** Endpoint ticker hanya memberi kondisi saat ini; kalau satu pengambilan gagal total, snapshot menit itu hilang permanen. Candle bisa ditambal sampai 6 jam ke belakang.
2. **Timestamp ticker = jam VPS** (`fetched_at_ms`), bukan jam transaksi. Zona waktu VPS diset UTC; `server_time` Indodax ikut disimpan untuk pengecekan selisih jam.
3. **Retry bisa menggeser waktu ambil** beberapa detik (maks. ±20 detik), tapi tetap di menit yang sama, jadi filter kelipatan 5 tetap aman.
4. **Ticker dan candle tidak sejajar waktunya.** Snapshot ticker 10:05:01 mencerminkan kondisi ~10:05, sedangkan candle `t`=10:04 berakhir 10:04:59. Kalau kelak keduanya digabung jadi satu dataset, sejajarkan berdasarkan waktu *selesai* candle agar tidak ada kebocoran informasi.
5. **Celah candle** bisa berarti tidak ada transaksi di menit itu (Indodax tidak membuat candle kosong), bukan selalu collector mati. `cek_status.py` menandainya.
6. **Statistik 24 jam di ticker bergulir**, bukan per periode, sehingga berbeda dengan volume candle.
7. Hanya API publik; tidak ada data order book penuh atau data per transaksi (trades).

## 8. Kalimat aman untuk Bab 3

> Data penelitian merupakan data primer yang dikumpulkan secara mandiri dari API publik Indodax untuk pasangan BTC/IDR. Pengumpulan dilakukan otomatis oleh program Python yang dijalankan setiap menit melalui penjadwal cron pada server virtual (VPS) berzona waktu UTC. Setiap menit program menyimpan dua jenis data ke basis data SQLite: (1) snapshot ticker, yang memuat harga transaksi terakhir, harga beli tertinggi (bid), harga jual terendah (ask), serta harga tertinggi, terendah, dan volume 24 jam; dan (2) candle 1 menit yang memuat harga pembukaan, tertinggi, terendah, penutupan, dan volume. Candle 1 menit dipilih karena merupakan resolusi terkecil yang disediakan Indodax (time frame yang tersedia: 1, 15, 30, 60, dan 240 menit, serta harian dan mingguan). Untuk eksperimen, snapshot ticker diambil setiap 5 menit, sedangkan time frame lain dapat dibentuk dengan agregasi candle 1 menit.

Jawaban singkat kalau ditanya "kenapa ticker 5 menit, bukan candle 5 menit?":
> Indodax tidak menyediakan candle 5 menit, jadi saya mengambil candle 1 menit sebagai resolusi terkecil. Ticker saya simpan tiap menit dan saya ambil sampel tiap 5 menit karena ticker memuat bid dan ask, sehingga bisa dihitung harga tengah dan spread. Candle 5 menit bisa dibentuk dari candle 1 menit kalau perlu dibandingkan.

## 9. Perintah penting

```bash
# di VPS
indodax cek                     # jumlah data, rentang (WIB), data terakhir, 5 harga terakhir, error 24 jam
indodax ekspor                  # CSV ticker 5 menit + candle 1 menit ke ~/ekspor/
sudo tail -f /opt/indodax/data/collector.log
sudo -u collector /opt/indodax/venv/bin/python /opt/indodax/cek_status.py          # celah candle, candle per hari
sudo -u collector /opt/indodax/venv/bin/python /opt/indodax/cek_status.py export   # CSV mentah semua baris (ticker per menit)

# di Mac
scp ubuntu@<IP_VPS>:'~/ekspor/*<stamp>.csv' ~/Documents/cronjob/
```

## 10. Opsi pengembangan (belum dikerjakan, menunggu keputusan)

- Tambah dataset `candle_5m` (resample candle 1 menit) di `prediksi_btc`.
- Tambah dataset `ticker_1m` (ekspor tanpa filter `% 5 = 0`).
- Keduanya menambah run Tahap 1. Karena aturan sudah dikunci 27 Okt 2026, penambahan ini harus ditulis sebagai eksperimen tambahan/eksploratif, kecuali desain diulang dari awal dengan data sampai Februari.

---

## Lampiran: source code lengkap

### `collector.py`

```python
"""
collector.py — penambang data BTC/IDR Indodax 24/7 (VPS Linux / Windows / Mac).

Mode cron (VPS):   python collector.py --once   -> ambil sekali lalu keluar (dipanggil cron tiap menit)
Mode loop:         python collector.py          -> jalan terus sendiri

Tiap menit:
  1) snapshot ticker  -> tabel ticker_snapshots
  2) candle 1 menit   -> tabel ohlc_1m (upsert; otomatis menambal menit yang terlewat,
                         termasuk setelah laptop restart, maks. BACKFILL_MAX_H jam ke belakang)

KEAMANAN: hanya PUBLIC API Indodax. Tidak ada API key, login, saldo, atau wallet.
Satu-satunya dependensi: requests (pip install requests).
"""
import logging, socket, sqlite3, sys, time
from logging.handlers import RotatingFileHandler
from pathlib import Path

import requests

TICKER_URL = "https://indodax.com/api/btc_idr/ticker"          # link dari dosbing
HISTORY_URL = "https://indodax.com/tradingview/history_v2"      # dok resmi GitHub Indodax
SYMBOL = "BTCIDR"
INTERVAL_S = 60
BACKFILL_MAX_H = 6          # jarak tambal maksimum per request setelah laptop mati/offline
LOCK_PORT = 47821           # mencegah 2 instance jalan bersamaan

BASE = Path(__file__).resolve().parent
DATA = BASE / "data"
DATA.mkdir(exist_ok=True)
DB = DATA / "indodax_btcidr.db"

log = logging.getLogger("collector")
log.setLevel(logging.INFO)
_fh = RotatingFileHandler(DATA / "collector.log", maxBytes=5_000_000, backupCount=3, encoding="utf-8")
_fh.setFormatter(logging.Formatter("%(asctime)s UTC %(levelname)s %(message)s"))
logging.Formatter.converter = time.gmtime
log.addHandler(_fh)
log.addHandler(logging.StreamHandler(sys.stdout))


def single_instance():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(("127.0.0.1", LOCK_PORT))
    except OSError:
        log.warning("Collector lain sudah jalan. Keluar.")
        sys.exit(0)
    return s  # harus tetap direferensikan selama program hidup


def init_db():
    con = sqlite3.connect(DB, timeout=30)
    con.execute("PRAGMA journal_mode=WAL")
    con.executescript("""
    CREATE TABLE IF NOT EXISTS ticker_snapshots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fetched_at_ms INTEGER NOT NULL,      -- jam laptop (UTC, ms)
        server_time INTEGER,                 -- jam server Indodax (detik)
        last_price REAL, buy REAL, sell REAL, high_24h REAL, low_24h REAL,
        vol_btc_24h REAL, vol_idr_24h REAL);
    CREATE INDEX IF NOT EXISTS ix_tick_time ON ticker_snapshots(fetched_at_ms);
    CREATE TABLE IF NOT EXISTS ohlc_1m (
        t INTEGER PRIMARY KEY,               -- awal candle (unix detik, UTC)
        open_p REAL, high_p REAL, low_p REAL, close_p REAL, volume REAL,
        updated_at_ms INTEGER);
    """)
    con.commit()
    return con


def make_session():
    s = requests.Session()
    s.headers["User-Agent"] = "skripsi-upnvjt-data-collector/1.0"
    return s


MAX_TRIES = 3               # 1 percobaan + 2 kesempatan ulang
RETRY_WAIT_S = (5, 15)      # jeda sebelum percobaan ke-2 dan ke-3


def get_json(sess, url, params=None):
    """GET + parse JSON, dicoba ulang s.d. MAX_TRIES kali kalau gagal."""
    for attempt in range(1, MAX_TRIES + 1):
        try:
            r = sess.get(url, params=params, timeout=15)   # verifikasi SSL default: aktif
            if r.status_code == 429:
                raise RuntimeError("429 Too Many Requests")
            r.raise_for_status()
            return r.json()
        except Exception as e:
            if attempt == MAX_TRIES:
                raise RuntimeError(f"gagal {MAX_TRIES}x: {type(e).__name__}: {e}") from e
            wait = 60 if "429" in str(e) else RETRY_WAIT_S[attempt - 1]
            log.warning(f"percobaan {attempt}/{MAX_TRIES} gagal ({type(e).__name__}: {e}); "
                        f"ulang dalam {wait} dtk")
            time.sleep(wait)


def save_ticker(sess, con, now_ms):
    t = get_json(sess, TICKER_URL)["ticker"]
    con.execute(
        "INSERT INTO ticker_snapshots (fetched_at_ms, server_time, last_price, buy, sell,"
        " high_24h, low_24h, vol_btc_24h, vol_idr_24h) VALUES (?,?,?,?,?,?,?,?,?)",
        (now_ms, t.get("server_time"), float(t["last"]), float(t["buy"]), float(t["sell"]),
         float(t["high"]), float(t["low"]), float(t.get("vol_btc") or 0), float(t.get("vol_idr") or 0)))
    con.commit()
    return f"last={t['last']}"


def save_ohlc(sess, con, now_ms):
    last_t = con.execute("SELECT MAX(t) FROM ohlc_1m").fetchone()[0]
    to = int(time.time())
    frm = max((last_t or to) - 5 * 60, to - BACKFILL_MAX_H * 3600)
    rows = get_json(sess, HISTORY_URL, {"symbol": SYMBOL, "tf": "1", "from": frm, "to": to})
    con.executemany(
        "INSERT INTO ohlc_1m (t, open_p, high_p, low_p, close_p, volume, updated_at_ms)"
        " VALUES (?,?,?,?,?,?,?) ON CONFLICT(t) DO UPDATE SET open_p=excluded.open_p,"
        " high_p=excluded.high_p, low_p=excluded.low_p, close_p=excluded.close_p,"
        " volume=excluded.volume, updated_at_ms=excluded.updated_at_ms",
        [(int(c["Time"]), float(c["Open"]), float(c["High"]), float(c["Low"]),
          float(c["Close"]), float(c["Volume"]), now_ms) for c in rows])
    con.commit()
    return f"candle={len(rows)}"


def collect_once(sess, con):
    """Ticker dan candle diambil terpisah: kalau satu gagal, yang lain tetap disimpan."""
    now_ms = int(time.time() * 1000)
    status, errors = [], []
    for name, job in (("ticker", save_ticker), ("ohlc", save_ohlc)):
        try:
            status.append(job(sess, con, now_ms))
        except Exception as e:
            con.rollback()
            errors.append(f"{name}: {e}")
    if errors:
        msg = " | ".join(errors)
        if status:
            log.error(f"sebagian gagal -> {msg}")
        else:
            raise RuntimeError(msg)
    return " ".join(status)


def main():
    _lock = single_instance()
    con = init_db()
    sess = make_session()
    if "--once" in sys.argv:             # mode cron: jalan sekali lalu keluar
        try:
            log.info(collect_once(sess, con))
        except Exception as e:
            log.error(f"gagal: {type(e).__name__}: {e}")
            sys.exit(1)
        return
    log.info(f"Collector mulai. DB: {DB}")
    fails = 0
    while True:
        try:
            msg = collect_once(sess, con)
            if fails:
                log.info(f"Pulih setelah {fails} kegagalan beruntun")
            fails = 0
            log.info(msg)
        except Exception as e:           # jangan pernah mati karena 1 error
            fails += 1
            con.rollback()
            log.error(f"gagal #{fails}: {type(e).__name__}: {e}")
            if "429" in str(e):
                time.sleep(60)
            sess = make_session()
        # tidur sampai detik ke-5 menit berikutnya (candle menit sebelumnya sudah tutup)
        time.sleep(INTERVAL_S - (time.time() % INTERVAL_S) + 5)


if __name__ == "__main__":
    main()
```

### `cek_status.py`

```python
"""
cek_status.py — cek kesehatan hasil tambang + ekspor CSV.
  python cek_status.py           -> ringkasan & celah data
  python cek_status.py export    -> tulis CSV ke folder data/
"""
import sqlite3, sys, time
from pathlib import Path
import pandas as pd

DATA = Path(__file__).resolve().parent / "data"
con = sqlite3.connect(DATA / "indodax_btcidr.db")

o = pd.read_sql("SELECT * FROM ohlc_1m ORDER BY t", con)
k = pd.read_sql("SELECT * FROM ticker_snapshots ORDER BY fetched_at_ms", con)
if o.empty:
    sys.exit("Belum ada candle.")

o["ts"] = pd.to_datetime(o["t"], unit="s", utc=True)
k["ts"] = pd.to_datetime(k["fetched_at_ms"], unit="ms", utc=True)
now = pd.Timestamp(time.time(), unit="s", tz="UTC")

print(f"Candle 1m : {len(o):,}  ({o.ts.min()} -> {o.ts.max()})")
print(f"Ticker    : {len(k):,}  (terakhir {k.ts.max()})")
lag = (now - o.ts.max()).total_seconds() / 60
print(f"Candle terakhir {lag:.1f} menit lalu -> {'OK' if lag < 5 else 'CEK COLLECTOR!'}")

gap = o["t"].diff().div(60).sub(1)
g = o.loc[gap > 0, ["ts"]].assign(menit_hilang=gap[gap > 0].astype(int))
print(f"\nCelah candle: {len(g)} celah, total {int(g.menit_hilang.sum()) if len(g) else 0} menit")
if len(g):
    print(g.tail(10).to_string(index=False))
    print("(Celah bisa juga berarti memang tidak ada transaksi di menit itu — cek volume sekitar.)")

per_hari = o.groupby(o.ts.dt.date).size()
print("\nCandle per hari UTC (ideal 1440):")
print(per_hari.to_string())

if len(sys.argv) > 1 and sys.argv[1] == "export":
    stamp = now.strftime("%Y%m%d_%H%M")
    o.drop(columns="ts").to_csv(DATA / f"indodax_btcidr_ohlc1m_{stamp}.csv", index=False)
    k.drop(columns="ts").to_csv(DATA / f"indodax_btcidr_ticker_{stamp}.csv", index=False)
    print(f"\nCSV tersimpan di {DATA}")
```

### `setup_vps.sh`

```bash
#!/usr/bin/env bash
# setup_vps.sh — pasang collector Indodax di VPS Ubuntu/Debian.
# Jalankan sebagai root, di folder yang berisi collector.py & cek_status.py:
#   sudo bash setup_vps.sh
set -euo pipefail
APP=/opt/indodax
USR=collector

echo "== 1. Paket sistem"
apt-get update -qq
apt-get install -y -qq python3 python3-venv cron ufw sqlite3 >/dev/null

echo "== 2. User khusus tanpa hak admin (collector tidak jalan sebagai root)"
id -u $USR >/dev/null 2>&1 || useradd --system --create-home --shell /usr/sbin/nologin $USR

echo "== 3. Salin script + virtualenv"
mkdir -p $APP
cp collector.py cek_status.py $APP/
python3 -m venv $APP/venv
$APP/venv/bin/pip install -q requests pandas
chown -R $USR:$USR $APP

echo "== 4. Zona waktu server = UTC (semua timestamp data UTC)"
timedatectl set-timezone UTC || true

echo "== 5. Cron tiap 1 menit (flock mencegah 2 proses tumpang tindih)"
cat > /etc/cron.d/indodax <<CRON
* * * * * $USR /usr/bin/flock -n /tmp/indodax.lock $APP/venv/bin/python $APP/collector.py --once >/dev/null 2>&1
CRON
chmod 644 /etc/cron.d/indodax
systemctl enable --now cron >/dev/null

echo "== 6. Firewall: hanya SSH yang dibuka (collector tidak butuh port masuk)"
ufw allow OpenSSH >/dev/null
ufw --force enable >/dev/null

echo
echo "Selesai. Tunggu 2-3 menit, lalu cek:"
echo "  sudo tail -f $APP/data/collector.log"
echo "  sudo -u $USR $APP/venv/bin/python $APP/cek_status.py"
```

### `indodax`

```bash
#!/usr/bin/env bash
# indodax — perintah singkat untuk cek & ekspor data collector.
#   indodax cek      -> jumlah data, rentang waktu, 5 harga terakhir, error 24 jam
#   indodax ekspor   -> buat CSV (ticker 5 menit + candle 1 menit) di ~/ekspor/
set -euo pipefail
DB=${INDODAX_DB:-/opt/indodax/data/indodax_btcidr.db}
LOG=$(dirname "$DB")/collector.log
VPS_IP=43.173.15.230
RUN=${INDODAX_RUN-"sudo -u collector"}        # baca DB sebagai user collector
q() { $RUN sqlite3 "$@"; }
WIB="'unixepoch','+7 hours'"

cek() {
  echo "== Jumlah data"
  q "$DB" "SELECT 'Snapshot 5 menit : ' || COUNT(*) FROM ticker_snapshots
           WHERE CAST(strftime('%M', fetched_at_ms/1000, 'unixepoch') AS INTEGER) % 5 = 0;
           SELECT 'Candle 1 menit   : ' || COUNT(*) FROM ohlc_1m;"
  echo; echo "== Rentang waktu (WIB)"
  q "$DB" "SELECT 'Snapshot : ' || datetime(MIN(fetched_at_ms)/1000,$WIB) || '  ->  ' || datetime(MAX(fetched_at_ms)/1000,$WIB) FROM ticker_snapshots;
           SELECT 'Candle   : ' || datetime(MIN(t),$WIB) || '  ->  ' || datetime(MAX(t),$WIB) FROM ohlc_1m;"
  echo; echo "== Data terakhir masuk"
  q "$DB" "SELECT CAST((strftime('%s','now') - MAX(fetched_at_ms)/1000)/60 AS INTEGER) || ' menit lalu' ||
           CASE WHEN strftime('%s','now') - MAX(fetched_at_ms)/1000 > 600 THEN '   <-- CEK, harusnya <= 5 menit!' ELSE '   (OK)' END
           FROM ticker_snapshots;"
  echo; echo "== 5 harga terakhir (WIB | last | buy | sell)"
  q -separator " | " "$DB" "SELECT datetime(fetched_at_ms/1000,$WIB), CAST(last_price AS INTEGER), CAST(buy AS INTEGER), CAST(sell AS INTEGER)
                   FROM ticker_snapshots ORDER BY id DESC LIMIT 5;"
  echo; echo "== Error/retry 24 jam terakhir"
  since=$(date -u -d '24 hours ago' '+%Y-%m-%d %H:%M')
  $RUN awk -v s="$since" '($1" "substr($2,1,5)) >= s && /ERROR|WARNING/' "$LOG" 2>/dev/null | wc -l
}

ekspor() {
  out=~/ekspor; mkdir -p "$out"; stamp=$(date -u '+%Y%m%d_%H%M')
  f1="$out/btcidr_ticker_5menit_${stamp}.csv"; f2="$out/btcidr_candle_1menit_${stamp}.csv"
  q -header -csv "$DB" "SELECT datetime(fetched_at_ms/1000,'unixepoch') AS waktu_utc, datetime(fetched_at_ms/1000,$WIB) AS waktu_wib,
      last_price, buy, sell, high_24h, low_24h, vol_btc_24h, vol_idr_24h FROM ticker_snapshots
      WHERE CAST(strftime('%M', fetched_at_ms/1000, 'unixepoch') AS INTEGER) % 5 = 0 ORDER BY id;" > "$f1"
  q -header -csv "$DB" "SELECT datetime(t,'unixepoch') AS waktu_utc, datetime(t,$WIB) AS waktu_wib,
      open_p AS open, high_p AS high, low_p AS low, close_p AS close, volume FROM ohlc_1m ORDER BY t;" > "$f2"
  echo "CSV dibuat:"; ls -lh "$f1" "$f2"
  echo; echo "Baris data: ticker $(($(wc -l < "$f1")-1)), candle $(($(wc -l < "$f2")-1))"
  echo; echo "Unduh ke Mac (jalankan di Terminal Mac):"
  echo "  scp ubuntu@${VPS_IP}:'~/ekspor/*${stamp}.csv' ~/Documents/cronjob/"
}

case "${1:-}" in
  cek) cek ;;
  ekspor) ekspor ;;
  *) echo "Pakai: indodax cek | indodax ekspor"; exit 1 ;;
esac
```

