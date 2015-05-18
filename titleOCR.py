# python "C:\Users\Styvens\Documents\dvd_remix\titleOCR.py" C:\Users\Styvens\Documents\Favela Jiu Jitsu\Disc 1 Open Guard Passes.avi" 50 2

import Image
import pytesseract
import cv2
import sys
import os
import argparse

parser = argparse.ArgumentParser(description='Recover the title of the chapters from the main video')
parser.add_argument('path',help="path of the video file")
parser.add_argument('-s','--substract',type=int,dest="background",help="rank of the frame to substract")
parser.add_argument('-d','--delay',type=int,dest="delay",default=0,help="frame number to skip after chapter start")
parser.add_argument('-c','--color',dest="color",nargs=3,type=int,help="specify color filtering [0..255] (R G B)")
parser.add_argument('-r','--radius',dest="colorTolerance",default=30,type=int,help="color tolerance (radius) (30)")
args=parser.parse_args()
if not os.path.exists(args.path):
	print "Can't find file "+ args.path
	sys.exit(1)

cap = cv2.VideoCapture(args.path)
if not cap.isOpened():
	print "Can't open file "+ args.path
	sys.exit(1)

delay=args.delay
if args.background is not None :
	cap.set(1,args.background)
	ret,imgRef = cap.read()
else :
	imgRef =None

if args.color is not None :
	colRef	= (args.color[2],args.color[1],args.color[0])
	colThres= args.colorTolerance
else :
	colRef = None

(baseP,extP)=os.path.splitext(args.path)
titleImgOutP=baseP+"_title"
if not os.path.exists(titleImgOutP):
	os.mkdir(titleImgOutP)
frameIn=open(baseP+"_frame.csv",'r')
titleOut=open(baseP+"_title.csv",'w')


i=1
for line in frameIn: 
	frNB=int(line)
	cap.set(1,frNB+delay)
	ret,imgTitle = cap.read()
	cv2.imwrite(titleImgOutP+"\\%02d_org.jpg" % i,imgTitle)
	if imgRef is not None:
		imgCV=cv2.absdiff(imgTitle,imgRef)
		imgCV = cv2.cvtColor(imgCV,cv2.COLOR_BGR2GRAY)
		ret,imgCV=cv2.threshold(imgCV,30,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
		#print ret
	elif colRef is not None:
		imgCV=cv2.cvtColor(imgTitle,cv2.COLOR_BGR2GRAY)
		for j in range(0,3):
			ret,chal1=cv2.threshold(imgTitle[:,:,j],colRef[j]-colThres,255,cv2.THRESH_BINARY)
			ret,chal2=cv2.threshold(imgTitle[:,:,j],colRef[j]+colThres,255,cv2.THRESH_BINARY_INV)
			imgFilter=cv2.multiply(chal1,chal2)
			imgCV=cv2.multiply(imgCV,imgFilter)
	else:
		imgCV=imgTitle
		imgCV = cv2.cvtColor(imgCV,cv2.COLOR_BGR2RGB)
	#cv2.imwrite(titleImgOutP+"\\%02d.jpg" % i,imgCV)
	pil_im = Image.fromarray(imgCV)
	#pil_im.show()
	pil_im.save(titleImgOutP+"\\%02d.jpg" % i)
	title = pytesseract.image_to_string(pil_im,lang='eng')
	title=title.replace('\n',' ').replace('\r','')
	print i, title
	titleOut.write("%02d,%s \n" %(i,title))
	i=i+1

frameIn.close()
titleOut.close()
cap.release()
sys.exit()

