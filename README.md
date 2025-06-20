Aplikasi OUO Backup & Storage merupakan aplikasi penyimpanan dan backup berbasis SQL. Menyediakan fitur penyimpanan dan backup data. Terinspirasi dari penyimpanan berbasis cloud dan pengalaman pribadi dimana
storage local selalu penuh dan membuat kewalahan.
Fitur aplikasi :
1. Upload file
2. Hapus file
3. Export file
4. Hapus akun
Ketentuan yang harus dimiliki :
XAMPP
Database ouo_db
users (username (UNIQUE, VARCHAR255), id(INT,AI), password(VARCHAR,255))
files (id(INT,AI),user_id(FOREIGNKEY,INT),filename(VARCHAR,255),filedata(LONGBLOB),created_at(TIMESTAMP,CURRENTTIMESTAMP)
install python
install mysql-connector
install tkinter
Sesuaikan struktur dengan struktur pada github
Cara menjalankan aplikasi : run main.py
- Lakukan registrasi username dan password
- Login
- Uji coba fitur yang ada
link dokumentasi : https://youtu.be/CuOIu-fWKOA
