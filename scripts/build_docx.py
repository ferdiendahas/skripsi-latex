#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
ROMAWI = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]

# Ukuran dalam satuan Word: sz = setengah poin, spacing = twip (1/20 poin).
TNR = "Times New Roman"
SZ_ISI = "24"      # 12 pt
SZ_BAB = "28"      # 14 pt
SZ_KODE = "18"     # 9 pt
SPASI_15 = "360"   # 1,5 baris
IND_BARIS = "720"   # indentasi baris pertama 1,27 cm
LEBAR_TEKS = "7938" # 14 cm: lebar teks A4 dengan margin 4 cm dan 3 cm
GAYA_TANPA_NOMOR = "JudulTanpaNomor"
MARGIN = {"left": "2268", "right": "1701", "top": "1701", "bottom": "1701"}


def mati(pesan: str) -> None:
    print(f"GAGAL  {pesan}", file=sys.stderr)
    raise SystemExit(1)


def baca(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def urutan_input(utama: Path) -> list[Path]:
    """Ambil urutan \\input{...} dari berkas utama, lewati baris berkomentar."""
    berkas = []
    for baris in baca(utama).splitlines():
        if baris.lstrip().startswith("%"):
            continue
        for nama in re.findall(r"\\input\{([^}]+)\}", baris):
            if nama == "metadata":
                continue
            kandidat = ROOT / (nama if nama.endswith(".tex") else f"{nama}.tex")
            if kandidat.is_file():
                berkas.append(kandidat)
    return berkas


def metadata() -> dict[str, str]:
    teks = baca(ROOT / "metadata.tex")
    return {k: v.strip() for k, v in re.findall(r"([a-z-]+)=\{(.*?)\},?\s*\n", teks, re.S)}


def blok_judul(meta: dict[str, str]) -> str:
    baris = [
        "PRA-SKRIPSI",
        f"\\textbf{{{meta.get('judul', '')}}}",
        f"{meta.get('nama', '')}",
        f"NPM {meta.get('npm', '')}",
        "Dosen Pembimbing:",
    ]
    for kunci in ("pembimbing-satu", "pembimbing-dua"):
        if meta.get(kunci):
            baris.append(meta[kunci])
    baris.append(f"Program Studi {meta.get('program-studi', 'Informatika')}")
    baris.append("Fakultas Ilmu Komputer")
    baris.append("UPN \"Veteran\" Jawa Timur")
    baris.append(meta.get("tahun", ""))
    return "\n\n".join(baris) + "\n\n"


def ganti_perintah(teks: str, nama: str, ubah) -> str:
    """Ganti \\nama{...} dengan menghitung kurung, agar argumen bersarang aman."""
    hasil = []
    sisa = teks
    while True:
        awal = sisa.find(f"\\{nama}{{")
        if awal < 0:
            hasil.append(sisa)
            return "".join(hasil)
        mulai = awal + len(nama) + 2
        dalam = 1
        posisi = mulai
        while posisi < len(sisa) and dalam:
            if sisa[posisi] == "{":
                dalam += 1
            elif sisa[posisi] == "}":
                dalam -= 1
            posisi += 1
        hasil.append(sisa[:awal])
        hasil.append(ubah(sisa[mulai : posisi - 1]))
        sisa = sisa[posisi:]


GAMBAR_KOSONG = (  # PNG 1x1 putih, dipakai bila TikZ gagal dirender
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06"
    b"\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\rIDATx\x9cc\xf8\xff\xff?\x00\x05\xfe"
    b"\x02\xfe\xa7V\x81\x1d\x00\x00\x00\x00IEND\xaeB`\x82"
)


def render_tikz(kode: str) -> Path | None:
    """Render satu tikzpicture menjadi PNG dengan class yang sama seperti PDF.

    Pandoc tidak dapat membaca TikZ. Bila figure hanya berisi teks pengganti,
    Pandoc menuliskannya sebagai HTML mentah yang dibuang oleh penulis .docx,
    sehingga keterangan gambarnya ikut hilang dan Daftar Gambar kosong. Karena
    itu tiap diagram dirender sungguhan, lalu dipasang sebagai gambar biasa.
    """
    import hashlib
    folder = ROOT / "build" / "docx" / "tikz"
    folder.mkdir(parents=True, exist_ok=True)
    kunci = hashlib.sha1(kode.encode("utf-8")).hexdigest()[:12]
    png = folder / f"tikz-{kunci}.png"
    if png.is_file():
        return png
    if shutil.which("xelatex") is None or shutil.which("pdftoppm") is None:
        return None
    tex = folder / f"tikz-{kunci}.tex"
    tex.write_text(
        "\\documentclass[jenis=praskripsi]{upnjatim-skripsi}\n"
        "\\input{metadata}\n"
        "\\usepackage[active,tightpage]{preview}\n"
        "\\PreviewEnvironment{tikzpicture}\n"
        "\\setlength\\PreviewBorder{3pt}\n"
        "\\begin{document}\n" + kode + "\n\\end{document}\n",
        encoding="utf-8",
    )
    subprocess.run(
        ["xelatex", "-interaction=nonstopmode", "-halt-on-error",
         f"-output-directory={folder}", str(tex)],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )
    pdf = tex.with_suffix(".pdf")
    if not pdf.is_file():
        return None
    subprocess.run(
        ["pdftoppm", "-r", "300", "-png", "-singlefile", str(pdf), str(png.with_suffix(""))],
        capture_output=True, check=False,
    )
    return png if png.is_file() else None


def _tikz_ke_gambar(m: re.Match) -> str:
    png = render_tikz(m.group(0))
    if png is None:
        png = ROOT / "build" / "docx" / "tikz" / "kosong.png"
        png.parent.mkdir(parents=True, exist_ok=True)
        png.write_bytes(GAMBAR_KOSONG)
        return (f"\\includegraphics{{{png}}}\n"
                "\\textit{[Gambar TikZ hanya tersedia pada versi PDF]}")
    return f"\\includegraphics{{{png}}}"


def _gambar_aset(path: str, ukuran: str) -> str:
    """Gambar dari assets/gambar/; bila belum ada, tulis nama berkasnya."""
    if (ROOT / path).is_file():
        return f"\\includegraphics[{ukuran}]{{{ROOT / path}}}"
    return f"\\texttt{{[{path}]}}"


LEBAR_TEKS_CM = 14.0


def _lebar_kolom(tabel: str) -> str:
    """Beri lebar pada kolom c/l/r bila kolom lain memakai p{...}.

    Pandoc menghitung lebar kolom tanpa ukuran dari panjang isinya di
    Markdown antara; untuk sel bergambar itu panjang path berkasnya, sehingga
    kolom tersebut membengkak dan kolom lain terjepit di Word."""
    m = re.match(r"\\begin\{(?:tabular|longtable)\}(?:\[[^\]]*\])?\{", tabel)
    if not m:
        return tabel
    awal, dalam, i = m.end(), 1, m.end()
    while i < len(tabel) and dalam:
        dalam += {"{": 1, "}": -1}.get(tabel[i], 0)
        i += 1
    spek = tabel[awal:i - 1]
    lebar = [float(x) for x in re.findall(r"p\{([\d.]+)cm\}", spek)]
    polos = re.sub(r"p\{[^}]*\}", "", spek)
    jumlah_polos = len(re.findall(r"[clr]", polos))
    if not lebar or not jumlah_polos:
        return tabel
    sisa = (LEBAR_TEKS_CM - sum(lebar)) / jumlah_polos
    ukuran = f"p{{{min(2.5, max(1.5, sisa)):.1f}cm}}"
    bagian = re.split(r"(p\{[^}]*\})", spek)
    spek_baru = "".join(b if b.startswith("p{") else re.sub(r"[clr]", ukuran, b) for b in bagian)
    return tabel[:awal] + spek_baru + tabel[i - 1:]


def bersihkan(teks: str, nomor_bab: int) -> str:
    """Terjemahkan perintah khusus class agar dimengerti Pandoc."""
    teks = re.sub(r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}",
                  _tikz_ke_gambar, teks, flags=re.S)
    # \gambarsementara{berkas}{lebar}{tinggi} dari class.
    teks = re.sub(r"\\gambarsementara\{([^}]*)\}\{([^}]*)\}\{([^}]*)\}",
                  lambda m: _gambar_aset(f"assets/gambar/{m.group(1)}", f"width={m.group(2)}"),
                  teks)
    # \glif[lebar]{kelompok}{nama}: glif tabel aksara (assets/gambar/<bab>/glif/).
    def _glif(m: re.Match) -> str:
        cocok = sorted((ROOT / "assets" / "gambar").glob(f"*/glif/{m.group(1)}/{m.group(2)}.png"))
        if cocok:
            return f"\\includegraphics[height=1cm]{{{cocok[0]}}}"
        return f"\\texttt{{[{m.group(2)}]}}"
    teks = re.sub(r"\\glif(?:\[[^\]]*\])?\{([^}]*)\}\{([^}]*)\}", _glif, teks)
    # Definisi makro yang hanya berarti untuk PDF dibuang; Pandoc tidak
    # memahami \newcolumntype maupun \IfFileExists di dalam makro.
    teks = re.sub(r"\\newcommand\{\\glif\}\[[^\]]*\]\[[^\]]*\]\{.*?\n\n", "\n\n", teks, flags=re.S)
    teks = re.sub(r"\\newcolumntype\{(\w)\}(?:\[\d\])?\{.*\}\s*\n", "", teks)
    teks = re.sub(r"(?<=[|@])L\{", "p{", teks)
    teks = re.sub(r"\\rule\[[^\]]*\]\{0pt\}\{[^}]*\}", "", teks)
    # longtable: judul kolom untuk halaman lanjutan (\\endfirsthead ...
    # \\endhead) dibaca Pandoc sebagai baris biasa, sehingga tercetak dua kali.
    teks = re.sub(r"\\endfirsthead.*?\\endhead", r"\\endhead", teks, flags=re.S)
    # Baris baru di dalam sel ikut dipertahankan oleh --wrap=preserve dan
    # memecah tabel Markdown antara; satukan isi tiap tabel menjadi satu baris
    # (komentar dibuang dulu agar tidak menelan sisa baris).
    def _satukan(m: re.Match) -> str:
        isi = re.sub(r"(?<!\\)%[^\n]*", "", m.group(0))
        # Sisipan kolom >{...}/<{...} dari paket array membuat Pandoc kehilangan
        # judul kolom \\multicolumn dan sel \\multirow; perataannya tidak
        # berpengaruh di Word, jadi dibuang.
        isi = re.sub(r"[<>]\{(?:[^{}]|\{[^{}]*\})*\}", "", isi)
        isi = _lebar_kolom(isi)
        return " ".join(isi.split())
    teks = re.sub(r"\\begin\{(tabular|longtable)\}.*?\\end\{\1\}", _satukan, teks, flags=re.S)
    # Opsi penempatan float ([htbp], [!htb]) menjadi atribut figure yang
    # tidak dapat ditulis sebagai gambar Markdown; tanpa dibuang, Pandoc
    # menuliskan figure sebagai HTML mentah yang hilang di .docx.
    teks = re.sub(r"\\begin\{(figure|table)\}\[[^\]]*\]", r"\\begin{\1}", teks)
    teks = ganti_perintah(teks, "sumber", lambda isi: f"\n\nSumber: {isi}\n\n")
    teks = ganti_perintah(teks, "lampiran", lambda isi: f"\\chapter{{Lampiran: {isi}}}")
    teks = teks.replace("\\checkmark", "✓")

    # Nomor subbab tidak ditulis sebagai teks; Word menomorinya sendiri lewat
    # daftar bertingkat yang ditautkan ke gaya Heading (lihat _pasang_penomoran).
    return teks


LINGKUNGAN = r"\\begin\{(equation|table|figure|longtable)\}(.*?)\\end\{\1\}"


def kumpulkan_label(berkas: list[Path]) -> tuple[dict[str, str], dict[Path, list[str]]]:
    """Petakan label ke nomor (mis. eq:bobot -> 2.1) seperti penomoran LaTeX.

    Juga mengembalikan nomor tiap figure/table per berkas, sesuai urutan
    kemunculan, untuk ditulis di depan keterangannya (longtable dihitung
    sebagai tabel, sama seperti LaTeX)."""
    peta: dict[str, str] = {}
    nomor_keterangan: dict[Path, list[str]] = {}
    bab = lampiran = 0
    for path in berkas:
        teks = baca(path)
        if "\\lampiran{" in teks:
            lampiran += 1
            awalan = f"L{lampiran}"
        else:
            if "\\chapter{" in teks:
                bab += 1
            awalan = str(bab)
        cacah = {"equation": 0, "table": 0, "figure": 0}
        daftar = []
        for m in re.finditer(LINGKUNGAN, teks, re.S):
            jenis = "table" if m.group(1) == "longtable" else m.group(1)
            cacah[jenis] += 1
            nomor = f"{awalan}.{cacah[jenis]}"
            if jenis != "equation":
                daftar.append(("Tabel" if jenis == "table" else "Gambar") + f" {nomor}")
            label = re.search(r"\\label\{([^}]+)\}", m.group(2))
            if label:
                peta[label.group(1)] = nomor
        nomor_keterangan[path] = daftar
    return peta, nomor_keterangan


def nomori_keterangan(teks: str, nomor: list[str]) -> str:
    """Tulis "Gambar 2.1 " / "Tabel 2.1 " di depan isi \\caption, karena Pandoc
    tidak menomori keterangan. \\caption* (tanpa nomor) dilewati."""
    antre = iter(nomor)

    def _satu(m: re.Match) -> str:
        isi = m.group(0)
        cap = re.search(r"\\caption(?:\[[^\]]*\])?\{", isi)
        label = next(antre, None)
        if cap is None or label is None:
            return isi
        ket = gaya_keterangan()
        if ket["label_tebal"] and not ket["tebal_semua"]:
            label = f"\\textbf{{{label}}}"
        return isi[:cap.end()] + label + " " + isi[cap.end():]

    def _lingkungan(m: re.Match) -> str:
        if m.group(1) == "equation":
            return m.group(0)
        return _satu(m)

    return re.sub(LINGKUNGAN, _lingkungan, teks, flags=re.S)


def sumber_gabungan(meta: dict[str, str], berkas: list[Path], blok_sampul: bool = True) -> str:
    # Blok judul teks hanya dipakai bila gambar sampul tidak tersedia, agar
    # sampulnya tidak tampil dua kali.
    bagian = [blok_judul(meta)] if blok_sampul else []
    peta_label, nomor_keterangan = kumpulkan_label(berkas)
    nomor_bab = 0
    pustaka_tercetak = False
    for path in berkas:
        teks = nomori_keterangan(baca(path), nomor_keterangan[path])
        teks = re.sub(r"\\ref\{([^}]+)\}", lambda m: peta_label.get(m.group(1), "?"), teks)
        # Daftar pustaka dicetak sebelum lampiran, sama seperti keluaran PDF.
        if "\\lampiran{" in teks and not pustaka_tercetak:
            bagian.append("\\chapter{DAFTAR PUSTAKA}\n")
            pustaka_tercetak = True
        judul = re.search(r"\\chapter\{([^}]*)\}", teks)
        if judul and "\\lampiran" not in teks:
            nomor_bab += 1
            judul_bab = f"BAB {ROMAWI[nomor_bab]} {judul.group(1).upper()}"
            teks = teks.replace(judul.group(0), f"\\chapter{{{judul_bab}}}", 1)
        bagian.append(bersihkan(teks, nomor_bab))
    if not pustaka_tercetak:
        bagian.append("\\chapter{DAFTAR PUSTAKA}\n")
    return "\n\n".join(bagian)


def _anak(induk: ET.Element, tag: str) -> ET.Element:
    ada = induk.find(f"{W}{tag}")
    if ada is None:
        ada = ET.SubElement(induk, f"{W}{tag}")
    return ada


def _atur(induk: ET.Element, tag: str, **atribut: str) -> None:
    simpul = _anak(induk, tag)
    for kunci, nilai in atribut.items():
        simpul.set(f"{W}{kunci}", nilai)


def _gaya(akar: ET.Element, style_id: str) -> ET.Element | None:
    for gaya in akar.findall(f"{W}style"):
        if gaya.get(f"{W}styleId") == style_id:
            return gaya
    return None


def _atur_font(gaya: ET.Element, ukuran: str, tebal: bool, miring: bool = False) -> None:
    rpr = _anak(gaya, "rPr")
    _atur(rpr, "rFonts", ascii=TNR, hAnsi=TNR, cs=TNR)
    _atur(rpr, "sz", val=ukuran)
    _atur(rpr, "szCs", val=ukuran)
    _atur(rpr, "color", val="auto")
    for tag, aktif in (("b", tebal), ("i", miring)):
        simpul = _anak(rpr, tag)
        simpul.set(f"{W}val", "1" if aktif else "0")


UKURAN_LATEX = {"scriptsize": "16", "footnotesize": "20", "small": "22",
                "normalsize": "24", "large": "28"}


def gaya_keterangan() -> dict[str, object]:
    """Baca \\captionsetup dari class agar keterangan di Word sama dengan PDF:
    ukuran huruf, label saja yang tebal atau seluruhnya, dan perataan."""
    cls = baca(ROOT / "upnjatim-skripsi.cls")
    umum = re.search(r"\\captionsetup\{([^\n]*)\}\s*\n", cls)
    tabel = re.search(r"\\captionsetup\[table\]\{([^\n]*)\}", cls)
    gambar = re.search(r"\\captionsetup\[figure\]\{([^\n]*)\}", cls)
    opsi = umum.group(1) if umum else ""
    font = re.search(r"(?<!label)font=(\{[^}]*\}|[^,]*)", opsi)
    token = font.group(1).strip("{}").split(",") if font else ["normalsize", "bf"]
    token = [t.strip() for t in token]
    rata = lambda m: ("center" if m and "justification=centering" in m.group(1) else "left")
    return {
        "sz": next((UKURAN_LATEX[t] for t in token if t in UKURAN_LATEX), SZ_ISI),
        "tebal_semua": "bf" in token,
        "label_tebal": "labelfont=bf" in opsi,
        "rata_tabel": rata(tabel),
        "rata_gambar": "center" if gambar is None else rata(gambar),
    }


def reference_docx(tujuan: Path) -> Path:
    """Buat reference.docx dari bawaan Pandoc, lalu setel gayanya sesuai pedoman."""
    bawaan = tujuan.parent / "reference-bawaan.docx"
    with bawaan.open("wb") as keluar:
        subprocess.run(
            ["pandoc", "--print-default-data-file", "reference.docx"],
            stdout=keluar, check=True,
        )

    with zipfile.ZipFile(bawaan) as zin:
        isi = {nama: zin.read(nama) for nama in zin.namelist()}

    for awalan in (f"{W}", ""):
        ET.register_namespace("w" if awalan else "", W.strip("{}"))
        break

    akar = ET.fromstring(isi["word/styles.xml"])
    bawaan_gaya = akar.find(f"{W}docDefaults")
    if bawaan_gaya is not None:
        rpr = _anak(_anak(bawaan_gaya, "rPrDefault"), "rPr")
        _atur(rpr, "rFonts", ascii=TNR, hAnsi=TNR, cs=TNR)
        _atur(rpr, "sz", val=SZ_ISI)
        _atur(rpr, "szCs", val=SZ_ISI)
        ppr = _anak(_anak(bawaan_gaya, "pPrDefault"), "pPr")
        _atur(ppr, "spacing", line=SPASI_15, lineRule="auto", before="0", after="0")
        _atur(ppr, "jc", val="both")

    ket = gaya_keterangan()
    aturan = {
        "Normal": (SZ_ISI, False, "both", None),
        "BodyText": (SZ_ISI, False, "both", None),
        "FirstParagraph": (SZ_ISI, False, "both", None),
        "Compact": (SZ_ISI, False, "both", None),
        "Heading1": (SZ_BAB, True, "center", ("0", "240")),
        "Heading2": (SZ_ISI, True, "left", ("240", "120")),
        "Heading3": (SZ_ISI, True, "left", ("180", "120")),
        "Heading4": (SZ_ISI, True, "left", ("180", "120")),
        "Caption": (ket["sz"], ket["tebal_semua"], ket["rata_tabel"], ("120", "120")),
        "TableCaption": (ket["sz"], ket["tebal_semua"], ket["rata_tabel"], ("120", "120")),
        "ImageCaption": (ket["sz"], ket["tebal_semua"], ket["rata_gambar"], ("120", "120")),
        "Bibliography": (SZ_ISI, False, "both", None),
        "Title": (SZ_BAB, True, "center", ("240", "240")),
        "Author": (SZ_ISI, False, "center", None),
    }
    for style_id, (ukuran, tebal, rata, jarak) in aturan.items():
        gaya = _gaya(akar, style_id)
        if gaya is None:
            continue
        _atur_font(gaya, ukuran, tebal)
        ppr = _anak(gaya, "pPr")
        _atur(ppr, "jc", val=rata)
        if jarak:
            _atur(ppr, "spacing", before=jarak[0], after=jarak[1], line=SPASI_15, lineRule="auto")

    # Paragraf isi: baris pertama masuk 1,27 cm dan jarak antarparagraf 6 pt,
    # sama seperti keluaran PDF. Judul, keterangan, dan pustaka tanpa indentasi.
    for style_id in ("Normal", "BodyText", "FirstParagraph"):
        gaya = _gaya(akar, style_id)
        if gaya is not None:
            ppr = _anak(gaya, "pPr")
            _atur(ppr, "ind", firstLine=IND_BARIS)
            _atur(ppr, "spacing", before="0", after="120", line=SPASI_15, lineRule="auto")
    # "Compact" dipakai Pandoc untuk butir daftar; butir tidak boleh menjorok.
    for style_id in ("Compact", "Heading1", "Heading2", "Heading3", "Heading4", "Caption",
                     "TableCaption", "ImageCaption", "Bibliography", "SourceCode"):
        gaya = _gaya(akar, style_id)
        if gaya is not None:
            _atur(_anak(gaya, "pPr"), "ind", firstLine="0", left="0")

    # Word mengutamakan atribut tema (asciiTheme/themeColor) daripada nilai
    # eksplisit. Tanpa dibuang, huruf ikut tema (Aptos) dan judul berwarna.
    for simpul in akar.iter(f"{W}rFonts"):
        for atribut in ("asciiTheme", "hAnsiTheme", "cstheme", "eastAsiaTheme"):
            simpul.attrib.pop(f"{W}{atribut}", None)
    for gaya in akar.findall(f"{W}style"):
        if "Hyperlink" in (gaya.get(f"{W}styleId") or ""):
            continue
        for simpul in gaya.iter(f"{W}color"):
            for atribut in ("themeColor", "themeShade", "themeTint"):
                simpul.attrib.pop(f"{W}{atribut}", None)
            simpul.set(f"{W}val", "000000")

    # Tiap bab mulai di halaman baru, sama seperti PDF.
    bab = _gaya(akar, "Heading1")
    if bab is not None:
        _anak(_anak(bab, "pPr"), "pageBreakBefore")

    # Tabel Pandoc tidak bergaris; PDF memakai garis penuh, jadi disamakan.
    tabel = _gaya(akar, "Table")
    if tabel is not None:
        tblpr = _anak(tabel, "tblPr")
        garis = _anak(tblpr, "tblBorders")
        for sisi in ("top", "left", "bottom", "right", "insideH", "insideV"):
            _atur(garis, sisi, val="single", sz="4", space="0", color="000000")
        marjin = _anak(tblpr, "tblCellMar")
        for sisi in ("left", "right"):
            _atur(marjin, sisi, w="108", type="dxa")
        ppr = _anak(tabel, "pPr")
        _atur(ppr, "ind", firstLine="0", left="0")
        _atur(ppr, "spacing", before="0", after="0", line="240", lineRule="auto")

    # Gaya judul tanpa nomor untuk bagian awal, daftar pustaka, dan lampiran.
    # Tetap outlineLvl 0 agar ikut tercantum di Daftar Isi, tetapi tidak
    # menambah hitungan bab sehingga subbab BAB I tetap 1.1.
    if _gaya(akar, GAYA_TANPA_NOMOR) is None:
        gaya = ET.SubElement(akar, f"{W}style")
        gaya.set(f"{W}type", "paragraph")
        gaya.set(f"{W}styleId", GAYA_TANPA_NOMOR)
        _atur(gaya, "name", val="Judul Tanpa Nomor")
        _atur(gaya, "basedOn", val="Heading1")
        _atur(gaya, "next", val="BodyText")
        ppr = _anak(gaya, "pPr")
        _atur(ppr, "outlineLvl", val="0")
        _atur(ppr, "ind", left="0", firstLine="0")
    # Gaya ini diturunkan dari Heading1 sehingga ikut mewarisi penomorannya.
    # numId 0 mematikan penomoran, agar judul seperti DAFTAR ISI tidak
    # terhitung sebagai bab dan subbab BAB I tetap mulai dari 1.1.
    numpr = _anak(_anak(_gaya(akar, GAYA_TANPA_NOMOR), "pPr"), "numPr")
    _atur(numpr, "ilvl", val="0")
    _atur(numpr, "numId", val="0")

    # Gaya entri Daftar Isi. Tanpa ini Word menurunkannya dari Normal yang
    # rata kanan-kiri dan menjorok, sehingga entrinya berantakan.
    for tingkat in range(1, 4):
        style_id = f"TOC{tingkat}"
        gaya = _gaya(akar, style_id)
        if gaya is None:
            gaya = ET.SubElement(akar, f"{W}style")
            gaya.set(f"{W}type", "paragraph")
            gaya.set(f"{W}styleId", style_id)
            _atur(gaya, "name", val=f"toc {tingkat}")
            _atur(gaya, "basedOn", val="Normal")
        ppr = _anak(gaya, "pPr")
        _atur(ppr, "jc", val="left")
        _atur(ppr, "spacing", before="0", after="0", line=SPASI_15, lineRule="auto")
        _atur(ppr, "ind", left=str((tingkat - 1) * 360), firstLine="0")
        tabs = _anak(ppr, "tabs")
        for simpul in tabs.findall(f"{W}tab"):
            tabs.remove(simpul)
        _atur(tabs, "tab", val="right", leader="dot", pos=LEBAR_TEKS)

    # Gaya entri daftar gambar/tabel ("table of figures" di Word).
    gaya = _gaya(akar, "TableofFigures")
    if gaya is None:
        gaya = ET.SubElement(akar, f"{W}style")
        gaya.set(f"{W}type", "paragraph")
        gaya.set(f"{W}styleId", "TableofFigures")
        _atur(gaya, "name", val="table of figures")
        _atur(gaya, "basedOn", val="Normal")
    ppr = _anak(gaya, "pPr")
    _atur(ppr, "jc", val="left")
    _atur(ppr, "spacing", before="0", after="0", line=SPASI_15, lineRule="auto")
    _atur(ppr, "ind", left="0", firstLine="0")
    tabs = _anak(ppr, "tabs")
    _atur(tabs, "tab", val="right", leader="dot", pos=LEBAR_TEKS)

    kode = _gaya(akar, "SourceCode") or _gaya(akar, "VerbatimChar")
    if kode is not None:
        rpr = _anak(kode, "rPr")
        _atur(rpr, "rFonts", ascii="Courier New", hAnsi="Courier New", cs="Courier New")
        _atur(rpr, "sz", val=SZ_KODE)
        _atur(rpr, "szCs", val=SZ_KODE)
    isi["word/styles.xml"] = ET.tostring(akar, encoding="UTF-8", xml_declaration=True)

    dokumen = ET.fromstring(isi["word/document.xml"])
    for sect in dokumen.iter(f"{W}sectPr"):
        _atur(sect, "pgMar", header="709", footer="709", gutter="0", **MARGIN)
    isi["word/document.xml"] = ET.tostring(dokumen, encoding="UTF-8", xml_declaration=True)

    # Tema pun disetel ke Times New Roman, untuk gaya yang masih mewarisinya.
    if "word/theme/theme1.xml" in isi:
        tema = isi["word/theme/theme1.xml"].decode("utf-8")
        tema = re.sub(r'(<a:latin typeface=")[^"]*(")', rf"\g<1>{TNR}\g<2>", tema)
        isi["word/theme/theme1.xml"] = tema.encode("utf-8")

    with zipfile.ZipFile(tujuan, "w", zipfile.ZIP_DEFLATED) as zout:
        for nama, data in isi.items():
            zout.writestr(nama, data)
    bawaan.unlink()
    return tujuan


NS = (
    'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
    'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
    'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
    'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
    'xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"'
)
R_ID = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
ID_SAMPUL = "rIdSampulUPN"
ID_FOOTER = "rIdFooterUPN"
EMU_MM = 36000
A4_EMU = (210 * EMU_MM, 297 * EMU_MM)


def pdf_siap(utama: Path, pdf: Path) -> Path | None:
    """Sampul .docx diambil dari halaman pertama PDF, jadi PDF harus ada."""
    if pdf.is_file():
        return pdf
    if shutil.which("latexmk") is None:
        return None
    # Jalankan seperti Makefile (jalur relatif), agar Biber menemukan berkasnya.
    subprocess.run(
        ["latexmk", f"-outdir={pdf.parent.relative_to(ROOT)}",
         str(utama.relative_to(ROOT))],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )
    return pdf if pdf.is_file() else None


def render_sampul(pdf: Path, tujuan: Path) -> Path | None:
    if shutil.which("pdftoppm") is None:
        return None
    subprocess.run(
        ["pdftoppm", "-f", "1", "-l", "1", "-r", "200", "-png", "-singlefile",
         str(pdf), str(tujuan.with_suffix(""))],
        check=False, capture_output=True,
    )
    return tujuan if tujuan.is_file() else None


def _p_judul(teks: str) -> str:
    return (f'<w:p {NS}><w:pPr><w:pStyle w:val="{GAYA_TANPA_NOMOR}"/></w:pPr>'
            f"<w:r><w:t>{teks}</w:t></w:r></w:p>")


def _p_field(instruksi: str) -> str:
    """Field TOC. Atribut w:dirty membuat Word memperbaruinya saat dibuka."""
    return (
        f'<w:p {NS}><w:r><w:fldChar w:fldCharType="begin" w:dirty="true"/></w:r>'
        f'<w:r><w:instrText xml:space="preserve">{instruksi}</w:instrText></w:r>'
        f'<w:r><w:fldChar w:fldCharType="separate"/></w:r>'
        f"<w:r><w:t>Klik kanan daftar ini lalu pilih Update Field.</w:t></w:r>"
        f'<w:r><w:fldChar w:fldCharType="end"/></w:r></w:p>'
    )


SIMBOL = {"\\epsilon": "ϵ", "\\varepsilon": "ε", "\\ell": "ℓ", "\\times": "×",
          "\\leftarrow": "←", "\\rightarrow": "→", "\\pm": "±"}


def latex_ke_teks(teks: str) -> str:
    """Ubah teks entri .toc/.lof/.lot menjadi teks biasa untuk daftar Word."""
    teks = re.sub(r"\\MakeUppercase\s*(?:\[\])?\s*\{([^{}]*)\}", lambda m: m.group(1).upper(), teks)
    teks = re.sub(r"\\enquote\s*\{([^{}]*)\}", r"“\1”", teks)
    # unicode-math menulis simbol miring sebagai \\mitepsilon, \\mitell, dst.
    teks = teks.replace("\\mit", "\\")
    for perintah, ganti in SIMBOL.items():
        teks = teks.replace(perintah, ganti)
    teks = teks.replace("\\ignorespaces", "").replace("~", " ").replace("$", "")
    teks = re.sub(r"\\[a-zA-Z]+\*?\s*", "", teks)     # sisa perintah, isinya dipertahankan
    teks = teks.replace("{", "").replace("}", "").replace("\\", "")
    return " ".join(teks.split())


def baca_daftar(akhiran: str) -> list[tuple[str, str, str, str]]:
    """Entri (jenis, nomor, judul, halaman) dari berkas daftar keluaran LaTeX."""
    berkas = ROOT / "build" / f"praskripsi.{akhiran}"
    if not berkas.is_file():
        return []
    entri = []
    for m in re.finditer(r"\\contentsline \{(\w+)\}\{(.*)\}\{([^{}]*)\}\{[^{}]*\}%", baca(berkas)):
        jenis, isi, halaman = m.groups()
        nomor = re.match(r"\\numberline \{([^{}]*)\}", isi)
        judul = isi[nomor.end():] if nomor else isi
        entri.append((jenis, nomor.group(1) if nomor else "", latex_ke_teks(judul), halaman))
    return entri


def _teks_entri(jenis: str, nomor: str, judul: str) -> tuple[str, str]:
    """Teks entri dan gayanya, mengikuti tampilan daftar pada PDF."""
    if jenis == "chapter":
        return (f"BAB {nomor} {judul.upper()}" if nomor else judul.upper()), "TOC1"
    if jenis in ("figure", "table"):
        label = "Gambar" if jenis == "figure" else "Tabel"
        return f"{label} {nomor} {judul}", "TableofFigures"
    gaya = {"section": "TOC2", "subsection": "TOC3"}.get(jenis, "TOC3")
    return f"{nomor} {judul}".strip(), gaya


def _p_daftar_terisi(instruksi: str, entri: list[tuple[str, str, str, str]]) -> list[str]:
    """Field TOC yang sudah berisi entri dan nomor halaman dari PDF.

    Word tidak selalu memperbarui field yang ditandai dirty (terutama di
    macOS), sehingga daftar kosong. Dengan isi awal ini daftar langsung
    tampil; pembaruan field oleh Word hanya menyesuaikan nomor halaman."""
    if not entri:
        return [_p_field(instruksi)]
    paragraf = []
    for indeks, (jenis, nomor, judul, halaman) in enumerate(entri):
        teks, gaya = _teks_entri(jenis, nomor, judul)
        awal = ""
        if indeks == 0:
            awal = (f'<w:r><w:fldChar w:fldCharType="begin" w:dirty="true"/></w:r>'
                    f'<w:r><w:instrText xml:space="preserve">{instruksi}</w:instrText></w:r>'
                    f'<w:r><w:fldChar w:fldCharType="separate"/></w:r>')
        akhir = '<w:r><w:fldChar w:fldCharType="end"/></w:r>' if indeks == len(entri) - 1 else ""
        teks_xml = teks.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        paragraf.append(
            f'<w:p {NS}><w:pPr><w:pStyle w:val="{gaya}"/></w:pPr>{awal}'
            f'<w:r><w:t xml:space="preserve">{teks_xml}</w:t></w:r>'
            f'<w:r><w:tab/></w:r><w:r><w:t>{halaman}</w:t></w:r>{akhir}</w:p>'
        )
    return paragraf


def _p_sampul() -> str:
    lebar, tinggi = A4_EMU
    return (
        f'<w:p {NS}><w:pPr><w:spacing w:before="0" w:after="0" w:line="240" '
        f'w:lineRule="auto"/><w:ind w:left="0" w:right="0" w:firstLine="0"/>'
        f'<w:jc w:val="left"/></w:pPr><w:r><w:drawing>'
        f'<wp:inline distT="0" distB="0" distL="0" distR="0">'
        f'<wp:extent cx="{lebar}" cy="{tinggi}"/><wp:docPr id="991" name="Sampul"/>'
        f'<a:graphic><a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">'
        f'<pic:pic><pic:nvPicPr><pic:cNvPr id="991" name="Sampul"/><pic:cNvPicPr/></pic:nvPicPr>'
        f'<pic:blipFill><a:blip r:embed="{ID_SAMPUL}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill>'
        f'<pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{lebar}" cy="{tinggi}"/></a:xfrm>'
        f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic>'
        f"</a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>"
    )


ID_NOMOR = "900"


def _abstract_num() -> ET.Element:
    """Daftar bertingkat yang ditautkan ke gaya Heading, seperti multilevel list Word.

    Tingkat 1 hanya menghitung bab tanpa mencetak apa pun, karena kata
    "BAB I" sudah menjadi bagian teks judulnya. Tingkat berikutnya memakai
    angka bab tersebut sehingga menghasilkan 1.1., 1.1.1., dan seterusnya.
    """
    pola = {0: "", 1: "%1.%2.", 2: "%1.%2.%3.", 3: "%1.%2.%3.%4."}
    abstrak = ET.Element(f"{W}abstractNum")
    abstrak.set(f"{W}abstractNumId", ID_NOMOR)
    for tingkat, teks in pola.items():
        lvl = ET.SubElement(abstrak, f"{W}lvl")
        lvl.set(f"{W}ilvl", str(tingkat))
        _atur(lvl, "start", val="1")
        _atur(lvl, "numFmt", val="decimal")
        _atur(lvl, "pStyle", val=f"Heading{tingkat + 1}")
        _atur(lvl, "lvlText", val=teks)
        _atur(lvl, "lvlJc", val="left")
        _atur(lvl, "suff", val="none" if tingkat == 0 else "tab")
        ppr = _anak(lvl, "pPr")
        _atur(ppr, "ind", left="0", firstLine="0")
        tabs = _anak(ppr, "tabs")
        _atur(tabs, "tab", val="left", pos=IND_BARIS)
    return abstrak


def _pasang_penomoran(isi: dict[str, bytes]) -> None:
    """Tautkan gaya Heading ke daftar bertingkat agar Word menomori sendiri."""
    if "word/numbering.xml" not in isi:
        return
    mentah = isi["word/numbering.xml"].decode("utf-8")
    for prefiks, uri in re.findall(r'xmlns:([A-Za-z0-9]+)="([^"]+)"', mentah):
        ET.register_namespace(prefiks, uri)
    akar = ET.fromstring(mentah)
    if akar.find(f".//{W}abstractNum[@{W}abstractNumId='{ID_NOMOR}']") is None:
        # Seluruh abstractNum harus mendahului elemen num.
        posisi = len(akar.findall(f"{W}abstractNum"))
        akar.insert(posisi, _abstract_num())
        nomor = ET.SubElement(akar, f"{W}num")
        nomor.set(f"{W}numId", ID_NOMOR)
        _atur(nomor, "abstractNumId", val=ID_NOMOR)
    isi["word/numbering.xml"] = ET.tostring(akar, encoding="UTF-8", xml_declaration=True)

    gaya_mentah = isi["word/styles.xml"].decode("utf-8")
    akar_gaya = ET.fromstring(gaya_mentah)
    for tingkat in range(4):
        gaya = _gaya(akar_gaya, f"Heading{tingkat + 1}")
        if gaya is None:
            continue
        numpr = _anak(_anak(gaya, "pPr"), "numPr")
        _atur(numpr, "ilvl", val=str(tingkat))
        _atur(numpr, "numId", val=ID_NOMOR)
    isi["word/styles.xml"] = ET.tostring(akar_gaya, encoding="UTF-8", xml_declaration=True)


def _footer_xml() -> bytes:
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f'<w:ftr {NS}><w:p><w:pPr><w:jc w:val="center"/></w:pPr>'
        '<w:r><w:fldChar w:fldCharType="begin"/></w:r>'
        '<w:r><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>'
        '<w:r><w:fldChar w:fldCharType="separate"/></w:r><w:r><w:t>1</w:t></w:r>'
        '<w:r><w:fldChar w:fldCharType="end"/></w:r></w:p></w:ftr>'
    ).encode("utf-8")


def _rujukan_footer() -> ET.Element:
    rujukan = ET.Element(f"{W}footerReference")
    rujukan.set(f"{W}type", "default")
    rujukan.set(R_ID, ID_FOOTER)
    return rujukan


def _sect_salin(asal: ET.Element, *, margin_nol: bool, format_nomor: str,
                mulai: str, pakai_footer: bool) -> ET.Element:
    sect = copy.deepcopy(asal)
    for tag in ("footerReference", "headerReference", "pgNumType"):
        for simpul in sect.findall(f"{W}{tag}"):
            sect.remove(simpul)
    if margin_nol:
        _atur(sect, "pgMar", left="0", right="0", top="0", bottom="0",
              header="0", footer="0", gutter="0")
    if pakai_footer:
        sect.insert(0, _rujukan_footer())
    _atur(sect, "pgNumType", fmt=format_nomor, start=mulai)
    return sect


def _sisip_tc(badan: ET.Element, gaya: str, kode: str,
              entri: list[tuple[str, str, str, str]]) -> None:
    """Tambahkan field TC tersembunyi ke tiap paragraf bergaya `gaya`, agar
    TOC \\f <kode> dapat mengumpulkannya. Teksnya diambil dari .lof/.lot
    (keterangan pendek, tanpa sitasi) bila jumlahnya cocok, seperti PDF."""
    paragrafs = [p for p in badan.iter(f"{W}p")
                 if p.find(f"{W}pPr/{W}pStyle") is not None
                 and p.find(f"{W}pPr/{W}pStyle").get(f"{W}val") == gaya]
    dari_latex = [_teks_entri(*e[:3])[0] for e in entri] if len(entri) == len(paragrafs) else None
    for paragraf in paragrafs:
        ppr = paragraf.find(f"{W}pPr")
        st = ppr.find(f"{W}pStyle") if ppr is not None else None
        if st is None or st.get(f"{W}val") != gaya:
            continue
        teks = "".join(t.text or "" for t in paragraf.iter(f"{W}t")).strip()
        if dari_latex:
            teks = dari_latex[paragrafs.index(paragraf)]
        teks = " ".join(teks.split()).replace('"', "'")
        if not teks:
            continue
        for xml in (f'<w:r {NS}><w:fldChar w:fldCharType="begin"/></w:r>',
                    f'<w:r {NS}><w:instrText xml:space="preserve"> TC "{teks}" \\f {kode} \\l 1 </w:instrText></w:r>',
                    f'<w:r {NS}><w:fldChar w:fldCharType="end"/></w:r>'):
            paragraf.append(ET.fromstring(xml))


TWIP_CM = 567


def lebar_tabel_latex(sumber: Path) -> list[list[float | None]]:
    """Lebar kolom (cm) tiap tabel sesuai urutan di sumber; None = tanpa ukuran."""
    hasil = []
    for m in re.finditer(r"\\begin\{(?:tabular|longtable)\}(?:\[[^\]]*\])?\{", baca(sumber)):
        teks, awal, dalam, i = m.string, m.end(), 1, m.end()
        while i < len(teks) and dalam:
            dalam += {"{": 1, "}": -1}.get(teks[i], 0)
            i += 1
        kolom = []
        for k in re.finditer(r"p\{([^}]*)\}|[clr]", teks[awal:i - 1]):
            if k.group(1) is None:
                kolom.append(None)
                continue
            ukuran = k.group(1).replace(" ", "")
            cm = re.fullmatch(r"([\d.]+)cm", ukuran)
            lebar_teks = re.fullmatch(r"([\d.]*)\\textwidth", ukuran)
            if cm:
                kolom.append(float(cm.group(1)))
            elif lebar_teks:
                kolom.append(float(lebar_teks.group(1) or 1) * LEBAR_TEKS_CM)
            else:
                kolom.append(None)
        hasil.append(kolom)
    return hasil


def _setel_lebar_tabel(badan: ET.Element, lebar: list[list[float | None]]) -> None:
    """Pakai lebar kolom LaTeX pada tabel Word. Markdown antara tidak membawa
    lebar kolom, sehingga Pandoc menebaknya dari panjang teks sel."""
    tabel = list(badan.iter(f"{W}tbl"))
    if len(tabel) != len(lebar):
        return
    for tbl, kolom in zip(tabel, lebar):
        if not kolom or all(k is None for k in kolom):
            continue
        tetap = [k for k in kolom if k is not None]
        sisa = max(LEBAR_TEKS_CM - sum(tetap), 0)
        kosong = len(kolom) - len(tetap)
        isi = [k if k is not None else (sisa / kosong if kosong else 0) for k in kolom]
        skala = min(1.0, LEBAR_TEKS_CM / sum(isi))      # jangan melebihi lebar teks
        twip = [round(k * skala * TWIP_CM) for k in isi]
        grid = tbl.find(f"{W}tblGrid")
        if grid is None or len(grid.findall(f"{W}gridCol")) != len(twip):
            continue
        for kol, w in zip(grid.findall(f"{W}gridCol"), twip):
            kol.set(f"{W}w", str(w))
        tblpr = tbl.find(f"{W}tblPr")
        _atur(tblpr, "tblW", w=str(sum(twip)), type="dxa")
        _atur(tblpr, "tblLayout", type="fixed")
        for baris in tbl.findall(f"{W}tr"):
            posisi = 0
            for sel in baris.findall(f"{W}tc"):
                tcpr = sel.find(f"{W}tcPr")
                if tcpr is None:
                    tcpr = ET.Element(f"{W}tcPr")
                    sel.insert(0, tcpr)
                rentang = tcpr.find(f"{W}gridSpan")
                n = int(rentang.get(f"{W}val")) if rentang is not None else 1
                lebar_sel = sum(twip[posisi:posisi + n])
                posisi += n
                tcw = tcpr.find(f"{W}tcW")
                if tcw is None:
                    tcw = ET.Element(f"{W}tcW")
                    tcpr.insert(0, tcw)
                tcw.set(f"{W}w", str(lebar_sel))
                tcw.set(f"{W}type", "dxa")


def susun_seperti_pdf(docx: Path, sampul: Path | None) -> None:
    """Tambah sampul, daftar isi/gambar/tabel, dan nomor halaman pada .docx."""
    with zipfile.ZipFile(docx) as zin:
        isi = {nama: zin.read(nama) for nama in zin.namelist()}

    mentah = isi["word/document.xml"].decode("utf-8")
    for prefiks, uri in re.findall(r'xmlns:([A-Za-z0-9]+)="([^"]+)"', mentah):
        ET.register_namespace(prefiks, uri)

    akar = ET.fromstring(mentah)
    badan = akar.find(f"{W}body")
    sect_akhir = badan.find(f"{W}sectPr")
    if sect_akhir is None:
        mati("Struktur .docx tidak terduga: sectPr tidak ditemukan")

    # Bagian utama memakai angka arab mulai 1, sama seperti PDF.
    for simpul in sect_akhir.findall(f"{W}footerReference"):
        sect_akhir.remove(simpul)
    sect_akhir.insert(0, _rujukan_footer())
    _atur(sect_akhir, "pgNumType", fmt="decimal", start="1")

    sumber_tex = docx.parent / "docx" / "sumber.tex"
    if sumber_tex.is_file():
        _setel_lebar_tabel(badan, lebar_tabel_latex(sumber_tex))

    # Gambar tanpa keterangan (mis. glif di sel tabel) dijadikan figure oleh
    # Pandoc dengan keterangan berupa alt bawaan "image". Keterangan itu tampil
    # di sel dan ikut terhitung di daftar gambar, jadi dibuang.
    for induk in list(badan.iter()):
        for paragraf in list(induk.findall(f"{W}p")):
            st = paragraf.find(f"{W}pPr/{W}pStyle")
            if (st is not None and st.get(f"{W}val") == "ImageCaption"
                    and "".join(t.text or "" for t in paragraf.iter(f"{W}t")).strip() == "image"):
                induk.remove(paragraf)

    # DAFTAR PUSTAKA dan LAMPIRAN bukan bab bernomor; pakai gaya tanpa nomor
    # agar tidak menambah hitungan bab.
    for paragraf in badan.findall(f"{W}p"):
        ppr = paragraf.find(f"{W}pPr")
        if ppr is None:
            continue
        gaya = ppr.find(f"{W}pStyle")
        if gaya is None or gaya.get(f"{W}val") != "Heading1":
            continue
        teks = "".join(simpul.text or "" for simpul in paragraf.iter(f"{W}t"))
        if teks.upper().startswith(("DAFTAR PUSTAKA", "LAMPIRAN")):
            gaya.set(f"{W}val", GAYA_TANPA_NOMOR)

    awalan: list[ET.Element] = []
    if sampul is not None:
        p_sampul = ET.fromstring(_p_sampul())
        _anak(p_sampul, "pPr").append(
            _sect_salin(sect_akhir, margin_nol=True, format_nomor="lowerRoman",
                        mulai="1", pakai_footer=False))
        awalan.append(p_sampul)

    # Judul pertama sudah berada di awal seksi baru; matikan page break-nya
    # agar tidak muncul halaman kosong sesudah sampul.
    p_isi = ET.fromstring(_p_judul("DAFTAR ISI"))
    _anak(_anak(p_isi, "pPr"), "pageBreakBefore").set(f"{W}val", "0")
    awalan.append(p_isi)
    # Entri bab bernomor dan subbab saja; daftar pada bagian awal tidak
    # dicantumkan, sama seperti field TOC Word yang hanya membaca gaya Heading.
    isi_toc = [e for e in baca_daftar("toc")
               if e[0] != "chapter" or e[1] or not e[2].upper().startswith("DAFTAR ")
               or e[2].upper().startswith("DAFTAR PUSTAKA")]
    for xml in _p_daftar_terisi(r' TOC \o "1-3" \h \z \u ', isi_toc):
        awalan.append(ET.fromstring(xml))
    # Field TOC yang kosong membuat Word menampilkan pesan galat, jadi daftar
    # gambar/tabel hanya dibuat bila keterangannya memang ada di naskah.
    # Sakelar \t pada field TOC mencocokkan NAMA gaya ("Image Caption"), bukan
    # ID-nya ("ImageCaption"); dengan ID, Word menganggap daftarnya kosong.
    # Daftar gambar/tabel memakai field TC tersembunyi pada tiap keterangan
    # (\\f g untuk gambar, \\f t untuk tabel). Sakelar \\t berbasis nama gaya
    # gagal di sebagian Word (nama gaya dan pemisah daftar bergantung pada
    # pengaturan regional), sehingga daftar menjadi kosong saat diperbarui.
    for judul, gaya, kode in (("DAFTAR GAMBAR", "ImageCaption", "g"),
                              ("DAFTAR TABEL", "TableCaption", "t")):
        if f'w:val="{gaya}"' not in mentah:
            continue
        entri = baca_daftar("lof" if gaya == "ImageCaption" else "lot")
        _sisip_tc(badan, gaya, kode, entri)
        awalan.append(ET.fromstring(_p_judul(judul)))
        for xml in _p_daftar_terisi(rf' TOC \h \z \f {kode} ', entri):
            awalan.append(ET.fromstring(xml))
    # Paragraf terakhir bagian awal memuat properti seksinya.
    _anak(awalan[-1], "pPr").append(
        _sect_salin(sect_akhir, margin_nol=False, format_nomor="lowerRoman",
                    mulai="2", pakai_footer=True))

    for posisi, simpul in enumerate(awalan):
        badan.insert(posisi, simpul)
    isi["word/document.xml"] = ET.tostring(akar, encoding="UTF-8", xml_declaration=True)

    # Tanpa penanda versi, Word membuka berkas dalam mode kompatibilitas dan
    # meminta konfirmasi pemutakhiran format setiap kali disimpan.
    if "word/settings.xml" in isi:
        pengaturan = isi["word/settings.xml"].decode("utf-8")
        # Skema OOXML mewajibkan urutan: updateFields lalu compat, keduanya
        # sebelum rsids/themeFontLang/clrSchemeMapping dan seterusnya.
        sisip = ""
        # Minta Word memperbarui semua field (daftar isi, gambar, tabel) saat
        # berkas dibuka; Word menampilkan dialog konfirmasi sekali.
        if "updateFields" not in pengaturan:
            sisip += '<w:updateFields w:val="true"/>'
        if "compatibilityMode" not in pengaturan:
            sisip += ('<w:compat><w:compatSetting w:name="compatibilityMode" '
                      'w:uri="http://schemas.microsoft.com/office/word" w:val="15"/>'
                      "</w:compat>")
        if sisip:
            sesudah = re.search(r"<(?:w:hdrShapeDefaults|w:footnotePr|w:endnotePr|w:compat|"
                                r"w:docVars|w:rsids|m:mathPr|w:attachedSchema|"
                                r"w:themeFontLang|w:clrSchemeMapping)\b", pengaturan)
            posisi = sesudah.start() if sesudah else pengaturan.index("</w:settings>")
            pengaturan = pengaturan[:posisi] + sisip + pengaturan[posisi:]
        isi["word/settings.xml"] = pengaturan.encode("utf-8")

    _pasang_penomoran(isi)
    isi["word/footer1.xml"] = _footer_xml()
    tambahan = (
        f'<Relationship Id="{ID_FOOTER}" Type="http://schemas.openxmlformats.org/'
        'officeDocument/2006/relationships/footer" Target="footer1.xml"/>'
    )
    if sampul is not None:
        isi["word/media/sampul.png"] = sampul.read_bytes()
        tambahan += (
            f'<Relationship Id="{ID_SAMPUL}" Type="http://schemas.openxmlformats.org/'
            'officeDocument/2006/relationships/image" Target="media/sampul.png"/>'
        )
    isi["word/_rels/document.xml.rels"] = (
        isi["word/_rels/document.xml.rels"].decode("utf-8")
        .replace("</Relationships>", f"{tambahan}</Relationships>").encode("utf-8")
    )

    tipe = isi["[Content_Types].xml"].decode("utf-8")
    if "footer+xml" not in tipe:
        tipe = tipe.replace(
            "</Types>",
            '<Override PartName="/word/footer1.xml" ContentType="application/vnd.'
            'openxmlformats-officedocument.wordprocessingml.footer+xml"/></Types>')
    if 'Extension="png"' not in tipe:
        tipe = tipe.replace(
            "</Types>", '<Default Extension="png" ContentType="image/png"/></Types>')
    isi["[Content_Types].xml"] = tipe.encode("utf-8")

    with zipfile.ZipFile(docx, "w", zipfile.ZIP_DEFLATED) as zout:
        for nama, data in isi.items():
            zout.writestr(nama, data)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--utama", type=Path, default=ROOT / "praskripsi.tex")
    parser.add_argument("--keluaran", type=Path, default=ROOT / "build" / "praskripsi.docx")
    args = parser.parse_args()

    if shutil.which("pandoc") is None:
        mati("Pandoc belum terpasang. macOS: brew install pandoc; Windows: unduh dari https://pandoc.org/installing.html")

    csl = ROOT / "assets" / "ieee.csl"
    if not csl.is_file():
        mati(f"Berkas gaya sitasi tidak ditemukan: {csl}")

    kerja = args.keluaran.parent / "docx"
    kerja.mkdir(parents=True, exist_ok=True)

    # Sampul diambil dari halaman pertama PDF; disiapkan lebih dulu karena
    # menentukan perlu tidaknya blok judul berupa teks.
    pdf = pdf_siap(args.utama, args.keluaran.with_suffix(".pdf"))
    sampul = render_sampul(pdf, kerja / "sampul.png") if pdf else None
    if sampul is None:
        print("PERINGATAN  Sampul gambar tidak tersedia; memakai blok judul teks")

    sumber = kerja / "sumber.tex"
    sumber.write_text(
        sumber_gabungan(metadata(), urutan_input(args.utama), blok_sampul=sampul is None),
        encoding="utf-8",
    )

    # Tahap 1: LaTeX -> Markdown, tanpa citeproc.
    antara = subprocess.run(
        # --columns besar: tabel tanpa lebar kolom eksplisit tidak diberi lebar
        # relatif dari panjang teks Markdown (mis. path gambar), sehingga Word
        # mengatur lebarnya sendiri dari isi sel.
        ["pandoc", str(sumber), "--from=latex", "--to=markdown", "--wrap=preserve",
         "--columns=100000",
         f"--resource-path={ROOT}"],
        capture_output=True, text=True,
    )
    if antara.returncode != 0:
        mati(f"Pandoc gagal membaca sumber LaTeX:\n{antara.stderr.strip()}")

    # Tandai tempat daftar pustaka; tanpa ini citeproc menaruhnya di akhir
    # dokumen, yaitu sesudah lampiran.
    markdown = re.sub(
        r"^(#\s+DAFTAR PUSTAKA.*)$",
        r"\1\n\n::: {#refs}\n:::\n",
        antara.stdout,
        count=1,
        flags=re.M,
    )
    berkas_md = kerja / "sumber.md"
    berkas_md.write_text(markdown, encoding="utf-8")

    # Tahap 2: Markdown -> Word, dengan sitasi IEEE dan gaya pedoman.
    perintah = [
        "pandoc", str(berkas_md),
        "--from=markdown",
        "--citeproc",
        # Locale Indonesia agar "hlm. 18" dikenali sebagai halaman: [31, hlm. 18].
        "--metadata=lang:id-ID",
        f"--bibliography={ROOT / 'bibliography' / 'references.bib'}",
        f"--csl={csl}",
        f"--reference-doc={reference_docx(kerja / 'reference.docx')}",
        f"--resource-path={ROOT}",
        "-o", str(args.keluaran),
    ]
    hasil = subprocess.run(perintah, capture_output=True, text=True)
    if hasil.returncode != 0:
        mati(f"Pandoc gagal menulis .docx:\n{hasil.stderr.strip()}")
    for aliran in (antara.stderr, hasil.stderr):
        if aliran.strip():
            print(aliran.strip())

    # Samakan dengan PDF: sampul, daftar isi/tabel, dan nomor halaman.
    susun_seperti_pdf(args.keluaran, sampul)
    print(f"LULUS  {args.keluaran}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
