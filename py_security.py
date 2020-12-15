import subprocess

from py_config import ConfigFactory
from py_logging import LoggerFactory


class HPro:
    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

    def readHPro(self):
        io = subprocess.Popen("h:/HPro.exe", shell=True, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, stdin=subprocess.PIPE, close_fds=True)
        lines = io.stdout.readlines()
        return lines


if __name__ == '__main__':
    # 设置配置文件和日志
    config = ConfigFactory(config_file='py_platform.ini').getConfig()
    logger = LoggerFactory(config=config).getLogger()

    hpro = HPro(config=config, logger=logger)
    logger.debug(hpro.readHPro()[0].decode('utf-8'))
