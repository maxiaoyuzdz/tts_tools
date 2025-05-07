import subprocess
import argparse

def main():
    parser = argparse.ArgumentParser(description="使用ffmpeg对音频进行裁剪和拼接处理")
    parser.add_argument("input1", help="第一个输入音频文件路径")
    parser.add_argument("input2", help="第二个输入音频文件路径")
    parser.add_argument("end_time1", type=float, help="第一个音频裁剪的结束时间（秒）")
    parser.add_argument("start_time2", type=float, help="第二个音频裁剪的起始时间（秒）")
    parser.add_argument("--output", default="output_final.wav", help="输出文件名（默认为 output_final.wav）")
    args = parser.parse_args()

    # 构建 filter_complex 字符串
    filter_complex = (
        f"[0:a]atrim=0:{args.end_time1},asetpts=PTS-STARTPTS[a1]; "
        f"[0:a]atrim={args.start_time2},asetpts=PTS-STARTPTS[a2]; "
        "[a1][1:a][a2]concat=n=3:v=0:a=1"
    )

    # 构建 ffmpeg 命令
    cmd = [
        'ffmpeg',
        '-i', args.input1,
        '-i', args.input2,
        '-filter_complex', filter_complex,
        args.output
    ]

    print("正在执行命令：")
    print(' '.join(cmd))

    # 执行命令
    try:
        subprocess.run(cmd, check=True)
        print(f"音频处理完成，输出文件已保存为：{args.output}")
    except subprocess.CalledProcessError as e:
        print(f"ffmpeg 执行失败，错误码：{e.returncode}")
        exit(1)

if __name__ == "__main__":
    main()