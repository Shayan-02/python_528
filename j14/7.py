from concurrent.futures import ProcessPoolExecutor
import time


def heavy_math(n):
    return sum(range(n))


if __name__ == "__main__":
    numbers = [50_000_000, 50_000_000, 50_000_000, 50_000_000]

    start = time.time()

    with ProcessPoolExecutor(max_workers=4) as executor:
        results = executor.map(heavy_math, numbers)

    for result in results:
        print(result)

    print(f"Total: {time.time() - start:.1f}s")
