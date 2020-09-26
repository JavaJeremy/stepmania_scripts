import glob
import os
import re  # RegEx
import logging
import tkinter as tk
from tkinter.filedialog import askdirectory

TITLE_LABEL = "#TITLE:"
MV_LABEL = "[MV]"
DEFAULT_ENCODING = "utf8"

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


def update_simfile_with_mv_label(simfile_path, title):
    with open(simfile_path, 'r', encoding=DEFAULT_ENCODING) as f:
        f_lines = f.readlines()
    with open(simfile_path, 'w', encoding=DEFAULT_ENCODING) as f:
        for f_line in f_lines:
            if TITLE_LABEL in f_line:
                f.writelines(f"{TITLE_LABEL}{title} {MV_LABEL};")
            else:
                f.writelines(f_line)


# select folder
root = tk.Tk()
root.withdraw()
pathToFolder = askdirectory(title='Select Folder')
print(f"Rootfolder: {pathToFolder}")
# find simfiles
os.chdir(pathToFolder)  # set default folder for glob search
simfileCount = 0
simfileWithVideoFileCount = 0
updated_simfile_mv_label_count = 0
simfilePathList = glob.glob("**/*.ssc", recursive=True) + glob.glob("**/*.sm", recursive=True)
for simfilePath in simfilePathList:
    # check if video file exists in folder of simfile
    simfileFolder = os.path.dirname(simfilePath)
    # print(f"Simfolder: {simfileFolder}")
    if has_video_file(simfileFolder):
        simfileWithVideoFileCount += 1
        simfile = open(simfilePath, 'r', encoding=DEFAULT_ENCODING)
        try:
            content = simfile.read()
            for line in content.split("\n"):
                if TITLE_LABEL in line:
                    simtitle = re.findall(f'{TITLE_LABEL}(.*?);', line, re.DOTALL)[0]
                    if MV_LABEL not in simtitle:
                        update_simfile_with_mv_label(simfilePath, simtitle)
                        updated_simfile_mv_label_count += 1
                        print(f"'{MV_LABEL}' added to '{simtitle}")
                    # else:
                    #     print(f"'{simtitle}' already has MV label")
                    # print(f"Video in: {simtitle}")
                    break
        except UnicodeDecodeError:
            # in case of this exception: open file and save again in utf-8 encoding
            logging.error(f"Could not open {simfilePath}")
        except IndexError:
            logging.error(f"Could not extract title from {line} in {simfilePath}")
    simfileCount += 1
print(f"{simfileCount} simfiles found")
print(f"{simfileWithVideoFileCount} simfiles with video files found")
print(f"Updated title with '{MV_LABEL}' of {updated_simfile_mv_label_count} simfiles")
