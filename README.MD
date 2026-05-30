# Creature Barn
This application allows the user to collect and manage monster and NPC character sheets in a local SQLite database.

## Installation
### Pre-requisites
You need to have Python3 installed on your system.  You can find the official installation at [Python.org](https://python.org).  
You need to have git installed on your system.  You can find the official installation at [git-scm.com](https://git-scm.com/).  
Then you can clone this repository from [GitHub](https://github.com/mggates39/CreatureBarn#)
```commandline
git clone https://github.com/mggates39/CreatureBarn.git
```


### Install TK-Inter
Ensure TCL/tk is installed:

Windows
```commandline
TK-Inter is fully installed with the base windwos python installation
```
Ubuntu
```commandline
sudo apt update
sudo apt install python3-tk
```
Fedora
```commandline
sudo dnf install python3-tkinter
```
### Setup local virtual runtime environment

Create a python virtual environment
```commandline
python -m venv myenv.
```
Activate the virtual environment

Windows
```commandline
.\myenv\Scripts\activate
```
Linux / MacOs
```commandline
source myenv/bin/activate
```
Install the external requirements
```commandline
pip install -r requirements.txt
```
Run the main code
 ```commandline
python main.py
```
Now initialize the database from within the application.

### Usage 
```
usage: main.py [-h] [-v] [-p PATH] [-b] [-f FILE] [-t {NPC,Creature}]
               [-a {export,save,both}]

Simple Creature and NPC Stat Parser and Storage

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -p PATH, --path PATH  Directory to batch process, defaults to ./source
  -b, --batch           Batch process all files in path
  -f FILE, --file FILE  file to process
  -t {NPC,Creature}, --type {NPC,Creature}
                        Type of the file or files in the path, default is NPC
  -a {export,save,both}, --action {export,save,both}
                        Action to perform on the batch or file, defaults to
                        export
```