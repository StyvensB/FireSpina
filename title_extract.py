#!/usr/bin/env python

import os , sys
import subprocess
#import schlex
import re
import argparse

parser = argparse.ArgumentParser(description='Read scene Title')
parser.add_argument('path',help="path of the video file")
parser.add_argument('-d','--delay',type=int,dest="delay",default=0,help="delay to wait for title in frame")
parser.add_argument('--clip',dest="clip",type=int,nargs=4,help="coordinates of the left,top,right,bottom corner of the rectangle to clip")
args=parser.parse_args()

videoPath=args.path
if not os.path.exists(videoPath):
	print "cut.py videofile"
	sys.exit(1)

if args.clip is not None:
	cropStr= ",crop=%d:%d:%d:%d" % (args.clip[2]-args.clip[0],args.clip[3]-args.clip[1],args.clip[0],args.clip[1])
else:
	cropStr=""

(baseP,extP)=os.path.splitext(videoPath)
baseN=os.path.basename(baseP)

titlePath=baseP+"_title"
if not os.path.exists(titlePath):
	os.mkdir(titlePath)


if not os.path.exists(baseP+"_frame.csv"):
	print "frame File not found"
	sys.exit(1)

#
# GET THE FPS
#
cmdline='ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of default=noprint_wrappers=1:nokey=0 "'+ videoPath+'"'
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

#
# GET THE CUTTING FRAME
#

frameIn=open(baseP+"_frame.csv",'r')
framelist=map(int,frameIn.readlines())
frameIn.close()

#
# CREATE IMAGE
#
if framelist[0]==0:
	i=0
else:
	i=1
framelist=map(lambda x:x+args.delay,framelist)
for cut in framelist:
	cutArg= "%f" % (cut/fps)
	print cutArg
	cmdline='ffmpeg -v warning -y -ss '+cutArg+' -i "'+videoPath +'" -vframes 1 "'+os.path.join(titlePath,"%02d.jpg"%(i))+'"'
	print cmdline
	try:
		subprocess.call(cmdline,stdout=sys.stdout,stderr=sys.stderr,shell=True)
	except subprocess.CalledProcessError as e:
		print "command:\n"+str(e.cmd)+"\n"
		print "output: \n"+e.output+"\n"
	i+=1


