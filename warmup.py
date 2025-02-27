import time


def fibonacci_warmup(duration=60):
    start_time = time.time()
    a, b = 0, 1
    count = 0

    while time.time() - start_time < duration:
        a, b = b, a + b
        count += 1

    print(f"Computed {count} Fibonacci numbers in {duration} seconds.")


if __name__ == "__main__":
    fibonacci_warmup()
