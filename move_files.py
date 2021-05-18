import os
import re
import shutil
import tkinter as tk
from pathlib import Path
from tkinter.filedialog import askdirectory


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
    move_folder = askdirectory(title='Folder to move simfiles')
    if move_folder == "":
        print("No folder selected, quitting")
        return
    print(f"Move to folder: {move_folder}")
    return search_folder, move_folder


def move_files(files, checks):
    moved_file_count = 0
    search_dir, target_dir = folder_selection()
    for file_path in files(search_dir):
        try:
            # if simfile is already in target dir, skip
            if os.path.dirname(file_path) in target_dir:
                continue
            file_dir = os.path.dirname(file_path)
            if checks(file_dir):
                origin_dir = file_dir
                target_dir = target_dir
                shutil.move(origin_dir, target_dir)
                moved_file_count += 1
                print(f"Moved '{file_dir}'")
            else:
                continue
        except shutil.Error as e:
            if "already exists" in str(e):
                duplicate_dir_from = Path(origin_dir)
                file_size_from = sum(f.stat().st_size for f in duplicate_dir_from.glob('**/*') if f.is_file())
                e_str = str(e)
                res = re.findall(r'\'(.*?)\'', e_str)
                duplicate_dir_to = Path(res[0])
                file_size_to = sum(f.stat().st_size for f in duplicate_dir_to.glob('**/*') if f.is_file())
                if file_size_from == file_size_to:
                    print(f"Duplicate found (already exists in target dir): '{file_dir}'")
                    print(f"removing...")
                    shutil.rmtree(origin_dir)
                    print(f"Successfully removed!")
                else:
                    print(f"Simfile with duplicate name found, but different size: '{file_dir}'")
            else:
                print('Error: %s' % e)
            continue
    print(f"Moved '{moved_file_count}' simfiles to the target dir")
