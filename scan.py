import cv2

def modify(x):
	a=x
	for f in modifier:
		a=f(a)
	return a

def checkOneChannel(imgTest):
	if len(imgTest.shape) == 3 :
		imgTest=cv2.cvtColor(imgTest, cv2.COLOR_BGR2GRAY)
	elif len(imgTest.shape) == 2:
		pass
	else:
		raise TypeErrror("imgTest as wrong dimension"+imgTest.shape)
	return imgTest
	
def corrMeasure(imgA,imgB):
	imgA=checkOneChannel(imgA)
	imgB=checkOneChannel(imgB)
	rmatch=cv2.matchTemplate(imgA,imgB,cv2.TM_CCOEFF_NORMED)
	return rmatch[0,0] >= threshold

def euclMeasure(imgA,imgB):
	imgA=checkOneChannel(imgA)
	imgB=checkOneChannel(imgB)
	rmatch=cv2.matchTemplate(imgA,imgB,cv2.TM_SQDIFF)
	#print rmatch[0,0],threshold
	return rmatch[0,0] <= threshold
	
def findExtremity(frGood,frBad):
	step=(frGood-frBad)/2
	frTemp=frGood-step
	frLim=frGood
	while(step>=1):
		cap.set(1,frTemp)
		ret,frameT= cap.read()
		frameT = modify(frameT)
		if measure(frameT,img):
			frLim=frTemp
			frTemp=frTemp-step
		else:
			frTemp=frTemp+step
		step=step/2
		#print "tmp:%d good:%d "% (frTemp,frLim)
	return frLim
	
def formatMili(t):
	m, s = divmod(t, 60)
	h, m = divmod(m, 60)
	return (h, m, s)

if __name__ == '__main__':
	import sys
	import os
	import argparse
	import json 

	parser = argparse.ArgumentParser(description='Detect transition between chapter in a videofile')
	parser.add_argument('path',help="path of the video file")
	parser.add_argument('-r','--reference',required=True,type=int,dest="reference",help="rank of the reference frame to compare to transition")
	parser.add_argument('-s','--skip',dest="skip",type=int,default=30,help="number of frame to skip between comparison")
	parser.add_argument('-t','--threshold',type=float,dest="threshold",default=0.6,help="value of the minimum correlation coefficient to trigger a detection [0..1] (0.6)")
	parser.add_argument('-b','--back',dest="back",type=int,default=0,help="number of frame to back track when match is found")
	parser.add_argument('-m','--method',dest="measure",choices=['correlation','euclidian'],default='correlation',help="Measure to compare reference and sample")
	parser.add_argument('--clip',dest="clip",type=int,nargs=4,help="coordinates of the left,top,right,bottom corner of the rectangle to clip")
	args=parser.parse_args()
	
	#Save Parameter
	(baseP,extP)=os.path.splitext(args.path)
	argsOut=open(baseP+"_conf.json",'w')
	argsJson=json.dumps(vars(args), sort_keys=True,indent=4, separators=(',', ': '))
	argsOut.write(argsJson)
	argsOut.close()
	
	if not os.path.exists(args.path):
		print "Can't find file "+ args.path
		sys.exit(1)
	try:	
		cap = cv2.VideoCapture(args.path)
	except:
		print "Video Format not supported"
		
	if not cap.isOpened():
		print "Can't open file "+ args.path
		sys.exit(1)

	modifier=[]
	#modifier.append(lambda x:cv2.bitwise_not(x) )
	if args.clip is not None :
		modifier.append(lambda x:x[args.clip[1]:args.clip[3],args.clip[0]:args.clip[2]] )
	if args.measure =="correlation" :
		measure=corrMeasure
	elif args.measure =="euclidian":
		measure=euclMeasure
	



	totalFrame=cap.get(7)	
	backTrack=args.back
	step=args.skip
	threshold=args.threshold
	cap.set(1,args.reference)# 1 for CV_CAP_PROP_POS_FRAMES
	ret,img = cap.read()
	img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	img=modify(img)



	## LOOP Initialisation
	cap.set(2,0)
	flag=False
	rank=0
	selFrame=[]
	frameSpan=range(1,int(totalFrame),step)
	

	for frameNB in frameSpan:
		cap.set(1,frameNB)
		ret,frame= cap.read()
		frameG= modify(frame)
		cond=measure(frameG,img)
		#print frameNB,cond
		if cond and  flag == False:
			if frameNB > step:
				frameStop=findExtremity(frameNB,frameNB-step)
			else:
				frameStop=frameNB
			selFrame.append(frameStop)
			flag= True
			rank=rank+1
			sys.stderr.write("%04.1f %%"% (cap.get(2)*100)+" %d:%02d:%04.2f \n" % formatMili(cap.get(0)/1000))
			#cap.set(1,frameNB)
		elif flag == True and not cond:
			flag = False
		#a=cap.set(1,cap.get(1)+step);

	## File Opening
	(baseP,extP)=os.path.splitext(args.path)
	frOut=open(baseP+"_frame.csv",'w')
	tOut=open(baseP+"_time.txt",'w')
	transImgOutP=baseP+"_intro"
	if not os.path.exists(transImgOutP):
		os.mkdir(transImgOutP)
	##Output Data
	for frIdx in selFrame:
		cap.set(1,frIdx)
		#cv2.imwrite(os.path.join(transImgOutP,"%02d.jpg" % rank),frameG)
		frOut.write("%05d\n" % frIdx)
		t = cap.get(0)/1000
		tOut.write("%d:%02d:%04.2f," % formatMili(t))
	##File Closing
	frOut.close()
	tOut.close()
	cap.release()
	sys.exit()
	# cv2.namedWindow("image", cv2.WINDOW_AUTOSIZE);
	# cv2.imshow("image", img);
	# waitKey();