import os
import glob
import logging
import re

from move_files import move_files
from shared_methods import get_folder, DEFAULT_ENCODING, get_steps_bg_video, BGCHANGES_LABEL


def update_step_file(file_path, new_file_type):
    simfile = open(file_path, 'r', encoding=DEFAULT_ENCODING)
    try:
        simfile_lines = simfile.readlines()
        bg_video_name = get_steps_bg_video(simfile_lines)
        if bg_video_name == "" or bg_video_name is None:
            print(f"No background video property found in file {file_path}")
        else:
            # CAREFUL: THIS EMPTIES FILE IF NOTHING IS DONE INSIDE HERE
            with open(file_path, 'w', encoding=DEFAULT_ENCODING) as file_writer:
                for f_line in simfile_lines:
                    if BGCHANGES_LABEL in f_line:
                        updated_line = re.sub("(=.*\.)[a-zA-Z]+(=)", f"\\1{new_file_type}\\2", f_line)
                        file_writer.writelines(updated_line)
                    else:
                        file_writer.writelines(f_line)
                        continue
    except UnicodeDecodeError:
        # in case of this exception: open file and save again in utf-8 encoding
        logging.error(f"Could not open {simfile.name} (change encoding to utf-8!)")
    except IndexError:
        logging.error(f"Could not extract background video property from {simfile.name}")


def convert_mpg():
    return None


def convert():
    """
    Converts all background videos with .mpg filetype to a different type
    because of a bug that makes them play back too fast in endless mode, and other modes
    keeps old .mpg file and renames it as backup
    :return:
    """
    try:
        # get necessary data
        parent_dir = get_folder()
        simfile_mpg_path_list = get_chart_with_mpg(parent_dir)
        i = 0
        for simfile_path in simfile_mpg_path_list:
            i += 1
            simfile_folder = os.path.dirname(simfile_path)
            simfile_name = os.path.basename(simfile_path)
            print(f"{i:03d}.Simfolder: {simfile_folder} - {simfile_name}")
            os.chdir(f"{parent_dir}/{simfile_folder}")
            simfile_step_path_list = glob.glob("*.ssc") + glob.glob("*.sm")
            # This needs to be tested first
            # for simfile_step_path in simfile_step_path_list:
            # update_step_file(simfile_step_path, "avi")

        mpg_count = i
        total_folder_count = len(next(os.walk(parent_dir))[1])
        mpg_percentage = mpg_count / (total_folder_count / 100)
        print(f"Simfiles with .mpg in percent ({mpg_count} out of {total_folder_count}): {int(mpg_percentage)}%")
    except Exception as error:
        print(str(error))


def get_chart_with_mpg(src_dir):
    # find simfiles with buggy filetype
    os.chdir(src_dir)  # set default folder for glob search
    return glob.glob("**/*.mpg", recursive=True)  # case insensitive


def main():
    def check(simfile):
        return True

    # convert()
    move_files(get_chart_with_mpg, check)


main()
