import os
import subprocess
import time

from util.py_config import ConfigFactory
from util.py_logging import LoggerFactory
from util.py_path import Path


class Security:
    def __int__(self, config: ConfigFactory, logger: LoggerFactory):
        self.config = config
        self.logger = logger
        self.mail_host = 'smtp - mail.outlook.com'
        self.mail_port = 587
        self.mail_ssl_port = 465
        self.mail_user = 'goldenhello1900 @ outlook.com'
        self.mail_password = '1qaz2wsx3edc'
        self.sender = 'goldenhello1900 @ outlook.com'
        self.receivers = 'goldenhello1900 @ outlook.com'
        self.secret_key = '12345678'
        self.encode = 'utf8'

    # @staticmethod
    def check_hpro_path(self) -> bool:
        hpro_file = Path.get_resource_path('/hpro/HPro.exe')
        return os.path.isfile(hpro_file)

    # @staticmethod
    def read_hpro(self):
        hpro_client_path = Path.get_resource_path("/hpro/HPro.exe")
        io = subprocess.Popen(hpro_client_path, shell=True, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, stdin=subprocess.PIPE, close_fds=True)
        time.sleep(10)
        lines = io.stdout.readlines()
        return lines


if __name__ == '__main__':
    # 设置配置文件和日志
    config = ConfigFactory(config_file='../py_platform.ini').get_config()
    logger = LoggerFactory(config_factory=config).get_logger()

    hpro = Security()
    print(hpro.read_hpro())
    # logger.debug(hpro.readHPro()[0].decode('utf-8'))
