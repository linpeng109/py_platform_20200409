import importlib
import threading
from socket import socket, AF_INET, SOCK_STREAM

from util.py_config import ConfigFactory
from util.py_logging import LoggerFactory
from util.py_path import Path


# Surpac通讯处理
class SurpacSocketClient:

    def __init__(self, config: ConfigFactory, logger: LoggerFactory, port: object):
        self.HOST = 'localhost'
        self.BUFSIZ = 1024
        self.PORT = port
        self.ENCODE = 'gbk'
        self.ADDR = (self.HOST, port)
        self.config = config
        self.logger = logger
        self.tcpCliSock = socket(AF_INET, SOCK_STREAM)
        self.tcpCliSock.connect(self.ADDR)

    def send_message(self, msg):
        self.tcpCliSock.sendall(msg.encode(self.ENCODE))
        result = self.tcpCliSock.recv(self.BUFSIZ)
        return result

    def close_socket(self):
        self.tcpCliSock.close()


class TbcScriptWorker(threading.Thread):
    def __init__(self, config, logger, port, msg):
        super(TbcScriptWorker, self).__init__()
        self.config = config
        self.logger = logger
        self.scl_path = Path.get_resource_path(config.get('master', 'surpac_scl_path'))
        self.surpac_socket_client = SurpacSocketClient(config=config, logger=logger, port=port)
        self.msg = msg

    def run(self):
        # 结尾必须添加\n, 否则socket无法识别命令结束
        tbc_command = 'set status [SclFunction "RECALL ANY FILE" {file = "%s\\%s" mode = "openInNewLayer"}]\n' % (
            self.scl_path, str(self.msg))
        tbc_command = str(tbc_command).replace('\\', '\\\\')
        self.logger.debug(tbc_command)
        message = 'RCTL\n' + 'TCLSCRIPTBEGIN\n' + tbc_command + ' TCLSCRIPTEND\n'
        result = self.surpac_socket_client.send_message(message)
        self.logger.debug('The TBC excute result:\n %s ' % result)
        self.surpac_socket_client.close_socket()
        return result


class TclScriptWorker(threading.Thread):
    def __init__(self, config, logger, port, msg):
        super(TclScriptWorker, self).__init__()
        self.config = config
        self.logger = logger
        self.scl_path = Path.get_resource_path(config.get('master', 'surpac_scl_path'))
        self.surpac_socket_client = SurpacSocketClient(config=config, logger=logger, port=port)
        self.msg = msg

    def run(self):
        # 结尾必须添加\n, 否则socket无法识别命令结束
        tcl_command = 'set status [SclFunction "RECALL ANY FILE" {file = "%s\\%s" mode = "openInNewLayer"}]\n' % (
            self.scl_path, str(self.msg))
        tcl_command = str(tcl_command).replace('\\', '\\\\')
        self.logger.debug(tcl_command)
        message = 'RCTL\n' + 'TCLSCRIPTBEGIN\n' + tcl_command + ' TCLSCRIPTEND\n'
        result = self.surpac_socket_client.send_message(message)
        self.logger.debug('The TCL excute result: %s ' % result)
        self.surpac_socket_client.close_socket()
        return result


class SurpacInitWorker(threading.Thread):
    def __init__(self, config, logger, port):
        super(SurpacInitWorker, self).__init__()
        self.config = config
        self.logger = logger
        self.scl_path = Path.get_resource_path(config.get('surpac', 'surpac_scl_path'))
        self.surpac_socket_client = SurpacSocketClient(config=config, logger=logger, port=port)
        self.msg = 'test_init.py'

    def run(self):
        # 结尾必须添加\n, 否则socket无法识别命令结束
        tcl_command = 'set status [SclFunction "RECALL ANY FILE" {file = "%s\\%s" mode = "openInNewLayer"}]\n' % (
            self.scl_path, str(self.msg))
        tcl_command = str(tcl_command).replace('\\', '\\\\')
        self.logger.debug(tcl_command)
        message = 'RCTL\n' + 'TCLSCRIPTBEGIN\n' + tcl_command + ' TCLSCRIPTEND\n'
        result = self.surpac_socket_client.send_message(message)
        self.logger.debug('The Surpac Init excute result: %s ' % result)
        self.surpac_socket_client.close_socket()
        return result


class SurpacChangeLanguageWorker(threading.Thread):
    def __init__(self, config, logger, port, msg):
        super(SurpacChangeLanguageWorker, self).__init__()
        self.config = config
        self.logger = logger
        self.scl_path = Path.get_resource_path(config.get('master', 'surpac_scl_path'))
        self.surpac_socket_client = SurpacSocketClient(config=config, logger=logger, port=port)
        self.msg = msg

    def run(self):
        # 结尾必须添加\n, 否则socket无法识别命令结束
        tcl_command = 'set status [SclFunction "RECALL ANY FILE" {file = "%s\\%s" mode = "openInNewLayer"}]\n' % (
            self.scl_path, str(self.msg))
        tcl_command = str(tcl_command).replace('\\', '\\\\')
        self.logger.debug(tcl_command)
        message = 'RCTL\n' + 'TCLSCRIPTBEGIN\n' + tcl_command + ' TCLSCRIPTEND\n'
        result = self.surpac_socket_client.send_message(message)
        self.logger.debug('The TCL excute result: %s ' % result)
        self.surpac_socket_client.close_socket()
        return result


class PyScriptWorker(threading.Thread):
    def __init__(self, config, logger, port, msg):
        super(PyScriptWorker, self).__init__()
        self.config = config
        self.logger = logger
        self.scl_path = Path.get_resource_path(config.get('master', 'surpac_scl_path'))
        self.surpac_socket_client = SurpacSocketClient(config=config, logger=logger, port=port)
        self.msg = msg

    def run(self):
        module_name = 'sclScript.%s' % str(self.msg.split('.')[0])
        self.logger.debug('module_name=%s' % module_name)
        meta_class = importlib.import_module(module_name)
        scl_command = meta_class.message
        message = 'RCTL\n' + 'TCLSCRIPTBEGIN\n' + scl_command + ' TCLSCRIPTEND\n'
        result = self.surpac_socket_client.send_message(message)
        self.logger.debug('The py excute result: %s ' % result)
        self.surpac_socket_client.close_socket()
        return result


class FunScriptWorker(threading.Thread):
    def __init__(self, config, logger, port, msg):
        super(FunScriptWorker, self).__init__()
        self.config = config
        self.logger = logger
        self.scl_path = Path.get_resource_path(config.get('master', 'surpac_scl_path'))
        self.surpac_socket_client = SurpacSocketClient(config=config, logger=logger, port=port)
        self.msg = msg

    def run(self):
        func_command = 'set status [ SclFunction \"%s\" {} ]' % str(self.msg)
        message = 'RCTL\n' + 'TCLSCRIPTBEGIN\n' + func_command + '\n' + 'TCLSCRIPTEND\n'
        self.logger.debug('message : %s' % message)
        result = self.surpac_socket_client.send_message(message)
        self.logger.debug('The Function excute result :%s' % result)
        self.surpac_socket_client.close_socket()
        return result
