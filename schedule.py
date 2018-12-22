import time
import threading


class Schedule:
    def __init__(self):
        self.loop = True

    def start(self, interval, func, wait=True):
        base_time = time.time()
        next_time = 0
        while self.loop:
            t = threading.Thread(target=func)
            t.start()
            if wait:
                t.join()
            next_time = ((base_time - time.time()) % interval) or interval
            time.sleep(next_time)

    def stop(self):
        self.loop = False
