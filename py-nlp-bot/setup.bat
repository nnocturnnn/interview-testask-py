@echo off

rem Create virtual environment
python -m venv myenv

rem Activate the virtual environment
myenv\Scripts\activate

rem Install requirements
pip install -r requirements.txt

choco install ffmpeg