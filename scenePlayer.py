#!/usr/bin/env python

import cv2

keys='''
	s - Save modification
	n - Next Segment
	p - Previous  Segment
	r - Return to segment start
	u - Update Segment start
	d - Delete Segment
	a - Add Segment
	1,4,7 - Move 1,10,100 frame backward
	3,6,9 - Move 1,10,100 frame forward
	Esc - Quit
'''


if __name__ == '__main__':
	import sys
	import os
	import argparse


	parser = argparse.ArgumentParser(description='Allow User to review cut point')
	parser.add_argument('path',help="path of the video file")
	parser.add_argument('-f','--frame',dest="frame",default="",help="path of the cut frame original file")
	

	args=parser.parse_args()	
	
	if  not os.path.isfile(args.path):
		print "scenePlayer.py videofile"
		sys.exit(1)
		
	(baseP,extP)=os.path.splitext(args.path)
	
	if not os.path.isfile(args.frame):
		args.frame=baseP+"_frame.csv"
	if  os.path.isfile(args.frame):
		frameIn=open(args.frame,'r')
		frameList=map(int,frameIn.readlines())
		frameIn.close()
	else:
		frameList=[0]
	
	
	
	cap = cv2.VideoCapture(args.path)
	if not cap.isOpened():
		print "Can't open file "+ args.path
		sys.exit(1)
	
	print keys	
	i=0
	FrameNB=frameList[i]
	cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES,FrameNB)
	totalFrame=cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT )
	ret, img = cap.read()
	h,w=img.shape[:2]
	saveIndex=0
	font = cv2.FONT_HERSHEY_SIMPLEX
	while True:
		text="Scene: %3d\nFrame: %6d\nDelta %5d" % (i,FrameNB,FrameNB-frameList[i])
		cv2.putText(img,text,(10,h-10), font, .6,(255,255,255),2)#cv2.cv.LINE_AA)
		cv2.imshow('frame', img)
		
		ch = 0xFF & cv2.waitKey(5)
		if ch == 27:
			break
		elif ch == ord('n'):
			i=(i+1)%len(frameList)
			FrameNB=frameList[i]
			print "\r"+'Next chapter'
		elif ch == ord('p'):
			i=(i-1)%len(frameList)
			FrameNB=frameList[i]
			print "\r"+'Previous chapter'
		elif ch == ord('r'):
			FrameNB=frameList[i]
			print 'Reset'
		elif ch == ord('u'):
			frameList[i]=FrameNB
			print "\r"+'Update'
		elif ch == ord('d'):
			del frameList[i]
			i=(i-1)%len(frameList)
			#FrameNB=frameList[i]
			print "\r"+'Delete'	
		elif ch == ord('a'):
			frameList.append(FrameNB)
			frameList.sort()
			i=frameList.index(FrameNB)
			print "\r"+'Add'
		elif ch == ord('s'):
			(baseB,extB)=os.path.splitext(args.frame)
			if args.frame:
				os.rename(args.frame,baseB+"_%3d"%saveIndex+extB)
			saveIndex=+1
			frameBackUp=open(baseP+"_frame.csv",'w')
			frameBackUp.writelines(map(lambda x:str(x)+"\n",frameList))
			frameBackUp.close()
			print "\r"+'Save'	
		elif ch == ord('1'):
			FrameNB+=-1
		elif ch == ord('3'):
			FrameNB+=1
		elif ch == ord('4'):
			FrameNB+=-10
		elif ch == ord('6'):
			FrameNB+=10
		elif ch == ord('7'):
			FrameNB+=-100
		elif ch == ord('9'):
			FrameNB+=100
		elif not ch==-1&0xFF:
			print ch
		if not ch==-1&0xFF:
			if FrameNB<totalFrame:
				cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES,FrameNB)
				ret, img = cap.read()
			else:
				FrameNB=totalFrame
	cv2.destroyAllWindows()
