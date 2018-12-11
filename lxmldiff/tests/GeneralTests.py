import unittest
import inspect
from lxmldiff import getPath, xDiffCore


class CompareAll(unittest.TestCase):
    

    @staticmethod
    def execute(folder_name):    
        _i = xDiffCore.xDiffExecutor()
        _i.path1 = "{}\\tests\\{}\\a.xml".format(getPath(), folder_name)
        _i.path2 =  "{}\\tests\\{}\\b.xml".format(getPath(), folder_name)
        _i.run()    
    
    def test1(self):
        name = inspect.currentframe().f_code.co_name
        self.__class__.execute(name)

    def test2(self):
        name = inspect.currentframe().f_code.co_name
        self.__class__.execute(name)
        
    def test3(self):
        name = inspect.currentframe().f_code.co_name
        self.__class__.execute(name)

    def test4(self):
        name = inspect.currentframe().f_code.co_name
        self.__class__.execute(name)
             
    def test7(self):
        name = inspect.currentframe().f_code.co_name
        self.__class__.execute(name)
        
