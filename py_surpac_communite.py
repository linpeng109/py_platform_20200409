import importlib
import threading

from py_path import Path
from py_socket import SurpacSocketClient


class ChangeLanguageThread(threading.Thread):
    def __init__(self, port, choice_language: str, config, logger):
        super(ChangeLanguageThread, self).__init__()
        self.port = port
        self.config = config
        self.logger = logger
        self.choice_language = choice_language

    def run(self) -> None:
        changeLanguage_chinese_command = r'''
            set env(SurpacDevInterface)  "Chinese"
            set status [ SclFunction "MESSAGE OPTIONS" {
              frm00207={
                {
                  language="chinese"
                  log_msg="off"
                  dbg_msg="off"
                  info_msg="on"
                  warn_msg="on"
                  iwarning="0"
                  isevere="0"
                  buffer_size="1000"
                  beep_on_error="off"
                }
              }
            }]        
        '''

        changeLanguage_english_command = r'''
            set env(SurpacDevInterface)  "English"
            set status [ SclFunction "MESSAGE OPTIONS" {
              frm00207={
                {
                  language="default"
                  log_msg="off"
                  dbg_msg="off"
                  info_msg="on"
                  warn_msg="on"
                  iwarning="0"
                  isevere="0"
                  buffer_size="1000"
                  beep_on_error="off"
                }
              }
            }]        
        '''
        if 'chinese' in self.choice_language:
            changeLanguage_command = changeLanguage_chinese_command
        elif 'english' in self.choice_language:
            changeLanguage_command = changeLanguage_english_command
        else:
            changeLanguage_command = ''
        surpac_socket = SurpacSocketClient(int(self.port), 'gbk')
        message = 'RCTL\n' + 'TCLSCRIPTBEGIN\n' + changeLanguage_command + ' TCLSCRIPTEND\n'
        result = surpac_socket.sendMsg(message)
        surpac_socket.closeSocket()


class TbcRunThread(threading.Thread):
    def __init__(self, port, item, config, logger):
        super(TbcRunThread, self).__init__()
        self.port = port
        self.item = item
        self.config = config
        self.logger = logger

    def run(self):
        self.logger.debug(
            'text=%s;descript=%s;cmd=%s;port=%s' % (self.item.text(0), self.item.text(1), self.item.text(2), self.port))
        surpac_socket = SurpacSocketClient(int(self.port), 'gbk')
        # 结尾必须添加\n, 否则socket无法识别命令结束
        tbcCommand = 'set status [SclFunction "RECALL ANY FILE" {file = "%s" mode = "openInNewLayer"}]\n' % str(
            self.item.text(2))
        message = 'RCTL\n' + 'TCLSCRIPTBEGIN\n' + tbcCommand + ' TCLSCRIPTEND\n'
        result = surpac_socket.sendMsg(message)
        self.logger.debug('The TBC excute result:\n %s ' % result)
        surpac_socket.closeSocket()
        # pass
        return


class TclRunThread(threading.Thread):
    def __init__(self, port, item, config, logger):
        super(TclRunThread, self).__init__()
        self.port = port
        self.item = item
        self.config = config
        self.logger = logger

    def run(self):
        self.logger.debug(
            'text=%s;descript=%s;cmd=%s;port=%s' % (self.item.text(0), self.item.text(1), self.item.text(2), self.port))
        surpac_socket = SurpacSocketClient(int(self.port), 'gbk')
        # 结尾必须添加\n, 否则socket无法识别命令结束
        tbcCommand = 'set status [SclFunction "RECALL ANY FILE" {file = "%s" mode = "openInNewLayer"}]\n' % str(
            self.item.text(2))
        message = 'RCTL\n' + 'TCLSCRIPTBEGIN\n' + tbcCommand + ' TCLSCRIPTEND\n'
        result = surpac_socket.sendMsg(message)
        self.logger.debug('The TBC excute result:\n %s ' % result)
        surpac_socket.closeSocket()
        return


class PyRunThread(threading.Thread):
    def __init__(self, port, item, config, logger):
        super(PyRunThread, self).__init__()
        self.port = port
        self.item = item
        self.config = config
        self.logger = logger

    def run(self):
        module_name = 'sclScript.%s' % str(self.item.text(2)).split('.')[0]
        # module_name = '%s' % str(self.item.text(2)).split('.')[0]
        self.logger.debug('module_name=%s' % module_name)
        metaClass = importlib.import_module(Path.resource_path(module_name))
        sclCommand = metaClass.message
        surpac_socket = SurpacSocketClient(int(self.port), 'gbk')
        message = 'RCTL\n' + 'TCLSCRIPTBEGIN\n' + sclCommand + ' TCLSCRIPTEND\n'
        result = surpac_socket.sendMsg(message)
        self.logger.debug('result=%s' % result)
        surpac_socket.closeSocket()
        return
