#coding:utf8
#delete the backupfile befor savedays

import datetime
import os
from ftplib import FTP

def cleanlocalbkfile(savedays,backupdir=r'e:\backup'):
    now=datetime.datetime.now()
    yetsavedays=(now-datetime.timedelta(savedays)).strftime('%Y%m%d')
    filelist=os.listdir(backupdir)
    dellist=[]
    for i in filelist:
        if yetsavedays in i:
            try:
                os.remove(backupdir+'\\'+i)
                dellist.append(backupdir+'\\'+i+' deleted')
            except:
                dellist.append(backupdir+'\\'+i+' delete failed')
    return dellist
    
def cleanftpbkfile(server,port,name,password,ftppath,savedays=5):
    now=datetime.datetime.now()
    yetsavedays=(now-datetime.timedelta(savedays)).strftime('%Y%m%d')
    dellist=[]
    ftph=FTP()
    try:
        ftph.connect(server,port,10)
        ftph.login(name,password)
    except:
        ftph.close()
        dellist.append('ftp can not connect')
        return dellist
    try:    
        ftph.cwd(ftppath)
    except:
        ftph.close()
        dellist.append('ftp backupdir is not find')
    filelist=ftph.nlst()
    #print yetsavedays
    #print filelist
    for i in filelist:
        if yetsavedays in i:
            try:
                ftph.delete(i)
                dellist.append(ftppath+'\\'+i+' deleted')
            except:
                dellist.append(ftppath+'\\'+i+' delete failed')
    return dellist
        
if __name__=='__main__':
    print cleanlocalbkfile(1)
    print cleanftpbkfile('10.30.30.56',21,'','admin','backup',2)
    