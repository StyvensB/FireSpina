
import glob
import sys
import os
import string


(baseP,extP)=os.path.splitext(sys.argv[1])
baseN=os.path.basename(baseP)
print baseP+"_title.csv",baseP+"_chapter"

if not os.path.exists(baseP+"_chapter"):
	print "chapters not found"
	sys.exit(1)

if not os.path.exists(baseP+"_title.csv"):
	print "title File not found"
	sys.exit(1)

titleIn=open(baseP+"_title.csv",'r')

for line in titleIn: 
	index,title = line.rstrip('\n').split(',',1)
	title=title.translate(string.maketrans("\/?*%","__---"))
	
	res=glob.glob(os.path.join(baseP+"_chapter",index+"*") )
	if not res:
		continue
	src=res[0]
	(dstB,dstX)=os.path.splitext(src)
	dst =os.path.join(baseP+"_chapter",index)+"_"+title+dstX 
	print src,"->",dst
	try:
		os.rename(src,dst)
	except WindowsError as detail:
		print detail

titleIn.close()
sys.exit()

