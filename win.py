#coding:utf8
import ctypes
#win api shellexecuteapiA and msgboxA

def execute(path):
    handler = None
    operator = "open"
    fpath = path
    param = None
    dirpath = None
    ncmd = 1
    shell32 = ctypes.windll.LoadLibrary("shell32.dll")
    shell32.ShellExecuteA(handler,operator,fpath,param,dirpath,ncmd)

def msgbox(msg='mesage'):
    user32 = ctypes.windll.LoadLibrary('user32.dll')
    user32.MessageBoxA(0, msg.decode('utf8').encode('gbk'), 'pubwinbackup',0)
    
if __name__ == '__main__':
        execute('config.ini')
        msgbox()