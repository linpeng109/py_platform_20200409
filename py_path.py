import os
import os.path
import sys
import pkgutil

class Path():

    @classmethod
    def splitFullPathFileName(self, fullPathFileName):
        fullPathFileName = fullPathFileName.lower()
        driver = os.path.splitdrive(fullPathFileName)[0]
        path = os.path.split(fullPathFileName)[0]
        filename = os.path.split(fullPathFileName)[1]
        ext = os.path.splitext(fullPathFileName)[1]
        main = filename.strip(ext)
        sep = os.sep
        return {'driver': driver, 'sep': sep, 'path': path, 'filename': filename, 'main': main, 'ext': ext}

    @classmethod
    def filenameIsContains(self, fullPathFileName: str, strs):
        filename = Path.splitFullPathFileName(fullPathFileName).get('filename').lower()
        result = True

        for str in strs:
            result = filename.__contains__(str.lower()) and result
        return result

    @classmethod
    def outpathIsExist(self, outputPath):
        isExist = os.path.isdir(outputPath)
        if not isExist:
            os.makedirs(outputPath)
            print('The Path is not exist. Created (%s).' % outputPath)

    @classmethod
    def resource_path(self, relative_path: str):
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)

    @classmethod
    def get_base_path(self):
        return os.path.abspath('.')

    @classmethod
    def join(self, p1, p2):
        return os.path.join(p1, p2)


if __name__ == '__main__':
    # fullname = '/home/pi/Shared/AFS-8510.xlsx'
    # result1 = splitFullPathFileName(fullname)
    # print(result1)
    # result = filenameIsContains(fullname, ['AFS', 'xlsx'])
    # print(result)
    # Path.outpathIsExist('e:/watchdogdir/aass')
    path = Path()
    p1 = path.get_base_path()
    p2 = 'sclScript'
    print(path.join(p1,p2))
