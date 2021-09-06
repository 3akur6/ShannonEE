import struct

from .logger import *


class HooksFactory:
    def __init__(self, target, logger):
        self.logger = logger

        self.target = target
        self.pypanda = self.target.pypanda
        self.pypanda_arch = self.pypanda.arch
        self.cpu = self.pypanda.get_cpu

    def hook_regs_fn(self, env, tb, hook):
        pypd = self.pypanda
        pypd_arch = self.pypanda_arch
        lr = hex(pypd_arch.get_reg(env, 'lr'))
        r0_value = hex(pypd_arch.get_reg(env, 'r0'))
        r1_value = hex(pypd_arch.get_reg(env, 'r1'))
        r2_value = pypd_arch.get_reg(env, 'r2')
        r2_str = pypd.read_str(self.cpu(), r2_value)
        r3_value = hex(pypd_arch.get_reg(env, 'r3'))
        pc_value = hex(pypd_arch.get_pc(env))
        self.logger.debug("[hook at {}, ret {}] r0->{} r1->{} r2->{} r3->{}".format(pc_value,
                                                                                    lr, r0_value, r1_value, r2_str, r3_value))

    def hook_log_printf_fn(self, env, tb, hook):
        pypd = self.pypanda
        pypd_arch = self.pypanda_arch
        cpu = self.cpu()
        r0_value = pypd_arch.get_reg(env, 'r0')

        log_context = struct.unpack('<Q', pypd.virtual_memory_read(
            self.cpu(), r0_value, 8))[0]
        flag = log_context >> (4 * 8)
        te_struct_addr = log_context & 0x0000_0000_ffff_ffff

        te_struct_message_addr = te_struct_addr + 4 * 4
        te_struct_linenum_addr = te_struct_addr + 5 * 4
        te_struct_file_addr = te_struct_addr + 6 * 4

        te_message_addr = pypd.virtual_memory_read(
            cpu, te_struct_message_addr, 4)
        te_linenum = pypd.virtual_memory_read(
            cpu, te_struct_linenum_addr, 4)
        te_file_addr = pypd.virtual_memory_read(
            cpu, te_struct_file_addr, 4)
        # te_message = pypanda.read_str(cpu, te_message_addr)
        # te_file = pypanda.read_str(cpu, te_file_addr)
        self.logger.debug("[[log_printf] {}:{}] {}".format(
            te_file_addr, te_linenum, te_message_addr))

    def hook_snprintf_fn(self, env, tb, hook):
        sp = self.pypanda_arch.get_reg(env, 'sp')
        msg_addr = sp
        msg_length = self.pypanda_arch.get_reg(env, 'r4')
        msg = self.pypanda.read_str(env, msg_addr, msg_length)

        self.logger.debug("[[snprintf] {} {}] {}".format(
            msg_addr, msg_length, msg))
