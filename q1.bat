@echo off
setlocal enabledelayedexpansion

:: 检查输入文件是否存在
if not exist output_result.txt (
    echo 错误：output_result.txt 文件不存在！
    pause
    exit /b 1
)

echo 正在处理音频文件...
for /f "tokens=1-3" %%a in (output_result.txt) do (
    set /a next=%%a+1
    echo 正在执行：audio_process.bat "temp_%%a.wav" "%%a.wav" "%%b" "%%c" "temp_!next!.wav"
    call audio_process.bat "temp_%%a.wav" "%%a.wav" "%%b" "%%c" "temp_!next!.wav"
    
    :: 检查上一条命令是否执行成功
    if errorlevel 1 (
        echo 错误：音频处理失败（参数：%%a, %%b, %%c）
        pause
        exit /b 1
    )
)

echo 所有任务已完成！
pause