import sqlite3 as sql
import numpy as np
import io
import datetime
import PIL

class messagedb:
    class __messagedbprivate(object):
        def __init__(self, *args, **kwargs):
            self.db=_createInMemoryDatabase()
            return super().__init__(*args, **kwargs)

        def Write(self,npArray,name):
            _write(self.db,npArray,name)
        def Read(self,name):
            '''
            Read for amesage with a specific name
            '''
            row = np.array(_read(self.db,name)[1])
            _deactivate(self.db,name)
            return row
        def AllActiveNames(self):
            actives = np.array(_listAllActive(self.db))
            return actives
        def WriteImage(self,img,name):
            pic_array = np.array(img)
            self.Write(pic_array,name)
        def ReadImage(self,name):
            pic_array = self.Read(name)
            return PIL.Image.fromarray(pic_array)
        def Peek(self,name):
            '''
            Read the specific message without deactivateing it
            '''
            return np.array(_read(self.db,name)[1])
        def IsActive(self,name):
            '''
            return the status of the message true if is active
            '''
            return _read(self.db,name)[2] == 1
        
    __instance = None
    @staticmethod
    def Singletone():
        if messagedb.__instance == None:
            messagedb.__instance = messagedb.__messagedbprivate()
        return messagedb.__instance
   

def _createInMemoryDatabase():
    '''
    Create an in memory database and table and return back a singletone instance of that table
    '''
    sql.register_adapter(np.ndarray, _adapt_array)
    sql.register_converter("array", _convert_array)
    con = sql.connect(':memory:',detect_types=sql.PARSE_DECLTYPES,isolation_level=None)
    cur = con.cursor()
    cur.execute("create table messagebus (name Text,arr array,active INTEGER,timestamp TEXT)")
    return cur

def _write(cur,npArray,name):
    '''
    Write a Numpy array to messagebus Database 
    If the name exisit it will override the current value and make it active
    Else It will create a new one
    '''
    now = np.datetime64(datetime.datetime.now())
    row_exisit = _read(cur,name)
    if row_exisit is not None:
        cur.execute("update messagebus set arr=?,active=1,timestamp=? where name=?", (npArray,now,name, ))
    else:
        cur.execute("insert into messagebus (name,arr,active,timestamp) values (?,?,?,?)", (name,npArray,1,now,))

def _read(cur,name):
    '''
        Read from the messagdb the numpy array for the name and make the active flag false
    '''
    cur.execute("select name,arr,active,timestamp from messagebus where name=?",(name,))
    return cur.fetchone()

def _listAllActive(cur):
    '''
        List all names that5 there status is active`
    '''
    cur.execute("select name from messagebus where active=1")
    names = cur.fetchall()
    return names

def _adapt_array(arr):
    """
    http://stackoverflow.com/a/31312102/190597 (SoulNibbler)
    """
    out = io.BytesIO()
    np.save(out, arr)
    out.seek(0)
    return sql.Binary(out.read())

def _convert_array(text):
    out = io.BytesIO(text)
    out.seek(0)
    return np.load(out)

def _deactivate(cur,name):
    cur.execute("update messagebus set active=0 where name=?", (name, ))



    