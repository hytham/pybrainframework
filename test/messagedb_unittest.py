import unittest
import sqlite3
import numpy as np
import PIL.Image as img
from messagedb import messagedb 
class messagebusdb_test(unittest.TestCase):
    def test(self):
        self.assertIsNotNone(messagedb.Singletone().db)
    def test_write_np(self):       
        x = np.arange(12).reshape(2,6)
        messagedb.Singletone().Write(x,"test")
        self.assertIsNotNone(messagedb.Singletone().db)

    def test_read_np(self):        
        x = np.arange(12).reshape(2,6)
        messagedb.Singletone().Write(x,"test")
        result = messagedb.Singletone().Read("test")
        self.assertEqual(x.shape,result.shape)

    def test_write_duplicate(self):
       
        x1 = np.arange(12).reshape(2,6)
        messagedb.Singletone().Write(x1,"test")
        x2 = np.arange(12).reshape(3,4)
        messagedb.Singletone().Write(x2,"test")
        result = messagedb.Singletone().Read("test")
        self.assertEqual(x2.shape,result.shape)

    def test_list_all_actives(self):
        x1 = np.arange(12).reshape(2,6)
        x2 = np.arange(12).reshape(3,4)
        messagedb.Singletone().Write(x1,"test1")
        messagedb.Singletone().Write(x2,"test2")
        messagedb.Singletone().Read("test1")
        active =  messagedb.Singletone().AllActiveNames()
        totalActive = len(active)
        self.assertEqual(1,totalActive)

    def test_image(self):
        pic = img.open("./test/res/download.jpg") 
        messagedb.Singletone().WriteImage(pic,"test")
        result = messagedb.Singletone().ReadImage("test")
        self.assertEqual(pic.size,result.size)
    



if __name__ == '__main__': 
    unittest.main() 
        
        