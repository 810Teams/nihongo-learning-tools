# Progress Tracker

Progress Tracker application runs on Terminal.

## Download

The application is available download by clicking [Download ZIP](https://github.com/810Teams/progress-tracker/archive/master.zip).

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

## Setting Up

When running the application for the first time, follow these steps.
1. Open Terminal.
2. Change directory to the application folder.
3. Run `setup.sh` in your Terminal.

Running `setup.sh` will generates files and directories to make the application runs normally. Generated files and directories include `charts`, `data`, `DEFAULT_STORAGE.txt` and `DEFAULT_STYLE.txt`. Make sure they are all generated. If not, try running the script again, or contact the developer if you think this is a bug.

## Using an Application

1. Open Terminal.
2. Change directory to the application folder.
3. Run `run.sh` or `main.py` directly with Python.

If you are familiar with Shell script, you can put the application folder anywhere you want. Then create a Shell script file in a place where you can reach easily, like your Desktop. This shell script could includes the following.

```sh
cd <APPLICATION_FOLDER_PATH>
sudo chmod 755 run.sh
./run.sh
```

For full user manual guide, please read [HELP.md](HELP.md) included in the application folder.

## Notes

This application was originally made for personal use, I cannot guarantee anything.
