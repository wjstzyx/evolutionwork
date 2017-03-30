import logging

class MyLog:

    def __init__(self, name):
        self.name = name
        self.log = logging.getLogger(name)
        self.log.setLevel(logging.INFO)
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console_formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        console.setFormatter(console_formatter)
        self.log.addHandler(console)

    def set_path(self, path):
        file_name = path + self.name + '.log'
        handler_file = logging.FileHandler(file_name)
        file_formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
        handler_file.setFormatter(file_formatter)
        self.log.addHandler(handler_file)

# name='test'
# log_path='E:\\test\\'
# logger = MyLog(name)
# logger.set_path(log_path)
# log = logger.log
# log.info(platform.platform())
# log.info('ddd322')
# log.info('ddd322')