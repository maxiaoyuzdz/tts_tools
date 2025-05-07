@echo off
setlocal enabledelayedexpansion

:: �����ļ�
set "inputFile=input.txt"
:: ����ļ�
set "outputFile=output_result.txt"

:: ��ջ򴴽�����ļ�����д���ͷ��
> "%outputFile%" echo. & del /q "%outputFile%" 2>nul & break>"%outputFile%"

:: ��� ffprobe �Ƿ���ڣ����ڻ�ȡ�߾���ʱ�䣩
where ffprobe >nul 2>nul
if %errorlevel% neq 0 (
    echo δ�ҵ� ffprobe���밲װ ffmpeg ��ȷ������� ffprobe ���ߡ�
    pause
    exit /b 1
)

:: ���ж�ȡ input.txt
for /f "tokens=1-6 delims=, " %%a in (%inputFile%) do (
    set "id=%%a"
    set "start=%%b"

    :: ȥ������ո�
    set "id=!id: =!"
    set "start=!start: =!"

    :: ��Ƶ�ļ���
    set "audioFile=!id!.wav"

    :: �����Ƶ�ļ��Ƿ����
    if exist "!audioFile!" (
        call :getAudioDuration "!audioFile!" duration
        set "line=!id!       !start!        !duration!"
        echo(!line!
        echo(!line!>>"%outputFile%"
    )
)

pause
exit /b

:: ʹ�� ffprobe ��ȡ�߾�����Ƶʱ������λ���룩
:getAudioDuration
set "file=%~1"
set "tempFile=__temp_duration.txt"

:: ʹ�� ffprobe ��ȡ��ȷʱ������������
ffprobe -v error -show_entries format=duration -of default=nw=1 "%file%" > "%tempFile%"

:: ��ȡ���
set /p duration=<"%tempFile%"

:: ���� duration= ǰ׺
for /f "tokens=2 delims==" %%d in ("!duration!") do set "duration=%%d"

del /q "%tempFile%"
goto :eof
    