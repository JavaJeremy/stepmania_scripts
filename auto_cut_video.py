import tkinter
from tkinter.filedialog import askopenfilename
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import ffmpeg


def file_selection(title):
    tkinter.Tk().withdraw()
    filename = askopenfilename(title=title)
    if filename == "":
        raise Exception("No file selected, quitting")
    print(f"Selected file: {filename}")
    return filename


def get_video_part(video_path, start_time, end_time):
    split_at = "."
    # cut video 1
    target_video_path_0 = f"{video_path.rsplit(split_at, 1)[0]} (auto cut)0.{video_path.rsplit(split_at, 1)[1]}"
    start_time = 0
    end_time = 4
    ffmpeg_extract_subclip(video_path, start_time, end_time, target_video_path_0)
    # cut video 2
    start_time = 56
    end_time = 59
    target_video_path_1 = f"{video_path.rsplit(split_at, 1)[0]} (auto cut)1.{video_path.rsplit(split_at, 1)[1]}"
    ffmpeg_extract_subclip(video_path, start_time, end_time, target_video_path_1)
    # join video parts
    video_pt_1 = ffmpeg.input(target_video_path_0)
    video_pt_2 = ffmpeg.input(target_video_path_1)
    v1 = video_pt_1.video
    # a1 = video_pt_1.audio
    v2 = video_pt_2.video
    # a2 = video_pt_2.audio
    # joined = ffmpeg.concat(v1, a1, v2, a2, v=1, a=1).node
    joined = ffmpeg.concat(v1, v2, v=1).node
    v3 = joined[0]
    # a3 = joined[1]
    target_video_path_3 = f"{video_path.rsplit(split_at, 1)[0]} (auto joined).{video_path.rsplit(split_at, 1)[1]}"
    # out = ffmpeg.output(v3, a3, target_video_path_3)
    out = ffmpeg.output(v3, target_video_path_3)
    out.run()
    return target_video_path_3


def main():
    try:
        audio_path = file_selection('Select simfile audio')
        video_path = file_selection('Select video to be cut')

        # get_video_part(video_path)

    except Exception as error:
        print(str(error))


main()
