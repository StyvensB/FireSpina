@echo off

setlocal
PATH=%PATH%;C:\ffmpeg-20150329-git-cf16b45-win64-static\bin\

REM check cut time File 
if not exist "%~dpn1_time.txt" (
 echo No time cut found
 echo  Run: %~dp0\scan.py %1
 exit /b 1
)

md "%~dpn1_chapter"

REM Read Files And Cut the video file

echo Start Splitting the file
FOR /f "usebackq delims=" %%i IN ("%~dpn1_time.txt") DO set times=%%i
set times=%times:~0,-1%
ffmpeg -v quiet  -i %1  -map 0 -f segment  -segment_times "%times%"    "%~dpn1_chapter\%%02d.%mp4"

endlocal