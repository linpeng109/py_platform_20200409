import os

import pythoncom
from win32comext.shell import shell

from py_config import ConfigFactory
from py_logging import LoggerFactory
from py_path import Path


class ShortCuts():
    PROGRAM_DATA_PATH = r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\GEOVIA'

    def __init__(self, config, logger):
        self.config = config
        self.logger = logger

    def resolve_shortcut(self, filename):
        shell_link = pythoncom.CoCreateInstance(
            shell.CLSID_ShellLink,
            None,
            pythoncom.CLSCTX_INPROC_SERVER,
            shell.IID_IShellLink)

        persistant_file = shell_link.QueryInterface(pythoncom.IID_IPersistFile)

        persistant_file.Load(filename)

        shell_link.Resolve(0, 0)
        linked_to_file = shell_link.GetPath(shell.SLGP_UNCPRIORITY)[0]
        return linked_to_file

    def getSurpacCmdList(self):
        surpac_cmd_list = []
        lnk_list = os.listdir(self.PROGRAM_DATA_PATH)
        for lnk in lnk_list:
            lnk_file = os.path.join(self.PROGRAM_DATA_PATH, lnk)
            if Path.filenameIsContains(lnk_file, 'surpac'):
                result = self.resolve_shortcut(lnk_file)
                if '_x64' in result:
                    result = result.replace('Program Files (x86)', 'Program Files')
                surpac_cmd_list.append(result)
        return surpac_cmd_list

    def getMineSchedCmdList(self):
        minesched_cmd_list = []
        lnk_list = os.listdir(self.PROGRAM_DATA_PATH)
        for lnk in lnk_list:
            lnk_file = os.path.join(self.PROGRAM_DATA_PATH, lnk)
            if Path.filenameIsContains(lnk_file, 'minsched'):
                result = self.resolve_shortcut(lnk_file)
                if '_x64' in result:
                    result = result.replace('Program Files (x86)', 'Program Files')
                minesched_cmd_list.append(result)
        return minesched_cmd_list

if __name__ == '__main__':
    config = ConfigFactory(config_file='py_platform.ini').getConfig()
    logger = LoggerFactory(config=config).getLogger()
    short_cuts = ShortCuts(config=config, logger=logger)
    # surpacList = short_cuts.getSurpacCmdList()
    # logger.debug(surpacList)
    mineschedList = short_cuts.getMineSchedCmdList()
    logger.debug(mineschedList)
