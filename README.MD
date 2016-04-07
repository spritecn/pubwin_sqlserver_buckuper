pubwin数据库备份工具
＝＝＝＝＝＝＝＝＝＝＝＝＝
使用方法：
1.更改配置文件config.ini
```
    [default]
    dbpassword=333aaab.1
    path=e:\backup\
    localfilesavedays=1
    ftpfilesavedays=1
    ftpbackup=on

    [times]
    time1=05:40
    time2=05:50

    [ftp]
    ftpserver=10.30.30.56
    ftpport=21
    ftpuser=
    ftppassword=admin
    ftppath=backup
```

    字段说明：
    ;dbpassword 数据库密码程序整体备份需要此密码

    ;bkmode  设置备份模式,当bkmode=pubwin时使用pubwin自动备份，设置为其他值均为程序整体备份

    ;pubwinbkpath pubwin自动备份文件的路径，如果pubwin默认目录的话程序会自动识别，如果有更改过，需要在此处设置

    ;localfilesavedays 本地备份保存时间，以天为单位

    ;ftpfilesavedays   ftp备份保存时间，以天为单位

    ;path:本地备份备份目录

    ;程序不会新建目录，请确保指定的目录已经存在

    ;ftpbackup=on  这个是ftp开关，on表示启用ftp备份,其他表示不启用

    ;[times]备份时间,格式按上面的写,一天可以备份一次或多次,

    ;备份多次后面加一行就可以了,但是等号前面的key不能重复 

    ;如果是使用pubwin自动备份备份的话，建议每天23:00左右备份一次就可以了

    ;[ftp]ftp相关设置

    ;ftpserver ftp服务器ip

    ;ftpport ftp端口一般为21

    ;ftpuser ftp登录用户名，为空时可匿名登录

    ;ftppassword ftp登录密码

    ;ftppath ftp子目录，如果有一个ftp想多个网吧都备份到这个ftp下可以使用子目录区别

2.运行pubwinbackuper.py,可以放入开机启动项
```
    python pubwinbackuper.py
```
3.pubwinbackrestore.py是用来恢复已经下载解压好的数据库备份，支持差异备份

4.如果您没有安装python环境，可以去我的博客下载打包好的exe版本
http://www.fantansy.cn/index.php/pubwinBackuper.html