from datetime import datetime
from enum import Enum


class LEVEL(Enum):
    INFO = 1
    ERROR = 2
    WARN = 3
    DEBUG = 4

    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


level = LEVEL.DEBUG


def separator():
    print("~~~~~~~~~~~~")


def info(*args, **kwargs):
    if level >= LEVEL.INFO:
        print(f"[{datetime.now().strftime('%b-%d %H:%M')}] INFO", *args, **kwargs)


# def error()
# def warn()
# def debug()
