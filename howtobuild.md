# This is How to build the yeep++ yppi and yppc executables

*note that this may be different between platforms*

### 1
###### make sure that you have python installed as we're going to use pyinstaller
open up the terminal in the yeep++ folder and type: 
``` bash
pyinstaller --onefile yppi.py
copy ./dist/yppi.exe ./
del dist
del build
pyinstaller --onefile yppc.py
copy ./dist/yppc.exe ./
del dist
del build
```
### 2
#### compiling the hello.ypp program
``` bash
yppc.exe hello.ypp
```
### 3
#### running the now compiled program
``` bash
hello.exe
```

### optional
#### you can also use the yeep plus plus interpreter
``` bash
yppi.exe hello.ypp
```