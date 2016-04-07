#coding:utf8
#pubwinbacker_py2exe.py

from distutils.core import setup
import glob
import sys
import py2exe

sys.argv.append('py2exe')
 
setup(version='0.1',
description='pubwin Backuper',
name='pubwin Backuper',
zipfile=None,
options = {"py2exe": {"compressed": 1,"optimize": 1,"ascii": 0,"bundle_files": 3}},
windows=[{"script":"pubwinbackuper.py", "icon_resources": [(0, "0.ico")]}])