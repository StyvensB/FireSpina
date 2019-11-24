# FiRe SpliNa

*Fire Splina*  is an utility suite allowing user to split instructional video file. Thus resulting in a better learning experience. Its features the following abilities.

  - Automate research of transition
  - Optical Recognition of title
  - Automatic split, format conversion
  - Automatic naming

Fire Splina is an assisting tool aiming at bash processing of video file. Thus it require as little user input as possible, yet is very configurable . Tell it what you are looking for and it will:

 - **Fi**nd it
 - **Re**ad it,
 - **Spli**t it and
 - **Na**me it   , ("Yeah!")



# Tech 

*Fire Splina* rely heavily on a few open source project all worth mentioning. Here is a list:
+ [Python] 2.7 as base scripting layer
+ [OpenCV] for python for frame manipulation
+ [ffmpeg] for splitting and conversion
+ [Tesseract] via [PyTesseract] as OCR engine

### Version
1.0

### Installation
Pretty Straightforward 
You need to install all those dependencies
 + [Python] 
 + [Numpy]
 + [ffmpeg] 
 + [Tesseract] 
 + [PyTesseract] 

And make sure there available in you **PATH** or can be imported in your python environment. You can follow each project specific directions to install them depending of your operating system.

##Usage

*Fire Splina* follow a three step approach. So you can stop, replay, or alter the process at any time.Plus you can always tweek or edit their text output. The three modules follows the philosophy  **Fi**nd the transition,**Re**ad the title, **Spli**t and  **Na**me the chapter and therefore are:
 + trans_***.py
 + title_***.py
 + chap_***.py


I highly recommend to use an external video editor allowing to navigate the video by frame index. It will help you a lot figuring out what parameter value of parameter to enter.

Each module have is own help menu. Depending on your environment you may run directly python script or have to run them as argument of the python interpreter in BATCH mode. You can display it by typing :
```sh
moduleName.py --help
```
#### Find with trans***.py
+ trans_black.py intend to find transition in a video file based on black frames.
+ trans_chroma.py intend to find transition in a video file based on a predominant color in certain frame. it then replace that color by black pixel using the chromakey filter.
+ trans_black.py intend to find transition in a video file based on the difference with a refernce frame previously exported with your favourite viedo player.
```sh
trans_black.py  /my/video/file.avi
```
trans***.py output its result in two editable text files. One holding the frame indexes, and one holding the time. Both indicate the location of a cut.

#### Extract and Read and with title_***.py
+ title_extract.py aim at retrieving the chapter frame title by extracting them from the  the video file. You can add a frame delay parameters to find the specific frame.
+ title_OCR.py use an OCR engine to decipher the title written in the frame. In case the tool would fail to reach a good enough accuracy. you can still edit the file and go on.

####Split and name with chap_***.py
+ chap_cut.py  is more a convenience wrapper for ffmpeg than a independent tool. 
+ chap_title.py does something simple.Yet it aims at doing it well. It takes input from title_OCR.py and rename the chapter video cut by chap_cut.py (ffmpeg). Make sure you have checked and corrected the output of title_OCR.py so you can avoid bad surprise.

## Development
I am the main developer of this Open Source project. I will continue developing it as a hobbyist according to my need. Want to Learn more about me [S.Belloge] .

Want to contribute? Great let's make it happen !

### TODO

 - Re-factor and remove redundancy(clean) 
 - Investigate search algorithm by time diffference
 - Investigate search algorithm with audio track
 - Add Code Comments Globally
 - Package for distribution or as standalone
 - Make GUI
 - Save CLI options in json file for replay
 - Develop the Readme file


License
----

MIT


[s.belloge]:https://www.linkedin.com/pub/styvens-belloge/35/756/518/en
[Tesseract]:code.google.com/p/tesseract-ocr
[ffmpeg]:https://www.ffmpeg.org/
[Python]:https://www.python.org/
[PyTesseract]:https://pypi.python.org/pypi/pytesseract
[Numpy]: www.numpy.org/