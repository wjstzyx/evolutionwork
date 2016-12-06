import os
import re
import shutil
firstdir=r'C:\Users\YuYang\Desktop\aflfile'
seconddir=r'C:\Users\YuYang\Desktop\afl_long'
files=os.listdir(firstdir)
for item in files:
	reaffile=open(firstdir+"\\"+item,'r')
	temp=reaffile.read()
	pattern=r'StrategyName = "(30min-rb-wf 30_10 getCCIreversal19)";'
	aa=re.search(pattern,temp)
	reaffile.close()
	if aa:
		print item
		scr=firstdir+"\\"+item
		dst=seconddir+"\\"+item
		shutil.move(scr,dst)
		# exit()

#shutil.move(r'C:\Users\YuYang\Desktop\aflfile\a-5min-1013000012.afl',r'C:\Users\YuYang\Desktop\afl_long\a-5min-1013000012.afl')


