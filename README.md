# Analisis ISPA di Indonesia 2026

Analisis end-to-end kasus Infeksi Saluran Pernapasan Akut (ISPA) di Indonesia pada
2026: lonjakan nasional, sebaran provinsi, dampak karhutla, dan kualitas udara.
Data dikompilasi ke CSV, dimuat ke SQLite, setiap pertanyaan bisnis dijawab dengan
**query SQL asli** (`sql/queries.sql`), divisualisasikan dalam 10 chart (`charts/`),
dan dinarasikan dalam notebook (`analysis.ipynb`).

## ⚠️ Sifat data: KOMPILASI dari angka resmi yang dipublikasikan

**Dataset ini dikompilasi dari angka-angka resmi yang dipublikasikan** (rilis pers
Kemenkes dan laporan yang mengutipnya). **Bukan** file mentah resmi: tidak ada
file CSV mentah ISPA yang bisa diunduh dari data.go.id atau Jakarta Open Data
pada saat proyek ini dibuat (dicek 16 Oktober 2026). Setiap angka dicatat bersama
sumber dan tanggalnya di `data/SOURCES.md`. Tidak ada satu pun angka yang dikarang.

## Dua seri yang tidak boleh dicampur

1. **Seri nasional SKDR** — laporan ISPA seluruh Indonesia melalui Sistem
   Kewaspadaan Dini dan Respons. Total **14.088.945 laporan** s.d. minggu
   epidemiologi ke-38 tahun 2026.
2. **Seri pemantauan karhutla** — pemantauan khusus dampak kesehatan karhutla di
   **63 kabupaten/kota, 7 provinsi**. Total **283.270 kasus**
   (18 Agustus–13 Oktober 2026).

Kedua seri memiliki cakupan dan tanggal yang berbeda dan **tidak pernah**
dijumlahkan atau digabung dalam satu total atau satu chart di dalam analisis ini.

## Ringkasan Eksekutif

- **Nasional (SKDR):** 14.088.945 laporan ISPA 2026 (s.d. minggu ke-38);
  laporan mingguan naik dari >400 ribu (minggu 27–31) menjadi ~420 ribu
  (minggu 32–37), naik 5,0%.
- **Konsentrasi:** 10 provinsi teratas = 10.530.385 laporan (**74,7%** total
  nasional); 4 teratas (Jabar, Jateng, Jakarta, Jatim) = 55,8%.
  Jabar tertinggi: 2.533.888 (17,98%). **86,3%** laporan top-10 dari Pulau Jawa.
- **Per kapita:** DKI Jakarta tertinggi **150,0 kasus per 1.000 penduduk**
  (populasi BPS 2026) — ~3x Jawa Barat (49,5) dan ~2,3x Banten (65,8).
  Jakarta mencatat kasus 1,16x Jawa Timur dengan penduduk hanya seperempatnya.
- **Karhutla (seri terpisah):** 283.270 kasus di 63 kab/kota (rata-rata 4.496
  per kab/kota). Kalsel 74.636 (26,3%) dan Sumsel 74.458 (26,3%) bersama = 52,6%;
  selisih keduanya hanya 178 kasus. Kumulatif naik **21,1x** dalam 7 minggu
  (13.449 pada 27 Agt → 283.270 pada 13 Okt). 13 Oktober saja: 3.897 kasus baru.
- **Usia (karhutla):** balita (0–5 tahun) **63.711 kasus (22,5%)**; usia >5 tahun
  219.559 (77,5%). Porsi balita stabil: 23,1% (21 Sep) → 22,5% (13 Okt).
- **Kualitas udara:** PM2,5 di 10 wilayah terburuk 507–1.837 (12 Okt 2026,
  15:00 WIB). Barito Kuala 1.837 = **6,1x** ambang ISPU "berbahaya" (>300).
  7 dari 10 wilayah terburuk di Kalimantan Tengah. Kemenkes: 12 kab/kota
  berkategori berbahaya, 9 wilayah sangat tidak sehat.
- **Jakarta:** 1.966.308 kasus Jan–Okt 2025; 2,5 juta Jan–Nov 2025; kenaikan
  musiman +15,7% pada September 2026 (data puskesmas Dinkes DKI).
- **Respons:** 2.106 tenaga kesehatan dimobilisasi; >2,8 juta masker
  didistribusikan; 1.691 puskesmas, 360 RS rujukan, 87 Labkesmas siaga.

## Data

- **Sumber:** kompilasi dari Kemenkes (Situation Report M39-2026; rilis pers),
  SKDR, ISPU KemenLH, Dinkes DKI Jakarta, BPS (Statistik Indonesia 2026).
  Daftar lengkap per angka: `data/SOURCES.md`.
- **File:** `data/compiled/*.csv` (6 file), dimuat ke SQLite oleh
  `scripts/load_to_sqlite.py` → `data/ispa_indonesia.db` (dibuat ulang oleh
  script; tidak di-commit ke git).
- **Populasi:** satu vintage (BPS 2026) untuk semua perbandingan per kapita.
  DI Yogyakarta, Sumatera Barat, dan NTB dikeluarkan dari peringkat per kapita
  karena tidak ada angka populasi satu vintage yang terverifikasi.

## Keterbatasan — baca sebelum mengutip

- Angka SKDR adalah **laporan kasus**, bukan jumlah orang unik.
- Cakupan dan kelengkapan pelaporan berbeda antarprovinsi.
- Angka peringkat 5–10 SKDR dibaca dari grafik (dibulatkan), bukan angka eksak.
- Korelasi tingkat provinsi adalah analisis ekologis: tidak membuktikan
  sebab-akibat pada level individu.
- Seri karhutla hanya mencakup 63 kabupaten/kota terdampak.
- Detail lengkap: `data/SOURCES.md` bagian "Batasan yang harus dipahami".

## Definisi Metrik

- **Kasus SKDR** = laporan ISPA yang tercatat di SKDR pada periode tersebut.
- **Kasus karhutla** = kasus ISPA pada pemantauan khusus dampak karhutla
  (63 kab/kota, 7 provinsi).
- **Kasus per 1.000 penduduk** = kasus / populasi × 1.000 (populasi BPS 2026).
- **Kategori ISPU**: Baik (0–50), Sedang (51–100), Tidak Sehat (101–200),
  Sangat Tidak Sehat (201–300), Berbahaya (>300).
- Semua rate dan pangsa dihitung dari tabel via SQL — tidak ada angka yang dikarang.

## Struktur Repo

```
ispa-indonesia/
├── analysis.ipynb                  # notebook naratif (Bahasa Indonesia): SQL + chart + insight
├── README.md
├── requirements.txt
├── .gitignore
├── build_ppt.py                    # membangun PPT portofolio
├── build_notebook.py               # membangun analysis.ipynb
├── build_module.py                 # membangun modul belajar (PDF)
├── scripts/
│   ├── load_to_sqlite.py           # load CSV -> data/ispa_indonesia.db (+ verifikasi total)
│   └── make_charts.py              # membangun 10 chart
├── sql/
│   └── queries.sql                 # 23 query dengan komentar Bahasa Indonesia
├── charts/                         # 10 chart PNG
└── data/
    ├── SOURCES.md                  # sumber + tanggal untuk setiap angka
    └── compiled/                   # 6 CSV kompilasi
```

## Cara Mereproduksi

```bash
pip install -r requirements.txt
python scripts/load_to_sqlite.py   # verifikasi: top-10 = 10.530.385, karhutla = 283.270
python scripts/make_charts.py      # membangun 10 chart
python build_notebook.py           # membangun analysis.ipynb (lalu jalankan di Jupyter)
python build_ppt.py                # membangun PPT portofolio
python build_module.py             # membangun modul belajar (PDF)
```

## Deliverables lain di repo ini
- Portofolio-Analisis-ISPA-Indonesia.pptx — deck portofolio 10 slide (16:9)
- Modul-Analisis-ISPA-Indonesia.pdf — modul belajar step-by-step (24 halaman)
