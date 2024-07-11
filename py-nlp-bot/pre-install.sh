#!/bin/bash

# Create virtual environment
python3 -m venv myenv

# Activate the virtual environment
source myenv/bin/activate

# Install requirements
pip install -r requirements.txt

# Install ffmpeg
brew install ffmpeg