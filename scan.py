import cv2
import sys
import os
import argparse

parser = argparse.ArgumentParser(description='Detect transition between chapter in a videofile')
parser.add_argument('path',help="path of the video file")
parser.add_argument('-r','--reference',required=True,type=int,dest="reference",help="rank of the reference frame to compare to transition")
parser.add_argument('-s','--skip',dest="skip",type=int,default=30,help="number of frame to skip between comparison")
parser.add_argument('-t','--threshold',type=float,dest="threshold",default=0.6,help="value of the minimum correlation coefficient to trigger a detection [0..1] (0.6)")
parser.add_argument('-b','--back',dest="back",type=int,default=0,help="number of frame to back track when match is found")
parser.add_argument('--clip',dest="clip",type=int,nargs=4,help="coordinates of the left,top,right,bottom corner of the rectangle to clip")
args=parser.parse_args()

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
	
def modify(x):
	a=x
	for f in modifier:
		a=f(a)
	return a

totalFrame=cap.get(7)	
backTrack=args.back
step=args.skip
cap.set(1,args.reference)# 1 for CV_CAP_PROP_POS_FRAMES
ret,img = cap.read()
img=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img=modify(img)

cap.set(2,0)
flag=False

(baseP,extP)=os.path.splitext(args.path)
frOut=open(baseP+"_frame.csv",'w')
tOut=open(baseP+"_time.txt",'w')
threshold=args.threshold

while(cap.get(1) < totalFrame):
	ret,frame= cap.read()
	frameG = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	frameG= modify(frameG)
	rmatch=cv2.matchTemplate(frameG,img,cv2.TM_CCOEFF_NORMED)
	frameNB = cap.get(1)
	if rmatch[0,0] >= threshold and  flag == False:
		frameStop=frameNB
		#cv2.imwrite(baseP+"%07d.jpg" % frameNB,frameG)
		#print baseP+"\\%d.jpg" % frameNB
		substep=int(step/2)
		frNB=frameNB-substep
		#print "tmp:%d good:%d "% (frNB,frameNB)
		if step< frameNB:
			while substep >0 :
				cap.set(1,frNB)
			   	ret,frame= cap.read()
				frameG = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
				frameG = modify(frameG)
				rmatch1=cv2.matchTemplate(frameG,img,cv2.TM_CCOEFF_NORMED)
				substep=int(substep/2)
				if rmatch1[0,0] >= threshold:
				  frameNB=frNB
				  frNB=frNB-substep
				else:
				  frNB=frNB+substep
				#print "tmp:%d good:%d "% (frNB,frameNB)
		frameNB=frameNB-backTrack
		frOut.write("%05d\n" % frameNB)
		cap.set(1,frameNB)
		t = cap.get(0)/1000
		m, s = divmod(t, 60)
		h, m = divmod(m, 60)
		tOut.write("%d:%02d:%04.2f," % (h, m, s))#, frameNB,rmatch[0,0], t
		sys.stderr.write("%04.1f %% %d:%02d:%04.2f \n" % (cap.get(2)*100,h, m, s))
		flag= True
		cap.set(1,frameStop)
	elif flag == True and rmatch[0,0] < 0.5:
		flag = False
	a=cap.set(1,cap.get(1)+step);

frOut.close()
tOut.close()
cap.release()
sys.exit()
# cv2.namedWindow("image", cv2.WINDOW_AUTOSIZE);
# cv2.imshow("image", img);
# waitKey();