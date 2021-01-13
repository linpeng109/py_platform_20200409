import importlib
import threading
from socket import socket, AF_INET, SOCK_STREAM

from py_path import Path
from py_config import ConfigFactory
from py_logging import LoggerFactory


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

    def sendMsg(self, msg):
        self.tcpCliSock.sendall(msg.encode(self.ENCODE))
        result = self.tcpCliSock.recv(self.BUFSIZ)
        return result

    def closeSocket(self):
        self.tcpCliSock.close()


class Tbc_script_worker(threading.Thread):
    def __init__(self, config, logger, port, msg):
        super(Tbc_script_worker, self).__init__()
        self.config = config
        self.logger = logger
        self.scl_path = Path.get_resource_path(config.get('master', 'surpac_scl_path'))
        self.surpac_socket_client = SurpacSocketClient(config=config, logger=logger, port=port)
        self.msg = msg

    def run(self):
        # 结尾必须添加\n, 否则socket无法识别命令结束
        tbcCommand = 'set status [SclFunction "RECALL ANY FILE" {file = "%s\\%s" mode = "openInNewLayer"}]\n' % (
            self.scl_path, str(self.msg))
        tbcCommand = str(tbcCommand).replace('\\', '\\\\')
        self.logger.debug(tbcCommand)
        message = 'RCTL\n' + 'TCLSCRIPTBEGIN\n' + tbcCommand + ' TCLSCRIPTEND\n'
        result = self.surpac_socket_client.sendMsg(message)
        self.logger.debug('The TBC excute result:\n %s ' % result)
        self.surpac_socket_client.closeSocket()
        return result


class Tcl_script_worker(threading.Thread):
    def __init__(self, config, logger, port, msg):
        super(Tcl_script_worker, self).__init__()
        self.config = config
        self.logger = logger
        self.scl_path = Path.get_resource_path(config.get('master', 'surpac_scl_path'))
        self.surpac_socket_client = SurpacSocketClient(config=config, logger=logger, port=port)
        self.msg = msg

    def run(self):
        # 结尾必须添加\n, 否则socket无法识别命令结束
        tclCommand = 'set status [SclFunction "RECALL ANY FILE" {file = "%s\\%s" mode = "openInNewLayer"}]\n' % (
            self.scl_path, str(self.msg))
        tclCommand = str(tclCommand).replace('\\', '\\\\')
        self.logger.debug(tclCommand)
        message = 'RCTL\n' + 'TCLSCRIPTBEGIN\n' + tclCommand + ' TCLSCRIPTEND\n'
        result = self.surpac_socket_client.sendMsg(message)
        self.logger.debug('The TCL excute result: %s ' % result)
        self.surpac_socket_client.closeSocket()
        return result


class Surpac_init_worker(threading.Thread):
    def __init__(self, config, logger, port):

        super(Surpac_init_worker, self).__init__()
        self.config = config
        self.logger = logger
        self.scl_path = Path.get_resource_path(config.get('surpac', 'surpac_scl_path'))
        self.surpac_socket_client = SurpacSocketClient(config=config, logger=logger, port=port)
        self.msg = 'test_init.py'

    def run(self):
        # 结尾必须添加\n, 否则socket无法识别命令结束
        tclCommand = 'set status [SclFunction "RECALL ANY FILE" {file = "%s\\%s" mode = "openInNewLayer"}]\n' % (
            self.scl_path, str(self.msg))
        tclCommand = str(tclCommand).replace('\\', '\\\\')
        self.logger.debug(tclCommand)
        message = 'RCTL\n' + 'TCLSCRIPTBEGIN\n' + tclCommand + ' TCLSCRIPTEND\n'
        result = self.surpac_socket_client.sendMsg(message)
        self.logger.debug('The Surpac Init excute result: %s ' % result)
        self.surpac_socket_client.closeSocket()
        return result


class Surpac_changelanguage_worker(threading.Thread):
    def __init__(self, config, logger, port, msg):
        super(Surpac_changelanguage_worker, self).__init__()
        self.config = config
        self.logger = logger
        self.scl_path = Path.get_resource_path(config.get('master', 'surpac_scl_path'))
        self.surpac_socket_client = SurpacSocketClient(config=config, logger=logger, port=port)
        self.msg = msg

    def run(self):
        # 结尾必须添加\n, 否则socket无法识别命令结束
        tclCommand = 'set status [SclFunction "RECALL ANY FILE" {file = "%s\\%s" mode = "openInNewLayer"}]\n' % (
            self.scl_path, str(self.msg))
        tclCommand = str(tclCommand).replace('\\', '\\\\')
        self.logger.debug(tclCommand)
        message = 'RCTL\n' + 'TCLSCRIPTBEGIN\n' + tclCommand + ' TCLSCRIPTEND\n'
        result = self.surpac_socket_client.sendMsg(message)
        self.logger.debug('The TCL excute result: %s ' % result)
        self.surpac_socket_client.closeSocket()
        return result


class Py_script_worker(threading.Thread):
    def __init__(self, config, logger, port, msg):
        super(Py_script_worker, self).__init__()
        self.config = config
        self.logger = logger
        self.scl_path = Path.get_resource_path(config.get('master', 'surpac_scl_path'))
        self.surpac_socket_client = SurpacSocketClient(config=config, logger=logger, port=port)
        self.msg = msg

    def run(self):
        module_name = 'sclScript.%s' % str(self.msg.split('.')[0])
        self.logger.debug('module_name=%s' % module_name)
        metaClass = importlib.import_module(module_name)
        sclCommand = metaClass.message
        message = 'RCTL\n' + 'TCLSCRIPTBEGIN\n' + sclCommand + ' TCLSCRIPTEND\n'
        result = self.surpac_socket_client.sendMsg(message)
        self.logger.debug('The py excute result: %s ' % result)
        self.surpac_socket_client.closeSocket()
        return result


class Fun_script_worker(threading.Thread):
    def __init__(self, config, logger, port, msg):
        super(Fun_script_worker, self).__init__()
        self.config = config
        self.logger = logger
        self.scl_path = Path.get_resource_path(config.get('surpac', 'surpac_scl_path'))
        self.surpac_socket_client = SurpacSocketClient(config=config, logger=logger, port=port)
        self.msg = msg

    def run(self):
        funcCommand = 'set status [ SclFunction \"%s\" {} ]' % str(self.msg)
        message = 'RCTL\n' + 'TCLSCRIPTBEGIN\n' + funcCommand + '\n' + 'TCLSCRIPTEND\n'
        self.logger.debug('message : %s' % message)
        result = self.surpac_socket_client.sendMsg(message)
        self.logger.debug('The Function excute result :%s' % result)
        self.surpac_socket_client.closeSocket()
        return result
