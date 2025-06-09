import os
import math
from moviepy.video.io.VideoFileClip import VideoFileClip

cpu = 'libx264'
intel = 'h264_qsv'
nvidia = 'h264_nvenc'
amd = 'h264_amf'

def split_video(input_path, output_dir, segment_minutes=10, encoder = cpu):
    # 加载视频
    video = VideoFileClip(input_path)
    duration = video.duration  # 视频总时长（秒）
    segment_duration = segment_minutes * 60
    num_segments = math.ceil(duration / segment_duration)

    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    print(f"视频总时长：{duration:.2f}秒，共分为 {num_segments} 段。")

    # 开始分割
    for i in range(num_segments):
        start_time = i * segment_duration
        end_time = min((i + 1) * segment_duration, duration)
        segment = video.subclipped(start_time, end_time)
        output_file = os.path.join(output_dir, f"video_part{i+1}.mp4")
        print(f"正在导出：{output_file}，时长：{end_time - start_time:.2f} 秒")

        segment.write_videofile(
            output_file,
            codec=encoder,
            audio_codec="aac",
            preset="fast",
            temp_audiofile='temp-audio.m4a',
            remove_temp=True
        )

    video.close()
    print("分割完成！")

# 示例用法（替换为你的视频路径和输出文件夹）
if __name__ == "__main__":
    input_video_path = "ScreenRecording_06-02-2025 10-37-59_1.mp4"         # 输入视频文件路径
    output_directory = "split"        # 分段视频输出目录
    split_video(input_video_path, output_directory, encoder = intel)
