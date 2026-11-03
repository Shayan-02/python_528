import time


start_time = time.time()

def heavy_math():
    total = sum(range(50_000_000))
    print("done")

heavy_math()
print(f"Total: {time.time() - start_time:.5f}s")
