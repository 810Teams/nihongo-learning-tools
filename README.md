# Kanji Tracker
Kanji Tracker application runs on Terminal.

## Download
The application is available for download in the [Releases](https://github.com/810Teams/personal-kanji-tracker/releases) tab. If not available in the releases tab, [download zip](https://github.com/810Teams/personal-kanji-tracker/archive/master.zip) instead on the master branch.

## Compatibility
This application was originally made for personal use and developed on Mac OS X, which is guaranteed to be compatible when runs on Mac OS X. Since this application runs on Terminal, Linux is probably compatible too. Lastly, running this application on Windows' cmd is not guaranteed to be compatible.

## Requirements

### Python
This application requires your device to have Python installed, can be downloaded from [python.org/downloads](https://www.python.org/downloads/).

### Additional Python Libraries
After having python installed, run these commands on Terminal.
```
pip3 install numpy
pip3 install pandas
pip3 install pygal
```

## Running Scripts

If you have already known how to run Shell scripts and Python via Terminal, you can skip this part. If not, please read the following.

### Shell Script

Running Shell script has 2 methods. First, changing directories to where the application folder is, then type this into the Terminal. Assuming `run.sh` is the Shell script file name.
```
./run.sh
```
Another method is dragging `run.sh` into your Terminal and press the ENTER key directly.

### Python

Running python has 2 methods. First, changing directories to where the application folder is, then type this into the Terminal. Assuming `main.py` is the Python file name.
```
python3 main.py
```
Another method is typing `python3 ` into in Terminal first, then drag `main.py` into your Terminal and press the ENTER key.

## Setting Up

When running the application for the first time, run `setup.sh` in your Terminal first. This will generates files and directories to make the application runs normally.

Generated files and directories include `charts`, `data`, `DEFAULT_STORAGE.txt` and `DEFAULT_STYLE.txt`. Make sure they are all generated. If not, try running the script again, or contact the developer if you think this is a bug.

## Using an Application

Running application has 2 methods. First, runs the shell script file called `run.sh` in the Terminal or else, runs `main.py` with Python directly. Running methods can be read at the section <a href="#running-scripts">Running Scripts</a>.

## Notes
This application was originally made for personal use, I cannot guarantee anything.
