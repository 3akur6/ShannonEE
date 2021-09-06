import logging


class Logger(logging.Logger):
    def __init__(self, name, level, log_to_file=True, mode='a', extra_info=True):
        logging.Logger.__init__(self, name, level)

        self.setLevel(level)

        # create formatter
        formatter = logging.Formatter(
            '%(asctime)s | %(name)s %(levelname)s | %(message)s')

        # create console handler and set level
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(formatter)
        self.addHandler(ch)

        if log_to_file:
            # create file handler and set level
            fh = logging.FileHandler('{}.log'.format(name), mode=mode)
            fh.setLevel(level)

            if extra_info is False:
                formatter = logging.Formatter('%(message)s')
                fh.terminator = ''

            fh.setFormatter(formatter)
            self.addHandler(fh)
