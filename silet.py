import os
from playwright.sync_api import sync_playwright
import time
import random

# Path ke file tokens.txt
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_PATH = os.path.join(SCRIPT_DIR, "tokens.txt")

# Fungsi untuk membaca token dari file
def load_tokens():
    if not os.path.exists(TOKEN_PATH):
        print("⚠️ File tokens.txt tidak ditemukan!")
        return []
    with open(TOKEN_PATH, "r") as f:
        tokens = [line.strip() for line in f.readlines() if line.strip()]
    return tokens

# Fungsi untuk login dan menjalankan task
def login_and_run_task(token):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            extra_http_headers={"Authorization": f"Bearer {token}"}
        )
        page = context.new_page()
        page.goto("https://silentprotocol.com")  # Ganti dengan URL yang benar

        print(f"✅ Login berhasil dengan token: {token}")

        # Menunggu antrian selesai (simulasi polling)
        while True:
            if "queue-finished" in page.url:  # Sesuaikan dengan URL setelah antrian selesai
                break
            print("⏳ Masih dalam antrian, cek lagi...")
            time.sleep(10)  # Tunggu 10 detik sebelum cek lagi

        print("🎉 Antrian selesai!")

        # Pilih task dan klik contribute
        try:
            page.click("button:has-text('Contribute')")  # Sesuaikan dengan selector yang benar
            time.sleep(3)  # Tunggu sebentar

            # Klik particle dalam kotak
            page.click(".particle-box")  # Sesuaikan dengan selector yang benar
            time.sleep(3)

            # Klik contribute lagi
            page.click("button:has-text('Contribute')")  # Sesuaikan dengan selector yang benar
            time.sleep(5)

            # Tunggu halaman teks abstrak muncul
            while not page.query_selector("textarea"):
                print("⏳ Menunggu kolom teks...")
                time.sleep(5)

            # Isi teks abstrak random
            abstract_text = f"Teks acak {random.randint(1000, 9999)}"
            page.fill("textarea", abstract_text)
            time.sleep(2)

            # Klik contribute setelah isi teks
            page.click("button:has-text('Contribute')")  # Sesuaikan dengan selector yang benar
            time.sleep(10)

            # Tunggu sampai muncul 'Back to Home' lalu klik
            while not page.query_selector("button:has-text('Back to Home')"):
                print("⏳ Menunggu tombol 'Back to Home'...")
                time.sleep(5)

            page.click("button:has-text('Back to Home')")
            time.sleep(5)

            # Tunggu sampai muncul 'Contribute Now' lalu klik
            while not page.query_selector("button:has-text('Contribute Now')"):
                print("⏳ Menunggu tombol 'Contribute Now'...")
                time.sleep(5)

            page.click("button:has-text('Contribute Now')")
            print("✅ Task selesai!")

        except Exception as e:
            print(f"❌ Terjadi kesalahan: {e}")

        browser.close()

# Load token dari file
tokens = load_tokens()
if not tokens:
    print("⚠️ Tidak ada token yang ditemukan.")
else:
    for token in tokens:
        login_and_run_task(token)