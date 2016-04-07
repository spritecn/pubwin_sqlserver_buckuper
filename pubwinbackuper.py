#coding:utf8
#the scripts for pubwin backup 
#it can be backup every day 

import os
import time
from  logging import *
import win
import ini
import zipf
import ftp
import clean


#设置log
loglevel=DEBUG
basicConfig(level=loglevel,
                format='%(asctime)s %(levelname)s  %(funcName)s:%(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                filename='pubwinbackup.log',
                filemode='a')
                
def dbtest(dbpasswd):
    #检查数据库是否可以登录
    cmd="osql -U netcafe -P "+dbpasswd+" -Q "+"\""+\
        ""+"\""
    popenstr=os.popen(cmd)
    popenstrreadlines=popenstr.readlines()
    if len(popenstrreadlines)==0:return 1
    return popenstrreadlines
    
def bkfilepath(backuppath):
    return backuppath+'\\db'+time.strftime('%Y%m%d_%H%M%S')+'.dbk'
    
def backupcmdstr(bkfilepath,dbpasswd):
    sqlstr="BACKUP DATABASE LOCAL TO DISK='%s'" %(bkfilepath) 
    osqlstr='osql -U netcafe -P %s -d master -Q "%s"'%(dbpasswd,sqlstr)
    debug('osqlstr %s'%(osqlstr))
    return osqlstr

def backup(osqlstr):
    #成功返回使用时间，失败返回0
    starttime=time.time()
    popenstr=os.popen(osqlstr)
    popenstrreadlines=popenstr.readlines()
    usetime=time.time()-starttime
    for i in popenstrreadlines:debug(i)
    if len(popenstrreadlines)==3:
        info('backup success usetime:%ss'%(usetime))
        info('backup end')
        return usetime
    info('backup failed')
    return 0
   
#主程序开始
                
#程序运行参数
info('----------------------------------------------------')
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
ftpsign=0

if ini.getftpbackup()=='on':
    ftpsign=1
    ftpdict=ini.getftp()
    info('ftp sign on,start ftptest')
    ftptest=ftp.ftptest(ftpdict['ftpserver'],ftpdict['ftpport'],ftpdict['ftpuser'],ftpdict['ftppassword'])
    if ftptest!=1:
        info('ftp test:config error')
        debug(ftptest)
        #win.msgbox('ftp 设置错误，请重新设置')
        ftpsign=0
    info('ftp test success')
localdays,ftpdays=ini.getsavedays()        
            
status=[]
for i in times:
    info('backup time %s: %s'%(i[0],i[1]))
    status.append(0)

a=dbtest(dbpasswd)
if a!=1:
    for i in a:debug(i)
    win.msgbox('!!!!数据库无法连接\n请检查数库是否启动，密码是否正确')
    win.execute('config.ini')
    os._exit(0)   

while 1:
    if daystr != time.strftime('%y%m%d'):
        daystr = time.strftime('%y%m%d')
        info('------------date changed %s---------------' %daystr)
        for i in xrange(0,len(status)):
            status[i]=0
        info('clean backup file start')
        info('local backup file clean start')
        localcleanfilelist=clean.cleanlocalbkfile(localdays,backuppath)
        if localcleanfilelist:
            for i in localcleanfilelist:info(i)
        info('local backup file clean end')
        if ftpsign==1:
            info('ftp backup file clean start')
            ftpcleanfilelist=clean.cleanftpbkfile(ftpdict['ftpserver'],ftpdict['ftpport'],ftpdict['ftpuser'],ftpdict['ftppassword'],ftpdict['ftppath'],ftpdays)
            if ftpcleanfilelist:
                for i in ftpcleanfilelist:info(i)
            info('ftp backup file clean end')
        info('clean backup file end')
                
    a=0
    for i in times:
        if i[1]==time.strftime('%H:%M') and status[a]==0:
            info('backup %s start'%i[0])
            bkfilepathstr=bkfilepath(backuppath)
            info('bkfilepathstr is %s'%bkfilepathstr)
            if not backup(backupcmdstr(bkfilepathstr,dbpasswd)):continue    
            status[a]=1
            info('zip start')
            try:
                zippath=zipf.filezip(bkfilepathstr)
            except:
                info('zip failed')
                continue
            info('zip success')
            info('delete bkfile start')
            try:
                os.remove(bkfilepathstr)
            except:
                info('delete %s failed'%bkfilepathstr)
                continue
            info('delete %s success'%bkfilepathstr) 
            if ftpsign==1:
                info('ftp update start')
                starttime=time.time()
                ftpupdate=ftp.ftpupload(ftpdict['ftpserver'],ftpdict['ftpport'],ftpdict['ftpuser'],ftpdict['ftppassword'],ftpdict['ftppath'],zippath)
                
                if ftpupdate!=1:
                    info('ftp update failed')
                    debug(ftpupdate)
                    info('backup %s end'%i[0]) 
                    continue
                usetime=int(time.time()-starttime)
                info('ftp update success use time %ss'%usetime)
                 
            info('backup %s end'%i[0])       
        a+=1
        
    time.sleep(20)
   

        
        
        


