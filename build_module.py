#!/usr/bin/env python3
"""Build Modul-Analisis-ISPA-Indonesia.pdf (A4 landscape, beginner-friendly ID)."""
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
    PageBreak, KeepTogether,
)

OUT = "/home/hatch/workspace/coursera-modules/Modul-Analisis-ISPA-Indonesia.pdf"
CHARTS = "/home/hatch/workspace/ispa-indonesia/charts"
W, H = landscape(A4)
NAVY = HexColor("#1E3A8A")
TEAL = HexColor("#0D9488")
CORAL = HexColor("#E76F51")
DARK = HexColor("#1F2937")
GRAY = HexColor("#6B7280")
LIGHT = HexColor("#EFF6FF")

styles = {
    "cover": ParagraphStyle("cover", fontName="Helvetica-Bold", fontSize=30, leading=36,
                            textColor=NAVY, alignment=TA_LEFT),
    "coversub": ParagraphStyle("coversub", fontName="Helvetica", fontSize=16, leading=22,
                               textColor=DARK, alignment=TA_LEFT),
    "h1": ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=22, leading=27,
                         textColor=NAVY, spaceBefore=6, spaceAfter=8),
    "h2": ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=16, leading=20,
                         textColor=TEAL, spaceBefore=8, spaceAfter=6),
    "body": ParagraphStyle("body", fontName="Helvetica", fontSize=12.5, leading=18,
                           textColor=DARK, spaceAfter=7),
    "bullet": ParagraphStyle("bullet", parent=ParagraphStyle("b", fontName="Helvetica",
                             fontSize=12.5, leading=18, textColor=DARK, spaceAfter=5,
                             leftIndent=16, bulletIndent=6)),
    "code": ParagraphStyle("code", fontName="Courier", fontSize=10.5, leading=15,
                          textColor=DARK, backColor=LIGHT, spaceAfter=8,
                          leftIndent=8, borderPadding=(6, 6, 6)),
    "caption": ParagraphStyle("caption", fontName="Helvetica-Oblique", fontSize=10.5,
                              leading=14, textColor=GRAY, alignment=TA_CENTER,
                              spaceBefore=4, spaceAfter=10),
    "warn": ParagraphStyle("warn", fontName="Helvetica", fontSize=12.5, leading=18,
                           textColor=HexColor("#92400E"), backColor=HexColor("#FEF3C7"),
                           borderPadding=(8, 8, 8), spaceAfter=8),
}

story = []


def P(text, style="body"):
    story.append(Paragraph(text, styles[style]))


def B(text):
    story.append(Paragraph(text, styles["bullet"], bulletText="•"))


def CODE(text):
    story.append(Paragraph(text.replace(" ", "&nbsp;").replace("\n", "<br/>"), styles["code"]))


def CHART(fname, caption, width=21 * cm):
    story.append(Image(f"{CHARTS}/{fname}", width=width, height=width * 0.58))
    P(caption, "caption")


def TABLE(data, widths=None):
    t = Table([[Paragraph(str(c), styles["body"]) for c in row] for row in data],
              colWidths=widths)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#FFFFFF")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("GRID", (0, 0), (-1, -1), 0.5, GRAY),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor("#FFFFFF"), LIGHT]),
    ]))
    story.append(t)
    story.append(Spacer(1, 10))


# ---------- COVER ----------
story.append(Spacer(1, 3 * cm))
P("MODUL BELAJAR", "cover")
P("Modul Analisis ISPA di Indonesia 2026", "cover")
P("Studi Kasus Kesehatan Masyarakat: dari Kompilasi Data sampai Rekomendasi", "coversub")
story.append(Spacer(1, 0.6 * cm))
P("Modul ini mengajak kamu membangun satu project analisis data nyata dari nol: "
  "kasus Infeksi Saluran Pernapasan Akut (ISPA) di Indonesia pada 2026. Kamu akan "
  "belajar mengompilasi data dari sumber resmi, memasukkannya ke SQLite, menjawab "
  "pertanyaan dengan SQL, memvisualisasikan dengan Python, dan menginterpretasikan "
  "hasilnya dengan jujur — termasuk batasan datanya.", "coversub")
story.append(Spacer(1, 0.5 * cm))
P("Dataset KOMPILASI: angka-angka resmi yang dipublikasikan (Kemenkes / SKDR / ISPU). "
  "Bukan file mentah resmi — setiap angka dicatat sumber dan tanggalnya. "
  "Lihat data/SOURCES.md.", "warn")
story.append(PageBreak())

# ---------- 1. APA ITU ISPA ----------
P("1. Apa Itu ISPA dan Mengapa 2026 Penting", "h1")
P("ISPA adalah Infeksi Saluran Pernapasan Akut — infeksi pada hidung, tenggorokan, "
  "dan saluran napas yang gejalanya meliputi batuk, pilek, nyeri tenggorokan, demam, "
  "dan pada kasus berat sesak napas. ISPA mudah menular lewat percikan droplet saat "
  "batuk atau bersin, sehingga menjadi penyakit dengan kunjungan terbanyak di "
  "puskesmas.", "body")
P("Pada 2026, tiga hal terjadi bersamaan: musim kemarau yang panjang, kebakaran hutan "
  "dan lahan (karhutla) yang meluas, dan kualitas udara yang memburuk. Kombinasi ini "
  "membuat laporan ISPA melonjak. Kemenkes mencatat 14.088.945 laporan ISPA nasional "
  "hingga minggu epidemiologi ke-38 tahun 2026.", "body")
P("Kenapa topik ini bagus untuk portofolio?", "h2")
B("Topik aktual dan berdampak sosial — bukan dataset mainan.")
B("Datanya menantang: tidak ada file mentah resmi, jadi kamu belajar kompilasi dan verifikasi sumber.")
B("Analisisnya berlapis: tren nasional, perbandingan provinsi, per kapita, kelompok usia, dan kualitas udara.")
B("Hasilnya harus diinterpretasikan hati-hati — latihan kejujuran analitis yang recruiter hargai.")
story.append(PageBreak())

# ---------- 2. PETA DATA ----------
P("2. Peta Data: Dua Seri yang Tidak Boleh Dicampur", "h1")
P("Ini konsep paling penting di project ini. Ada DUA seri data dengan cakupan dan "
  "tanggal berbeda:", "body")
TABLE([
    ["Seri", "Cakupan", "Periode", "Total"],
    ["Nasional SKDR", "Seluruh Indonesia (laporan SKDR)", "s.d. minggu ke-38 2026", "14.088.945 laporan"],
    ["Pemantauan karhutla", "63 kab/kota, 7 provinsi terdampak", "18 Agt–13 Okt 2026", "283.270 kasus"],
])
P("Aturan emas: kedua seri TIDAK PERNAH dijumlahkan, tidak pernah digabung dalam "
  "satu total atau satu chart. Seri karhutla adalah pemantauan khusus di wilayah "
  "terdampak, bukan potongan dari total nasional. Mencampurnya adalah kesalahan "
  "analisis yang paling sering terjadi pada data seperti ini.", "body")
P("Sumber-sumber lain yang dipakai:", "h2")
B("ISPU KemenLH: konsentrasi PM2,5 dan kategori kualitas udara.")
B("Dinkes DKI Jakarta: seri bulanan dan tahunan kasus ISPA Jakarta.")
B("BPS (Statistik Indonesia 2026): populasi per provinsi sebagai denominator per kapita.")
B("WHO: penjelasan mekanisme asap kebakaran terhadap saluran pernapasan.")
story.append(PageBreak())

# ---------- 3. MENILAI SUMBER ----------
P("3. Cara Menilai Kualitas Sumber", "h1")
P("Karena datanya dikompilasi, kualitas sumber adalah bagian dari analisis. "
  "Sebelum memakai sebuah angka, tanyakan:", "body")
B("Siapa penerbit aslinya? Utamakan instansi resmi (Kemenkes, BPS, KemenLH, Dinkes).")
B("Apakah angka itu kutipan langsung dari instansi, atau sudah diolah pihak ketiga? Artikel yang mengutip Kemenkes dengan nama pejabat dan tanggal rilis lebih kuat daripada artikel tanpa atribusi.")
B("Apakah tanggal dan cakupannya jelas? Angka tanpa tanggal dan cakupan tidak bisa dipakai.")
B("Apakah konsisten antar sumber? Angka karhutla 283.270 muncul di beberapa media dengan rincian yang sama — itu tanda baik.")
B("Apakah angkanya eksak atau dibaca dari grafik? Angka peringkat 5–10 SKDR dibaca dari grafik batang (dibulatkan) — catat itu, jangan berpura-pura eksak.")
P("Praktik yang dipakai project ini: setiap angka dicatat di data/SOURCES.md bersama "
  "sumber dan tanggal rilisnya. Kalau sebuah angka tidak punya sumber, angka itu "
  "tidak masuk dataset.", "body")
story.append(PageBreak())

# ---------- 4. KOMPILASI ----------
P("4. Langkah 1 — Kompilasi Dataset (CSV)", "h1")
P("Dataset disimpan sebagai file CSV di data/compiled/. Setiap file punya kolom "
  "sumber dan catatan, supaya siapa pun bisa menelusur tiap angka. Contoh isi "
  "file skdr_provinsi_2026.csv:", "body")
TABLE([
    ["provinsi", "kasus_skdr_2026", "populasi_2026", "catatan"],
    ["Jawa Barat", "2.533.888", "51.160.000", "Angka eksak dari teks artikel"],
    ["Banten", "832.030", "12.640.000", "Dibaca dari grafik — nilai dibulatkan"],
    ["DI Yogyakarta", "388.380", "(kosong)", "Dikeluarkan dari peringkat per kapita"],
])
P("Tiga keputusan penting pada tahap ini:", "body")
B("Angka 4 provinsi teratas dikutip eksak dari teks artikel; peringkat 5–10 dibaca dari grafik dan dicatat sebagai nilai dibulatkan.")
B("Populasi memakai SATU vintage (BPS 2026). Tiga provinsi tanpa angka populasi satu vintage yang terverifikasi (DIY, Sumbar, NTB) dikeluarkan dari peringkat per kapita — nilai absolutnya tetap ditampilkan.")
B("Seri karhutla disimpan di file terpisah (karhutla_series.csv, karhutla_provinsi.csv) agar tidak pernah tercampur dengan seri nasional.")
story.append(PageBreak())

# ---------- 5. SQLITE ----------
P("5. Langkah 2 — Load ke SQLite dan Verifikasi", "h1")
P("SQLite adalah database ringan yang menyimpan seluruh dataset dalam satu file "
  "(.db). Script scripts/load_to_sqlite.py membaca semua CSV dan membuat satu tabel "
  "per file, lalu memverifikasi total yang harus cocok dengan angka publikasi:", "body")
CODE("python scripts/load_to_sqlite.py\n# skdr_provinsi: 10 rows\n# Top-10 SKDR sum: 10,530,385 (must be 10,530,385)\n# Karhutla total 13 Okt: 283270 (must be 283270)")
P("Verifikasi seperti ini disebut <b>reconciliation</b>: jumlahkan data yang dimuat, "
  "bandingkan dengan angka sumber. Kalau tidak cocok, ada yang salah pada tahap "
  "kompilasi — jangan lanjut sebelum cocok.", "body")
P("Mengapa SQLite, bukan langsung analisis di pandas? Karena pertanyaan bisnis "
  "dijawab dengan query SQL asli (file sql/queries.sql), persis seperti di dunia "
  "kerja analis data: data tinggal di database, analisis mengambil lewat query.", "body")
story.append(PageBreak())

# ---------- 6. SQL DASAR ----------
P("6. Langkah 3 — SQL Dasar: SELECT, WHERE, ORDER BY", "h1")
P("Query pertama: peringkat 10 provinsi berdasarkan jumlah kasus. Baca query ini "
  "baris per baris:", "body")
CODE("SELECT provinsi,\n       CAST(kasus_skdr_2026 AS INTEGER) AS kasus\nFROM skdr_provinsi\nORDER BY kasus DESC;")
B("<b>SELECT ... FROM ...</b> — pilih kolom dari tabel. CAST mengubah teks menjadi angka karena CSV menyimpan semua nilai sebagai teks.")
B("<b>ORDER BY kasus DESC</b> — urutkan dari terbesar ke terkecil. Tanpa ini, urutan baris tidak terjamin.")
P("Hasilnya: Jawa Barat 2.533.888 di puncak, NTB 331.950 di dasar top-10. "
  "Untuk pangsa terhadap total nasional, tambahkan perhitungan:", "body")
CODE("SELECT ROUND(100.0 * CAST(kasus_skdr_2026 AS INTEGER) / 14088945, 2)\n       AS persen_nasional\nFROM skdr_provinsi;")
P("100.0 (bukan 100) dipakai supaya pembagiannya menghasilkan desimal, bukan "
  "pembagian bulat. Jabar = 17,98% dari total nasional.", "body")
story.append(PageBreak())

# ---------- 7. AGREGASI ----------
P("7. Langkah 4 — Agregasi SQL: SUM, GROUP BY, CASE WHEN", "h1")
P("Pertanyaan: berapa porsi 4 provinsi teratas dari top-10? Jawab dengan "
  "CASE WHEN (pengelompokan kondisional) + GROUP BY:", "body")
CODE("SELECT CASE WHEN provinsi IN ('Jawa Barat','Jawa Tengah',\n  'DKI Jakarta','Jawa Timur')\n  THEN '4 provinsi teratas' ELSE '6 provinsi lain' END AS kelompok,\n  SUM(CAST(kasus_skdr_2026 AS INTEGER)) AS kasus\nFROM skdr_provinsi\nGROUP BY kelompok;")
P("Hasil: 4 provinsi teratas = 7.868.005 (74,7% dari top-10), 6 provinsi lain = "
  "2.662.380 (25,3%). Pola yang sama dipakai untuk Pulau Jawa vs luar Jawa "
  "(86,3% vs 13,7%) dan untuk pengelompokan lainnya.", "body")
P("Konsep kunci:", "h2")
B("<b>SUM()</b> menjumlahkan satu kolom untuk seluruh baris dalam kelompok.")
B("<b>GROUP BY</b> membagi baris menjadi kelompok, lalu agregasi dihitung per kelompok.")
B("<b>CASE WHEN</b> memberi label kelompok berdasarkan kondisi — seperti IF di Excel.")
story.append(PageBreak())

# ---------- 8. PER KAPITA ----------
P("8. Langkah 5 — Normalisasi Per Kapita", "h1")
P("Angka absolut menipu: provinsi berpenduduk besar otomatis mencatat kasus lebih "
  "banyak. Normalisasi membagi kasus dengan populasi:", "body")
CODE("kasus per 1.000 penduduk = kasus / populasi x 1.000")
P("Contoh: DKI Jakarta 1.600.814 / 10.670.000 x 1.000 = <b>150,0 per 1.000</b>. "
  "Jawa Barat 2.533.888 / 51.160.000 x 1.000 = <b>49,5 per 1.000</b>. Peringkatnya "
  "terbalik dibanding peringkat absolut — dan itulah gunanya normalisasi.", "body")
CHART("03_per_kapita.png", "Kasus per 1.000 penduduk: Jakarta jauh di atas provinsi lain.")
P("Cara membaca chart ini: batang Jakarta tiga kali lebih panjang dari Jawa Barat "
  "bukan karena Jakarta mencatat kasus lebih banyak, melainkan karena beban per "
  "penduduknya jauh lebih berat. Inilah insight yang hilang kalau hanya melihat "
  "angka absolut.", "body")
story.append(PageBreak())

# ---------- 9. MEMBACA CHART ----------
P("9. Langkah 6 — Membaca Chart Top-10 dan Pangsa", "h1")
CHART("01_top10_absolut.png", "10 provinsi dengan kasus ISPA terbanyak (SKDR 2026).")
P("Cara membaca: sumbu panjang adalah jumlah kasus; urutan menurun dari atas. "
  "Perhatikan jarak antar batang: 4 teratas jauh di atas sisanya — itu pola "
  "konsentrasi, bukan sebaran merata.", "body")
CHART("02_pangsa_top10.png", "Pangsa 10 provinsi teratas dari total nasional.")
P("Pie chart ini menjawab 'seberapa terkonsentrasi?' dalam satu pandangan: "
  "tiga per empat laporan nasional berasal dari 10 provinsi. Pie chart cocok "
  "untuk pangsa (bagian dari keseluruhan), bukan untuk perbandingan banyak kategori.", "body")
story.append(PageBreak())

# ---------- 10. KARHUTLA ----------
P("10. Langkah 7 — Seri Karhutla: Usia, Provinsi, Pertumbuhan", "h1")
P("Ingat: ini seri TERPISAH. Pertanyaan dan jawabannya:", "body")
B("Berapa totalnya? 283.270 kasus (18 Agt–13 Okt 2026), 63 kab/kota, rata-rata 4.496 per kab/kota.")
B("Siapa yang terdampak? Balita 63.711 (22,5%), usia >5 tahun 219.559 (77,5%).")
B("Di mana? Kalsel 74.636 (26,3%) dan Sumsel 74.458 (26,3%) — selisih hanya 178 kasus.")
B("Seberapa cepat tumbuh? 13.449 (27 Agt) → 174.694 (21 Sep) → 283.270 (13 Okt) = 21,1x dalam 7 minggu.")
CHART("04_karhutla_provinsi.png", "Kalsel dan Sumsel bersama = 52,6% kasus karhutla.")
CHART("05_karhutla_usia.png", "Hampir 1 dari 4 kasus karhutla adalah balita.")
story.append(PageBreak())
CHART("06_karhutla_pertumbuhan.png", "Pertumbuhan kumulatif seri karhutla.")
CHART("10_balita_stabil.png", "Porsi balita stabil di ~23% pada dua titik waktu.")
P("Cara membaca chart pertumbuhan: sumbu tegak adalah total kumulatif (bukan kasus "
  "baru harian). Garis yang menanjak curam berarti kasus baru terus berdatangan "
  "dengan cepat — bukan berarti kasus lama menumpuk. Pada 13 Oktober saja tercatat "
  "3.897 kasus baru harian.", "body")
story.append(PageBreak())

# ---------- 11. ISPU ----------
P("11. Langkah 8 — ISPU dan PM2,5", "h1")
P("ISPU (Indeks Standar Pencemar Udara) mengelompokkan kualitas udara: Baik (0–50), "
  "Sedang (51–100), Tidak Sehat (101–200), Sangat Tidak Sehat (201–300), dan "
  "Berbahaya (>300). PM2,5 adalah partikel halus yang bisa masuk jauh ke saluran "
  "pernapasan.", "body")
CHART("07_ispu.png", "PM2,5 di 10 wilayah terburuk, 12 Okt 2026.")
P("Garis putus-putus adalah ambang 'berbahaya' (>300). Semua batang melampauinya; "
  "Barito Kuala (1.837) mencapai 6,1 kali ambang. Tujuh dari 10 wilayah terburuk "
  "berada di Kalimantan Tengah. Kemenkes juga mencatat 12 kabupaten/kota "
  "berkategori berbahaya dan 9 wilayah sangat tidak sehat.", "body")
P("Hati-hati: chart ini menunjukkan kualitas udara dan kasus ISPA di wilayah yang "
  "sama, tetapi itu adalah korelasi tingkat wilayah — bukan bukti bahwa satu orang "
  "tertentu sakit karena asap. Itu yang disebut analisis ekologis (lihat Bab 13).", "body")
story.append(PageBreak())

# ---------- 12. JAKARTA + MINGGUAN ----------
P("12. Langkah 9 — Studi Jakarta dan Tren Mingguan", "h1")
CHART("08_jakarta_bulanan.png", "Kasus ISPA Jakarta per bulan, Jan–Jun 2023.")
P("Pola bulanan Jakarta 2023 relatif stabil (99.130–119.734 per bulan, rata-rata "
  "106.382), dengan puncak Maret 119.734 (+20,8% dibanding Mei). Bandingkan dengan "
  "lonjakan 2026: Jakarta mencatat 1.966.308 kasus pada Jan–Okt 2025 dan kenaikan "
  "musiman +15,7% pada September 2026 (data puskesmas Dinkes DKI).", "body")
CHART("09_mingguan_nasional.png", "Laporan mingguan nasional: awal vs puncak kemarau.")
P("Laporan mingguan nasional naik dari >400 ribu (minggu 27–31) menjadi ~420 ribu "
  "(minggu 32–37), naik 5,0%. Angka ini dipakai sebagai batas bawah / dibulatkan "
  "sesuai redaksi sumber — bukan angka eksak mingguan.", "body")
story.append(PageBreak())

# ---------- 13. INTERPRETASI ----------
P("13. Interpretasi: Apa yang Boleh dan Tidak Boleh Disimpulkan", "h1")
P("BOLEH disimpulkan (didukung data):", "h2")
B("Laporan ISPA 2026 sangat besar dan terkonsentrasi: 74,7% di 10 provinsi.")
B("Beban per kapita Jakarta (150,0/1.000) jauh di atas provinsi lain.")
B("Kasus karhutla tumbuh 21,1x dalam 7 minggu; balita ~23% dari kasus karhutla.")
B("Kualitas udara di wilayah terdampak jauh di atas ambang berbahaya.")
P("TIDAK BOLEH disimpulkan (tidak didukung data):", "h2")
B("Asap karhutla adalah PENYEBAB tunggal lonjakan ISPA nasional. Kemenkes sendiri menekankan ISPA juga dipengaruhi virus, bakteri, cuaca, mobilitas, dan faktor lain.")
B("Provinsi dengan kasus terbanyak adalah provinsi yang udaranya paling buruk. Jawa mendominasi laporan, tetapi karhutla terparah ada di Sumatra–Kalimantan.")
B("Satu orang sakit karena asap hanya dari data tingkat provinsi (ecological fallacy).")
B("Angka laporan = jumlah orang sakit. Laporan menghitung kunjungan/laporan; satu orang bisa tercatat berulang.")
story.append(PageBreak())

# ---------- 14. KETERBATASAN ----------
P("14. Keterbatasan Data", "h1")
B("Laporan bukan orang unik — satu orang bisa tercatat lebih dari sekali.")
B("Cakupan dan kelengkapan pelaporan berbeda antarprovinsi.")
B("Angka peringkat 5–10 SKDR dibaca dari grafik (dibulatkan), bukan angka eksak.")
B("Seri karhutla hanya mencakup 63 kabupaten/kota terdampak dan tidak boleh dijumlahkan ke total nasional.")
B("Tiga provinsi dikeluarkan dari peringkat per kapita karena tidak ada angka populasi satu vintage yang terverifikasi.")
B("Redaksi sumber berbeda tentang apakah 9 wilayah 'sangat tidak sehat' termasuk dalam 12 wilayah 'berbahaya' — kedua angka dilaporkan apa adanya tanpa dijumlahkan.")
B("Tidak ada deret waktu mingguan lengkap yang dipublikasikan — hanya pita mingguan (400 ribu / 420 ribu).")
P("Menuliskan batasan seperti ini bukan kelemahan. Sebaliknya, ini yang membedakan "
  "analisis yang bisa dipercaya dari analisis yang sekadar terlihat meyakinkan.", "body")
story.append(PageBreak())

# ---------- 15. GLOSARIUM ----------
P("15. Glosarium", "h1")
TABLE([
    ["Istilah", "Arti"],
    ["ISPA", "Infeksi Saluran Pernapasan Akut — infeksi hidung, tenggorokan, dan saluran napas."],
    ["SKDR", "Sistem Kewaspadaan Dini dan Respons — sistem laporan penyakit Kemenkes."],
    ["Karhutla", "Kebakaran hutan dan lahan."],
    ["ISPU", "Indeks Standar Pencemar Udara — Baik, Sedang, Tidak Sehat, Sangat Tidak Sehat, Berbahaya."],
    ["PM2,5", "Partikel halus berdiameter ≤2,5 mikron; masuk jauh ke saluran pernapasan."],
    ["Minggu epidemiologi", "Pekan kalender standar untuk pelaporan penyakit (minggu ke-1 s.d. ke-52)."],
    ["Per kapita", "Nilai dibagi jumlah penduduk — untuk perbandingan yang adil antarwilayah."],
    ["Analisis ekologis", "Analisis memakai data agregat wilayah; tidak membuktikan sebab-akibat individu."],
    ["Reconciliation", "Memeriksa hasil olahan terhadap angka sumber agar tidak ada selisih."],
    ["Balita", "Anak berusia 0–5 tahun (bawah lima tahun)."],
])
story.append(PageBreak())

# ---------- 16. COBA SENDIRI ----------
P("16. Coba Sendiri (Challenge)", "h1")
P("Uji pemahamanmu dengan data di repo ini:", "body")
B("1. Hitung pangsa gabungan Kalsel + Sumsel dari total seri karhutla memakai SQL. (Jawaban: 52,6%.)")
B("2. Tambahkan satu provinsi ke tabel SKDR dari rilis Kemenkes terbaru, lalu hitung ulang pangsa top-10. Apa yang berubah?")
B("3. Cari angka populasi DIY, Sumbar, dan NTB dari satu vintage BPS yang sama, lalu masukkan ke peringkat per kapita. Apakah Jakarta tetap nomor satu?")
B("4. Buat satu chart baru: bandingkan kasus per kapita Jakarta vs rata-rata 7 provinsi lain yang punya data populasi.")
B("5. Tulis satu paragraf interpretasi untuk chart barumu — lalu uji: apakah ada klaim sebab-akibat yang tidak didukung data?")
story.append(Spacer(1, 0.8 * cm))
P("Penutup", "h2")
P("Project ini menunjukkan bahwa analisis data yang baik bukan hanya soal chart "
  "yang bagus, tetapi soal kejujuran terhadap data: tahu dari mana angka berasal, "
  "apa batasannya, dan apa yang boleh disimpulkan. Skill itu yang membedakan analis "
  "yang dipercaya. Selamat mencoba — dan selalu cantumkan sumbermu.", "body")
P("Sumber lengkap: data/SOURCES.md. Repo: ispa-indonesia-2026-analysis.", "body")

doc = SimpleDocTemplate(OUT, pagesize=landscape(A4),
                        leftMargin=1.8 * cm, rightMargin=1.8 * cm,
                        topMargin=1.5 * cm, bottomMargin=1.5 * cm,
                        title="Modul Analisis ISPA di Indonesia 2026",
                        author="BAGHIZ ASSHIDDIQIE ARASYA")
doc.build(story)
print("Module saved:", OUT)
