# coding:gb2312
import os
print '-------------------------------------------------'
print '----sqlserver���ݻָ����ߣ�֧�ֲ��챸�ݻָ�------'
print '----------------------------------by sprite------'
print 
print 
dbusername=raw_input('���������ݿ��¼�û���(pubwin������netcafe):')
dbpassword=raw_input('���������ݿ��¼���룺')
dbname=raw_input('������Ҫ�ָ������ݿ�����(pubwin������local):')
backupFile=raw_input('�����뱸���ļ�·��(ֱ�����봰�ڼ���)��')
backupFile=backupFile.replace('"','')
if not os.path.isfile(backupFile):
	print '�ļ�������'
	exit(0)
cmdStr='osql -U '+dbusername+' -P '+dbpassword +' -h-1 -Q "RESTORE HEADERONLY FROM DISK=N'+"'"+backupFile+"'"
filehead=os.popen(cmdStr)
templist=filehead.read().split('Chinese_PRC_CI_AS')
if len(templist)<2:
	print '���ݿ����Ӵ���򱸷��ļ�����'
	exit(0)
diffbackuplist=list()
if  len(templist)<3:
	print 'The bakupfile is Just have only one postion,restore start'
	cmd='osql -U '+dbusername+' -P '+dbpassword +' -Q '+'"RESTORE DATABASE '+dbname+' FROM DISK=N'+"'"+backupFile+"'"
	os.system(cmd)
	print '�ָ���ɣ�����������б��������»ָ�'
	exit(0)
else:
	for i in templist:
		l=i.split()
		if len(l)>2:
			tl=(l[5],l[9],l[18],l[19])
			diffbackuplist.append(tl)
	for i in diffbackuplist:
		print "���ݱ��:%2s������������:%s��������ʱ��:%s"%(i[0],i[2],i[3])

	postionstr=raw_input('����Ҫ�ָ��ı��ݱ��:')
	if int(postionstr)>len(diffbackuplist) or int(postionstr)<1:
		print 'wrong postion'
		exit(0)
	if postionstr=='1':
		cmd='osql -U '+dbusername+' -P '+dbpassword +' -Q '+'"RESTORE DATABASE '+dbname+' FROM DISK=N'+"'"+backupFile+"'"
		print '***************restor start*********************'
		os.system(cmd)
		print '�ָ���ɣ�����������б��������»ָ�'
	else:
		cmd1='osql -U '+dbusername+' -P '+dbpassword +' -Q '+'"RESTORE DATABASE '+dbname+' FROM DISK=N'+"'"+backupFile+"'"+' WITH NORECOVERY'
		cmd2='osql -U '+dbusername+' -P '+dbpassword +' -Q '+'"RESTORE DATABASE '+dbname+' FROM DISK=N'+"'"+backupFile+"'"+' WITH FILE='+postionstr+',RECOVERY'
		print '***************restor start*********************'
		os.system(cmd1)
		os.system(cmd2)
		print '�ָ���ɣ�����������б��������»ָ�'