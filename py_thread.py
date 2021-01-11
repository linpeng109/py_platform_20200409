import importlib
import threading

from py_socket import SurpacSocketClient


class TbcRunThread(threading.Thread):
    def __init__(self, port, item):
        super(TbcRunThread, self).__init__()
        self.port = port
        self.item = item

    def run(self):
        print('text=%s' % self.item.text(0))
        print('descript=%s' % self.item.text(1))
        print('cmd=%s' % self.item.text(2))
        print('port=%s' % self.port)
        surpac_socket = SurpacSocketClient(int(self.port), 'gbk')
        # 结尾必须添加\n, 否则socket无法识别命令结束
        tbcCommand = 'set status [SclFunction "RECALL ANY FILE" {file = "%s" mode = "openInNewLayer"}]\n' % str(
            self.item.text(2))
        message = 'RCTL\n' + 'TCLSCRIPTBEGIN\n' + tbcCommand + ' TCLSCRIPTEND\n'
        result = surpac_socket.sendMsg(message)
        print('The TBC excute result:\n %s ' % result)
        surpac_socket.closeSocket()
        # pass
        return


class TclRunThread(threading.Thread):
    def __init__(self, port, item):
        super(TclRunThread, self).__init__()
        self.port = port
        self.item = item

    def run(self):
        print('text=%s' % self.item.text(0))
        print('descript=%s' % self.item.text(1))
        print('cmd=%s' % self.item.text(2))
        print('port=%s' % self.port)
        surpac_socket = SurpacSocketClient(int(self.port), 'gbk')
        # 结尾必须添加\n, 否则socket无法识别命令结束
        tbcCommand = 'set status [SclFunction "RECALL ANY FILE" {file = "%s" mode = "openInNewLayer"}]\n' % str(
            self.item.text(2))
        message = 'RCTL\n' + 'TCLSCRIPTBEGIN\n' + tbcCommand + ' TCLSCRIPTEND\n'
        result = surpac_socket.sendMsg(message)
        print('The TCL excute result:\n %s ' % result)
        surpac_socket.closeSocket()
        return


class PyRunThread(threading.Thread):
    def __init__(self, port, item):
        super(PyRunThread, self).__init__()
        self.port = port
        self.item = item

    def run(self):
        module_name = 'sclScript.%s' % str(self.item.text(2)).split('.')[0]
        # module_name = '%s' % str(self.item.text(2)).split('.')[0]
        print('module_name=%s' % module_name)
        metaClass = importlib.import_module(module_name)
        sclCommand = metaClass.message
        surpac_socket = SurpacSocketClient(int(self.port), 'gbk')
        message = 'RCTL\n' + 'TCLSCRIPTBEGIN\n' + sclCommand + ' TCLSCRIPTEND\n'
        result = surpac_socket.sendMsg(message)
        print(result)
        surpac_socket.closeSocket()
        return
