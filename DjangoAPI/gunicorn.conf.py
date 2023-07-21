import multiprocessing

bind = '167.99.192.225:8000'  # Ganti dengan host dan port yang sesuai
workers = multiprocessing.cpu_count() * 2 + 1  # Jumlah worker yang diinginkan, disarankan menggunakan formula ini
timeout = 120  # Timeout dalam detik, sesuaikan dengan kebutuhan Anda

# Opsional: Konfigurasi logging
accesslog = '-'  # Untuk logging akses ke stdout
errorlog = '-'  # Untuk logging error ke stdout
loglevel = 'info'  # Level logging yang diinginkan, bisa diganti menjadi 'debug' untuk detail yang lebih tinggi

# Opsional: Konfigurasi fitur lainnya
# preload_app = True  # Load aplikasi sebelum fork worker
# max_requests = 1000  # Batas jumlah maksimal request per worker
# max_requests_jitter = 100  # Jitter untuk max_requests
# keepalive = 2  # Waktu keep-alive connection
# threads = 4  # Jumlah thread yang diinginkan jika menggunakan Django dengan Gunicorn

# Callback function saat Gunicorn mulai menjalankan worker
def on_starting(server):
    print('Server Gunicorn telah dimulai')