#coding:utf8
#the scripts for pubwin backup 
#it can be backup every day 

import os
import time
from  logging import *
import win
import ini
import zipf

#设置log
loglevel=DEBUG
basicConfig(level=loglevel,
                format='%(asctime)s %(levelname)s  %(funcName)s:%(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                filename='pubwinBackuper.log',
                filemode='a')
                
def getpath():
    #获取当地程序所在目录
    info(os.path.abspath('.'))
    return os.path.abspath('.')
    
    
def dbtest(dbpasswd):
    #检查数据库是否可以登录
    cmd="osql -U netcafe -P "+dbpasswd+" -Q "+"\""+\
        ""+"\""
    popenstr=os.popen(cmd)
    popenstrreadlines=popenstr.readlines()
    if len(popenstrreadlines)==0:return 1
    for i in popenstrreadlines:debug(i)
    return 0
    
def bkfilepath(backuppath):
    return backuppath+'\\data'+time.strftime('%y%m%d%H%M%S')+'.bk'
    
def backupcmdstr(bkfilepath,dbpasswd):
    sqlstr="BACKUP DATABASE LOCAL TO DISK='%s'" %(bkfilepath) 
    osqlstr='osql -U netcafe -P %s -d master -Q "%s"'%(dbpasswd,sqlstr)
    debug('osqlstr %s'%(osqlstr))
    return osqlstr

def backup(osqlstr):
    #成功返回使用时间，失败返回0
    info('make backup file start')
    starttime=time.time()
    popenstr=os.popen(osqlstr)
    popenstrreadlines=popenstr.readlines()
    usetime=time.time()-starttime
    for i in popenstrreadlines:debug(i)
    if len(popenstrreadlines)==3:
        info('backup success usetime:%ss'%(usetime))
        info('make backup file end')
        return usetime
    info('backup failed')
    return 0
   
#主程序开始
                
#程序运行参数

backuppath=ini.getbackuppath()
if backuppath[-1]=='\\':backuppath=backuppath[:-1]
info('backup path is %s' %backuppath)

if not os.path.isdir(backuppath):
    debug('%s is not a dir' %backuppath)
    win.msgbox('!!!目录 %s 不存在，请重新设置' %backuppath)
    win.execute('config.ini')
    os._exit(0)
    
    
dbpasswd=ini.getdbpassword()
debug('database pw is  %s'%dbpasswd)
times=ini.gettimes()
daystr=time.strftime('%y%m%d')

status=[]
for i in times:
    info('backup time %s: %s'%(i[0],i[1]))
    status.append(0)

if dbtest(dbpasswd)==0:
    win.msgbox('!!!!数据库无法连接\n请检查数库是否启动，密码是否正确')
    win.execute('config.ini')
    os._exit(0)   

while 1:
    if daystr != time.strftime('%y%m%d'):
        daystr = time.strftime('%y%m%d')
        info('date changed %s' %daystr)
        for i in xrange(0,len(status)):
            status[i]=0
    a=0
    for i in times:
        if i[1]==time.strftime('%H:%M') and status[a]==0:
            info('backup %s start'%i[0])
            bkfilepathstr=bkfilepath(backuppath)
            info('bkfilepathstr is %s'%bkfilepathstr)
            backup(backupcmdstr(bkfilepathstr,dbpasswd))
            status[a]=1
            info('zip start')
            try:
                zipf.filezip(bkfilepathstr)
            except:
                info('zip failed')
            info('zip success')
            info('delete bkfile start')
            try:
                os.remove(bkfilepathstr)
            except:
                info('delete failed')
            info('delete success') 
            info('backup %s  end' %i[0])
        a+=1
        
    time.sleep(20)
   

        
        
        


