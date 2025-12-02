TikTok Comment Cleaner 🧹

Aplikasi web sederhana untuk membersihkan data komentar TikTok yang kotor (bahasa alay), mengekstrak kata kunci (keywords), dan melakukan analisis sentimen sederhana.

Dibuat menggunakan Python dan Streamlit.

Fitur

Auto-Cleaning: Mengubah bahasa alay menjadi baku (misal: "yg" -> "yang", "bgt" -> "banget").

Keyword Extraction: Mengambil kata-kata penting dari komentar.

Sentiment Analysis: Menentukan apakah komentar bersifat Positif, Negatif, Netral, atau Pertanyaan.

Excel Output: Hasil bisa langsung didownload dalam format Excel yang rapi.

Cara Menggunakan (Untuk Teman)

Buka link website (link akan muncul setelah kamu deploy).

Upload file Excel (.xlsx) berisi komentar TikTok mentah.

Tunggu proses selesai.

Klik tombol Download.

Cara Install di Komputer Sendiri (Localhost)

Jika ingin menjalankan di laptop sendiri sebelum diupload:

Pastikan sudah install Python.

Install library yang dibutuhkan:

pip install -r requirements.txt


Jalankan aplikasi:

streamlit run app.py


Cara Deploy ke Streamlit Cloud (Online)

Upload semua file ini (app.py, requirements.txt) ke Repository GitHub (Public).

Buka share.streamlit.io.

Login dengan GitHub.

Klik "New App".

Pilih repository kamu, lalu klik Deploy.

Selesai! Web kamu sudah online.
