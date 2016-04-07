#coding:utf8
#zip and unzip in windows

import zipfile
import os
def filezip(path=r'C:\xsmonitor\empty.exe'):
     d,ext=os.path.splitext(path)
     p,f=os.path.split(path)
     zippath=d+'.zip'
     zipf=zipfile.ZipFile(zippath,'w',zipfile.zlib.DEFLATED)
     zipf.write(path,f)
     zipf.close()
     return zippath
     
def unzip(path=r'C:\xsmonitor\empty.zip'):
     p,f=os.path.split(path)
     zipf=zipfile.ZipFile(path)
     zipf.extractall(p)