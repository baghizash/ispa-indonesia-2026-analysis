# Panduan Membangun Dashboard — Power BI Desktop

## 1. Persiapan (10 menit)
1. Jika CSV kit belum ada atau data sumber berubah, bangun ulang dulu dari
   folder proyek: `python powerbi/build_powerbi_kit.py` (script menurunkan
   semua CSV kit dari `data/compiled/` dan mencetak tabel verifikasi).
2. Buka Power BI Desktop → Get Data → Text/CSV → impor ke-12 CSV di folder
   ini: `fact_total_nasional.csv`, `fact_kasus_provinsi.csv`,
   `fact_kasus_mingguan.csv`, `fact_karhutla_series.csv`,
   `fact_karhutla_provinsi.csv`, `fact_karhutla_usia.csv`, `fact_ispu.csv`,
   `fact_jakarta_bulanan.csv`, `dim_provinsi.csv`, `dim_minggu.csv`,
   `dim_kelompok_usia.csv`, `dim_wilayah.csv`.
3. Pastikan tipe data:
   - Semua kolom `kasus_*`, `laporan_per_minggu`, `pm25`, `populasi_2026`,
     `minggu_mulai`, `minggu_akhir`, `jumlah_minggu`, `tahun`,
     `nomor_bulan` = Whole Number.
   - `tanggal` (karhutla), `tanggal_snapshot`, `tanggal_mulai`,
     `tanggal_akhir`, `bulan_tanggal` = Date.
   - Sisanya Text. Kolom yang memang kosong sebagian (misalnya
     `kasus_baru_harian`, `populasi_2026` untuk 3 provinsi) biarkan kosong;
     jangan isi nol.
4. Buka Model view. Buat relasi (semuanya satu-ke-banyak, single direction):
   - `dim_provinsi[provinsi_id]` → `fact_kasus_provinsi[provinsi_id]`
   - `dim_provinsi[provinsi_id]` → `fact_karhutla_provinsi[provinsi_id]`
   - `dim_minggu[periode_id]` → `fact_kasus_mingguan[periode_id]`
   - `dim_kelompok_usia[kelompok_usia_id]` → `fact_karhutla_usia[kelompok_usia_id]`
   - `dim_wilayah[wilayah_id]` → `fact_ispu[wilayah_id]`
   - `fact_total_nasional`, `fact_karhutla_series`, dan
     `fact_jakarta_bulanan` TIDAK diberi relasi apa pun (disengaja:
     tabel parameter 1 baris dan dua seri snapshot/bulanan yang berdiri
     sendiri).
5. **Date table: tidak perlu ditandai.** Model ini tidak punya deret tanggal
   harian yang kontinu — tanggal karhutla hanya 3 titik snapshot dan seri
   mingguan SKDR memakai dimensi periode (`dim_minggu`). Menandai tabel
   tanggal akan memaksa kalender kontinu yang tidak ada datanya. Urutkan
   sumbu waktu memakai kolom tanggal/periode apa adanya.

## 2. Measures (15 menit)
1. Salin seluruh blok DAX dari `measures_dax.md` ke dalam model. Saran
   pengelompokan folder display: "SKDR Provinsi", "SKDR Mingguan",
   "Karhutla", "ISPU", "Jakarta".
2. Baca bagian "Catatan level" di `measures_dax.md` SEBELUM membuat visual —
   ini mencegah dua jebakan utama proyek ini: menjumlahkan SKDR dengan
   karhutla, dan mengira jumlah `fact_kasus_provinsi` adalah total nasional.
3. Uji cepat: buat card `Total Kasus Nasional SKDR` tanpa filter → harus
   **14.088.945**. Card `Pangsa 10 Provinsi Teratas %` → **74,7%**. Card
   `Pangsa Balita %` → **22,5%**. Jika beda, cek relasi dan tabel fakta
   yang dipakai.

## 3. Bangun 4 halaman (30–45 menit)
Ikuti `dashboard_layout.md` halaman per halaman:
- Halaman 1–2: HANYA seri SKDR (`fact_total_nasional`,
  `fact_kasus_provinsi`, `fact_kasus_mingguan`).
- Halaman 3: HANYA seri karhutla (ketiga `fact_karhutla_*`), lengkap dengan
  pita peringatan seri terpisah.
- Halaman 4: `fact_ispu` + `fact_jakarta_bulanan` + tabel metodologi (ketik
  manual dari `dashboard_layout.md`).

## 4. Verifikasi akhir (10 menit)
- [ ] Halaman 1 KPI: total nasional 14.088.945; pangsa 10 teratas 74,7%;
      Jakarta 150,0 per 1.000; rata-rata laporan per minggu 410.909.
- [ ] Halaman 2: urutan per kapita Jakarta 150,0 > Banten 65,8 > Jawa Tengah
      61,2 > Jawa Barat 49,5 > Jawa Timur 32,5; 3 provinsi tanpa populasi
      tampil kosong (bukan nol, bukan error).
- [ ] Halaman 3: total karhutla 283.270; balita 63.711 (22,5%); pertumbuhan
      21,1x; jumlah `fact_karhutla_provinsi` = 283.270 (sama dengan snapshot
      terakhir seri waktu).
- [ ] Halaman 4: Barito Kuala 1.837 (6,1x ambang 300); 10 dari 10 wilayah
      kategori Berbahaya; garis referensi 300 terlihat.
- [ ] Tidak ada satu pun visual atau total yang menjumlahkan SKDR dan
      karhutla.
- [ ] Simpan sebagai `ISPA-Indonesia-2026.pbix` (file .pbix tidak di-push ke
      GitHub — GitHub tidak bisa me-render-nya; tambahkan screenshot
      dashboard ke repo sebagai gantinya bila sudah dibangun).

## Troubleshooting
- **KPI total nasional menunjukkan 10.530.385**: visual memakai
  `Total Kasus SKDR` (jumlah 10 provinsi teratas). Ganti ke
  `Total Kasus Nasional SKDR` dari `fact_total_nasional`.
- **Total kasus terlihat dua kali lipat di halaman karhutla**: kemungkinan
  `kasus_kumulatif` dijumlahkan lintas tanggal. Pakai measure
  `Total Kasus Karhutla` (mengambil snapshot terakhir), jangan tarik kolom
  mentahnya langsung ke visual.
- **Kasus per 1000 Penduduk kosong untuk DI Yogyakarta, Sumatera Barat,
  NTB**: benar dan disengaja — ketiga provinsi itu tidak punya populasi BPS
  2026 satu vintage yang terverifikasi. Jangan isi populasi dari sumber lain.
- **Baris "5 provinsi lain (gabungan)" muncul di slicer/peta karhutla**:
  itu gabungan Kalimantan Barat, Kalimantan Tengah, Kalimantan Timur,
  Jambi, dan Riau. Sembunyikan dari peta (gabungan tidak punya lokasi
  tunggal) dan beri catatan pada bar chart.
- **Angka provinsi tidak cocok dengan README**: pastikan visual memakai
  tabel fakta seri yang benar, dan ingat angka peringkat 5–10 SKDR memang
  dibaca dari grafik sehingga dibulatkan (lihat kolom `kualitas_angka`).
- **Sumbu tanggal karhutla tidak urut**: urutkan visual berdasarkan kolom
  `tanggal`, bukan berdasarkan nilai kasus; hanya ada 3 titik snapshot.
