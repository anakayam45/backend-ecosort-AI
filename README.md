# Pilahin AI - Backend API Documentation

Dokumentasi ini memuat informasi teknis mengenai struktur *endpoint* API yang tersedia pada *backend* Pilahin AI berbasis FastAPI.

---

## 📑 Ringkasan Endpoint

| No | Method | Endpoint | Deskripsi | Input / Parameter | Tipe Konten (Request) | Format Respons (Success) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **1** | <kbd>GET</kbd> | `/` | Menampilkan halaman utama aplikasi | *Tidak ada* | *None* | File HTML (`text/html`) |
| **2** | <kbd>POST</kbd> | `/predict_url` | Prediksi objek berdasarkan URL gambar | `process_id`<br>`image_url` | `application/json` / `multipart/form-data` | JSON:<br>`{"process_id": "...", "classes": "..."}` |
| **3** | <kbd>POST</kbd> | `/predict_image` | Prediksi objek berdasarkan *upload* file gambar | `process_id`<br>`file` *(jpeg, jpg, png)* | `multipart/form-data` | JSON:<br>`{"process_id": "...", "classes": "..."}` |

---

## 🛠️ Detail Spesifikasi API

### 1. Main Page (`GET /`)
* **Kegunaan:** Memuat antarmuka pengguna (UI) awal.
* **Struktur Tabel:**

| Komponen | Spesifikasi | Keterangan |
| :--- | :--- | :--- |
| **HTTP Method** | `GET` | — |
| **Response Headers** | `Content-Type: text/html` | Mengembalikan file `templates/index.html` |
| **Status Code** | `200 OK` | Request berhasil diproses |

---

### 2. Prediksi via URL (`POST /predict_url`)
* **Kegunaan:** Melakukan klasifikasi citra menggunakan alamat URL gambar eksternal.
* **Struktur Tabel:**

| Jenis Data | Parameter / Key | Tipe Data | Keterangan / Contoh Nilai |
| :--- | :--- | :--- | :--- |
| **Request Body** | `session_id` | *String* | ID unik untuk tracking proses (misal: `PROC-12345`) |
| | `image_url` | *String* | Tautan langsung ke gambar (misal: `https://example.com/image.jpg`) |
| **Response Body** | `session_id` | *String* | Mengembalikan ID proses yang sama |
| | `category` | *String* | Hasil klasifikasi objek/sampah/makanan dari model AI |
| | `confidence` | *float* | Nilai tingkat akurasi klasifikasi
---

### 3. Prediksi via File Upload (`POST /predict_image`)
* **Kegunaan:** Melakukan klasifikasi citra dengan mengunggah berkas gambar langsung dari penyimpanan lokal.
* **Struktur Tabel:**

| Jenis Data | Parameter / Key | Tipe Data | Keterangan / Ketentuan Berkas |
| :--- | :--- | :--- | :--- |
| **Request Payload**| `session_id` | *String* | ID unik untuk tracking proses |
| | `file` | *Binary / File* | Berkas gambar dengan format: `image/jpeg`, `image/jpg`, atau `image/png` |
| **Response Body** | `session_id` | *String* | Mengembalikan ID proses yang sama |
| | `category` | *String* | Hasil klasifikasi objek/sampah/makanan dari model AI |
| | `confidence` | *float* | Nilai tingkat akurasi klasifikasi
---

## 🚀 Cara Menjalankan Project secara Lokal

1. **Install Python versi 3.11.9**

   Download melalui url ini [Python 3.11.9](https://www.python.org/downloads/release/python-3119/), kemudian instaal dan pastikan mencentang opsi **"Add Python to PATH"**

2. **Pastikan dependensi sudah terinstal:**
   ```bash
   pip install -r requirements.txt

3. **Untuk menjalankan server:**
   ```bash
   python app.py