import os
import os.path
import sys


class Path:

    # @classmethod
    @staticmethod
    def split_full_path_filename(full_path_filename):
        full_path_filename = full_path_filename.lower()
        driver = os.path.splitdrive(full_path_filename)[0]
        __path = os.path.split(full_path_filename)[0]
        filename = os.path.split(full_path_filename)[1]
        ext = os.path.splitext(full_path_filename)[1]
        main = filename.strip(ext)
        sep = os.sep
        return {'driver': driver, 'sep': sep, 'path': __path, 'filename': filename, 'main': main, 'ext': ext}

    @staticmethod
    def filename_is_contains_appname(full_path_filename: str, appname: str):
        filename = Path.split_full_path_filename(full_path_filename).get('filename').lower()
        result = True
        for str in appname:
            result = filename.__contains__(str.lower()) and result
        return result

    @staticmethod
    def outpathIsExist(self, outputPath):
        isExist = os.path.isdir(outputPath)
        if not isExist:
            os.makedirs(outputPath)
            print('The Path is not exist. Created (%s).' % outputPath)

    @staticmethod
    def get_resource_path(relative_path: str):
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    @staticmethod
    def get_base_path():
        return os.path.abspath('.')

    @staticmethod
    def join(p1, p2):
        return os.path.join(p1, p2)


if __name__ == '__main__':
    # fullname = '/home/pi/Shared/AFS-8510.xlsx'
    # result1 = splitFullPathFileName(fullname)
    # print(result1)
    # result = filenameIsContains(fullname, ['AFS', 'xlsx'])
    # print(result)
    # Path.outpathIsExist('e:/watchdogdir/aass')
    # path = Path()
    # p1 = path.get_base_path()
    # p2 = 'sclScript'
    # print(path.join(p1, p2))
    print(Path.filename_is_contains_appname('D:\\Program Files\\GEOVIA\\Surpac\\662_x64\\x64\\bin\\surpac2.exe',
                                            appname="surpac2.exe"))
    print(Path.filename_is_contains_appname('C:\\Program Files (x86)\\GEOVIA\\Surpac\\662\\nt_i386\\bin\\surpac2.exe',
                                            appname="surpac2.exe"))
    print(Path.filename_is_contains_appname('C:\\Program Files\\GEOVIA\\Surpac\\69_x64\\x64\\bin\\surpac2.exe',
                                            appname="surpac2.exe"))
