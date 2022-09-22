# This file is placed in the Public Domain.


"handler"


import queue
import threading
import time


from .bus import Bus
from .cbs import Callbacks
from .obj import Object
from .thr import  launch


def __dir__():
    return (
            "Handler",
           )


class Handler(Object):

    def __init__(self):
        Object.__init__(self)
        self.cache = Object()
        self.queue = queue.Queue()
        self.stopped = threading.Event()
        Bus.add(self)

    @staticmethod
    def forever():
        while 1:
            time.sleep(1.0)

    @staticmethod
    def handle(event):
        Callbacks.dispatch(event)

    def loop(self):
        while not self.stopped.isSet():
            self.handle(self.poll())

    def poll(self):
        return self.queue.get()

    def put(self, event):
        self.queue.put_nowait(event)

    @staticmethod
    def register(typ, cbs):
        Callbacks.add(typ, cbs)

    def restart(self):
        self.stop()
        self.start()

    def start(self):
        self.stopped.clear()
        launch(self.loop)

    def stop(self):
        self.stopped.set()
