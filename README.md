# Guess The Hero: Mobile Legends
## 🎮 Deskripsi Proyek

**Guess The Hero** adalah sebuah game kuis interaktif berbasis *computer vision* yang menantang pemain untuk menebak nama hero Mobile Legends hanya dari suaranya. Uniknya, game ini tidak memerlukan keyboard atau mouse untuk menjawab. Sebagai gantinya, pemain cukup memiringkan kepala ke kiri atau ke kanan untuk memilih jawaban.

Proyek ini merupakan implementasi dari berbagai teknologi multimedia, menggabungkan pemrosesan video secara *real-time*, deteksi wajah, pemutaran audio, dan antarmuka pengguna yang dinamis.

**Fitur Utama:**
- **Kontrol Gerakan Kepala**: Menggunakan `MediaPipe` untuk mendeteksi kemiringan kepala sebagai input jawaban.
- **Gameplay Audio-Visual**: Menebak hero berdasarkan klip suara ikonik mereka.
- **UI Dinamis**: Antarmuka (pertanyaan dan pilihan) akan mengikuti posisi wajah pemain di layar.
- **Real-time Feedback**: Memberikan umpan balik visual (benar/salah) dan audio secara langsung setelah pemain menjawab.
- **Skor dan Waktu**: Melacak skor dan total waktu bermain untuk setiap sesi.

## 👥 Tim Pengembang

| Nama Lengkap      | NIM        | ID GitHub         |
| ----------------- | ---------- | ----------------- |
| **[Muhammad Riveldo Hermawan Putra]**   | **[122140037]** | **[MuhammadRiveldo]** |
| **[Joshia Fernandes Sectio Purba]**| **[122140171]**| **[Joshia05]**|
| **[Bayu Praneswara Haris]**| **[122140219]**| **[WindBard5]**|

## 📖 Logbook Proyek

| Minggu | Tanggal           | Aktivitas & Progress                                                                                             |
| :----: | ----------------- | ---------------------------------------------------------------------------------------------------------------- |
| **1**  | 10 - 16 Nov 2025  | - Perancangan konsep dan ide awal game "Guess The Hero".<br>- Riset teknologi: `OpenCV` dan `MediaPipe`.<br>- Setup struktur proyek dan repositori Git. |
| **2**  | 17 - 23 Nov 2025  | - Implementasi dasar deteksi wajah dan *landmark* menggunakan `MediaPipe`.<br>- Membuat modul `tilt_detector.py` untuk mendeteksi kemiringan kepala.<br>- Pengumpulan aset awal (suara dan gambar hero). |
| **3**  | 24 - 30 Nov 2025  | - Mengembangkan `question_manager.py` untuk logika soal.<br>- Membuat `audio_manager.py` untuk memutar suara hero dan SFX.<br>- Merancang dan mengimplementasikan UI overlay awal (`ui_overlay.py`). |
| **4**  | 01 - 07 Des 2025  | - Integrasi semua modul ke dalam `main.py`.<br>- Menambahkan loop game utama, sistem skor, dan layar akhir.<br>- *Debugging* dan penyempurnaan interaksi kontrol kepala.<br>- Menambahkan file `README.md`. |

## 🚀 Instalasi & Penggunaan

Pastikan Anda memiliki **Python 3.8+** dan **Git** terpasang di sistem Anda.

**1. Clone Repositori**
```bash
git clone https://github.com/MuhammadRiveldo/Tugas-Besar-Sistem-Teknologi-Multimedia.git
cd [Tugas-Besar-Sistem-Teknologi-Multimedia]
```

**2. Buat Virtual Environment (Direkomendasikan)**
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

**3. Instal Dependensi**
Program ini membutuhkan beberapa library Python. Instal semuanya menggunakan file `requirements.txt`.
```bash
pip install -r requirements.txt
```

**4. Jalankan Program**
Untuk memulai game, jalankan file `main.py`.
```bash
python main.py
```

**Cara Bermain:**
1.  Pastikan wajah Anda terlihat jelas oleh kamera.
2.  Setelah *countdown*, permainan akan dimulai. Dengarkan suara hero yang diputar.
3.  **Miringkan kepala ke kiri** untuk memilih jawaban **A**.
4.  **Miringkan kepala ke kanan** untuk memilih jawaban **B**.
5.  Setelah 5 pertanyaan, skor akhir dan waktu bermain akan ditampilkan.
6.  Tekan tombol **Spasi** untuk bermain lagi atau **Esc** untuk keluar.

## Link Demo
[Link Percobaan Game](https://drive.google.com/file/d/16BN_I1dFnxAERXDs6cSxPX6G5bihTJ5t/view?usp=drivesdk)

---
*Proyek ini dibuat untuk memenuhi Tugas Besar mata kuliah Sistem Teknologi Multimedia.*
