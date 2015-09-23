# python "C:\Users\Styvens\Documents\dvd_remix\titleOCR.py" C:\Users\Styvens\Documents\Favela Jiu Jitsu\Disc 1 Open Guard Passes.avi" 50 2

import Image
import pytesseract
import cv2
import numpy
import sys
import os
import argparse


def modify(x):
	a=x
	for f in modifier:
		a=f(a)
	return a

parser = argparse.ArgumentParser(description='Recover the title of the chapters from the main video')
parser.add_argument('path',help="path of the video file")
parser.add_argument('-d','--delay',type=int,dest="delay",default=0,help="frame number to skip after chapter start")
parser.add_argument('--clip',dest="clip",type=int,nargs=4,help="coordinates of the left,top,right,bottom corner of the rectangle to clip")
parser.add_argument('-m','--method',dest="method",choices=['substract','color','accumulate'],help="Method to use to highlight the title")
# Method Specific Options
#	Background subtraction
g1=parser.add_argument_group('Substract')
g1.add_argument('--background',type=int,dest="background",help="rank of the frame to subtract")
#	Colour Filtering
g2=parser.add_argument_group('Color')
g2.add_argument('--color',dest="color",nargs=3,type=int,help="specify color used by filter [0..255] (R G B)")
g2.add_argument('--tolerance',dest="colorTolerance",default=30,type=int,help="color tolerance (radius) (30)")
#	Time Accumulation
g3=parser.add_argument_group('Accumulate')
g3.add_argument('--samples',dest="sample",default=10,type=int,help="number of samples to accumulate(10)")
g3.add_argument('--span',dest="span",default=50,type=int,help="number of frames on which to accumulate (50)")

args=parser.parse_args()

# Check Argument validity
if not os.path.exists(args.path):
	print "Can't find file "+ args.path
	sys.exit(1)

cap = cv2.VideoCapture(args.path)
if not cap.isOpened():
	print "Can't open file "+ args.path
	sys.exit(1)

delay=args.delay
width  = cap.get(3) # CV_CAP_PROP_FRAME_WIDTH
height = cap.get(4) # CV_CAP_PROP_FRAME_HEIGHT

modifier=[]
#modifier.append(lambda x:cv2.bitwise_not(x) )
if args.clip is not None :
	modifier.append(lambda x:x[args.clip[1]:args.clip[3],args.clip[0]:args.clip[2],:] )
	width  = args.clip[2]-args.clip[0] # CV_CAP_PROP_FRAME_WIDTH
	height = args.clip[3]-args.clip[1]
	
if args.method == 'substract':
	if args.background is not None :
		cap.set(1,args.background)
		ret,imgRef = cap.read()
		imgRef=modify(imgRef)
	else:
		print "substract method need BACKGROUND"
		sys.exit(1)
elif args.method == 'color':
	if args.color is not None :
		colRef	= (args.color[2],args.color[1],args.color[0])
		colThres= args.colorTolerance
	else :
		print "color method need COLOR"
		sys.exit(1)



	
# Open the necessary Files
(baseP,extP)=os.path.splitext(args.path)
titleImgOutP=baseP+"_title"
if not os.path.exists(titleImgOutP):
	os.mkdir(titleImgOutP)
frameIn=open(baseP+"_frame.csv",'r')
titleOut=open(baseP+"_title.csv",'w')

#Start Processing Loop
i=1
totalFrame=cap.get(7)
for line in frameIn: 
	try:
		frNB=int(line)
		cap.set(1,frNB+delay)
		ret,imgTitle = cap.read()
		imgTitle=modify(imgTitle)
		cv2.imwrite(titleImgOutP+"\\%02d_org.jpg" % i,imgTitle)
		if args.method == 'substract':
			imgCV=cv2.absdiff(imgTitle,imgRef)
			imgCV = cv2.cvtColor(imgCV,cv2.COLOR_BGR2GRAY)
			ret,imgCV=cv2.threshold(imgCV,30,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
			#print ret
		elif args.method == 'color':
			imgCV=numpy.zeros((height,width), numpy.uint8)
			imgCV[:]=255
			for j in range(0,3):
				ret,chal1=cv2.threshold(imgTitle[:,:,j],colRef[j]-colThres,255,cv2.THRESH_BINARY)
				ret,chal2=cv2.threshold(imgTitle[:,:,j],colRef[j]+colThres,255,cv2.THRESH_BINARY_INV)
				imgFilter=cv2.bitwise_and(chal1,chal2)
				imgCV=cv2.bitwise_and(imgCV,imgFilter)
		elif args.method == 'accumulate':
			imgCV=cv2.cvtColor(imgTitle,cv2.COLOR_BGR2GRAY)
			for j in range(1,args.sample):
				cap.set(1,frNB+delay+j*int(args.span/args.sample))
				ret,imgTemp = cap.read()
				imgTemp=modify(imgTemp)
				imgTemp=cv2.cvtColor(imgTemp,cv2.COLOR_BGR2GRAY)
				imgCV=cv2.bitwise_and(imgCV,imgTemp)
		else:
			imgCV=imgTitle
			imgCV = cv2.cvtColor(imgCV,cv2.COLOR_BGR2RGB)
		#cv2.imwrite(titleImgOutP+"\\%02d.jpg" % i,imgCV)
		pil_im = Image.fromarray(imgCV)
		#pil_im.show()
		pil_im.save(titleImgOutP+"\\%02d.jpg" % i)
		#Perform the OCR
		title = pytesseract.image_to_string(pil_im,lang='eng')
		title=title.replace('\n',' ').replace('\r','')
		print i, title
		titleOut.write("%02d,%s \n" %(i,title))
		i=i+1
	except:
		print "Unexpected error:", sys.exc_info()[0]
	


frameIn.close()
titleOut.close()
cap.release()
sys.exit()

