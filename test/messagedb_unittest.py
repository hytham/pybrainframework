import unittest
import sqlite3
import numpy as np
import PIL.Image as img
from messagedb import messagedb 
class messagebusdb_test(unittest.TestCase):
    def test(self):
        mdb = messagedb()
        self.assertIsNotNone(mdb.instance.db)

    def test_write_np(self):
        mdb = messagedb()
        x = np.arange(12).reshape(2,6)
        mdb.instance.Write(x,"test")
        self.assertIsNotNone(mdb.instance.db)

    def test_read_np(self):
        mdb = messagedb()
        x = np.arange(12).reshape(2,6)
        mdb.instance.Write(x,"test")
        result = mdb.instance.Read("test")
        self.assertEqual(x.shape,result.shape)

    def test_write_duplicate(self):
        mdb = messagedb()
        x1 = np.arange(12).reshape(2,6)
        mdb.instance.Write(x1,"test")
        x2 = np.arange(12).reshape(3,4)
        mdb.instance.Write(x2,"test")
        result = mdb.instance.Read("test")
        self.assertEqual(x2.shape,result.shape)

    def test_list_all_actives(self):
        mdb = messagedb()
        x1 = np.arange(12).reshape(2,6)
        x2 = np.arange(12).reshape(3,4)
        mdb.instance.Write(x1,"test1")
        mdb.instance.Write(x2,"test2")
        mdb.instance.Read("test1")
        active = mdb.instance.AllActiveNames()
        totalActive = len(active)
        self.assertEqual(1,totalActive)

    def test_image(self):
        mdb = messagedb()
        pic = img.open("./test/download.jpg") 
        mdb.instance.WriteImage(pic,"test")
        result = mdb.instance.ReadImage("test")
        self.assertEqual(pic.size,result.size)
    



if __name__ == '__main__': 
    unittest.main() 
        
        