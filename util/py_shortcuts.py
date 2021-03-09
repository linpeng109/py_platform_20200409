import os

import pythoncom
from win32comext.shell import shell

from util.py_config import ConfigFactory
from util.py_logging import LoggerFactory
from util.py_path import Path


class ShortCuts:
    # PROGRAM_DATA_PATH = r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\GEOVIA'
    # PROGRAM_DATA_PATH = r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Gemcom Software'

    def __init__(self, config: ConfigFactory, logger: LoggerFactory):
        self.config = config
        self.logger = logger
        self.program_data_path = config.get('master', 'program_data_path')

    @staticmethod
    def resolve_shortcut(filename):
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

    def get_surpac_cmd_list(self):
        surpac_cmd_list = []
        lnk_list = os.listdir(self.program_data_path)
        for lnk in lnk_list:
            lnk_file = os.path.join(self.program_data_path, lnk)
            if Path.filename_is_contains_appname(appname='surpac', full_path_filename=lnk_file):
                result = self.resolve_shortcut(lnk_file)
                if '_x64' in result:
                    result = result.replace('Program Files (x86)', 'Program Files')
                surpac_cmd_list.append(result)
        return surpac_cmd_list

    def get_minesched_cmd_list(self):
        minesched_cmd_list = []
        lnk_list = os.listdir(self.program_data_path)
        for lnk in lnk_list:
            lnk_file = os.path.join(self.program_data_path, lnk)
            if Path.filename_is_contains_appname(appname='minsched', full_path_filename=lnk_file):
                result = self.resolve_shortcut(lnk_file)
                if '_x64' in result:
                    result = result.replace('Program Files (x86)', 'Program Files')
                minesched_cmd_list.append(result)
        return minesched_cmd_list

    def get_whittle_cmd_list(self):
        whittle_cmd_list = []
        lnk_list = os.listdir(self.program_data_path)
        for lnk in lnk_list:
            lnk_file = os.path.join(self.program_data_path, lnk)
            if Path.filename_is_contains_appname(appname='whittle', full_path_filename=lnk_file):
                result = self.resolve_shortcut(lnk_file)
                if '_x64' in result:
                    result = result.replace('Program Files (x86)', 'Program Files')
                whittle_cmd_list.append(result)
        return whittle_cmd_list


if __name__ == '__main__':
    config = ConfigFactory(config_file='../py_platform.ini').get_config()
    logger = LoggerFactory(config_factory=config).get_logger()
    short_cat = ShortCuts(config=config, logger=logger)
    logger.debug(short_cat.get_surpac_cmd_list())
    logger.debug(short_cat.get_whittle_cmd_list())
    logger.debug(short_cat.get_minesched_cmd_list())
