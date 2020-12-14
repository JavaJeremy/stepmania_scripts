import os


def has_video_file(simfolder, video_extensions):
    for rootPath, dirs, filenames in os.walk(simfolder):
        for fileName in filenames:
            # lower() -> case insensitive so e.g. ".MPG" is also found
            if fileName.lower().endswith(video_extensions):
                # video file exists
                # print(f"Video: {os.path.join(rootPath, fileName)}")
                return True
        break  # prevent descending into subfolders
    return False
