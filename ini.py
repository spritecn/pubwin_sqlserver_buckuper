#coding:gbk

# read config file config.ini

from ConfigParser import ConfigParser

config=ConfigParser()
config.read('config.ini')

def getdbpassword():
    return config.get('default','dbpassword')
    
def getbackuppath():
    return config.get('default','path')

def getftpbackup():
        return config.get('default','ftpbackup')
def gettimes():
    return config.items('times')
 
def getftp():
    ftplist=config.items('ftp')
    ftpdict=dict(ftplist)
    return ftpdict
    
def getsavedays():
    savedays=[]
    try:
        savedays.append(int(config.get('default','localfilesavedays'))+1)
    except:
        savedays.append(31)
    try:
        savedays.append(int(config.get('default','ftpfilesavedays'))+1)
    except:
        savedays.append(31)
    return savedays
        
    
     
if __name__ == '__main__':
    import os
    print getftp()
    print getsavedays()
    os.system('pause')
    