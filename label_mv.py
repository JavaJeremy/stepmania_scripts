import glob
import os
import re  # RegEx
import logging
import tkinter as tk
from tkinter.filedialog import askdirectory

TITLE_LABEL = "#TITLE:"
MV_LABEL = "[MV]"
DEFAULT_ENCODING = "utf8"


def get_title(sim_file_lines):
    for line in sim_file_lines:
        if TITLE_LABEL in line:
            return re.findall(f'{TITLE_LABEL}(.*?);', line, re.DOTALL)[0]


def has_video_file(simfolder):
    for rootPath, dirs, filenames in os.walk(simfolder):
        for fileName in filenames:
            # lower() -> case insensitive so e.g. ".MPG" is also found
            if fileName.lower().endswith((".avi", ".mpeg", ".mpg")):
                # video file exists
                # print(f"Video: {os.path.join(rootPath, fileName)}")
                return True
        break  # prevent descending into subfolders
    return False


def update_simfile_with_mv_label(simfile_path, f_lines, title):
    with open(simfile_path, 'w', encoding=DEFAULT_ENCODING) as f:
        for f_line in f_lines:
            if TITLE_LABEL in f_line:
                f.writelines(f"{TITLE_LABEL}{title} {MV_LABEL};")
            else:
                f.writelines(f_line)


def remove_label_from_simfile(simfile_path, f_lines, title):
    with open(simfile_path, 'w', encoding=DEFAULT_ENCODING) as f:
        for f_line in f_lines:
            if TITLE_LABEL in f_line:
                title_without_label = title.replace(f" {MV_LABEL}", '')
                f.writelines(f"{TITLE_LABEL}{title_without_label};")
            else:
                f.writelines(f_line)


def main():
    # select folder
    root = tk.Tk()
    root.withdraw()
    path_to_folder = askdirectory(title='Select Folder')
    if path_to_folder == "":
        print("No folder selected, quitting")
        return
    print(f"Root folder: {path_to_folder}")
    # find simfiles
    os.chdir(path_to_folder)  # set default folder for glob search
    simfile_count = 0
    simfile_with_video_file_count = 0
    updated_simfile_mv_label_count = 0
    removed_label_simfile_count = 0
    simfile_path_list = glob.glob("**/*.ssc", recursive=True) + glob.glob("**/*.sm", recursive=True)

    for simfilePath in simfile_path_list:
        # check if video file exists in folder of simfile
        simfile_folder = os.path.dirname(simfilePath)
        # print(f"Simfolder: {simfileFolder}")
        simfile = open(simfilePath, 'r', encoding=DEFAULT_ENCODING)
        try:
            simfile_lines = simfile.readlines()
            simtitle = get_title(simfile_lines)
            if simtitle == "" or simtitle is None:
                print(f"No title found in file {simfilePath}")
                continue
            if has_video_file(simfile_folder):
                simfile_with_video_file_count += 1
                if MV_LABEL not in simtitle:
                    update_simfile_with_mv_label(simfilePath, simfile_lines, simtitle)
                    updated_simfile_mv_label_count += 1
                    print(f"'{MV_LABEL}' added to '{simtitle}")
                # else:
                #     print(f"'{simtitle}' already has MV label")
                # print(f"Video in: {simtitle}")
            else:  # no video - check if label needs to be removed then
                if MV_LABEL in simtitle:
                    remove_label_from_simfile(simfilePath, simfile_lines, simtitle)
                    removed_label_simfile_count += 1
        except UnicodeDecodeError:
            # in case of this exception: open file and save again in utf-8 encoding
            logging.error(f"Could not open {simfile.name} (change encoding to utf-8!)")
        except IndexError:
            logging.error(f"Could not extract title from {simfile.name}")
        simfile_count += 1
    print(f"{simfile_count} simfiles found")
    print(f"{simfile_with_video_file_count} simfiles with video files found")
    print(f"Added '{MV_LABEL}' to title of {updated_simfile_mv_label_count} simfiles")
    print(f"Removed '{MV_LABEL}' from title of {removed_label_simfile_count} simfiles")


main()
