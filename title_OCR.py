#!/usr/bin/env python


import Image
import pytesseract
import numpy
import sys
import os
import argparse




parser = argparse.ArgumentParser(description='Recover the title of the chapters from the main video')
parser.add_argument('path',help="path of the video file")

args=parser.parse_args()

# Check Argument validity
#if not os.path.exists(args.path):
#	print "Can't find file "+ args.path
#	sys.exit(1)

# Open the necessary Files
(baseP,extP)=os.path.splitext(args.path)
titleImgOutP=baseP+"_title"

if not os.path.exists(titleImgOutP):
	print "Can't find file "+ titleImgOutP
	sys.exit(1)


imgList=os.listdir(titleImgOutP)
#print imgList
titleOut=open(baseP+"_title.csv",'w')

#Start Processing Loop
i=0
for imgPath in imgList:
	try:
		(imgBasePath,imgExt) = os.path.splitext(imgPath)
		if not (imgExt==".jpg" or imgExt==".png"):
			continue
		#print os.path.join(titleImgOutP,imgPath)
		pil_im = Image.open(os.path.join(titleImgOutP,imgPath))
		#pil_im.show()
		#Perform the OCR
		pil_im.load()
		title = pytesseract.image_to_string(pil_im,lang='eng')
		title=title.replace('\n',' ').replace('\r','')
		print i,imgPath,title
		titleOut.write("%02d,%s \n" %(i,title))
		i=i+1
	except:
		print "Unexpected error:", sys.exc_info()


titleOut.close()
sys.exit()

