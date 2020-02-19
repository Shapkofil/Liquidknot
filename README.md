# Liquidknot
---
### Ray-Marching Rendering Engine for Blender
---
## Installation
### Requirements
- Blender (2.80 or higher)  
[https://www.blender.org/download/](https://www.blender.org/download/)
- Python (3.5 or higher)  
[https://www.python.org/](https://www.python.org/)
- Virtualenv module  
[https://pypi.org/project/virtualenv/](https://pypi.org/project/virtualenv/)
```bash
pip install virtualenv
# or
python -m pip install virtualenv
```
### Installation
#### Pre-build archives
- __Coming soon__
#### User Universal Install
- Download the master branch as a zip
- Open Blender
- Go to Edit->Preferences->Addons
- Click the install... button (top right)
- Select the __*.zip__ archive you downloaded
- Search for liquidknot (top right)
- Check the check box  
**First time enabling the addon should take around 30 seconds before the check appears**
#### Dev Install
- Clone dev branch  
**_CLONE INTO BLENDER'S scripts addons FOLDER_**  
[https://docs.blender.org/manual/en/latest/editors/preferences/file_paths](https://docs.blender.org/manual/en/latest/editors/preferences/file_paths)
- (optional) You can create the virtualenv yourself:
```bash
# In the main addon's directory
virtuanenv openGL/.venv
source openGL/.venv/bin/activate
pip install -r requirements.txt
```
- Follow the steps 2-8 from User Universal Install

- Dev Docs:
__Coming soon__
### Usage
- open demo/demo.blend in blender  
Thats a document used by me for testing features.  
Should give you a great understanding of most features
