@echo off
setlocal enabledelayedexpansion

:: 输入文件
set "inputFile=input.txt"
:: 输出文件
set "outputFile=output_result.txt"

:: 清空或创建输出文件（不写入表头）
> "%outputFile%" echo. & del /q "%outputFile%" 2>nul & break>"%outputFile%"

:: 检查 ffprobe 是否存在（用于获取高精度时间）
where ffprobe >nul 2>nul
if %errorlevel% neq 0 (
    echo 未找到 ffprobe，请安装 ffmpeg 并确保其包含 ffprobe 工具。
    pause
    exit /b 1
)

:: 逐行读取 input.txt
for /f "tokens=1-6 delims=, " %%a in (%inputFile%) do (
    set "id=%%a"
    set "start=%%b"

    :: 去除多余空格
    set "id=!id: =!"
    set "start=!start: =!"

    :: 音频文件名
    set "audioFile=!id!.wav"

    :: 检查音频文件是否存在
    if exist "!audioFile!" (
        call :getAudioDuration "!audioFile!" duration
        set "line=!id!       !start!        !duration!"
        echo(!line!
        echo(!line!>>"%outputFile%"
    )
)

pause
exit /b

:: 使用 ffprobe 获取高精度音频时长（单位：秒）
:getAudioDuration
set "file=%~1"
set "tempFile=__temp_duration.txt"

:: 使用 ffprobe 获取精确时长（浮点数）
ffprobe -v error -show_entries format=duration -of default=nw=1 "%file%" > "%tempFile%"

:: 读取结果
set /p duration=<"%tempFile%"

:: 清理 duration= 前缀
for /f "tokens=2 delims==" %%d in ("!duration!") do set "duration=%%d"

del /q "%tempFile%"
goto :eof
    