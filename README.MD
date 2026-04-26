# Creature Barn
This application allows the user to collect and manage monster and NPC character sheets in a local SQLite database.

## Installation
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