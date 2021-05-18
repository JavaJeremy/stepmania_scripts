import tkinter as tk
from tkinter.filedialog import askdirectory
import os
import logging
from shared_constants import *
from shared_methods import get_files_of_type, get_steps_title


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
    Completes simfile folder by adding missing files (empty templates) and properties in the step file
    """
    try:
        # get necessary data
        simfile_path = get_folder()
        # simfile = os.path.dirname(chart_file_path)
        step_file = get_files_of_type(simfile_path, STEP_FILE_EXTENSIONS)[0]
        try:
            simfile = open(simfile_path + "/" + step_file, 'r', encoding=DEFAULT_ENCODING)
            simfile_lines = simfile.readlines()
            simtitle = get_steps_title(simfile_lines)
            if simtitle == "" or simtitle is None:
                print(f"No title found in file {simfile_path}")
                # TODO: DELETE AND CREATE STEP FILE BECAUSE SOMETHING IS BROKEN HERE
        except UnicodeDecodeError:
            # in case of this exception: open file and save again in utf-8 encoding
            print(f"Could not open {simfile.name} (change encoding to utf-8!)")
        except IndexError:
            print(f"Could not extract title from {simfile.name}")
        except PermissionError:
            print(f"Not allowed to open {simfile.name} - try as Admin!")
        song_name = simtitle if simtitle else input('Song name:')
        #TODO bis hier gekommen - hier gehts weiter...
        song_subtitle = input('Subtitle (optional):')
        artist_name = input('Artist name:')
        simfile_creator = input('Simfile creator (optional):')
        # logging
        # if not song_subtitle:
        #     print(f"{song_name} by {artist_name}")
        # else:
        #     print(f"{song_name} ({song_subtitle}) by {artist_name}")
        # create simfile
        # os.mkdir(simfile_path)
        # create empty files for simfile
        chart_file_name = f"{song_name}.ssc"
        music_file_name = f"{song_name}.ogg"
        banner_file_name = f"{song_name}.png"
        bg_file_name = f"{song_name}-bg.png"
        jacket_file_name = f"{song_name}-jacket.png"
        video_file_name = f"{song_name}.avi"
        for file_name in [chart_file_name,
                          music_file_name,
                          banner_file_name,
                          bg_file_name,
                          jacket_file_name,
                          video_file_name]:
            open(os.path.join(simfile_path, file_name), "w")
        with open(os.path.join(simfile_path, chart_file_name), 'w') as f:
            f.writelines(f"{TITLE_LABEL}{song_name};\n")
            f.writelines(f"{SUBTITLE_LABEL}{song_subtitle};\n")
            f.writelines(f"{ARTIST_LABEL}{artist_name};\n")
            f.writelines(f"{CREDIT_LABEL}{simfile_creator};\n")
            f.writelines(f"{MUSIC_LABEL}{music_file_name};\n")
            f.writelines(f"{BANNER_LABEL}{banner_file_name};\n")
            f.writelines(f"{BACKGROUND_LABEL}{bg_file_name};\n")
            f.writelines(f"{JACKET_LABEL}{jacket_file_name};\n")
            f.writelines(f"{BGCHANGES_LABEL}0.000={video_file_name}=1.000=0=0=1,99999.000=-nosongbg-=1.000=0=0=0"
                         f"=StretchNoLoop====;\n")
            # create empty difficulties
            difficulties = [
                ("Beginner", "1"),
                ("Easy", "3"),
                ("Medium", "5"),
                ("Hard", "7"),
                ("Challenge", "9")
            ]
            for difficulty, level in difficulties:
                f.writelines(f"//--------------- dance-single - {simfile_creator} ----------------\n")
                f.writelines(f"#STEPSTYPE:dance-single;\n")
                f.writelines(f"#DIFFICULTY:{difficulty};\n")
                f.writelines(f"#METER:{level};\n")
                f.writelines(f"#CHARTSTYLE:Pad;\n")
                f.writelines(f"#CREDIT:{simfile_creator};\n")
                f.writelines(f"#NOTES:;\n")
    except Exception as error:
        print(str(error))


main()
