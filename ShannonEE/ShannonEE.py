from avatar2 import *
from avatar2.peripherals import *
from pandare import *
import logging
import os

from .peripherals import *
from .hooks import *
from .callbacks import *
from .logger import *


class ShannonEE:
    def __init__(self, segments, patches=None, hooks=None, callbacks=None):
        self.logger = Logger(__class__.__name__, logging.DEBUG, mode='w')

        self.segments = segments
        self.patches = patches
        self.hooks = hooks
        self.callbacks = callbacks

        '''
        BOOT segment runs at ARM decode mode, while others run at ARM-thumb decode mode,
        so we should dump mem after executing BOOT segment in ARM mode then switching to ARM-thumb mode
        '''
        self.prepare()

        self.avatar = Avatar(arch=ARM_CORTEX_R7_THUMB)
        self.target = self.avatar.add_target(PyPandaTarget)

        self.init_segments()
        self.avatar.init_targets()

        self.init_hooks()
        self.init_callbacks()

        self.patch()

    def prepare(self):
        avatar = Avatar(arch=ARM_CORTEX_R7_ARM)
        panda = avatar.add_target(PyPandaTarget, entry_address=0x40000000)

        self._init_segments(self.segments, avatar)
        avatar.init_targets()

        self._patch(self.patches, panda)  # patch memory
        self._init_callbacks(self.callbacks, panda,
                             self.logger)  # register callbacks

        panda.regs.pc = 0x40000000

        # break here to repatch
        bp = 0x4071aed2
        panda.bp(bp)
        panda.cont()
        panda.wait()
        self._patch(self.patches, panda)  # patch again

        # bp = 0x4071b0b4
        # for _ in range(0, 5):
        #     panda.bp(bp)
        #     panda.cont()
        #     panda.wait()
        #     self._patch(self.patches, panda)  # patch again

        # bp = 0x4071b228
        # panda.bp(bp)
        # panda.cont()
        # panda.wait()
        # self._patch(self.patches, panda)

        # panda.cont()
        # panda.wait()

        self._steps(panda, 2000, self.logger)

        for seg in self.segments:
            vaddr = seg['address']
            size = seg['size']
            file_name = "{}_[{},{}].dump".format(
                seg.get('name', 'MPU'), hex(vaddr), hex(vaddr + size - 1))
            peripheral = seg.get('peripheral', None)

            if peripheral is None:
                self._dump_memory(panda.pypanda, vaddr, size, file_name)

        panda.shutdown()
        avatar.shutdown()

    @staticmethod
    def _init_segments(segments, avatar):
        for seg in segments:
            name = seg.get('name', None)
            address = seg['address']
            size = seg['size']
            file_name = seg.get('file_name', None)
            file = os.path.join(
                os.getcwd(), file_name) if file_name is not None else None
            peripheral = seg.get('peripheral', None)

            avatar.add_memory_range(
                name=name, address=address, file=file, size=size, emulate=peripheral)

    def init_segments(self):
        self._init_segments(self.segments, self.avatar)

    '''
    step into by instructions
    '''
    @staticmethod
    def _steps(panda, steps, logger):
        for _ in range(0, steps):
            panda.step()
            pc = panda.rr('pc')
            logger.debug('[cpu steps] {}'.format(hex(pc)))

    def steps(self, steps):
        self._steps(self.target, steps, self.logger)

    @staticmethod
    def _patch(patches, panda):
        for p in patches:
            address = p['address']
            size = p['size']
            value = p['value']
            panda.wm(address, size, value)

    def patch(self):
        self._patch(self.patches, self.target)

    @staticmethod
    def _dump_memory(pypanda, vaddr, size, file_name):
        file_out = open(file_name, 'wb')
        cpu = pypanda.get_cpu()
        mem = pypanda.virtual_memory_read(cpu, vaddr, size)
        file_out.write(mem)
        file_out.close()

    def dump_memory(self, vaddr, size, file_name):
        self._dump_memory(self.pypanda, vaddr, size, file_name)

    @staticmethod
    def _init_hooks(hooks, panda, logger):
        for hk in hooks:
            address = hk['address']
            func = hk['function'](panda, logger)

            panda.add_hook(address, func)

    def init_hooks(self):
        self._init_hooks(self.hooks, self.target, self.logger)

    @staticmethod
    def _init_callbacks(callbacks, panda, logger):
        for cb in callbacks:
            type_ = cb['type']
            func = cb['function'](panda, logger)

            panda.register_callback(type_, func)

    def init_callbacks(self):
        self._init_callbacks(self.callbacks, self.target, self.logger)
