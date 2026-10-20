# -*- coding: utf-8 -*-
"""
Membangun CSV kit Power BI untuk proyek ISPA Indonesia 2026.

Semua angka kit DITURUNKAN dari data di ../data/compiled/ (dan total nasional
SKDR yang tercatat di ../data/SOURCES.md). Tidak ada agregat yang diketik tangan.

Aturan grain (WAJIB):
- Seri SKDR dan seri karhutla TIDAK PERNAH digabung dalam satu tabel fakta.
- fact_kasus_provinsi hanya berisi 10 provinsi teratas SKDR. Total nasional
  14.088.945 disimpan di tabel terpisah fact_total_nasional (1 baris) supaya
  tidak ada grain campuran.
- fact_kasus_mingguan grain-nya 1 baris per PERIODE laporan, karena sumber
  hanya mempublikasikan rentang minggu (27-31 dan 32-37), bukan angka per
  minggu individu.

Jalankan:  ~/workspace/mienv/bin/python powerbi/build_powerbi_kit.py
"""
import re
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parent.parent
SRC = BASE / "data" / "compiled"
OUT = BASE / "powerbi"
OUT.mkdir(exist_ok=True)


def fmt_id(n, dec=0):
    s = f"{n:,.{dec}f}"
    return s.replace(",", " ").replace(".", ",").replace(" ", ".")


# ---------------------------------------------------------------- sumber
mingguan = pd.read_csv(SRC / "mingguan_nasional.csv")
skdr = pd.read_csv(SRC / "skdr_provinsi_2026.csv")
kar_series = pd.read_csv(SRC / "karhutla_series.csv", parse_dates=["tanggal"])
kar_prov = pd.read_csv(SRC / "karhutla_provinsi.csv")
jakarta = pd.read_csv(SRC / "jakarta_bulanan.csv", parse_dates=["bulan"])
ispu = pd.read_csv(SRC / "ispu_wilayah.csv")

# Total nasional SKDR dibaca dari SOURCES.md (satu-satunya tempat angka ini
# tercatat; ia BUKAN jumlah fact provinsi yang hanya berisi 10 provinsi teratas).
sources_text = (BASE / "data" / "SOURCES.md").read_text(encoding="utf-8")
m = re.search(r"Total nasional 2026 \(s\.d\. minggu ke-38\) \| ([\d.]+) laporan", sources_text)
assert m, "Total nasional tidak ditemukan di SOURCES.md"
TOTAL_NASIONAL = int(m.group(1).replace(".", ""))

# ---------------------------------------------------------------- dim_provinsi
PULAU = {
    "Jawa Barat": "Jawa", "Jawa Tengah": "Jawa", "DKI Jakarta": "Jawa",
    "Jawa Timur": "Jawa", "Banten": "Jawa", "DI Yogyakarta": "Jawa",
    "Sulawesi Selatan": "Sulawesi", "Sumatera Utara": "Sumatera",
    "Sumatera Barat": "Sumatera", "Nusa Tenggara Barat": "Nusa Tenggara",
    "Kalimantan Selatan": "Kalimantan", "Sumatera Selatan": "Sumatera",
    "5 provinsi lain (gabungan)": "Beragam (gabungan)",
}

prov_rows = []
for _, r in skdr.iterrows():
    prov_rows.append({
        "provinsi": r["provinsi"],
        "populasi_2026": r["populasi_2026"],
        "sumber_populasi": r["sumber_populasi"],
    })
# Provinsi yang hanya muncul di seri karhutla
for _, r in kar_prov.iterrows():
    if r["provinsi"] not in [p["provinsi"] for p in prov_rows]:
        prov_rows.append({
            "provinsi": r["provinsi"],
            "populasi_2026": r["populasi_2026"],
            "sumber_populasi": r["sumber_populasi"],
        })

dim_provinsi = pd.DataFrame(prov_rows)
dim_provinsi.insert(0, "provinsi_id",
                    [f"P{i:02d}" for i in range(1, len(dim_provinsi) + 1)])
dim_provinsi["pulau"] = dim_provinsi["provinsi"].map(PULAU)
dim_provinsi = dim_provinsi[["provinsi_id", "provinsi", "pulau",
                             "populasi_2026", "sumber_populasi"]]
dim_provinsi.to_csv(OUT / "dim_provinsi.csv", index=False)
PID = dict(zip(dim_provinsi["provinsi"], dim_provinsi["provinsi_id"]))

# ---------------------------------------------------------------- fact_kasus_provinsi (SKDR, 10 provinsi teratas)
fact_prov = pd.DataFrame({
    "provinsi_id": skdr["provinsi"].map(PID),
    "kasus_skdr_2026": skdr["kasus_skdr_2026"].astype(int),
    "kualitas_angka": [
        "Eksak" if "eksak" in str(c).lower() else "Dibaca dari grafik (dibulatkan)"
        for c in skdr["catatan"]
    ],
})
fact_prov.to_csv(OUT / "fact_kasus_provinsi.csv", index=False)

# ---------------------------------------------------------------- fact_total_nasional (SKDR, 1 baris)
fact_total = pd.DataFrame([{
    "tahun": 2026,
    "minggu_terakhir": 38,
    "total_kasus_skdr_2026": TOTAL_NASIONAL,
    "sumber": "Kemenkes, Situation Report Penyakit Infeksi Emerging dan Potensial KLB/Wabah (dikutip GoodStats)",
    "catatan": "Total seluruh provinsi s.d. minggu epidemiologi ke-38 tahun 2026. "
               "BUKAN jumlah fact_kasus_provinsi (hanya 10 provinsi teratas).",
}])
fact_total.to_csv(OUT / "fact_total_nasional.csv", index=False)

# ---------------------------------------------------------------- dim_minggu + fact_kasus_mingguan
minggu_rows, fact_mingguan_rows = [], []
for i, (_, r) in enumerate(mingguan.iterrows(), start=1):
    awal, akhir = (int(x) for x in str(r["minggu_epidemiologi"]).split("-"))
    n = akhir - awal + 1
    pid_ = f"M{i}"
    minggu_rows.append({
        "periode_id": pid_, "label_periode": r["periode"],
        "minggu_mulai": awal, "minggu_akhir": akhir, "jumlah_minggu": n,
    })
    fact_mingguan_rows.append({
        "periode_id": pid_,
        "laporan_per_minggu": int(r["laporan_per_minggu"]),
        "jumlah_minggu": n,
        "total_laporan_periode_estimasi": int(r["laporan_per_minggu"]) * n,
        "catatan": r["catatan"],
    })
pd.DataFrame(minggu_rows).to_csv(OUT / "dim_minggu.csv", index=False)
pd.DataFrame(fact_mingguan_rows).to_csv(OUT / "fact_kasus_mingguan.csv", index=False)

# ---------------------------------------------------------------- karhutla: seri waktu (TERPISAH dari SKDR)
fact_kar_series = kar_series[[
    "tanggal", "kasus_kumulatif", "kasus_baru_harian", "kasus_aktif",
    "penduduk_terdampak",
]].copy()
fact_kar_series["cakupan_kabupaten_kota"] = 63
fact_kar_series["cakupan_provinsi"] = 7
fact_kar_series["tanggal"] = fact_kar_series["tanggal"].dt.date
fact_kar_series.to_csv(OUT / "fact_karhutla_series.csv", index=False)

# ---------------------------------------------------------------- karhutla: per provinsi
fact_kar_prov = pd.DataFrame({
    "provinsi_id": kar_prov["provinsi"].map(PID),
    "kasus_karhutla": kar_prov["kasus_karhutla_18agt_13okt_2026"].astype(int),
    "tanggal_mulai": "2026-08-18",
    "tanggal_akhir": "2026-10-13",
    "catatan": kar_prov["catatan"],
})
fact_kar_prov.to_csv(OUT / "fact_karhutla_provinsi.csv", index=False)

# ---------------------------------------------------------------- karhutla: per kelompok usia (format panjang)
dim_usia = pd.DataFrame([
    {"kelompok_usia_id": "U1", "kelompok_usia": "Balita (0 sampai 5 tahun)"},
    {"kelompok_usia_id": "U2", "kelompok_usia": "Di atas 5 tahun"},
])
dim_usia.to_csv(OUT / "dim_kelompok_usia.csv", index=False)

usia_rows = []
for _, r in kar_series.iterrows():
    tgl = r["tanggal"].date()
    if pd.notna(r["balita_0_5_tahun"]):
        usia_rows.append({"tanggal": tgl, "kelompok_usia_id": "U1",
                          "kasus": int(r["balita_0_5_tahun"])})
    if pd.notna(r["usia_diatas_5_tahun"]):
        usia_rows.append({"tanggal": tgl, "kelompok_usia_id": "U2",
                          "kasus": int(r["usia_diatas_5_tahun"])})
pd.DataFrame(usia_rows).to_csv(OUT / "fact_karhutla_usia.csv", index=False)

# ---------------------------------------------------------------- ISPU / PM2.5
def kategori_ispu(v):
    if v > 300:
        return "Berbahaya"
    if v > 200:
        return "Sangat Tidak Sehat"
    if v > 100:
        return "Tidak Sehat"
    if v > 50:
        return "Sedang"
    return "Baik"

dim_wilayah = pd.DataFrame({
    "wilayah_id": [f"W{i:02d}" for i in range(1, len(ispu) + 1)],
    "wilayah": ispu["wilayah"],
    "provinsi": ispu["provinsi"],
})
dim_wilayah.to_csv(OUT / "dim_wilayah.csv", index=False)
WID = dict(zip(dim_wilayah["wilayah"], dim_wilayah["wilayah_id"]))

fact_ispu = pd.DataFrame({
    "wilayah_id": ispu["wilayah"].map(WID),
    "tanggal_snapshot": "2026-10-12",
    "pm25": ispu["pm25_12okt2026_1500wib"].astype(int),
    "kategori_ispu": [kategori_ispu(v) for v in ispu["pm25_12okt2026_1500wib"]],
    "sumber": ispu["sumber"],
})
fact_ispu.to_csv(OUT / "fact_ispu.csv", index=False)

# ---------------------------------------------------------------- Jakarta bulanan (seri 2023, terpisah)
NAMA_BULAN = {1: "Januari", 2: "Februari", 3: "Maret", 4: "April", 5: "Mei",
              6: "Juni", 7: "Juli", 8: "Agustus", 9: "September", 10: "Oktober",
              11: "November", 12: "Desember"}
fact_jkt = pd.DataFrame({
    "bulan_tanggal": jakarta["bulan"].dt.date,
    "tahun": jakarta["bulan"].dt.year,
    "nomor_bulan": jakarta["bulan"].dt.month,
    "nama_bulan": jakarta["bulan"].dt.month.map(NAMA_BULAN),
    "kasus_jakarta": jakarta["kasus_ispa_jakarta_2023"].astype(int),
    "catatan": "Seri bulanan Dinkes DKI Jakarta tahun 2023 (Januari sampai Juni). "
               "Seri terpisah, bukan bagian seri SKDR 2026.",
})
fact_jkt.to_csv(OUT / "fact_jakarta_bulanan.csv", index=False)

# ---------------------------------------------------------------- VERIFIKASI
print("=" * 70)
print("VERIFIKASI (dihitung ulang dari CSV kit yang baru dibuat)")
print("=" * 70)
fp = pd.read_csv(OUT / "fact_kasus_provinsi.csv")
dp = pd.read_csv(OUT / "dim_provinsi.csv").set_index("provinsi_id")
fp["provinsi"] = fp["provinsi_id"].map(dp["provinsi"])
fp["populasi"] = fp["provinsi_id"].map(dp["populasi_2026"])
fp["per1000"] = fp["kasus_skdr_2026"] / fp["populasi"] * 1000

top10 = fp["kasus_skdr_2026"].sum()
print(f"Total nasional SKDR (fact_total_nasional) : {fmt_id(TOTAL_NASIONAL)}")
print(f"Jumlah fact_kasus_provinsi (10 teratas)   : {fmt_id(top10)}")
print(f"Pangsa 10 provinsi teratas                : {fmt_id(top10 / TOTAL_NASIONAL * 100, 1)}%")
for nama in ["DKI Jakarta", "Jawa Barat", "Banten", "Jawa Timur", "Jawa Tengah"]:
    row = fp[fp["provinsi"] == nama].iloc[0]
    print(f"Per 1.000 {nama:<14}: {fmt_id(row['per1000'], 1)}  "
          f"(pangsa {fmt_id(row['kasus_skdr_2026'] / TOTAL_NASIONAL * 100, 2)}%)")
jawa = fp[fp["provinsi_id"].map(dp["pulau"]) == "Jawa"]["kasus_skdr_2026"].sum()
print(f"Pangsa Pulau Jawa dari 10 teratas         : {fmt_id(jawa / top10 * 100, 1)}%")

fm = pd.read_csv(OUT / "fact_kasus_mingguan.csv")
rata_mingguan = (fm["laporan_per_minggu"] * fm["jumlah_minggu"]).sum() / fm["jumlah_minggu"].sum()
print(f"Rata-rata laporan per minggu (mg 27-37)   : {fmt_id(rata_mingguan)}")
print(f"Kenaikan mingguan 400rb ke 420rb          : "
      f"{fmt_id((420000 - 400000) / 400000 * 100, 1)}%")

ks = pd.read_csv(OUT / "fact_karhutla_series.csv", parse_dates=["tanggal"])
terakhir = ks.sort_values("tanggal").iloc[-1]
pertama = ks.sort_values("tanggal").iloc[0]
print(f"Karhutla total kumulatif terakhir         : {fmt_id(int(terakhir['kasus_kumulatif']))}")
print(f"Karhutla pertumbuhan kali                 : "
      f"{fmt_id(terakhir['kasus_kumulatif'] / pertama['kasus_kumulatif'], 1)}x")
print(f"Karhutla kasus baru harian terakhir       : {fmt_id(int(terakhir['kasus_baru_harian']))}")
print(f"Karhutla rata-rata per kab/kota           : "
      f"{fmt_id(terakhir['kasus_kumulatif'] / 63)}")

fu = pd.read_csv(OUT / "fact_karhutla_usia.csv", parse_dates=["tanggal"])
tgl_max = fu["tanggal"].max()
fu_last = fu[fu["tanggal"] == tgl_max]
balita = int(fu_last[fu_last["kelompok_usia_id"] == "U1"]["kasus"].iloc[0])
total_usia = int(fu_last["kasus"].sum())
print(f"Karhutla balita (snapshot terakhir)       : {fmt_id(balita)} "
      f"dari {fmt_id(total_usia)} = {fmt_id(balita / total_usia * 100, 1)}%")

fkp = pd.read_csv(OUT / "fact_karhutla_provinsi.csv")
fkp["provinsi"] = fkp["provinsi_id"].map(dp["provinsi"])
dua = fkp[fkp["provinsi"].isin(["Kalimantan Selatan", "Sumatera Selatan"])]["kasus_karhutla"].sum()
print(f"Karhutla Kalsel + Sumsel                  : {fmt_id(int(dua))} "
      f"= {fmt_id(dua / int(terakhir['kasus_kumulatif']) * 100, 1)}% dari total karhutla")
print(f"Karhutla jumlah fact provinsi             : {fmt_id(int(fkp['kasus_karhutla'].sum()))}")

fi = pd.read_csv(OUT / "fact_ispu.csv")
dw = pd.read_csv(OUT / "dim_wilayah.csv").set_index("wilayah_id")
fi["wilayah"] = fi["wilayah_id"].map(dw["wilayah"])
fi["provinsi"] = fi["wilayah_id"].map(dw["provinsi"])
mx = fi.loc[fi["pm25"].idxmax()]
print(f"ISPU PM2.5 terburuk                       : {mx['wilayah']} = {fmt_id(int(mx['pm25']))} "
      f"({fmt_id(mx['pm25'] / 300, 1)}x ambang berbahaya 300)")
print(f"ISPU wilayah asal Kalimantan Tengah       : "
      f"{int((fi['provinsi'] == 'Kalimantan Tengah').sum())} dari {len(fi)} wilayah")
print(f"ISPU rata-rata 10 wilayah                 : {fmt_id(fi['pm25'].mean(), 1)}")

fj = pd.read_csv(OUT / "fact_jakarta_bulanan.csv")
print(f"Jakarta bulanan total Jan-Jun 2023        : {fmt_id(int(fj['kasus_jakarta'].sum()))}")
print(f"Jakarta rata-rata per bulan 2023          : {fmt_id(fj['kasus_jakarta'].mean(), 1)}")
print(f"Jakarta bulan tertinggi                   : "
      f"{fj.loc[fj['kasus_jakarta'].idxmax(), 'nama_bulan']} "
      f"{fmt_id(int(fj['kasus_jakarta'].max()))}")
print("=" * 70)
print("File kit tertulis di:", OUT)
for f in sorted(OUT.glob("*.csv")):
    print(" -", f.name, f"({len(pd.read_csv(f))} baris)")
