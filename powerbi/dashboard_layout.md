# Dashboard Layout — ISPA Indonesia 2026 (4 halaman, 16:9)

Palet: teal kesehatan `#0F766E` (primer, seri SKDR), oranye `#D97706`
(aksen seri karhutla), merah `#B91C1C` (bahaya ISPU), slate `#475569` (netral).
Font: Segoe UI / Calibri. Satu ide per halaman, judul rata kiri, angka kunci
besar. Halaman karhutla selalu diberi pita peringatan oranye bertuliskan
"SERI KARHUTLA — TERPISAH DARI SKDR".

## Halaman 1 — Ringkasan Nasional SKDR
- **KPI cards (4)**: Total Kasus Nasional SKDR **14.088.945** (s.d. minggu
  ke-38 2026); Pangsa 10 Provinsi Teratas **74,7%**; Kasus per 1000 Penduduk
  tertinggi (DKI Jakarta) **150,0**; Rata-rata Laporan per Minggu **410.909**
  (minggu 27–37).
- **Bar chart horizontal**: 10 provinsi teratas menurut Total Kasus SKDR
  (measure Pangsa Provinsi % sebagai label tambahan). Acuan: Jawa Barat
  2.533.888 di puncak, Nusa Tenggara Barat 331.950 di urutan ke-10.
- **Column chart kecil**: Laporan Mingguan Maks per label periode dari
  `dim_minggu` (Awal musim kemarau 400.000 → Puncak musim kemarau 420.000,
  Kenaikan Laporan Mingguan +5,0%).
- **Slicers**: Pulau (dari `dim_provinsi`). (Sumber: `fact_kasus_provinsi`,
  `fact_total_nasional`, `fact_kasus_mingguan`.)
- Catatan kaki: "Sumber: Kemenkes via SKDR, Situation Report M39-2026.
  Angka provinsi peringkat 5–10 dibaca dari grafik (dibulatkan)."

## Halaman 2 — Per Kapita & Konsentrasi Provinsi
- **Bar chart horizontal terurut**: Kasus per 1000 Penduduk per provinsi.
  Acuan: DKI Jakarta 150,0; Banten 65,8; Jawa Tengah 61,2; Jawa Barat 49,5;
  Jawa Timur 32,5; Sulawesi Selatan dan Sumatera Utara di bawahnya.
  DI Yogyakarta, Sumatera Barat, dan Nusa Tenggara Barat tampil tanpa nilai
  per kapita (populasi satu vintage tidak terverifikasi) — beri catatan.
- **Donut chart**: Pangsa Provinsi % dari total nasional (10 provinsi teratas
  74,7%; sisa 25,3% adalah provinsi di luar 10 teratas, ditampilkan sebagai
  teks catatan, bukan irisan data karena tidak ada di fact provinsi).
- **Tabel**: Provinsi | Total Kasus SKDR | Pangsa Provinsi % | Populasi 2026
  | Kasus per 1000 Penduduk | Kualitas Angka. Sorot kolom Kualitas Angka
  untuk 4 provinsi "Eksak" vs 6 provinsi "Dibaca dari grafik (dibulatkan)".
- **KPI**: Pangsa Pulau Jawa dari 10 teratas **86,3%** (teks statis dari
  tabel verifikasi, karena ukuran ini dihitung lintas provinsi dalam fact).
- **Slicers**: Pulau, Provinsi (multi-select). (Sumber: `fact_kasus_provinsi`.)

## Halaman 3 — Karhutla: Dampak Kesehatan (SERI TERPISAH)
- **Pita peringatan** di bagian atas halaman: "Seri pemantauan karhutla
  (63 kabupaten/kota, 7 provinsi, 18 Agt–13 Okt 2026). TIDAK dijumlahkan ke
  seri SKDR."
- **KPI cards (4)**: Total Kasus Karhutla **283.270**; Pertumbuhan Karhutla
  Kali **21,1x**; Kasus Balita Karhutla **63.711** (Pangsa Balita 22,5%);
  Kasus Baru Harian Terakhir **3.897** (13 Okt 2026).
- **Line/area chart**: `kasus_kumulatif` per tanggal snapshot dari
  `fact_karhutla_series` (13.449 pada 27 Agt → 174.694 pada 21 Sep →
  283.270 pada 13 Okt). Hanya 3 titik snapshot — jangan haluskan garisnya.
- **Bar chart**: Total Kasus Karhutla per Provinsi (Kalimantan Selatan
  74.636; Sumatera Selatan 74.458; 5 provinsi lain (gabungan) 134.176).
  Catatan wajib di bawah visual: baris ketiga adalah gabungan 5 provinsi.
- **Donut chart kecil**: pangsa kelompok usia pada snapshot terakhir
  (Balita 22,5% vs Di atas 5 tahun 77,5%), dari `fact_karhutla_usia`.
- **Slicers**: Tanggal snapshot (untuk seri dan usia). (Sumber: ketiga
  `fact_karhutla_*`. Jangan campur dengan halaman 1–2.)

## Halaman 4 — Kualitas Udara & Konteks Jakarta + Metodologi
- **Bar chart horizontal**: PM2.5 per wilayah dari `fact_ispu`, warna merah
  untuk semua bar (semua kategori Berbahaya), garis referensi pada 300
  (ambang berbahaya). Acuan: Barito Kuala 1.837; Kapuas 1.681; Muaro Jambi
  terendah di daftar ini 507.
- **KPI cards (3)**: Wilayah PM2.5 Tertinggi **Barito Kuala**; PM2.5 Kali
  Ambang Berbahaya **6,1x**; Jumlah Wilayah Berbahaya **10 dari 10** wilayah
  terburuk. Teks pendukung: 7 dari 10 wilayah asal Kalimantan Tengah;
  PM2.5 Rata-rata 987,2.
- **Line chart kecil**: tren bulanan Jakarta 2023 dari
  `fact_jakarta_bulanan` (Januari 102.609 → puncak Maret 119.734 → Juni
  102.475; Rata-rata Kasus Jakarta per Bulan 106.381,8). Beri subjudul
  jelas: "Seri Dinkes DKI 2023, konteks musiman — bukan seri 2026."
- **Tabel metodologi**: dua seri yang terpisah (SKDR nasional vs pemantauan
  karhutla), sifat data kompilasi dari angka resmi yang dipublikasikan
  (bukan file mentah), keterbatasan (angka SKDR adalah laporan kasus bukan
  orang unik; peringkat provinsi 5–10 dibaca dari grafik; korelasi provinsi
  bersifat ekologis), sumber lengkap di `data/SOURCES.md`.
- **Tombol navigasi** kembali ke Halaman 1.

## Aturan konsisten
- Judul halaman: 20pt bold, rata kiri, warna slate gelap.
- Angka KPI: 28pt bold; teal untuk SKDR, oranye untuk karhutla, merah untuk
  ISPU. Warna seri tidak boleh tertukar antarhalaman.
- Persen 1 desimal dengan koma desimal (74,7%), ribuan dengan titik
  (14.088.945), per kapita 1 desimal (150,0).
- Tidak ada visual yang menjumlahkan SKDR dan karhutla; tidak ada slicer
  tanggal di Halaman 1–2; halaman 3 selalu memuat pita peringatan seri
  terpisah.
- Setiap halaman memuat catatan kaki sumber dan tanggal snapshot datanya.
