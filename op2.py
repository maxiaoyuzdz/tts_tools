import subprocess
import argparse
import os

def main():


    parser = argparse.ArgumentParser(description="批量处理音频文件")
    parser.add_argument("input_wav", help="初始主输入音频文件")
    parser.add_argument("params_file", help="参数文本文件路径")
    args = parser.parse_args()

    input1 = args.input_wav
    output_final = "output_final.wav"
    output_temp = "output_final_temp.wav"

    with open(args.params_file, "r") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) < 3:
            print(f"跳过无效行: {line}")
            continue

        index = parts[0]
        start_time = float(parts[1])
        duration = float(parts[2])

        print(f"处理第 {index} 行，开始时间：{start_time}，持续时间：{duration}")

        end_time_1 = start_time
        start_time_2 = start_time + duration
        input2 = f"{index}.wav"

        # 构建 filter_complex
        filter_complex = (
            f"[0:a]atrim=0:{end_time_1},asetpts=PTS-STARTPTS[a1]; "
            f"[0:a]atrim={start_time_2},asetpts=PTS-STARTPTS[a2]; "
    
            "[a1][1:a][a2]concat=n=3:v=0:a=1"
        )

        # 确定输出文件名
        current_output = f"output_temp_{i}.wav" if i < len(lines) - 1 else output_final

        # 构建 ffmpeg 命令
        cmd = [
            "ffmpeg",
            "-y",  # 覆盖输出文件
            "-i", input1,
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
        if input1 != args.input_wav and os.path.exists(input1):
            try:
                os.remove(input1)
                print(f"已删除临时文件: {input1}")
            except OSError as e:
                print(f"删除临时文件失败: {input1}, 错误: {e}")

        # 更新输入文件为当前输出
        input1 = current_output

    print("所有处理完成，最终输出文件已保存为：", output_final)

if __name__ == "__main__":
    main()