import functools
import time


def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(
            f"Функция {func.__name__!r} --- {int(total_time // 60)} мин {total_time % 60:.4f} сек "
        )
        return result

    return wrapper_timer
