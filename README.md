If all fails:

Inside Software:

inspector.py filename
-Is a tool to open an image in matplotlib and inspect each pixels value. Useful for tuning thresholds. 

core.py
- Runs the multiple bug detection algorithm on an image taken at the run time, detects bugs and then loops. 

Core.py 
- Opens an image in the software directory and runs bug detection on it once. 

bugDetect.py 
- The Multibug image detection that checks for consentric and small bugs.
- The algorithm that both core.py and Core.py use. 

main.py
- runs single bug image detection multiple times on an image taken at run time. 

mainTimedRun.py 
- runs single bug image detection once and times it. 

bugDetectFast.py
- The file that the main files call. Returns [minx,miny,maxx,maxy] to make a rectangle from. 

ledsTest.py 
- Tests the leds.py file that turns the Pi LEDs off and on.


