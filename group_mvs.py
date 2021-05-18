import os
import glob

from move_files import move_files
from shared_constants import *
from shared_methods import has_file_of_type


def get_chart_files(search_folder):
    os.chdir(search_folder)  # set default folder for glob search
    chart_list = glob.glob("**/*.ssc", recursive=True) + glob.glob("**/*.sm", recursive=True)
    # Info - could be more than simfiles because .ssc and .sm can both be in one simfile
    chart_file_count = len(chart_list)
    print(f"{chart_file_count} chart files found")
    return chart_list


def has_video_file(simfile):
    return has_file_of_type(simfile, VIDEO_FILE_EXTENSIONS)


def main():
    move_files(get_chart_files, has_video_file)


main()
