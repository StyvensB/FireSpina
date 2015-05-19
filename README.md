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
0.1.2

### Installation
Pretty Straightforward 
You need to install all those dependencies
 + [Python] 
 + [OpenCV]  
 + [Numpy]
 + [ffmpeg] 
 + [Tesseract] 
 + [PyTesseract] 

And make sure there available in you **PATH** or can be imported in your python environment. You can follow each project specific directions to install them depending of your operating system.

##Usage

*Fire Splina* consist of *four* different module. So you can stop, replay, or alter the process at any time.Plus you can always tweek or edit their text output. The four modules follows the philosophy  **Fi**nd ,**Re**ad **Spli**t and  **Na**me and therefore are:
 + scan.py
 + titleOCR.py
 + cut.bat/(sh)
 + rename.py

I highly recommend to use an external video editor allowing to navigate the video by frame index. It will help you a lot figuring out what parameter value of parameter to enter.

Each module have is own help menu. Depending on your environment you may run directly python script or have to run them as argument of the python interpreter in BATCH mode. You can display it by typing :
```sh
moduleName.py --help
```
#### Find with scan.py
Scan.py intend to find transition in a video file based on a reference image or frame. As of now this reference image can only be specified by a frame index using the **-r or --reference** options. The heuristics rely also on two optionnal parameters. The threshold value triggering a match and the number of frame to skip betwwen each evaluation.
```sh
scan.py --reference 90 --skip 30 --threshold 0.6 /my/video/file.avi
```
Scan.py output its result in two editable text files. One holding the frame indexes, and one holding the time. Both indicate the location of a cut.

#### Read with titleOCR.py
TitleOCR.py aim at retrieving the chapter title by reading it on the video file. You can add parameters and specify some filtering treatment to dramatically improve the quality of the optical recognition (OCR). In case the tool would fail to reach a good enough accuracy. you can still edit the file and go on.

####Split with cut.bat
Cut.bat is more a convenience wrapper for ffmpeg than a independent tool. Its aim to be edited by the user so it can add is more specific options directly to ffmpeg. Linux users can for now directly use the ffmpeg command inside the file.
####Name with rename.py
Rename.py does something simple.Yet it aims at doing it well. It takes input from titleOCR.py and rename the file outputted by cut.bat (ffmpeg). Make sure you have checked and corrected the output of titleOCR.py so you can avoid bad surprise.

## Development
I am the main developer of this Open Source project. I will continue developing it as a hobbyist according to my need. Want to Learn more about me [S.Belloge] .

Want to contribute? Great let's make it happen !

### TODO

 - Re-factor (clean) and add similarity measure 
 - Re-factor (clean) and add search algorithm
 - Make a BaSH version of cut.bat
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
[OpenCV]:http://opencv.org/
[PyTesseract]:https://pypi.python.org/pypi/pytesseract
[Numpy]: www.numpy.org/