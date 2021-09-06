import re
from avatar2 import *
from avatar2.peripherals import *
from nose.tools import *
from pandare import *

from .logger import *
from .consts import *


class UARTPeripheral(AvatarPeripheral):
    def hw_read(self, offset, size):
        if offset == 0x18:
            self.status ^= 1
            if self.status == 0:
                return 0x20

        return 0

    def hw_write(self, offset, size, value):
        if offset == 0x0:
            self.logger.info(chr(value))

            return size
        return 0

    def __init__(self, name, address, size, **kwargs):
        AvatarPeripheral.__init__(self, name, address, size)

        self.logger = Logger(camel_to_snake(
            __class__.__name__), logging.INFO, extra_info=False)
        self.status = 0
        self.write_handler[0:size] = self.hw_write
        self.read_handler[0:size] = self.hw_read


class MMIOPeripheral(AvatarPeripheral):
    def hw_read(self, offset, size):
        if offset in self.saved_offsets_with_ret.keys():
            return self.saved_offsets_with_ret[offset]

        if offset in self.offsets_ret_const.keys():
            return self.offsets_ret_const[offset]

        return 0x0

    def hw_write(self, offset, size, value):
        if offset in self.offsets_ret_const.keys():
            return size

        self.saved_offsets_with_ret[offset] = value
        return size

    def __init__(self, name, address, size, **kwargs):
        AvatarPeripheral.__init__(self, name, address, size)

        self.saved_offsets_with_ret = {}
        self.offsets_ret_const = {}
        self.write_handler[0:size] = self.hw_write
        self.read_handler[0:size] = self.hw_read


class ClockPeripheral(MMIOPeripheral):
    def hw_read(self, offset, size):
        if offset in self.offsets_ret_clock.keys():
            return self.offsets_ret_clock[offset](self.cyclic_clock())

        return super().hw_read(offset, size)

    def hw_write(self, offset, size, value):
        if offset in self.offsets_ret_clock.keys():
            self.clock = value
        else:
            super().hw_write(offset, size, value)

        return 1

    def cyclic_clock(self, clock_cycle=0x10000_0000):
        self.clock = ((self.clock + 1) % clock_cycle)
        return self.clock

    def __init__(self, name, address, size, **kwargs):
        super().__init__(name, address, size)
        self.clock = 0
        self.offsets_ret_clock = {}
        self.write_handler[0:size] = self.hw_write
        self.read_handler[0:size] = self.hw_read


class Periph0x4p8e7(MMIOPeripheral):
    def __init__(self, name, address, size, **kwargs):
        MMIOPeripheral.__init__(self, name, address, size)

        self.saved_offsets_with_ret = {
            0x0: NORMAL_MODE,  # modify to change boot mode, alternatives: DUMP_MODE, NORMAL_MODE
        }


class Periph0x8p3e7(MMIOPeripheral):
    def __init__(self, name, address, size, **kwargs):
        MMIOPeripheral.__init__(self, name, address, size)

        self.saved_offsets_with_ret = {
            0x4: 0x03550000, 0x2004: 0x00030000, 0x201c: 0x00000002,
            0x202c: 0x00000001,
            # 0xc034: 0xfffffffc
        }
        self.offsets_ret_const = {
            0x2078: 0x80000000, 0x2090: 0x3f000000,
        }
        self.offsets_ret_clock = {
            # 0x201c: (lambda x: x | 0xffffff00),
            # 0x202c: (lambda x: x | 0xffffff00),
            # 0x2078: (lambda x: x | 0xffffff00),
            # 0x2088: (lambda x: x | 0xffffff00),
            # 0x4308: (lambda x: x | 0xffffff00),
            # 0x2090: (lambda x: x | 0x3e000000)
        }


class Periph0x9p5B4e7(MMIOPeripheral):
    def __init__(self, name, address, size, **kwargs):
        super().__init__(name, address, size)
        self.saved_offsets_with_ret = {
            0x88: 0x2
        }


class Periph0x9p645e7(MMIOPeripheral):
    def __init__(self, name, address, size, **kwargs):
        super().__init__(name, address, size)
        self.saved_offsets_with_ret = {
            0x28: 0x1
        }


def camel_to_snake(name):
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()
