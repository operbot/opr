# This file is placed in the Public Domain.


"thread"


import queue
import threading
import time


from .obj import name


def __dir__():
    return (
            'Thread',
            'launch'
           )


class Thread(threading.Thread):

    def __init__(self, func, thrname, *args, daemon=True):
        super().__init__(None, self.run, name, (), {}, daemon=daemon)
        self._exc = None
        self._evt = None
        self.name = thrname or name(func)
        self.queue = queue.Queue()
        self.queue.put_nowait((func, args))
        self.sleep = None
        self.starttime = time.time()
        self.state = None
        self._result = None

    def __iter__(self):
        return self

    def __next__(self):
        for k in dir(self):
            yield k

    def join(self, timeout=None):
        super().join(timeout)
        return self._result

    def run(self) -> None:
        func, args = self.queue.get()
        if args:
            self._evt = args[0]
        self.setName(self.name)
        self.starttime = time.time()
        self._result = func(*args)


def launch(func, *args, **kwargs):
    thrname = kwargs.get("name", name(func))
    thr = Thread(func, thrname, *args)
    thr.start()
    return thr
