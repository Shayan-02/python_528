import multiprocessing
import time


def heavy_math(name):
    total = sum(range(50_000_000))
    print(f"{name} done")


if __name__ == "__main__":
    start = time.time()

    p1 = multiprocessing.Process(target=heavy_math, args=("Task A",))
    p2 = multiprocessing.Process(target=heavy_math, args=("Task B",))

    p1.start()
    p2.start()
    p1.join()
    p2.join()

    print(f"Total: {time.time() - start:.1f}s")
