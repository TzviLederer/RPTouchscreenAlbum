# RP Touchscreen Album
Displaying images on raspberry pi 7" touchscreen

## Description
The script will display images in loop on raspberry pi touchscreen.  
The images will be resized and cropped to fit the screen without distortion.  
Use it for horizontal images, the code will work for vertical images, but they will be cropped.  
Supported images formats:
 - .jpg
 - .jpeg
 - .png


## How to use
### requirements
 - python 3

### install environment
After installing python and pip, run `pip install -r requirements.txt` from the project directory. 
All requirements will be installed.

### run
run the script:  
```python3 main.py -p <path/to/data/dir>```  
To change the waiting time for each image, run:  
```python3 main.py -p <path/to/data/dir> -t <time_in_seconds>```  
To exit the code, type 'q' or ESC.  

### add reminders
The project supports three different reminders:
 - Weekly reminders
 - Monthly reminders
 - One time reminders   

To set a reminder, add it to the `reminders.txt` file, or specify another file with `-r` flag 
(e.g. `python3 main.py -p path/to/directory -r path/to/reminders.txt`).  
The file will have the following format:  
type;time;message  

**Types:**  
 - `w` for weekly
 - `m` for monthly
 - `o` for once  

**Times:**  
 - 1-7 for weekly reminders (1-sunday, 7-saturday)
 - 1-31 for monthly reminders (1 - first in the mont)
 - dd/mm/yyyy for once - date  

Examples:  
w;3;Yoga - reminder every thursday with "Yoga" message.  
o;2/12/2020;Meeting with the devil - the reminder will be set to 2/12/2020.  
More examples in the `reminders.txt` file in this repository.  

### Handle reminders
When the time arrive, the reminders will be shown at the top of the screen.  
To mark them as done, press on the bar, and a list will appear.  
Press on the rectangles aside messages to mark them as read, they will not be shown in the bar after that. 