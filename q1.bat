@echo off
setlocal enabledelayedexpansion

:: ��������ļ��Ƿ����
if not exist output_result.txt (
    echo ����output_result.txt �ļ������ڣ�
    pause
    exit /b 1
)

echo ���ڴ�����Ƶ�ļ�...
for /f "tokens=1-3" %%a in (output_result.txt) do (
    set /a next=%%a+1
    echo ����ִ�У�audio_process.bat "temp_%%a.wav" "%%a.wav" "%%b" "%%c" "temp_!next!.wav"
    call audio_process.bat "temp_%%a.wav" "%%a.wav" "%%b" "%%c" "temp_!next!.wav"
    
    :: �����һ�������Ƿ�ִ�гɹ�
    if errorlevel 1 (
        echo ������Ƶ����ʧ�ܣ�������%%a, %%b, %%c��
        pause
        exit /b 1
    )
)

echo ������������ɣ�
pause