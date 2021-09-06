import logging


class CallbacksFactory:
    def __init__(self, target, logger):
        self.logger = logger
        self.target = target
        self.pypanda = self.target.pypanda
        self.pypanda_arch = self.pypanda.arch

    def mmio_before_write_cb(self, env, physaddr, vaddr, size, val):
        pc = self.pypanda_arch.get_pc(env)
        lr = self.pypanda_arch.get_reg(env, 'lr')
        self.logger.debug("[mmio_before_write]\tpc->{}\tlr->{}\tvaddr->{}\tsize->{}\tval->{}".format(
            hex(pc), hex(lr), hex(vaddr), size, hex(val[0])))

    def mmio_after_read_cb(self, env, physaddr, vaddr, size, val):
        pc = self.pypanda_arch.get_pc(env)
        lr = self.pypanda_arch.get_reg(env, 'lr')
        self.logger.debug("[mmio_after_read]\tpc->{}\tlr->{}\tvaddr->{}\tsize->{}\tval->{}".format(
            hex(pc), hex(lr), hex(vaddr), size, hex(val[0])))

    def virt_mem_before_write_cb(self, env, pc, addr, size, buf):
        pc = self.pypanda_arch.get_pc(env)
        self.logger.debug("[virt_mem_before_write]\tpc->{}\taddr->{}\tbuf->{}".format(
            hex(pc), hex(addr), hex(buf)))

    def top_loop_cb(self, env):
        self.logger.debug("[loop] {}".format(
            hex(self.pypanda_arch.get_pc(env))))

    def after_cpu_exec_enter_cb(self, env):
        self.logger.debug("[after_cpu_exec_enter]\tlr->{}".format(
            hex(self.pypanda_arch.get_reg(env, 'lr'))))

    def before_cpu_exec_exit_cb(self, env, ranblock):
        self.logger.debug("[before_cpu_exec_exit]\tenv->{}".format(
            hex(self.pypanda_arch.get_pc(env))))
