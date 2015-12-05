# XTD  
This is a driver for the XTD utilizing the Raspberry Pi.  

# Installation and Usage  
Download the code from the [respository](https://github.com/rshin808/XTD).  
Go to the mainDriver directory. The directory tree is shown below:  
```
XTD/
    examples/
    mainDriver/
```  
mainDriver contains the current working code for a default and interactive driver.  
In order to run the default driver  use the command:  
```
python defaultDriver.py
```

In order to run the interactive driver use the command:  
```
python driver.py
```

To set the defaultDriver.py to run on startup, edit the "/etc/rc.local" file.  
Add this line:  
```
python /path-to-XTD/XTD/mainDriver/defaultDriver.py &
```  
