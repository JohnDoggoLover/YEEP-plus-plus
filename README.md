# This is how to use the yeep++ tooling on linux, check the "howtobuild.md" file too see how to build yeep++ executibles on other platforms
## you have to clone the repository first
```bash
git clone https://github.com/JohnDoggoLover/YEEP-plus-plus
cd YEEP-plus-plus
```
## option 1
#### using yppi
```bash
./yppi ./hello.ypp 
```
## option 2
#### using yppc
###### ***this option requires you to have pyinstaller installed***
```bash
./yppc ./hello.ypp
clear
./hello
```
***note the reson I put clear there is becuase yppc outputs a lot of diagnostic data and  if you run two commands like that it doesn't show the input line***
## optional
I recomend adding the YEEP-plus-plus folder to path!
```bash
echo 'export PATH="$PATH:/path/to/the/yeep/plus/plus/folder"' >> ~/.bashrc
source ~/.bashrc
```
