% upnjatim-skripsi.cls -- template tidak resmi pra-skripsi/skripsi
% Fakultas Ilmu Komputer UPN "Veteran" Jawa Timur.
% Struktur diadaptasi dari filkomproposal.cls (template tidak resmi FILKOM UB)
% karya Pande Kadek Nathan Prabhaswara Sudiara Putra, LPPL 1.3c.
% Distributed under the LPPL 1.3c or later.
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{upnjatim-skripsi}[2026/09/13 v0.1.0 Template tidak resmi skripsi Fasilkom UPN Veteran Jatim]

\RequirePackage{kvoptions}
\SetupKeyvalOptions{family=upn,prefix=upn@}
\DeclareStringOption[praskripsi]{jenis}
\DeclareStringOption[putih]{sampul}
\DeclareBoolOption{ketat}
\DeclareBoolOption{pemenggalan}
\ProcessKeyvalOptions*
\LoadClass[a4paper,12pt,oneside]{report}

\newif\ifupn@praskripsi
\def\upn@tmp{praskripsi}
\ifx\upn@jenis\upn@tmp
  \upn@praskripsitrue
\else
  \def\upn@tmp{skripsi}
  \ifx\upn@jenis\upn@tmp
    \upn@praskripsifalse
    \ClassWarningNoLine{upnjatim-skripsi}{jenis=skripsi baru menyediakan sampul; halaman pengesahan, persetujuan, orisinalitas, dan abstrak belum tersedia}
  \else
    \ClassError{upnjatim-skripsi}{Opsi jenis=\upn@jenis\space tidak dikenal}{Gunakan jenis=praskripsi atau jenis=skripsi.}
  \fi
\fi

\newif\ifupn@sampuloranye
\def\upn@tmp{oranye}
\ifx\upn@sampul\upn@tmp \upn@sampuloranyetrue \fi

\RequirePackage[indonesian]{babel}
\RequirePackage{fontspec}
\RequirePackage{csquotes}
\DeclareQuoteAlias[american]{english}{indonesian}
\RequirePackage[left=4cm,right=3cm,top=3cm,bottom=3cm,footskip=0.6cm]{geometry}
\RequirePackage{setspace}
\RequirePackage{indentfirst}
\RequirePackage{graphicx}
\RequirePackage{xcolor}
\RequirePackage{tikz}
\usetikzlibrary{arrows.meta,positioning,shapes.geometric,shapes.misc,calc}
\RequirePackage{titlesec}
\RequirePackage{titletoc}
\RequirePackage{caption}
\RequirePackage{booktabs}
\RequirePackage{longtable}
\RequirePackage{array}
\RequirePackage{tabularx}
\RequirePackage{multirow}
\RequirePackage{enumitem}
\RequirePackage[fleqn]{amsmath}
\RequirePackage{unicode-math}
\setmathfont{texgyretermes-math.otf}
% Times New Roman tidak punya glif ✓; ambil dari font matematika agar
% \checkmark juga aman dipakai di luar mode matematika (mis. tabel jadwal).
\AtBeginDocument{%
  \let\upn@checkmark\checkmark
  \renewcommand{\checkmark}{\ensuremath{\upn@checkmark}}}
\RequirePackage{listings}
\RequirePackage{xurl}
\RequirePackage{xkeyval}
\RequirePackage[backend=biber,style=ieee,language=english,autolang=none,
  isbn=false,doi=true,url=true,dashed=false]{biblatex}
\DeclareLanguageMapping{indonesian}{english}
\RequirePackage{hyperref}
\urlstyle{same}

% ---------------------------------------------------------------------------
% Font: Times New Roman (isi), Arial (sampul), Courier New (kode).
% Tanpa opsi ketat, font TeX Gyre dipakai sebagai pengganti (mis. Overleaf).
% ---------------------------------------------------------------------------
\newcommand{\upn@cadangan}[3]{%
  \ClassWarningNoLine{upnjatim-skripsi}{Font #2 tidak ditemukan; memakai #3 sebagai pengganti. Gunakan #2 untuk hasil akhir}%
  #1{#3}[Extension=.otf,UprightFont=*-regular,BoldFont=*-bold,
    ItalicFont=*-italic,BoldItalicFont=*-bolditalic]}
\newcommand{\upn@pilihfont}[3]{%
  \IfFontExistsTF{#2}{#1{#2}}{%
    \ifupn@ketat
      \ClassError{upnjatim-skripsi}{Font #2 wajib saat opsi ketat dipakai}{Pasang #2 atau hapus opsi ketat.}%
    \else
      \upn@cadangan{#1}{#2}{#3}%
    \fi}}
\upn@pilihfont{\setmainfont}{Times New Roman}{texgyretermes}
\upn@pilihfont{\setmonofont}{Courier New}{texgyrecursor}
\upn@pilihfont{\newfontfamily\upn@fontsampul}{Arial}{texgyreheros}

% ---------------------------------------------------------------------------
% Metadata
% ---------------------------------------------------------------------------
\newcommand{\upn@judul}{}
\newcommand{\upn@nama}{}
\newcommand{\upn@npm}{}
\newcommand{\upn@pembimbingsatu}{}
\newcommand{\upn@pembimbingdua}{}
\newcommand{\upn@prodi}{Informatika}
\newcommand{\upn@fakultas}{Fakultas Ilmu Komputer}
\newcommand{\upn@universitas}{Universitas Pembangunan Nasional Veteran Jawa Timur}
\newcommand{\upn@kementerian}{Kementerian Pendidikan Tinggi, Sains, dan Teknologi}
\newcommand{\upn@kota}{Surabaya}
\newcommand{\upn@tahun}{\the\year}
\newcommand{\upn@logo}{assets/logo-upnjatim.png}

\define@key{upn}{judul}{\renewcommand{\upn@judul}{#1}}
\define@key{upn}{nama}{\renewcommand{\upn@nama}{#1}}
\define@key{upn}{npm}{\renewcommand{\upn@npm}{#1}}
\define@key{upn}{pembimbing-satu}{\renewcommand{\upn@pembimbingsatu}{#1}}
\define@key{upn}{pembimbing-dua}{\renewcommand{\upn@pembimbingdua}{#1}}
\define@key{upn}{program-studi}{\renewcommand{\upn@prodi}{#1}}
\define@key{upn}{fakultas}{\renewcommand{\upn@fakultas}{#1}}
\define@key{upn}{universitas}{\renewcommand{\upn@universitas}{#1}}
\define@key{upn}{kementerian}{\renewcommand{\upn@kementerian}{#1}}
\define@key{upn}{kota}{\renewcommand{\upn@kota}{#1}}
\define@key{upn}{tahun}{\renewcommand{\upn@tahun}{#1}}
\define@key{upn}{logo}{\renewcommand{\upn@logo}{#1}}
\newcommand{\upnsetup}[1]{\setkeys{upn}{#1}}

\newcommand{\upn@wajib}[2]{%
  \ifx#1\@empty
    \ClassError{upnjatim-skripsi}{Metadata #2 belum diisi}{Isi kunci #2 pada metadata.tex.}%
  \fi}
\AtBeginDocument{%
  \upn@wajib{\upn@judul}{judul}%
  \upn@wajib{\upn@nama}{nama}%
  \upn@wajib{\upn@npm}{npm}%
  \upn@wajib{\upn@pembimbingsatu}{pembimbing-satu}%
  \hypersetup{hidelinks,unicode,pdftitle={\upn@judul},pdfauthor={\upn@nama}}%
}

% ---------------------------------------------------------------------------
% Tata letak isi: 12 pt, spasi 1,5 baris Word (20,7 pt), tanpa jarak antar
% paragraf seperti template Word 2025, indentasi baris pertama 1,27 cm.
% ---------------------------------------------------------------------------
\setstretch{1.43}
\setlength{\parindent}{1.27cm}
\setlength{\parskip}{0pt}
% Pedoman dan template Word tidak memenggal kata di ujung baris; kata yang
% tidak muat dipindahkan utuh ke baris berikutnya. Nyalakan pemenggalan
% dengan opsi class "pemenggalan".
\ifupn@pemenggalan
  \setlength{\emergencystretch}{2em}
\else
  \hyphenpenalty=10000
  \exhyphenpenalty=10000
  \tolerance=9999
  \setlength{\emergencystretch}{3em}
\fi
\clubpenalty=10000
\widowpenalty=10000
\displaywidowpenalty=10000
\setlength{\mathindent}{1.27cm}

\setlist{nosep}
\setlist[enumerate]{leftmargin=1.25cm,labelwidth=0.6cm,labelsep=0pt,align=left}
\setlist[itemize]{leftmargin=1.25cm,labelwidth=0.6cm,labelsep=0pt,align=left}

% ---------------------------------------------------------------------------
% Penomoran: BAB I, subbab 1.1., gambar/tabel/persamaan 2.1
% ---------------------------------------------------------------------------
\renewcommand{\thechapter}{\Roman{chapter}}
\renewcommand{\thesection}{\arabic{chapter}.\arabic{section}}
\renewcommand{\thesubsection}{\thesection.\arabic{subsection}}
\renewcommand{\thesubsubsection}{\thesubsection.\arabic{subsubsection}}
\renewcommand{\thefigure}{\arabic{chapter}.\arabic{figure}}
\renewcommand{\thetable}{\arabic{chapter}.\arabic{table}}
\renewcommand{\theequation}{\arabic{chapter}.\arabic{equation}}
\setcounter{secnumdepth}{3}
\setcounter{tocdepth}{2}

% 16,8 pt x setstretch 1,43 = jarak baris judul bab 24 pt (Pedoman hlm. 31).
\newcommand{\upn@fontbab}{\fontsize{14pt}{16.8pt}\selectfont\setlength{\parskip}{0pt}}
\newcommand{\upn@kapital}{\MakeUppercase}
\titleformat{\chapter}[display]
  {\centering\bfseries\upn@fontbab}{BAB \thechapter}{0pt}{\MakeUppercase}
\titleformat{name=\chapter,numberless}[block]
  {\centering\bfseries\upn@fontbab}{}{0pt}{\upn@kapital}
% Dikalibrasi terhadap Pedoman hlm. 31: puncak "BAB I" +-31 mm; judul ke teks
% 41,4 pt (satu baris kosong) seperti template Word 2025.
\titlespacing*{\chapter}{0pt}{-22.7pt}{21.3pt}
\titlespacing*{name=\chapter,numberless}{0pt}{-22.7pt}{21.3pt}
\titleformat{\section}[hang]
  {\bfseries\normalsize}{\makebox[1.27cm][l]{\thesection.}}{0pt}{}
\titleformat{\subsection}[hang]
  {\bfseries\normalsize}{\thesubsection.}{0.5em}{}
\titleformat{\subsubsection}[hang]
  {\bfseries\normalsize}{\thesubsubsection.}{0.5em}{}
% Sebelum judul: subbab 32,6 pt dan sub-subbab 29,6 pt antar garis dasar
% (Pedoman hlm. 31-38). Sesudah judul tanpa jarak tambahan; kalimat pertama
% langsung di baris berikutnya (atas permintaan dosen pembimbing).
\titlespacing*{\section}{0pt}{12pt}{0pt}
\titlespacing*{\subsection}{0pt}{9pt}{0pt}
\titlespacing*{\subsubsection}{0pt}{9pt}{0pt}

% ---------------------------------------------------------------------------
% Daftar isi, gambar, tabel
% ---------------------------------------------------------------------------
\newcommand{\upn@titik}{\titlerule*[0.4em]{.}}
% Makro terakhir pada format entri menerima judul sebagai argumen.
\titlecontents{chapter}[0pt]{\bfseries}
  {BAB \thecontentslabel\space\MakeUppercase}{\MakeUppercase}{\upn@titik\contentspage}
\titlecontents{section}[1.9cm]{}
  {\contentslabel[\thecontentslabel.]{1.27cm}}{}{\upn@titik\contentspage}
\titlecontents{subsection}[3.2cm]{}
  {\contentslabel[\thecontentslabel.]{1.3cm}}{}{\upn@titik\contentspage}
\titlecontents{figure}[2.5cm]{}
  {\contentslabel[\textbf{\figurename~\thecontentslabel}]{2.5cm}}{}{\upn@titik\contentspage}
\titlecontents{table}[2.2cm]{}
  {\contentslabel[\textbf{\tablename~\thecontentslabel}]{2.2cm}}{}{\upn@titik\contentspage}

\newcommand{\upn@daftar}[2]{% #1 judul, #2 ekstensi berkas
  \clearpage
  \chapter*{#1}%
  \phantomsection
  \addcontentsline{toc}{chapter}{\MakeUppercase{#1}}%
  \begingroup
  \setlength{\parskip}{0pt}%
  \@starttoc{#2}%
  \endgroup
  \clearpage}
\newcommand{\daftarisi}{\upn@daftar{Daftar Isi}{toc}}
\newcommand{\daftargambar}{\upn@daftar{Daftar Gambar}{lof}}
\newcommand{\daftartabel}{\upn@daftar{Daftar Tabel}{lot}}

% ---------------------------------------------------------------------------
% Gambar, tabel, kode sumber
% ---------------------------------------------------------------------------
\captionsetup{font={normalsize,bf},labelsep=space,skip=6pt}
\captionsetup[table]{position=top,justification=raggedright,singlelinecheck=false}
\captionsetup[figure]{position=bottom,justification=centering}
% Lebar judul longtable bawaan hanya 4 inci (kotak di tengah), sehingga judul
% yang rata kiri tampak menjorok. Samakan dengan lebar teks.
\setlength{\LTcapwidth}{\textwidth}
\newcommand{\sumber}[1]{%
  \par\vspace{3pt}{\centering\fontsize{11pt}{13pt}\selectfont Sumber: #1\par}}

% Placeholder gambar: #1 berkas di assets/gambar/, #2 lebar, #3 tinggi. Selama
% berkasnya belum ada, tampil kotak bertuliskan nama berkas; begitu berkas
% ditaruh, gambar asli langsung dipasang tanpa mengubah naskah. Sesudah
% menambah gambar, kompilasi dengan `latexmk -g` agar perubahan terdeteksi.
\newcommand{\gambarsementara}[3]{%
  \IfFileExists{assets/gambar/#1}%
    {\includegraphics[width=#2,height=#3,keepaspectratio]{assets/gambar/#1}}%
    {{\setlength{\fboxsep}{0pt}%
      \fbox{\parbox[c][#3][c]{#2}{\centering\footnotesize\ttfamily
        assets/gambar/#1}}}}}

% Diagram TikZ hitam putih. Bentuk baku diagram alir: lonjong untuk
% mulai/selesai, persegi untuk proses, belah ketupat untuk keputusan, jajar
% genjang untuk masukan/keluaran. Pemakaian:
%   \begin{tikzpicture}[alir] \node[terminal] (a) {Mulai}; ... \end{tikzpicture}
\tikzset{
  alir/.style={font=\small, node distance=5mm and 10mm,
    every node/.append style={align=center}},
  terminal/.style={draw, rounded rectangle, minimum width=2.4cm,
    minimum height=7mm},
  proses/.style={draw, rectangle, text width=3.8cm, minimum height=7mm},
  keputusan/.style={draw, diamond, aspect=2.4, inner sep=1pt,
    text width=2.6cm},
  io/.style={draw, trapezium, trapezium left angle=70,
    trapezium right angle=110, trapezium stretches body,
    text width=3.4cm, minimum height=7mm},
  panah/.style={-{Stealth[length=2mm]}},
}

\DeclareCaptionFont{upnkode}{\fontsize{9pt}{11pt}\selectfont}
\captionsetup[lstlisting]{font=upnkode,labelfont=bf,labelsep=colon,
  justification=raggedright,singlelinecheck=false,skip=3pt}
\renewcommand{\lstlistingname}{Algoritme}
\lstset{
  basicstyle=\setstretch{1}\ttfamily\fontsize{9pt}{11pt}\selectfont,
  numberstyle=\ttfamily\fontsize{9pt}{11pt}\selectfont,
  numbers=left, numbersep=8pt, xleftmargin=2em, framexleftmargin=2em,
  frame=single, breaklines=true, columns=fullflexible, keepspaces=true,
  showstringspaces=false, tabsize=2, captionpos=t, numberbychapter=false,
  aboveskip=6pt, belowskip=6pt
}

% ---------------------------------------------------------------------------
% Daftar pustaka: IEEE, spasi tunggal
% ---------------------------------------------------------------------------
% Bahasa aktif babel "indonesian" dipetakan ke lbx english; isi keduanya.
\DefineBibliographyStrings{english}{
  and={dan}, in={dalam}, url={Tersedia}, urlseen={Diakses},
}
\DefineBibliographyStrings{indonesian}{
  and={dan}, in={dalam}, url={Tersedia}, urlseen={Diakses},
}
% biblatex-ieee mengubah judul ke sentence case; pertahankan kapitalisasi
% sesuai berkas .bib (contoh Pedoman hlm. 23) agar judul Indonesia tidak rusak.
\DeclareFieldFormat{sentencecase}{#1}
\setlength{\bibitemsep}{6pt}
% Judul dicetak di luar grup spasi tunggal agar posisinya sama dengan judul bab.
\newcommand{\daftarpustaka}{%
  \clearpage
  \chapter*{Daftar Pustaka}%
  \phantomsection
  \addcontentsline{toc}{chapter}{DAFTAR PUSTAKA}%
  \begingroup
  \setstretch{1}%
  \printbibliography[heading=none]%
  \endgroup}

% ---------------------------------------------------------------------------
% Bagian dokumen
% ---------------------------------------------------------------------------
\newcommand{\bagianutama}{\clearpage\pagenumbering{arabic}}

\newcounter{lampiran}
\newcommand{\lampiran}[1]{%
  \clearpage
  \refstepcounter{lampiran}%
  \edef\upn@nolampiran{\arabic{lampiran}}%
  % \\ tidak boleh berada di dalam \MakeUppercase; kapitalkan per baris.
  \begingroup
  \let\upn@kapital\@firstofone
  \chapter*{\MakeUppercase{Lampiran \upn@nolampiran}\\\MakeUppercase{#1}}%
  \endgroup
  \phantomsection
  \addcontentsline{toc}{chapter}{LAMPIRAN \upn@nolampiran\space\MakeUppercase{#1}}%
  \setcounter{figure}{0}\setcounter{table}{0}\setcounter{equation}{0}%
  \renewcommand{\thefigure}{L\arabic{lampiran}.\arabic{figure}}%
  \renewcommand{\thetable}{L\arabic{lampiran}.\arabic{table}}%
  \renewcommand{\theequation}{L\arabic{lampiran}.\arabic{equation}}}

% ---------------------------------------------------------------------------
% Sampul mengikuti "template skripsi 2025.docx": tanpa pita oranye, logo
% 3,82 cm pada 40,4 mm dari kiri dan 13 mm dari atas, pita kuning bergaris
% tepi gelap pada 61-65 mm, teks Arial pada 39,9 mm dari kiri. Posisi diukur
% dari PDF template tersebut (koordinat garis dasar baris pertama tiap blok).
% ---------------------------------------------------------------------------
\definecolor{upnoranye}{HTML}{FF914D}
\definecolor{upnkuning}{HTML}{FFFF00}
\definecolor{upntepipita}{HTML}{263953}

\newcommand{\upn@labeljenis}{%
  \textbf{\ifupn@praskripsi PRA-SKRIPSI\else SKRIPSI\fi}}

\newcommand{\buatsampul}{%
  \clearpage
  \pagenumbering{roman}%
  \thispagestyle{empty}%
  \hypersetup{pageanchor=false}%
  \IfFileExists{\upn@logo}{}{%
    \ClassError{upnjatim-skripsi}{Logo tidak ditemukan: \upn@logo}{Periksa kunci logo pada metadata.tex.}}%
  \begin{tikzpicture}[remember picture,overlay,x=1mm,y=-1mm,
      shift={(current page.north west)},
      blok/.style={anchor=base west,inner sep=0pt}]
    \ifupn@sampuloranye
      \fill[upnoranye] (0,65.7) rectangle (210,297);
    \fi
    \filldraw[fill=upnkuning,draw=upntepipita,line width=0.9mm]
      (-2,61.25) rectangle (206.35,65.25);
    \node[anchor=north west,inner sep=0pt] at (40.4,13)
      {\includegraphics[width=38.2mm,keepaspectratio]{\upn@logo}};
    \begin{scope}[every node/.append style={font=\upn@fontsampul\setstretch{1}}]
    \ifupn@sampuloranye\color{white}\fi
    \node[blok] at (39.86,85.36)
      {\fontsize{14pt}{16.1pt}\selectfont\upn@labeljenis};
    \node[blok] at (39.86,102.19)
      {\parbox[t]{140mm}{\fontsize{18pt}{20.7pt}\selectfont\bfseries
       \setlength{\parskip}{0pt}\hyphenpenalty=10000\exhyphenpenalty=10000
       \tolerance=9999\emergencystretch=3em\hbadness=10000
       \MakeUppercase{\upn@judul}\par}};
    \node[blok] at (39.86,149.55)
      {\parbox[t]{140mm}{\fontsize{14pt}{16.1pt}\selectfont\raggedright
       \textbf{\MakeUppercase{\upn@nama}}\par
       NPM \upn@npm\par}};
    \node[blok] at (39.86,180.38)
      {\parbox[t]{140mm}{\fontsize{14pt}{16.1pt}\selectfont\raggedright
       \textbf{DOSEN PEMBIMBING}\par
       \upn@pembimbingsatu\par
       \ifx\upn@pembimbingdua\@empty\else\upn@pembimbingdua\par\fi}};
    \node[blok] at (39.86,216.23)
      {\parbox[t]{150mm}{\fontsize{12pt}{13.8pt}\selectfont\bfseries\raggedright
       \MakeUppercase{\upn@kementerian}\par
       \MakeUppercase{\upn@universitas}\par
       \MakeUppercase{\upn@fakultas}\par
       \MakeUppercase{Program Studi \upn@prodi}\par
       \MakeUppercase{\upn@kota}\par
       \upn@tahun\par}};
    \end{scope}
  \end{tikzpicture}%
  \null
  \clearpage
  \hypersetup{pageanchor=true}%
  \setcounter{page}{2}}

\endinput
