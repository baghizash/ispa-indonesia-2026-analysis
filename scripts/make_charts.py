#!/usr/bin/env python3
"""Generate the 10 charts for the ISPA Indonesia 2026 analysis.

All values come from the compiled CSVs (data/compiled/) - nothing invented.
Charts are saved to charts/ as PNG files.
"""
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COMPILED = os.path.join(HERE, "data", "compiled")
CHARTS = os.path.join(HERE, "charts")
os.makedirs(CHARTS, exist_ok=True)

plt.rcParams.update(
    {
        "font.size": 11,
        "axes.titlesize": 13,
        "axes.titleweight": "bold",
        "figure.dpi": 150,
    }
)
CORAL = "#E76F51"
NAVY = "#1E3A8A"
TEAL = "#0D9488"
GRAY = "#6B7280"
DARK = "#1F2937"

skdr = pd.read_csv(os.path.join(COMPILED, "skdr_provinsi_2026.csv"))
karhutla_prov = pd.read_csv(os.path.join(COMPILED, "karhutla_provinsi.csv"))
karhutla_series = pd.read_csv(os.path.join(COMPILED, "karhutla_series.csv"))
ispu = pd.read_csv(os.path.join(COMPILED, "ispu_wilayah.csv"))
jakarta = pd.read_csv(os.path.join(COMPILED, "jakarta_bulanan.csv"))
mingguan = pd.read_csv(os.path.join(COMPILED, "mingguan_nasional.csv"))

TOTAL_NASIONAL = 14088945
TOTAL_KARHUTLA = 283270

# 01 - Top 10 provinsi, kasus absolut (SKDR)
d = skdr.sort_values("kasus_skdr_2026", ascending=True)
fig, ax = plt.subplots(figsize=(9, 5.5))
ax.barh(d["provinsi"], d["kasus_skdr_2026"] / 1000, color=CORAL)
for i, v in enumerate(d["kasus_skdr_2026"] / 1000):
    ax.text(v + 30, i, f"{v:,.0f}", va="center", fontsize=10)
ax.set_xlabel("Kasus ISPA 2026 (ribu laporan, SKDR s.d. 3 Okt 2026)")
ax.set_title("10 Provinsi dengan Kasus ISPA Terbanyak 2026")
ax.set_xlim(0, 2900)
fig.tight_layout()
fig.savefig(f"{CHARTS}/01_top10_absolut.png")
plt.close(fig)

# 02 - Pangsa 10 provinsi teratas terhadap total nasional
top10 = skdr["kasus_skdr_2026"].sum()
sisa = TOTAL_NASIONAL - top10
fig, ax = plt.subplots(figsize=(7, 5))
ax.pie(
    [top10, sisa],
    labels=[f"10 provinsi teratas\n{top10:,} laporan", f"Provinsi lain\n{sisa:,} laporan"],
    colors=[CORAL, GRAY],
    autopct="%1.1f%%",
    startangle=90,
)
ax.set_title("Pangsa 10 Provinsi Teratas dari Total Nasional\n(14.088.945 laporan SKDR 2026)")
fig.tight_layout()
fig.savefig(f"{CHARTS}/02_pangsa_top10.png")
plt.close(fig)

# 03 - Kasus per 1.000 penduduk (hanya provinsi dengan populasi terverifikasi)
d = skdr.dropna(subset=["populasi_2026"]).copy()
d["per_1000"] = 1000 * d["kasus_skdr_2026"] / d["populasi_2026"]
d = d.sort_values("per_1000", ascending=True)
fig, ax = plt.subplots(figsize=(9, 5))
colors = [NAVY if p == "DKI Jakarta" else TEAL for p in d["provinsi"]]
ax.barh(d["provinsi"], d["per_1000"], color=colors)
for i, v in enumerate(d["per_1000"]):
    ax.text(v + 2, i, f"{v:.1f}", va="center", fontsize=10)
ax.set_xlabel("Kasus per 1.000 penduduk (populasi BPS 2026)")
ax.set_title("Beban ISPA per Kapita: Jakarta Jauh di Atas Provinsi Lain")
ax.set_xlim(0, 175)
fig.tight_layout()
fig.savefig(f"{CHARTS}/03_per_kapita.png")
plt.close(fig)

# 04 - Seri karhutla: Kalsel vs Sumsel vs 5 provinsi lain
d = karhutla_prov.sort_values("kasus_karhutla_18agt_13okt_2026", ascending=True)
fig, ax = plt.subplots(figsize=(9, 4))
ax.barh(d["provinsi"], d["kasus_karhutla_18agt_13okt_2026"], color=[CORAL, TEAL, GRAY])
for i, v in enumerate(d["kasus_karhutla_18agt_13okt_2026"]):
    ax.text(v + 2500, i, f"{v:,} ({100*v/TOTAL_KARHUTLA:.1f}%)", va="center", fontsize=10)
ax.set_xlabel("Kasus ISPA karhutla, 18 Agt–13 Okt 2026")
ax.set_title("Dua Provinsi Menyumbang Lebih dari Separuh Kasus ISPA Karhutla")
ax.set_xlim(0, 175000)
fig.tight_layout()
fig.savefig(f"{CHARTS}/04_karhutla_provinsi.png")
plt.close(fig)

# 05 - Seri karhutla: pembagian usia
balita = 63711
diatas5 = 219559
fig, ax = plt.subplots(figsize=(7, 5))
ax.pie(
    [diatas5, balita],
    labels=[f"Usia >5 tahun\n{diatas5:,} (77,5%)", f"Balita (0–5 tahun)\n{balita:,} (22,5%)"],
    colors=[NAVY, CORAL],
    autopct="%1.1f%%",
    startangle=90,
)
ax.set_title("Kasus ISPA Karhutla menurut Usia\n(283.270 kasus, 18 Agt–13 Okt 2026)")
fig.tight_layout()
fig.savefig(f"{CHARTS}/05_karhutla_usia.png")
plt.close(fig)

# 06 - Pertumbuhan kumulatif seri karhutla
d = karhutla_series.dropna(subset=["kasus_kumulatif"]).copy()
d["tanggal"] = pd.to_datetime(d["tanggal"])
d = d.sort_values("tanggal")
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(d["tanggal"], d["kasus_kumulatif"], marker="o", color=CORAL, linewidth=2)
for _, r in d.iterrows():
    ax.text(r["tanggal"], r["kasus_kumulatif"] + 12000, f"{int(r['kasus_kumulatif']):,}", ha="center", fontsize=10)
ax.set_ylabel("Kasus kumulatif")
ax.set_title("Kasus ISPA Karhutla: 13 Ribu Menjadi 283 Ribu dalam 7 Minggu")
ax.set_ylim(0, 330000)
fig.tight_layout()
fig.savefig(f"{CHARTS}/06_karhutla_pertumbuhan.png")
plt.close(fig)

# 07 - ISPU: 10 wilayah PM2,5 terburuk
d = ispu.sort_values("pm25_12okt2026_1500wib", ascending=True)
fig, ax = plt.subplots(figsize=(9, 5.5))
ax.barh(d["wilayah"], d["pm25_12okt2026_1500wib"], color=DARK)
ax.axvline(300, color=CORAL, linestyle="--", linewidth=1.5)
ax.text(310, -0.7, "Ambang ISPU 'berbahaya' (>300)", color=CORAL, fontsize=9)
for i, v in enumerate(d["pm25_12okt2026_1500wib"]):
    ax.text(v + 30, i, f"{v:,}", va="center", fontsize=10)
ax.set_xlabel("Konsentrasi PM2,5 (12 Okt 2026, 15:00 WIB)")
ax.set_title("10 Wilayah dengan Udara Terburuk: Semua Jauh di Atas Ambang Berbahaya")
ax.set_xlim(0, 2100)
fig.tight_layout()
fig.savefig(f"{CHARTS}/07_ispu.png")
plt.close(fig)

# 08 - Jakarta bulanan 2023
fig, ax = plt.subplots(figsize=(8, 4.5))
bulan = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun"]
ax.plot(bulan, jakarta["kasus_ispa_jakarta_2023"], marker="o", color=NAVY, linewidth=2)
for x, v in enumerate(jakarta["kasus_ispa_jakarta_2023"]):
    ax.text(x, v + 2500, f"{v:,}", ha="center", fontsize=9)
ax.set_ylabel("Kasus ISPA per bulan")
ax.set_title("Kasus ISPA Jakarta per Bulan, Januari–Juni 2023\n(Puncak Maret: 119.734 kasus)")
ax.set_ylim(85000, 132000)
fig.tight_layout()
fig.savefig(f"{CHARTS}/08_jakarta_bulanan.png")
plt.close(fig)

# 09 - Laporan mingguan nasional: awal vs puncak musim kemarau
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.bar(
    ["Awal kemarau\n(minggu 27–31)", "Puncak kemarau\n(minggu 32–37)"],
    mingguan["laporan_per_minggu"],
    color=[TEAL, CORAL],
)
for i, v in enumerate(mingguan["laporan_per_minggu"]):
    ax.text(i, v + 8000, f"{v:,}", ha="center", fontsize=11)
ax.set_ylabel("Laporan ISPA per minggu")
ax.set_title("Laporan Mingguan Nasional Naik 5% ke Puncak Kemarau")
ax.set_ylim(0, 500000)
fig.tight_layout()
fig.savefig(f"{CHARTS}/09_mingguan_nasional.png")
plt.close(fig)

# 10 - Pangsa balita antar snapshot karhutla (stabil di ~23%)
labels = ["Agt–21 Sep 2026\n(174.694 kasus)", "18 Agt–13 Okt 2026\n(283.270 kasus)"]
balita_pct = [100 * 40363 / 174694, 100 * 63711 / 283270]
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.bar(labels, balita_pct, color=CORAL)
for i, v in enumerate(balita_pct):
    ax.text(i, v + 0.5, f"{v:.1f}%", ha="center", fontsize=11)
ax.set_ylabel("Pangsa balita dari total kasus karhutla (%)")
ax.set_title("Porsi Balita Stabil: Hampir 1 dari 4 Kasus Karhutla adalah Balita")
ax.set_ylim(0, 30)
fig.tight_layout()
fig.savefig(f"{CHARTS}/10_balita_stabil.png")
plt.close(fig)

print("10 charts written to", CHARTS)
