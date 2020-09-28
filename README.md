# Stepmania Scripts
Scripts to use for editing multiple simfiles at once.
# How to execute a script :rocket:
You need Python in order to execute a script.
You can download it [here](https://www.python.org/downloads/), make sure you have at least version 3.8.0.  
[![python_download](docs/python_download.png?raw=true)](#)  
Then you can execute the scripts by opening them with `python.exe`.  
[![example script file](docs/example_script_file.png?raw=true)](#)  

# #1 label_mv.py
## What it does  
[![example result](docs/example_results.png?raw=true)](#)  
1. Adds "[MV]" to all chart titles that have a background video.  
2. Removes "[MV]" from all chart titles (if it exists) that do not have a background video.  
## Usage
Select the any folder that has simfiles. It can be a single simfile folder, a collection or the entire Stepmania `Songs` folder:
[![Folder selection](docs/folder_selection.png?raw=true)](#)  
Click on `Select Folder`, and the script will start running immediatly.  
Click on `Cancel` to abort the script.  
[![example output](docs/example_output.png?raw=true "Example output")](#)  
## Details
Only chart files with the file extension `.sm` and `.ssc` are searched for and possibly edited. If any file with the file extension `.avi`, `.mpeg`, `.mpg` or `.mp4` (case-insensitive) is found in the same folder as the chart file, it is assumed that the simfile has a background video.
## Errors
All problems listed here can occur for each found simfile. The affected simfile is then skipped, and the process continues.
1. `No title found in file {simfilePath}`
Pretty self-explanatory I believe, just give your title in your chart a value.  
[![Missing title](docs/missing_title.png?raw=true)](#)  
1. `Could not open {simfile.name} (change encoding to utf-8!)`  
You can find that file and change the encoding to UTF8 to fix this issue.  
Here's an example of how to do it with the Win10 editor (on the bottom right you can see what encoding the file is currently in):
[![Save with UTF8 encoding](docs/save_with_utf8.png?raw=true "Title")](#)  
Since I only had a few files that were encoded this way I just fixed them manually. If you happen to get this error for too many files to change manually then this script is unfortunately not for you.   
 ...unless you can add some code to deal with this and send me a pull request ;)
