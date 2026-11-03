import threading
import time


def download_page(url):
    print(f"Downloading {url}...")
    time.sleep(2)
    print(f"Finished {url}")


start = time.time()

# t1 = threading.Thread(target=download_page, args=("https://www.digikala.com/",))
# t2 = threading.Thread(target=download_page, args=("https://ayandehedu.ir/",))
# t3 = threading.Thread(target=download_page, args=("https://ayandehbartaredu.ir/",))

# t1.start()
# t2.start()
# t3.start()

# t1.join()
# t2.join()
# t3.join()

t1 = download_page("https://www.digikala.com/")
t2 = download_page("https://ayandehedu.ir/")
t3 = download_page("https://ayandehbartaredu.ir/")

print(f"Total: {time.time() - start:.1f}s")
