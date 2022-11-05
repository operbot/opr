# This file is placed in the Public Domain.


"event"

__version__ = "1"


## imports


import threading


from .bus import Bus
from .prs import Parsed


## classes


class Event(Parsed):

    """Event class

    events to use in the Handler
    """

    def __init__(self):
        Parsed.__init__(self)
        self.__ready__ = threading.Event()
        self.control = "!"
        self.result = []
        self.type = "event"

    def bot(self):
        """Event.bot()

        return originating bot.
        """
        return Bus.byorig(self.orig)

    def ready(self):
        """Event.ready()

        flag event as ready.
        """
        self.__ready__.set()

    def reply(self, txt):
        """Event.reply(txt)

        add txt to the result list.
        """
        self.result.append(txt)

    def show(self):
        """Event.show()

        display the result list by sending text to the bus.
        """
        for txt in self.result:
            Bus.say(self.orig, self.channel, txt)

    def wait(self):
        """Event.wait()

        wait for the event to finish.
        """
        self.__ready__.wait()
