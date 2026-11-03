import multiprocessing
import time


def heavy_computation(name, duration):
    time.sleep(duration)
    print(f"{name} done")


if __name__ == "__main__":
    start = time.time()

    p1 = multiprocessing.Process(target=heavy_computation, args=("Task A", 2))
    p2 = multiprocessing.Process(target=heavy_computation, args=("Task B", 3))
    p3 = multiprocessing.Process(target=heavy_computation, args=("Task C", 1))

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()

    print(f"Total time: {time.time() - start:.1f}s")
