# Liquidknot
---
### Ray-Marching Rendeting Engine for Blender
---
## Installation
### Requirements
- Linux distro (Ubuntu, PopOS, est.)  
soon comming for Windows and MacOS
- Blender (2.79 or higher)  
[https://www.blender.org/download/](https://www.blender.org/download/)
- Python (3.5 or higher)  
[https://www.python.org/](https://www.python.org/)
- Virtualenv module  
[https://pypi.org/project/virtualenv/](https://pypi.org/project/virtualenv/)
```bash
pip install virtualenv
```
### Installation
#### The easy way **_UNSTABLE_**
- ~~Download the master branch as a zip~~
- ~~Open Blender~~
- ~~Go to Edit->Preferences->Addons~~
- ~~Click the install... button (top rigth)~~
- ~~Select the __*.zip__ archive you downloaded~~
#### The hard way _(but stable)_
- **_CLONE INTO BLENDER'S scripts addons FOLDER_**  
[https://docs.blender.org/manual/en/latest/editors/preferences/file_paths](https://docs.blender.org/manual/en/latest/editors/preferences/file_paths)
- run setup.sh
```bash
# In the main addon's directory
chmod +x setup.sh 
./setup.sh
```
- alternatively you can create the virtualenv yourself:
```bash
# In the main addon's directory
virtuanenv openGL/.venv
source openGL/.venv/bin/activate
pip install -r requirements.txt
```
- enable Liquidknot inside Blender:  
Edit->Preferences->Addons->Liquidknot
### Usage
- open demo/demo.blend in blender  
Thats a document used by me for testing features.  
Should give you a great understanding of most features
