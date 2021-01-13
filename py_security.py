import subprocess
import time

from py_config import ConfigFactory
from py_logging import LoggerFactory


class HPro:
    mail_host = 'smtp - mail.outlook.com'
    mail_port = 587
    mail_ssl_port = 465
    mail_user = 'goldenhello1900 @ outlook.com'
    mail_password = '1qaz2wsx3edc'
    sender = 'goldenhello1900 @ outlook.com'
    receivers = 'goldenhello1900 @ outlook.com'
    secret_key = '12345678'
    encode = 'utf8'

    def __init__(self, config: ConfigFactory, logger: LoggerFactory):
        self.config = config
        self.logger = logger

    def readHPro(self):
        io = subprocess.Popen("d:/HPro.exe", shell=True, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, stdin=subprocess.PIPE, close_fds=True)
        time.sleep(10)
        lines = io.stdout.readlines()
        return lines


if __name__ == '__main__':
    # 设置配置文件和日志
    config = ConfigFactory(config_file='py_platform.ini').getConfig()
    logger = LoggerFactory(config=config).getLogger()

    hpro = HPro(config=config, logger=logger)
    print(hpro.readHPro())
    # logger.debug(hpro.readHPro()[0].decode('utf-8'))
