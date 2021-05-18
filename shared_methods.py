import os
import re  # RegEx
import tkinter as tk
from tkinter.filedialog import askdirectory
from shared_constants import *


def get_folder(dialog_title='Select Folder'):
    # select folder
    root = tk.Tk()
    root.withdraw()
    path_to_folder = askdirectory(title=dialog_title)
    if path_to_folder == "":
        raise Exception("No folder selected - quitting")
    print(f"Folder: {path_to_folder}")
    return path_to_folder


def has_file_of_type(folder, file_extensions):
    """
    :param folder:
    :param file_extensions: (".avi", ".mpeg", ".mpg", ".mp4")
    :return:
    """
    for rootPath, dirs, filenames in os.walk(folder):
        for fileName in filenames:
            # lower() -> case insensitive so e.g. ".MPG" is also found
            if fileName.lower().endswith(file_extensions):
                # file exists
                # print(f"File: {os.path.join(rootPath, fileName)}")
                return True
        break  # prevent descending into subfolders
    return False


def get_files_of_type(folder, file_extensions):
    """
    :param folder:
    :param file_extensions: (".avi", ".mpeg", ".mpg", ".mp4")
    :return:
    """
    files = []
    for rootPath, dirs, filenames in os.walk(folder):
        for fileName in filenames:
            # lower() -> case insensitive so e.g. ".MPG" is also found
            if fileName.lower().endswith(file_extensions):
                # file exists
                # print(f"File: {os.path.join(rootPath, fileName)}")
                files.append(fileName)
        break  # prevent descending into subfolders
    return files


def get_steps_title(sim_file_lines):
    for line in sim_file_lines:
        if TITLE_LABEL in line:
            return re.findall(f'{TITLE_LABEL}(.*?);', line, re.DOTALL)[0]


def get_steps_bg_video(sim_file_lines):
    for line in sim_file_lines:
        if BGCHANGES_LABEL in line:
            return re.findall('=(.*\.[\w\d]+)=', line, re.DOTALL)[0]
