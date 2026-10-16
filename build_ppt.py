#!/usr/bin/env python3
"""Build Portofolio-Analisis-ISPA-Indonesia.pptx (16:9, 10 slides, ID)."""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn

NAVY = RGBColor(0x1E, 0x3A, 0x8A)
TEAL = RGBColor(0x0D, 0x94, 0x88)
CORAL = RGBColor(0xE7, 0x6F, 0x51)
DARK = RGBColor(0x1F, 0x29, 0x37)
GRAY = RGBColor(0x6B, 0x72, 0x80)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
CHARTS = "/home/hatch/workspace/ispa-indonesia/charts"

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank = prs.slide_layouts[6]


def solid_bg(slide, color):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color


def textbox(slide, left, top, width, height):
    tx = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = tx.text_frame
    tf.word_wrap = True
    return tf


def add_par(tf, text, size, color, bold=False, italic=False, first=False, align=None):
    p = tf.paragraphs[0] if first else tf.add_paragraph()
    p.space_after = Pt(8)
    if align is not None:
        p.alignment = align
    r = p.add_run()
    r.text = text
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    r.font.color.rgb = color
    return p


def add_bullet(tf, text, size=17, first=False):
    p = add_par(tf, text, size, DARK, first=first)
    pPr = p._p.get_or_add_pPr()
    pPr.append(pPr.makeelement(qn("a:buChar"), {"char": "\u2022"}))
    pPr.set("marL", "171450")
    pPr.set("indent", "-171450")
    p.space_after = Pt(10)
    p.space_before = Pt(2)
    return p


def content_title(slide, text):
    tf = textbox(slide, 0.7, 0.3, 11.9, 0.9)
    add_par(tf, text, 30, NAVY, bold=True, first=True)
    bar = slide.shapes.add_shape(1, Inches(0.7), Inches(1.15), Inches(1.5), Inches(0.06))
    bar.fill.solid()
    bar.fill.fore_color.rgb = TEAL
    bar.line.fill.background()


def content_slide(title, bullets, chart=None, caption=None, full_width=False):
    s = prs.slides.add_slide(blank)
    solid_bg(s, WHITE)
    content_title(s, title)
    bw = 11.9 if full_width else 5.6
    tf = textbox(s, 0.7, 1.5, bw, 5.2)
    for i, b in enumerate(bullets):
        add_bullet(tf, b, first=(i == 0))
    if chart:
        s.shapes.add_picture(f"{CHARTS}/{chart}.png", Inches(6.8), Inches(1.5),
                             width=Inches(5.8))
    if caption:
        tf2 = textbox(s, 6.8, 6.6, 5.8, 0.6)
        add_par(tf2, caption, 11, GRAY, italic=True, first=True)
    return s


# 1 — Title
s = prs.slides.add_slide(blank)
solid_bg(s, NAVY)
tf = textbox(s, 0.9, 1.3, 11.5, 1.6)
add_par(tf, "ISPA di Indonesia 2026", 44, WHITE, bold=True, first=True)
tf = textbox(s, 0.9, 2.9, 11.5, 1.0)
add_par(tf, "Lonjakan Kasus, Sebaran Provinsi, dan Dampak Karhutla & Kualitas Udara",
        24, WHITE, first=True)
bar = s.shapes.add_shape(1, Inches(0.9), Inches(4.1), Inches(1.5), Inches(0.07))
bar.fill.solid()
bar.fill.fore_color.rgb = TEAL
bar.line.fill.background()
tf = textbox(s, 0.9, 4.5, 11.5, 1.6)
add_par(tf, "BAGHIZ ASSHIDDIQIE ARASYA", 20, WHITE, bold=True, first=True)
add_par(tf, "Analisis Data Kesehatan Masyarakat  •  SQL + Python  •  Oktober 2026", 16, WHITE)
tf = textbox(s, 0.9, 6.5, 11.5, 0.5)
add_par(tf, "Data kompilasi dari angka resmi Kemenkes / SKDR / ISPU — setiap angka bersumber.",
        12, RGBColor(0xBF, 0xDB, 0xFE), italic=True, first=True)

# 2 — Masalah
content_slide(
    "Mengapa ISPA 2026 Mendesak?",
    [
        "ISPA adalah infeksi saluran pernapasan akut: batuk, pilek, sesak napas.",
        "Laporan nasional 2026 tembus 14.088.945 laporan (SKDR, s.d. minggu ke-38).",
        "Laporan mingguan di atas 400 ribu sejak minggu ke-27 — naik ke ~420 ribu pada puncak kemarau.",
        "Bersamaan dengan karhutla dan kualitas udara yang memburuk di Sumatra dan Kalimantan.",
        "Pertanyaan: seberapa besar, di mana, siapa yang paling terdampak?",
    ],
    chart="09_mingguan_nasional",
    caption="Laporan mingguan nasional naik 5% ke puncak kemarau.",
)

# 3 — Data & metode
content_slide(
    "Data & Metode",
    [
        "Dataset KOMPILASI dari angka resmi yang dipublikasikan (Kemenkes, SKDR, ISPU, Dinkes DKI, BPS).",
        "Tidak ada file CSV mentah ISPA di data.go.id / Jakarta Open Data — setiap angka dicatat sumber + tanggalnya.",
        "Dua seri dipisah ketat: seri nasional SKDR vs seri pemantauan karhutla (cakupan dan tanggal berbeda).",
        "Pipeline: kompilasi CSV → SQLite → query SQL → chart Python → interpretasi.",
        "Perbandingan antarprovinsi dinormalisasi per 1.000 penduduk (BPS 2026).",
    ],
    chart="02_pangsa_top10",
    caption="10 provinsi teratas = 74,7% laporan nasional.",
)

# 4 — Temuan 1: konsentrasi
content_slide(
    "Temuan 1: Kasus Sangat Terkonsentrasi",
    [
        "10 provinsi teratas mencatat 10.530.385 laporan = 74,7% total nasional.",
        "4 provinsi teratas saja (Jabar, Jateng, Jakarta, Jatim) = 55,8% nasional.",
        "Jawa Barat tertinggi: 2.533.888 laporan (17,98% nasional).",
        "86,3% laporan top-10 berasal dari Pulau Jawa.",
        "Peringatan: dominasi Jawa ikut dipengaruhi jumlah penduduk dan kelengkapan pelaporan.",
    ],
    chart="01_top10_absolut",
    caption="10 provinsi dengan kasus ISPA terbanyak, SKDR 2026.",
)

# 5 — Temuan 2: per kapita
content_slide(
    "Temuan 2: Per Kapita, Jakarta Beban Terberat",
    [
        "Angka absolut menipu: provinsi besar otomatis mencatat kasus lebih banyak.",
        "Setelah dibagi populasi: Jakarta 150,0 kasus per 1.000 penduduk.",
        "Itu ~3x Jawa Barat (49,5) dan ~2,3x Banten (65,8).",
        "Jakarta mencatat kasus 1,16x Jawa Timur dengan penduduk hanya seperempatnya.",
        "Implikasi: surveilans dan kesiapan RS Jakarta perlu prioritas pada puncak kemarau.",
    ],
    chart="03_per_kapita",
    caption="Kasus per 1.000 penduduk (populasi BPS 2026).",
)

# 6 — Temuan 3: karhutla
content_slide(
    "Temuan 3: 283.270 Kasus ISPA Karhutla",
    [
        "Seri pemantauan karhutla (terpisah dari seri nasional): 283.270 kasus, 18 Agt–13 Okt 2026.",
        "Tercatat di 63 kabupaten/kota, 7 provinsi — rata-rata 4.496 kasus per kab/kota.",
        "Kalsel (74.636) dan Sumsel (74.458) bersama = 52,6% kasus karhutla; selisih hanya 178 kasus.",
        "Kumulatif naik 21,1x dalam 7 minggu: 13.449 (27 Agt) → 283.270 (13 Okt).",
        "13 Oktober saja: 3.897 kasus baru harian.",
    ],
    chart="06_karhutla_pertumbuhan",
    caption="Pertumbuhan kumulatif seri karhutla.",
)

# 7 — Temuan 4: balita
content_slide(
    "Temuan 4: Hampir 1 dari 4 Kasus Karhutla adalah Balita",
    [
        "Balita (0–5 tahun): 63.711 kasus = 22,5% dari total seri karhutla.",
        "Usia di atas 5 tahun: 219.559 kasus (77,5%).",
        "Porsi balita stabil: 23,1% (21 Sep) → 22,5% (13 Okt).",
        "Anak adalah kelompok rentan utama paparan asap: saluran napas lebih kecil, frekuensi napas lebih tinggi.",
        "Respons: 2.106 tenaga kesehatan dimobilisasi; >2,8 juta masker didistribusikan.",
    ],
    chart="05_karhutla_usia",
    caption="Kasus ISPA karhutla menurut usia.",
)

# 8 — Temuan 5: kualitas udara
content_slide(
    "Temuan 5: Udara Jauh di Atas Ambang Berbahaya",
    [
        "PM2,5 di 10 wilayah terburuk: 507–1.837 (12 Okt 2026, 15:00 WIB).",
        "Barito Kuala 1.837 = 6,1 kali ambang ISPU 'berbahaya' (>300).",
        "7 dari 10 wilayah terburuk berada di Kalimantan Tengah.",
        "Kemenkes: 12 kab/kota berkategori berbahaya, 9 wilayah sangat tidak sehat.",
        "Asap karhutla mengandung PM2,5 yang masuk jauh ke saluran pernapasan (WHO).",
    ],
    chart="07_ispu",
    caption="Konsentrasi PM2,5, 10 wilayah terburuk.",
)

# 9 — Rekomendasi
content_slide(
    "Rekomendasi",
    [
        "Lindungi balita di wilayah karhutla: masker anak, pembelajaran jarak jauh saat ISPU berbahaya, posko kesehatan.",
        "Fokus pada Kalsel dan Sumsel: 52,6% kasus karhutla — pertahankan distribusi masker dan tenaga kesehatan.",
        "Perhatikan Jakarta: beban per kapita 150,0/1.000 — perkuat surveilans puskesmas dan kesiapan RS saat puncak kemarau.",
        "Mulai sebelum kemarau: laporan sudah >400 ribu/minggu sejak minggu ke-27.",
        "Perbaiki transparansi data: publikasikan tabel provinsi lengkap dan deret mingguan SKDR dalam format terbuka.",
    ],
    full_width=True,
)

# 10 — Penutup
s = prs.slides.add_slide(blank)
solid_bg(s, NAVY)
tf = textbox(s, 0.9, 1.2, 11.5, 1.2)
add_par(tf, "Kesimpulan", 40, WHITE, bold=True, first=True)
tf = textbox(s, 0.9, 2.6, 11.5, 2.2)
add_par(tf, "ISPA 2026 bukan sekadar musim batuk-pilek: 14,1 juta laporan nasional,",
        22, WHITE, first=True)
add_par(tf, "283 ribu kasus di wilayah karhutla, dan udara 6 kali ambang berbahaya.",
        22, WHITE)
add_par(tf, "Data yang transparan adalah langkah pertama penanganan yang tepat.",
        22, WHITE)
tf = textbox(s, 0.9, 5.3, 11.5, 1.0)
add_par(tf, "BAGHIZ ASSHIDDIQIE ARASYA", 18, WHITE, bold=True, first=True)
add_par(tf, "Sumber lengkap: data/SOURCES.md  •  Repo: ispa-indonesia-2026-analysis",
        14, RGBColor(0xBF, 0xDB, 0xFE))
tf = textbox(s, 0.9, 6.6, 11.5, 0.5)
add_par(tf, "Dataset kompilasi dari angka resmi yang dipublikasikan — lihat README untuk batasan dan caveat.",
        12, RGBColor(0xBF, 0xDB, 0xFE), italic=True, first=True)

prs.save("/home/hatch/workspace/your_files/Portofolio-Analisis-ISPA-Indonesia.pptx")
print("PPT saved, slides:", len(prs.slides._sldIdLst))
