import tkinter
from tkinter.filedialog import askopenfilename
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import ffmpeg


def file_selection():
    tkinter.Tk().withdraw()
    filename = askopenfilename(title='Select video to be cut')
    if filename == "":
        raise Exception("No file selected, quitting")
    print(f"Selected file: {filename}")
    return filename


def main():
    try:
        video_path = file_selection()
        split_at = "."
        target_video_path = f"{video_path.rsplit(split_at, 1)[0]} (auto cut).{video_path.rsplit(split_at, 1)[1]}"
        start_time = 0
        end_time = 4
        # cut video
        ffmpeg_extract_subclip(video_path, start_time, end_time, target_video_path)
        # todo: cut multiple parts of video and put them together
        # # Assuming frame rate is 30 fps, 33.3 seconds applies 1000 frames.
        # v1 = main_video.video.filter('trim', duration=33.3)
        # v2 = outro.video
        #
        # joined = ffmpeg.concat(v1, v2, v=1).node
        # v3 = joined[0]
        # a3 = joined[1]
        #
        # out = ffmpeg.output(v3, a3, 'out.mp4')
        # out.run()
    except Exception as error:
        print(str(error))


main()
