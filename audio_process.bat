@echo off
setlocal

REM 检查参数数量
if "%~5"=="" (
    echo 用法: %~nx0 参数1.wav 参数2.wav 参数3 参数4 参数5.wav
    exit /b 1
)

REM 执行FFmpeg命令
ffmpeg -i "%~1" -i "%~2" -filter_complex "[0:a]atrim=0:%~3,asetpts=PTS-STARTPTS[a1]; [0:a]atrim=%~4,asetpts=PTS-STARTPTS[a2]; [a1][1:a][a2]concat=n=3:v=0:a=1" "%~5"

endlocal