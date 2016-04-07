#coding:utf8
#ftpupload ftptest

from ftplib import FTP
import os

def ftptest(server,port,name,password):
    ftph=FTP()
    try:
        ftph.connect(server,port,5)
    except:
        error='can not connect server: %s'%(server)
        ftph.close()
        return error
    try:
        ftph.login(name,password)
    except:
        error='ftp username or password error'
        ftph.close()
        return error
    #ftph.close()
    return 1

def ftpupload(server,port,name,password,ftppath,uploadfilepath):
    try:
        ftph=FTP()
        ftph.connect(server,port,10)
        ftph.login(name,password)
    except:
        ftph.close()
        return 'ftp can not connect'
    try:
        ftph.cwd(ftppath)
    except:
        ftph.mkd(ftppath)
        ftph.cwd(ftppath)
    p,f=os.path.split(uploadfilepath)
    try:
        fileh=open(uploadfilepath,'rb')
    except:
        ftph.close()
        return 'uploadfile can not be opened'
    try:
        ftph.storbinary('STOR '+f,fileh,1024)
    except:
        fileh.close()
        ftph.close()
        return 'ftp upload error'
    fileh.close()
    ftph.close()    
    return 1
   
    
if __name__ == '__main__':
    print ftptest('10.30.30.56',21,'','admin')
    #print ftpupload('190.160.100.35',21,'admin','admin','upload',r'E:\backup\data150313141649.zip')
    