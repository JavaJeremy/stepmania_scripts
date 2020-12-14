import tkinter as tk
from tkinter.filedialog import askdirectory
import os


def get_folder():
    # select folder
    root = tk.Tk()
    root.withdraw()
    path_to_folder = askdirectory(title='Select Folder')
    if path_to_folder == "":
        raise Exception("No folder selected, quitting")
    print(f"Folder: {path_to_folder}")
    return path_to_folder


def main():
    """
    Creates simfile folder with empty template files and some basic infos in the .ssc file
    """
    try:
        # get necessary data
        parent_dir = get_folder()
        song_name = input('Song name:')
        song_subtitle = input('Subtitle (optional):')
        artist_name = input('Artist name:')
        simfile_creator = input('Simfile creator (optional):')
        # logging
        if not song_subtitle:
            print(f"{song_name} by {artist_name}")
        else:
            print(f"{song_name} ({song_subtitle}) by {artist_name}")
        # create simfile
        simfile_path = os.path.join(parent_dir, song_name)
        os.mkdir(simfile_path)
        # create empty files for simfile
        step_file_name = f"{song_name}.ssc"
        music_file_name = f"{song_name}.ogg"
        banner_file_name = f"{song_name}.png"
        bg_file_name = f"{song_name}-bg.png"
        jacket_file_name = f"{song_name}-jacket.png"
        video_file_name = f"{song_name}.avi"
        for file_name in [step_file_name,
                          music_file_name,
                          banner_file_name,
                          bg_file_name,
                          jacket_file_name,
                          video_file_name]:
            open(os.path.join(simfile_path, file_name), "w")
    except Exception as error:
        print(str(error))


main()
