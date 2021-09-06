from ShannonEE.ShannonEE import ShannonEE
from ShannonEE.hooks import HooksFactory
from ShannonEE.callbacks import CallbacksFactory
from ShannonEE.peripherals import *

import os

segments = [
    {'address': 0x00000000, 'size': 0x2000000},
    {'name': 'MAIN_TCM', 'address': 0x04000000, 'size': 0x20000,
     'file_name': 'MAIN_TCM_[04000000,0401ffff]_1826092679825801319.tmp.bin'},
    {'address': 0x04800000, 'size': 0x4000},
    {'name': 'BOOT', 'address': 0x40000000, 'size': 0x4600000,
     'file_name': 'BOOT_[40000000,445fffff]_12863093404423111288.tmp.bin'},
    {'address': 0x44600000, 'size': 0x100000},
    {'address': 0x45100000, 'size': 0x700000},
    {'address': 0x45800000, 'size': 0x100000},
    {'address': 0x45900000, 'size': 0x700000},
    {'address': 0x46000000, 'size': 0x1600000},
    {'address': 0x47600000, 'size': 0x200000},
    {'address': 0x47800000, 'size': 0x200000},
    {'address': 0x47a00000, 'size': 0x600000},
    {'address': 0x48000000, 'size': 0x30, 'peripheral': Periph0x4p8e7},
    {'address': 0x80000000, 'size': 0x3000000},
    {'address': 0x83000000, 'size': 0x3000, 'peripheral': Periph0x8p3e7},
    {'address': 0x83003000, 'size': 0x13000},
    {'address': 0x84000000, 'size': 0x20, 'peripheral': UARTPeripheral},
    {'address': 0x84000020, 'size': 0x10000},
    {'address': 0x85000000, 'size': 0x1000},
    {'address': 0x95b40000, 'size': 0x10000, 'peripheral': Periph0x9p5B4e7},
    {'address': 0x96450000, 'size': 0x10000, 'peripheral': Periph0x9p645e7},
    {'address': 0xe2000000, 'size': 0x1e000000},
]

patches = [
    {'address': 0x40000454, 'size': 4, 'value': 0xeaffff42},  # b 0x40000164
    {'address': 0x40000164, 'size': 4, 'value': 0xea003fa6},  # b 0x40010004
    # {'address': 0x4072f412, 'size': 2, 'value': 0xe7db},
    # {'address': 0x4072f49a, 'size': 2, 'value': 0xe7d4},
    # {'address': 0x4072f52c, 'size': 2, 'value': 0xe7be},
    # {'address': 0x4072f890, 'size': 2, 'value': 0xe7f5},
    # {'address': 0x40fc1e5a, 'size': 2, 'value': 0xe7ff},
    {'address': 0x406cfd8a, 'size': 2, 'value': 0xe0a9},
    # {'address': 0x04014098, 'size': 2, 'value': 0xe00b},
    # {'address': 0x040139ae, 'size': 2, 'value': 0xe00c},
    # {'address': 0x40a23dd6, 'size': 2, 'value': 0xe007},

    # data patch
    {'address': 0x83004308, 'size': 4, 'value': 0x00000002},
]

hooks = [
    {'address': 0x40fc2d82, 'function': (
        lambda panda, logger: HooksFactory(panda, logger).hook_regs_fn)},
    {'address': 0x04012866, 'function': (
        lambda panda, logger: HooksFactory(panda, logger).hook_regs_fn)},
    {'address': 0x406cd35a, 'function': (
        lambda panda, logger: HooksFactory(panda, logger).hook_log_printf_fn)},
    {'address': 0x40FB9A9A, 'function': (
        lambda panda, logger: HooksFactory(panda, logger).hook_snprintf_fn)},
]

callbacks = [
    {'type': 'mmio_before_write', 'function': (
        lambda panda, logger: CallbacksFactory(panda, logger).mmio_before_write_cb)},
    {'type': 'mmio_after_read', 'function': (
        lambda panda, logger: CallbacksFactory(panda, logger).mmio_after_read_cb)},
    {'type': 'virt_mem_before_write', 'function': (
        lambda panda, logger: CallbacksFactory(panda, logger).virt_mem_before_write_cb)},
    {'type': 'top_loop', 'function': (
        lambda panda, logger: CallbacksFactory(panda, logger).top_loop_cb)},
    {'type': 'after_cpu_exec_enter', 'function': (
        lambda panda, logger: CallbacksFactory(panda, logger).after_cpu_exec_enter_cb)},
    {'type': 'before_cpu_exec_exit', 'function': (
        lambda panda, logger: CallbacksFactory(panda, logger).before_cpu_exec_exit_cb)},
]

# delete UART log file
uart_peripheral_log = 'uart_peripheral.log'
if os.path.exists(uart_peripheral_log):
    os.remove(uart_peripheral_log)

shm = ShannonEE(segments, patches, hooks, callbacks)
