-- =====================================================================
-- Analisis ISPA Indonesia 2026 — Query SQL
-- Dataset KOMPILASI dari angka resmi yang dipublikasikan (lihat data/SOURCES.md).
-- Dua seri TIDAK PERNAH dicampur: seri nasional SKDR dan seri pemantauan karhutla.
-- Semua angka dihitung dari tabel; tidak ada angka yang dikarang.
-- =====================================================================

-- ---------------------------------------------------------------------
-- BAGIAN A — SERI NASIONAL SKDR (total nasional 14.088.945 laporan, s.d. minggu ke-38 2026)
-- ---------------------------------------------------------------------

-- A1. Total 10 provinsi teratas dan pangsa terhadap total nasional
-- Jawab: berapa besar porsi 10 provinsi teratas dari seluruh laporan nasional?
SELECT SUM(CAST(kasus_skdr_2026 AS INTEGER)) AS total_top10,
       ROUND(100.0 * SUM(CAST(kasus_skdr_2026 AS INTEGER)) / 14088945, 1) AS persen_dari_nasional
FROM skdr_provinsi;

-- A2. Peringkat 10 provinsi berdasarkan jumlah kasus absolut
SELECT provinsi, CAST(kasus_skdr_2026 AS INTEGER) AS kasus,
       ROUND(100.0 * CAST(kasus_skdr_2026 AS INTEGER) / 14088945, 2) AS persen_nasional
FROM skdr_provinsi
ORDER BY kasus DESC;

-- A3. Peringkat per kapita (kasus per 1.000 penduduk) — hanya provinsi dengan populasi terverifikasi
-- Jawab: setelah dibagi jumlah penduduk, provinsi mana yang bebannya paling berat?
-- DI Yogyakarta, Sumatera Barat, NTB dikeluarkan karena tidak ada angka populasi satu vintage yang terverifikasi.
SELECT provinsi, CAST(kasus_skdr_2026 AS INTEGER) AS kasus,
       CAST(populasi_2026 AS INTEGER) AS populasi,
       ROUND(1000.0 * CAST(kasus_skdr_2026 AS INTEGER) / CAST(populasi_2026 AS INTEGER), 1) AS kasus_per_1000_penduduk
FROM skdr_provinsi
WHERE populasi_2026 != ''
ORDER BY kasus_per_1000_penduduk DESC;

-- A4. Empat provinsi teratas vs sisanya (konsentrasi geografis)
SELECT CASE WHEN provinsi IN ('Jawa Barat', 'Jawa Tengah', 'DKI Jakarta', 'Jawa Timur')
            THEN '4 provinsi teratas' ELSE '6 provinsi lain (top 10)' END AS kelompok,
       SUM(CAST(kasus_skdr_2026 AS INTEGER)) AS kasus,
       ROUND(100.0 * SUM(CAST(kasus_skdr_2026 AS INTEGER)) / 10530385, 1) AS persen_top10
FROM skdr_provinsi
GROUP BY kelompok;

-- A5. Pulau Jawa vs luar Jawa di dalam top 10 (Jawa = Jabar, Jateng, Jakarta, Jatim, Banten, DIY)
SELECT CASE WHEN provinsi IN ('Jawa Barat', 'Jawa Tengah', 'DKI Jakarta', 'Jawa Timur', 'Banten', 'DI Yogyakarta')
            THEN 'Pulau Jawa' ELSE 'Luar Jawa' END AS wilayah,
       SUM(CAST(kasus_skdr_2026 AS INTEGER)) AS kasus,
       ROUND(100.0 * SUM(CAST(kasus_skdr_2026 AS INTEGER)) / 10530385, 1) AS persen_top10
FROM skdr_provinsi
GROUP BY wilayah;

-- A6. Rasio kasus Jakarta terhadap Jawa Timur (perbandingan 2 provinsi)
SELECT ROUND(1600814.0 / 1374373, 2) AS rasio_jakarta_vs_jatim;

-- A7. Laporan mingguan nasional: awal vs puncak musim kemarau
SELECT periode, minggu_epidemiologi, CAST(laporan_per_minggu AS INTEGER) AS laporan_per_minggu
FROM mingguan_nasional;

-- A8. Kenaikan laporan mingguan dari awal ke puncak musim kemarau (persen)
SELECT ROUND(100.0 * (420000 - 400000) / 400000, 1) AS kenaikan_persen_awal_ke_puncak;

-- ---------------------------------------------------------------------
-- BAGIAN B — SERI PEMANTAUAN KARHUTLA (63 kab/kota, 7 provinsi, 18 Agt–13 Okt 2026)
-- Seri ini TERPISAH dari seri nasional SKDR. Jangan dijumlahkan ke total nasional.
-- ---------------------------------------------------------------------

-- B1. Total karhutla dan pembagian usia
SELECT kasus_kumulatif AS total,
       balita_0_5_tahun AS balita,
       usia_diatas_5_tahun AS usia_diatas_5,
       ROUND(100.0 * CAST(balita_0_5_tahun AS INTEGER) / CAST(kasus_kumulatif AS INTEGER), 1) AS persen_balita,
       ROUND(100.0 * CAST(usia_diatas_5_tahun AS INTEGER) / CAST(kasus_kumulatif AS INTEGER), 1) AS persen_diatas_5
FROM karhutla_series WHERE tanggal = '2026-10-13';

-- B2. Dua provinsi tertinggi vs 5 provinsi lain (seri karhutla)
SELECT provinsi, CAST(kasus_karhutla_18agt_13okt_2026 AS INTEGER) AS kasus,
       ROUND(100.0 * CAST(kasus_karhutla_18agt_13okt_2026 AS INTEGER) / 283270, 1) AS persen_total_karhutla
FROM karhutla_provinsi
ORDER BY kasus DESC;

-- B3. Selisih Kalsel vs Sumsel (dua provinsi tertinggi seri karhutla)
SELECT 74636 - 74458 AS selisih_kalsel_sumsel,
       ROUND(100.0 * (74636 - 74458) / 74636, 2) AS selisih_persen;

-- B4. Pertumbuhan kumulatif seri karhutla antar snapshot
SELECT tanggal, CAST(kasus_kumulatif AS INTEGER) AS kasus_kumulatif
FROM karhutla_series
ORDER BY tanggal;

-- B5. Faktor pertumbuhan 27 Agt -> 13 Okt (berapa kali lipat)
SELECT ROUND(283270.0 / 13449, 1) AS kali_lipat_27agt_ke_13okt;

-- B6. Pangsa balita antar snapshot (apakah porsi anak berubah?)
SELECT tanggal, CAST(kasus_kumulatif AS INTEGER) AS total,
       CAST(balita_0_5_tahun AS INTEGER) AS balita,
       ROUND(100.0 * CAST(balita_0_5_tahun AS INTEGER) / CAST(kasus_kumulatif AS INTEGER), 1) AS persen_balita
FROM karhutla_series
WHERE balita_0_5_tahun != ''
ORDER BY tanggal;

-- B7. Rata-rata kasus per kabupaten/kota terdampak (seri karhutla)
SELECT ROUND(283270.0 / 63, 0) AS rata_rata_kasus_per_kabkota;

-- ---------------------------------------------------------------------
-- BAGIAN C — KUALITAS UDARA (ISPU, 12 Okt 2026 15:00 WIB)
-- ---------------------------------------------------------------------

-- C1. 10 wilayah dengan PM2,5 tertinggi
SELECT wilayah, provinsi, CAST(pm25_12okt2026_1500wib AS INTEGER) AS pm25
FROM ispu_wilayah
ORDER BY pm25 DESC;

-- C2. Wilayah dengan PM2,5 di atas 1.000 (kategori berbahaya, ambang ISPU >300)
SELECT COUNT(*) AS wilayah_pm25_diatas_1000
FROM ispu_wilayah
WHERE CAST(pm25_12okt2026_1500wib AS INTEGER) > 1000;

-- C3. Rasio PM2,5 tertinggi terhadap ambang berbahaya (>300)
SELECT ROUND(1837.0 / 300, 1) AS kali_lipat_ambang_berbahaya_barito_kuala;

-- C4. Jumlah wilayah per provinsi dalam daftar 10 terburuk
SELECT provinsi, COUNT(*) AS jumlah_wilayah
FROM ispu_wilayah
GROUP BY provinsi
ORDER BY jumlah_wilayah DESC;

-- ---------------------------------------------------------------------
-- BAGIAN D — JAKARTA (seri kota, terpisah)
-- ---------------------------------------------------------------------

-- D1. Rata-rata kasus bulanan Jakarta semester I 2023
SELECT ROUND(AVG(CAST(kasus_ispa_jakarta_2023 AS INTEGER)), 0) AS rata_rata_bulanan,
       MIN(CAST(kasus_ispa_jakarta_2023 AS INTEGER)) AS terendah,
       MAX(CAST(kasus_ispa_jakarta_2023 AS INTEGER)) AS tertinggi
FROM jakarta_bulanan;

-- D2. Bulan tertinggi vs terendah Jakarta 2023 (selisih dan rasio)
SELECT ROUND((119734 - 99130) * 100.0 / 99130, 1) AS selisih_persen_maret_vs_mei;

-- D3. Total semester I 2023 Jakarta
SELECT SUM(CAST(kasus_ispa_jakarta_2023 AS INTEGER)) AS total_jan_jun_2023
FROM jakarta_bulanan;
