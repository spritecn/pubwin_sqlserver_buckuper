# coding:gb2312
import os
print '-------------------------------------------------'
print '----sqlserver备份恢复工具，支持差异备份恢复------'
print '----------------------------------by sprite------'
print 
print 
dbusername=raw_input('请输入数据库登录用户名(pubwin请输入netcafe):')
dbpassword=raw_input('请输入数据库登录密码：')
dbname=raw_input('请输入要恢复的数据库名称(pubwin请输入local):')
backupFile=raw_input('请输入备份文件路径(直接拖入窗口即可)：')
backupFile=backupFile.replace('"','')
if not os.path.isfile(backupFile):
	print '文件不存在'
	exit(0)
cmdStr='osql -U '+dbusername+' -P '+dbpassword +' -h-1 -Q "RESTORE HEADERONLY FROM DISK=N'+"'"+backupFile+"'"
filehead=os.popen(cmdStr)
templist=filehead.read().split('Chinese_PRC_CI_AS')
if len(templist)<2:
	print '数据库连接错误或备份文件错误'
	exit(0)
diffbackuplist=list()
if  len(templist)<3:
	print 'The bakupfile is Just have only one postion,restore start'
	cmd='osql -U '+dbusername+' -P '+dbpassword +' -Q '+'"RESTORE DATABASE '+dbname+' FROM DISK=N'+"'"+backupFile+"'"
	os.system(cmd)
	print '恢复完成，如果过程中有报错，请重新恢复'
	exit(0)
else:
	for i in templist:
		l=i.split()
		if len(l)>2:
			tl=(l[5],l[9],l[18],l[19])
			diffbackuplist.append(tl)
	for i in diffbackuplist:
		print "备份编号:%2s　　备份日期:%s　　备份时间:%s"%(i[0],i[2],i[3])

	postionstr=raw_input('请需要恢复的备份编号:')
	if int(postionstr)>len(diffbackuplist) or int(postionstr)<1:
		print 'wrong postion'
		exit(0)
	if postionstr=='1':
		cmd='osql -U '+dbusername+' -P '+dbpassword +' -Q '+'"RESTORE DATABASE '+dbname+' FROM DISK=N'+"'"+backupFile+"'"
		print '***************restor start*********************'
		os.system(cmd)
		print '恢复完成，如果过程中有报错，请重新恢复'
	else:
		cmd1='osql -U '+dbusername+' -P '+dbpassword +' -Q '+'"RESTORE DATABASE '+dbname+' FROM DISK=N'+"'"+backupFile+"'"+' WITH NORECOVERY'
		cmd2='osql -U '+dbusername+' -P '+dbpassword +' -Q '+'"RESTORE DATABASE '+dbname+' FROM DISK=N'+"'"+backupFile+"'"+' WITH FILE='+postionstr+',RECOVERY'
		print '***************restor start*********************'
		os.system(cmd1)
		os.system(cmd2)
		print '恢复完成，如果过程中有报错，请重新恢复'