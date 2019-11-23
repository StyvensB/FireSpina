#!/usr/bin/env python

import os , sys
import subprocess
#import schlex
import os
import argparse

parser = argparse.ArgumentParser(description='Read scene Title')
parser.add_argument('path',help="path of the video file")
parser.add_argument('-d','--delay',type=int,dest="delay",default=0,help="delay to wait for title in frame")
args=parser.parse_args()

videoPath=args.path
if not os.path.exists(videoPath):
	print "cut.py videofile"
	sys.exit(1)
	
(baseP,extP)=os.path.splitext(videoPath)
baseN=os.path.basename(baseP)


if not os.path.exists(baseP+"_chapter"):
	os.mkdir(baseP+"_chapter")


if not os.path.exists(baseP+"_frame.csv"):
	print "frame File not found"
	sys.exit(1)

frameIn=open(baseP+"_frame.csv",'r')
framelist=frameIn.readlines()
frameIn.close()

## Adjust to keyFrames
#if os.path.exists(baseP+"_key.csv"):
#	keyIn=open(baseP+"_key.csv",'r')
#	keylist=keyIn.readlines()
#	keyIn.close()
#	
#	cutsIntList = map(int,framelist)
#	keysIntList = map(int,keylist)
#	
#	i=0
#	p=keysIntList[0]
#	res=[]
#	for cut in cutsIntList:
#		while i< len(keysIntList) and cut > keysIntList[i] :
#			p=keysIntList[i]
#			i=i+1
#		res.append(p)
#		print cut,"->", p
#	
#	framelist=map(str,res)

if int(framelist[0])==0:
	del framelist[0]
framelist=map(lambda(x):str(int(x)+args.delay),framelist)
frameArgs=','.join(framelist[0:]).replace("\n",'')

print frameArgs
#args=['ffmpeg','-v','warning','-i',videoPath,'-map','0','-v:copy -f','segment','-segment_frames','"'+frameArgs+'"','"'+baseP+'_chapter\\%02d.mp4"']
cmdline='ffmpeg -v warning  -i "'+videoPath +'" -c:s mov_text -map 0  -reset_timestamps 1 -f segment  -segment_frames "'+frameArgs+'" -segment_list_type csv -segment_list "'+baseP+"_video.csv"+'" "'+  baseP+'_chapter\%02d.mp4"'
print cmdline
try:
	subprocess.call(cmdline,stdout=sys.stdout,stderr=subprocess.STDOUT,shell=True)
except subprocess.CalledProcessError as e:
	print "command:\n"+str(e.cmd)+"\n"
	print "output: \n"+e.output+"\n"
	


