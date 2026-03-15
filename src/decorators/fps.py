import time

def limit_fps(method):
    def wrapper(self, *args, **kwargs):
        start = time.time()

        result = method(self, *args, **kwargs)

        frame_delay = 1 / self.fps
        elapsed = time.time() - start
        sleep_time = frame_delay - elapsed

        if sleep_time > 0:
            time.sleep(sleep_time)

        return result

    return wrapper