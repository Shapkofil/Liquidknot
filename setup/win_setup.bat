cd ..\openGL
pip install virtualenv --user
python -m virtualenv %cd%\.venv
%cd%\.venv\Scripts\pip.exe install -r %cd%\..\setup\requirements.txt
mkdir temp