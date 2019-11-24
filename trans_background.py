#!/usr/bin/env python

import re
import subprocess
import sys
import os
import argparse


parser = argparse.ArgumentParser(description='Detect scene Change in the video')
parser.add_argument('path',help="path of the video file")
parser.add_argument('background',help="path of the background file")
parser.add_argument('-d','--duration',type=float,dest="duration",default=1,help="min black scene duration")
parser.add_argument('-t','--threshold',dest="threshold",type=float,default=.10,help="Ratio of black pixel sufficient to consider the frame black")
parser.add_argument('-x','--simulate',dest="simulate",action="store_true",help="simulate by displaying result of the video")
parser.add_argument('--merge',dest="merge",type=int,default=200,help="Min distance between two black transition")
parser.add_argument('--clip',dest="clip",type=int,nargs=4,help="coordinates of the left,top,right,bottom corner of the rectangle to clip")
args=parser.parse_args()

if not os.path.isfile(args.path):
	print "black.py videofile"
	sys.exit(1)

if args.clip is not None:
	cropStr= ",crop=%d:%d:%d:%d" % (args.clip[2]-args.clip[0],args.clip[3]-args.clip[1],args.clip[0],args.clip[1])
else:
	cropStr=""

(baseP,extP)=os.path.splitext(args.path)


import pipes
if args.simulate:
	print "Simulate"
	cmdline='ffplay -hide_banner -f lavfi "movie='+pipes.quote(args.path)+cropStr+'[org];movie='+ pipes.quote(args.background)+cropStr+"[title];[title] fifo [vid];[org][vid]blend=all_mode=difference[mix];[mix]blackdetect=d=%3.f"%args.duration+":pix_th=%.2f"%args.threshold+':pic_th=0.99" '
	print cmdline
	try:
		p=subprocess.Popen(cmdline,stdout=sys.stdout,stderr=sys.stderr,shell=True)	
	except subprocess.CalledProcessError as e:
		print "command:\n"+str(e.cmd)+"\n"
		print "output: \n"+e.output+"\n"
	sys.exit(1)


cmdline='ffprobe -hide_banner -f lavfi "movie='+pipes.quote(args.path)+cropStr+'[org];movie='+ pipes.quote(args.background)+cropStr+"[title];[title] fifo [vid];[org][vid]blend=all_mode=subtract[mix];[mix]blackdetect=d=%3.f"%args.duration+":pix_th=%.2f"%args.threshold+':pic_th=0.99,select=gt(pts-prev_selected_pts\,1)" '
print cmdline
try:
	p=subprocess.Popen(cmdline,stdout=sys.stdout,stderr=subprocess.PIPE,shell=True)	
except subprocess.CalledProcessError as e:
	print "command:\n"+str(e.cmd)+"\n"
	print "output: \n"+e.output+"\n"




debugOut=open(baseP+'_dump.txt','w')
reTime=re.compile(r'black_start:(\d+.?\d*)')

secList=[]

for line in p.stderr:
	res=reTime.search(line)
	if res :
		print res.group(0)
		secList.append(float(res.group(1)))
		debugOut.write(line)
	else:
		sys.stderr.write(line)

cmdline='ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of default=noprint_wrappers=1:nokey=0 "'+ args.path+'"'
print cmdline
try:
	p=subprocess.Popen(cmdline,stdout=subprocess.PIPE,stderr=sys.stderr,shell=True)	
except subprocess.CalledProcessError as e:
	print "command:\n"+str(e.cmd)+"\n"
	print "output: \n"+e.output+"\n"

reFPS=re.compile(r'r_frame_rate=(\d+)\/(\d+)')
res=reFPS.match(p.stdout.read()	)
print res.group(0)
fps=float(res.group(1))/float(res.group(2))

def acc(y,x):
	y.append((x,x-y[-1][0]))
	return y

secList=map(lambda x:int(x*fps),secList)
tempList=reduce(acc,secList,[(secList[0]-args.merge-1,0)])
print tempList
tempFile=open(baseP+"_breaks.txt","w")
tempFile.write(str(tempList))
tempFile.close()
tempList=filter(lambda x: x[1]>args.merge,tempList)

secList=map(lambda x:x[0],tempList)

sceneList=map(lambda x:"%d\n"%int(x),secList)
frameOut=open(baseP+"_frame.csv",'w')
frameOut.writelines(sceneList)
frameOut.close()
debugOut.close()