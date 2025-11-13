## first you have to install git
install git from this link: https://git-scm.com/install
## second
open up the terminal and type:
``` bash
git clone https://github.com/JohnDoggoLover/YEEP-plus-plus
cd YEEP-plus-plus
```

# This is How to build the yeep++ yppi  executable

*note that this may be different between platforms*

### 1
###### make sure that you have python installed as we're going to use pyinstaller
open up the terminal in the yeep++ folder and type: 
``` bash
python -m PyInstaller --onefile yppi.py
copy ./dist/yppi.exe ./
del dist
del build
```
### 2 
##### now we fcan run yppi.exe!
``` bash
./yppi.exe ./hello.ypp
```
