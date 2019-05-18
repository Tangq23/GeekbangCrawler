import os


class Singleton(object):
    def __init__(self, cls):
        self._cls = cls
        self._instance = {}
    def __call__(self):
        if self._cls not in self._instance:
            self._instance[self._cls] = self._cls()
        return self._instance[self._cls]

@Singleton
class geekCourseFileOperator(object):

    def __init__(self):
        self._rootDirPath = os.path.join(os.getcwd(),'course')
        self._courseName = ''
        self._downloadPath = ''

    def set_rootDirPath(self,filePath):
        self._rootDirPath = filePath
        print(self._rootDirPath)
        if self.filePathExist(filePath) == False:
            os.mkdir(filePath)

    def get_rootDirPath(self):
        return self._rootDirPath

    def set_courseName(self,courseName):
        self._courseName = courseName
        if self.filePathExist(self._rootDirPath) == False:
            os.mkdir(self._rootDirPath)
        self._downloadPath = os.path.join(self._rootDirPath,courseName)
        if self.filePathExist(self._downloadPath) == False:
            os.mkdir(self._downloadPath)

    def get_downloadPath(self):
        return self._downloadPath

    def filePathExist(self,filePath):
        return os.path.exists(filePath)

