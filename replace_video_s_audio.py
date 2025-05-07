import subprocess
import argparse
import os
from pydub import AudioSegment
import pyrubberband as pyrb
import numpy as np

def extract_mp3_from_video(video_input, audio_output):
    """
    使用 ffmpeg 从视频文件中提取音频并保存为 MP3 文件
    """
    if not os.path.exists(audio_output):
        try:
            cmd = [
                "ffmpeg",
                "-i", video_input,  # 输入视频文件
                "-q:a", "0",        # 保持音频质量
                "-map", "a",        # 仅提取音频流
                audio_output        # 输出音频文件
            ]
            print("正在提取音频，执行命令：")
            print(" ".join(cmd))
            subprocess.run(cmd, check=True)
            print(f"音频提取完成，保存为：{audio_output}")
        except subprocess.CalledProcessError as e:
            print(f"提取音频失败，错误码：{e.returncode}")
            exit(1)

def extract_wav_from_video(video_input, audio_output):
    """
    使用 ffmpeg 从视频文件中提取音频并保存为 WAV 文件
    """
    if not os.path.exists(audio_output):
        try:
            cmd = [
                "ffmpeg",
                "-i", video_input,  # 输入视频文件
                "-q:a", "0",        # 保持音频质量
                "-map", "a",        # 仅提取音频流
                "-c:a", "pcm_s16le",  # 设置音频编码为 WAV 格式
                audio_output        # 输出音频文件
            ]
            print("正在提取音频，执行命令：")
            print(" ".join(cmd))
            subprocess.run(cmd, check=True)
            print(f"音频提取完成，保存为：{audio_output}")
        except subprocess.CalledProcessError as e:
            print(f"提取音频失败，错误码：{e.returncode}")
            exit(1)

def convert_mp3_to_wav(mp3_file, wav_file):
    """
    Convert an MP3 file to a WAV file using ffmpeg.
    
    :param mp3_file: Path to the input MP3 file.
    :param wav_file: Path to the output WAV file.
    """
    # 只有这个mp3存在的时候
    if os.path.exists(mp3_file):
        if not os.path.exists(wav_file):
            try:
                cmd = [
                    "ffmpeg",
                    "-i", mp3_file,       # Input MP3 file
                    "-c:a", "pcm_s16le",  # Output codec for WAV (16-bit PCM)
                    "-ar", "44100",       # Sample rate (44.1 kHz)
                    "-ac", "2",           # Stereo audio
                    wav_file              # Output WAV file
                ]
                print(f"正在转换 {mp3_file} 为 {wav_file}，执行命令：")
                print(" ".join(cmd))
                subprocess.run(cmd, check=True)
                print(f"转换完成，保存为：{wav_file}")
            except subprocess.CalledProcessError as e:
                print(f"转换失败，错误码：{e.returncode}")
                exit(1)

def replace_audio_in_video(video_input, audio_input, output_file):
    """
    Replace the audio in a video file with a new audio file using ffmpeg.
    
    :param video_input: Path to the input video file.
    :param audio_input: Path to the input audio file (WAV).
    :param output_file: Path to the output video file.
    """
    try:
        cmd = [
            "ffmpeg",
            "-i", video_input,       # Input video file
            "-i", audio_input,       # Input audio file (WAV)
            "-c:v", "copy",          # Copy video stream without re-encoding
            "-c:a", "aac",           # Encode audio to AAC format
            "-map", "0:v:0",         # Map the first video stream from the first input
            "-map", "1:a:0",         # Map the first audio stream from the second input
            "-shortest",             # Match the duration of the shortest input
            output_file              # Output video file
        ]
        print(f"正在替换音频，执行命令：")
        print(" ".join(cmd))
        subprocess.run(cmd, check=True)
        print(f"音频替换完成，保存为：{output_file}")
    except subprocess.CalledProcessError as e:
        print(f"音频替换失败，错误码：{e.returncode}")
        exit(1)

def change_audio_speed(input_path, output_path, speed_factor):
    """
    改变音频播放速度，保持音调不变。

    :param input_path: 输入音频文件路径
    :param output_path: 输出音频文件路径
    :param speed_factor: 速度因子（>1 加快，<1 放慢）
    """
    # 读取音频
    audio = AudioSegment.from_wav(input_path)
    audio = audio.set_channels(1)  # 转换为单声道
    samples = np.array(audio.get_array_of_samples())
    # samples = np.array(audio.get_array_of_samples(), dtype=np.float32)  # 转换为 NumPy 数组
    sample_rate = audio.frame_rate

    # 时间拉伸处理（注意：传入的是 1 / speed_factor）
    # stretched_samples = pyrb.time_stretch(samples, sample_rate, 1.0 / speed_factor)
    try:
        stretched_samples = pyrb.time_stretch(samples, sample_rate, speed_factor)

    except Exception as e:
        print(f"Error during time stretching: {e}")

    # 构造新的AudioSegment
    new_audio = AudioSegment(
        stretched_samples.tobytes(),
        frame_rate=sample_rate,
        sample_width=audio.sample_width,
        channels=audio.channels,
    )

    # 导出文件
    new_audio.export(output_path, format="wav")
def main():


    parser = argparse.ArgumentParser(description="批量处理音频文件")
    parser.add_argument("input_mp4", help="初始主输入视频文件")
    parser.add_argument("params_file", help="参数文本文件路径")
    args = parser.parse_args()

    video_input = args.input_mp4
    initial_audio_input = "extracted_audio.wav"

    # 提取音频
    extract_wav_from_video(video_input, initial_audio_input)


    # 将从视频抽离的音频作为输入，开始操作
    audio_input = initial_audio_input
    # 设置音频最终输出文件
    output_final = "output_final.wav"
    # output_temp = "output_final_temp.wav"

    # 读取参数文件
    with open(args.params_file, "r" , encoding="utf-8") as f:
        lines = f.readlines()

    # 用于存储每一行的前三个参数
    params_list = []

    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        parts = line.split(",") 
        if len(parts) >= 3:  # 确保至少有三个参数
            # 提取前三个参数
            param1 = parts[0].strip()
            param2 = parts[1].strip()
            param3 = parts[2].strip()
            file_name = f"{param1}.mp3"
            # 在源头上先把不存在的音频处理掉
            if os.path.exists(file_name):
                params_list.append((param1, param2, param3))
    
    # 将生产的mp3文件转换成wav文件
    for index, params in enumerate(params_list):
        file_name = f"{params[0]}.mp3"
        wav_name = f"{params[0]}.wav"
        convert_mp3_to_wav(file_name, wav_name)


    # 调整每个文件的播放时长，确保不前后重叠
    last_file_name = "none"
    last_start_time = 0
    last_end_time = 0
    temp_last_file = "temp.wav"

    for index, params in enumerate(params_list):
        current_file_name = f"{params[0]}.wav"
        current_start_time = float(params[1])
        if last_file_name != "none":
            try:
                result = subprocess.run(
                    ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1", last_file_name],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                duration = result.stdout.strip()
                # 提取精确值
                if duration.startswith("duration="):
                    duration = duration.split("=")[1]
                last_duration_val = float(duration)
                
                last_end_time = last_start_time + last_duration_val

                print(f"last_file_name : {last_file_name}, last_duration_val {last_duration_val} s, last_end_time: {last_end_time} , current_start_time: {current_start_time} ")

                if  current_start_time < last_end_time:
                    adjust_last_duration_target_val = current_start_time - 0.1 - last_start_time
                    # 将上个音频加速一点点
                    speed_factor: float = (
                                    last_duration_val / adjust_last_duration_target_val
                                )
                    if os.path.exists(temp_last_file):
                        os.remove(temp_last_file)

                    change_audio_speed(
                                    last_file_name, temp_last_file, speed_factor
                                )
                    print(f"========================================")
                    temp_result = subprocess.run(
                        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1", temp_last_file],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    temp_duration = temp_result.stdout.strip()
                    # 提取精确值
                    if temp_duration.startswith("duration="):
                        temp_duration = temp_duration.split("=")[1]
                    temp_duration_val = float(temp_duration)
                    print(f"temp_duration_val : {temp_duration_val} s")

                    os.remove(last_file_name)
                    os.rename(temp_last_file, last_file_name)
            except Exception as e:
                print(f"Error processing last file {last_file_name}: {e}")
                
        last_file_name = current_file_name
        last_start_time = current_start_time
            
                    
                    


                




    # 打印提取的参数
    for index, params in enumerate(params_list):
        # print(params) 有可能文件名不存在，因为如果mp3不存在的话，wav也不存在
        # 获取wav文件名
        file_name = f"{params[0]}.wav"
        # 获取开始时间和持续时间
        start_time= float(params[1])
        duration_val = 0

        print(file_name)
        if os.path.exists(file_name):
            # 使用 ffprobe 获取播放时间
            try:
                result = subprocess.run(
                    ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1", file_name],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                duration = result.stdout.strip()
                # 提取精确值
                if duration.startswith("duration="):
                    duration = duration.split("=")[1]
                print(f"File: {file_name}, Duration: {duration} seconds")
                duration_val = float(duration)
                print(f"处理第 {index} 行，文件：{file_name}, 开始时间：{start_time}，持续时间：{duration_val}")
                end_time_1 = start_time
                start_time_2 = start_time + duration_val
                input2 = file_name
                # 构建 filter_complex
                filter_complex = (
                    f"[0:a]atrim=0:{end_time_1},asetpts=PTS-STARTPTS[a1]; "
                    f"[0:a]atrim={start_time_2},asetpts=PTS-STARTPTS[a2]; "
            
                    "[a1][1:a][a2]concat=n=3:v=0:a=1"
                )

                # 确定输出文件名
                current_output = f"output_temp_{index}.wav" if index < len(params_list) - 1 else output_final
                # 构建 ffmpeg 命令
                cmd = [
                    "ffmpeg",
                    "-y",  # 覆盖输出文件
                    "-i", audio_input,
                    "-i", input2,
                    "-filter_complex", filter_complex,
                    "-c:a", "pcm_s16le",  # 输出为 16bit PCM WAV
                    current_output
                ]

                print(f"正在处理第 {index} 行，执行命令：")
                print(" ".join(cmd))

                try:
                    subprocess.run(cmd, check=True)
                except subprocess.CalledProcessError as e:
                    print(f"ffmpeg 执行失败，错误码：{e.returncode}")
                    exit(1)

                # 删除上一轮的临时文件（如果不是初始输入文件）
                if audio_input != initial_audio_input and os.path.exists(audio_input):
                    try:
                        os.remove(audio_input)
                        print(f"已删除临时文件: {audio_input}")
                    except OSError as e:
                        print(f"删除临时文件失败: {audio_input}, 错误: {e}")
                
                # 更新输入文件为当前输出
                audio_input = current_output

            except Exception as e:
                print(f"Error processing file {file_name}: {e}")

    # 删除从视频抽离的音频文件，也就是最早的输入
    os.remove(initial_audio_input)
    print("删除中间临时文件，")
    for index, params in enumerate(params_list):
        # print(params)
        file_name = f"{params[0]}.wav"
        if  os.path.exists(file_name):
            os.remove(file_name)
    

    print("所有处理完成，最终输出音频文件已保存为：", output_final)
    

    # video_input  output_final
    # 将 ffmpeg -i original.mp4 -i audio.wav -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 -shortest output.mp4
    print("合并回原视频")
    replace_audio_in_video(video_input, output_final, "output.mp4")
    os.remove(output_final)



if __name__ == "__main__":
    main()