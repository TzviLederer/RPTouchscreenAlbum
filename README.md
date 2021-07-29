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
run the script:  
```python3 main.py -p <path/to/data/dir>```  
To change the waiting time for each image, run:  
```python3 main.py -p <path/to/data/dir> -t <time_in_seconds>```  
To exit the code, type 'q' or ESC.  
