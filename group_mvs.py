import tkinter as tk
from tkinter.filedialog import askdirectory
import glob
import shutil
from pathlib import Path
import re  # RegEx
from shared_constants import *
from shared_methods import has_video_file


def folder_selection():
    # select search folder
    root = tk.Tk()
    root.withdraw()
    search_folder = askdirectory(title='Folder to search for simfiles')
    if search_folder == "":
        print("No folder selected, quitting")
        return
    print(f"Search folder: {search_folder}")
    # select grouping folder
    root = tk.Tk()
    root.withdraw()
    move_folder = askdirectory(title='Folder to move simfiles with mv')
    if move_folder == "":
        print("No folder selected, quitting")
        return
    print(f"Move to folder: {move_folder}")
    return search_folder, move_folder


def get_chart_files(search_folder):
    os.chdir(search_folder)  # set default folder for glob search
    chart_list = glob.glob("**/*.ssc", recursive=True) + glob.glob("**/*.sm", recursive=True)
    # Info - could be more than simfiles because .ssc and .sm can both be in one simfile
    chart_file_count = len(chart_list)
    print(f"{chart_file_count} chart files found")
    return chart_list


def main():
    simfile_with_video_file_count = 0
    origin_dir = ""
    search_folder, move_folder = folder_selection()
    chart_files = get_chart_files(search_folder)
    for chart_file_path in chart_files:
        try:
            simfile = os.path.dirname(chart_file_path)
            # if simfile is already in music video folder, skip
            if os.path.dirname(chart_file_path) in move_folder:
                continue
            # check if video file exists in simfile
            if has_video_file(simfile, VIDEO_FILE_EXTENSIONS):
                # move to music video folder
                # if it was already moved on the previous loop skip
                # this can happen when there are two chart files in one simfile
                if origin_dir == simfile:
                    continue
                origin_dir = simfile
                target_dir = move_folder
                shutil.move(origin_dir, target_dir)
                simfile_with_video_file_count += 1
                print(f"Moved '{simfile}'")
        except shutil.Error as e:
            if "already exists" in str(e):
                duplicate_dir_from = Path(origin_dir)
                file_size_from = sum(f.stat().st_size for f in duplicate_dir_from.glob('**/*') if f.is_file())
                e_str = str(e)
                res = re.findall(r'\'(.*?)\'', e_str)
                duplicate_dir_to = Path(res[0])
                file_size_to = sum(f.stat().st_size for f in duplicate_dir_to.glob('**/*') if f.is_file())
                if file_size_from == file_size_to:
                    print(f"Duplicate found (already exists in MV-Folder): '{simfile}'")
                    print(f"removing...")
                    shutil.rmtree(origin_dir)
                    print(f"Successfully removed!")
                else:
                    print(f"Simfile with duplicate name found, but different size: '{simfile}'")
            else:
                print('Error: %s' % e)
            continue
    print(f"Moved '{simfile_with_video_file_count}' simfiles to the music video folder")


main()
