import glob
import os
import re  # RegEx
import logging
import tkinter as tk
from tkinter.filedialog import askdirectory

TITLE_LABEL = "#TITLE:"
MV_LABEL = "[MV]"
DEFAULT_ENCODING = "utf8"
VIDEO_FILE_EXTENSIONS = (".avi", ".mpeg", ".mpg", ".mp4")


def get_title(sim_file_lines):
    for line in sim_file_lines:
        if TITLE_LABEL in line:
            return re.findall(f'{TITLE_LABEL}(.*?);', line, re.DOTALL)[0]


def remove_label_from_simfile(simfile_path, f_lines, title):
    with open(simfile_path, 'w', encoding=DEFAULT_ENCODING) as f:
        for f_line in f_lines:
            if TITLE_LABEL in f_line:
                # write title without the label
                title_without_label = title.replace(f" {MV_LABEL}", '')
                f.writelines(f"{TITLE_LABEL}{title_without_label};\n")
                # check if there's any more labels after ";" on the same line and split if needed
                # e.g., '#TITLE:Test [MV];#SUBTITLE:(Test);'
                labels_in_line = [x for x in f_line.split(";") if not x.isspace()]
                labels_in_line_count = len(labels_in_line)
                if labels_in_line_count > 1:
                    for i in range(1, labels_in_line_count):
                        new_label_line = labels_in_line[i].strip()
                        f.writelines(f"{new_label_line};\n")
            else:
                f.writelines(f_line)


# noinspection DuplicatedCode
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
    removed_label_simfile_count = 0
    simfile_path_list = glob.glob("**/*.ssc", recursive=True) + glob.glob("**/*.sm", recursive=True)

    for simfilePath in simfile_path_list:
        # check if video file exists in folder of simfile
        # print(f"Simfolder: {simfileFolder}")
        simfile = open(simfilePath, 'r', encoding=DEFAULT_ENCODING)
        try:
            simfile_lines = simfile.readlines()
            simtitle = get_title(simfile_lines)
            # check if title exists
            if simtitle == "" or simtitle is None:
                print(f"No title found in file {simfilePath}")
                continue
            # remove label
            if MV_LABEL in simtitle:
                remove_label_from_simfile(simfilePath, simfile_lines, simtitle)
                removed_label_simfile_count += 1
                print(f"'{MV_LABEL}' removed from '{simtitle}'")
        except UnicodeDecodeError:
            # in case of this exception: open file and save again in utf-8 encoding
            logging.error(f"Could not open {simfile.name} (change encoding to utf-8!)")
        except IndexError:
            logging.error(f"Could not extract title from {simfile.name}")
        simfile_count += 1
    print(f"{simfile_count} simfiles found")
    print(f"Removed '{MV_LABEL}' from title of {removed_label_simfile_count} simfiles")
    input("Press enter to exit")


main()
