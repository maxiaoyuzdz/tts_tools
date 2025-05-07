@echo off
for %%a in (*.wav *.flac *.m4a *.aac *.ogg *.wma) do (
    ffmpeg -i "%%a" -b:a 128k -ac 1 "%%~na.mp3"
)