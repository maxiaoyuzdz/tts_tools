@echo off
setlocal

REM ����������
if "%~5"=="" (
    echo �÷�: %~nx0 ����1.wav ����2.wav ����3 ����4 ����5.wav
    exit /b 1
)

REM ִ��FFmpeg����
ffmpeg -i "%~1" -i "%~2" -filter_complex "[0:a]atrim=0:%~3,asetpts=PTS-STARTPTS[a1]; [0:a]atrim=%~4,asetpts=PTS-STARTPTS[a2]; [a1][1:a][a2]concat=n=3:v=0:a=1" "%~5"

endlocal