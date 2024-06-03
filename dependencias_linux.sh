#!/bin/bash

echo "Instalando dependencias"

sudo apt update
sudo apt upgrade -y
sudo apt install python3 -y
sudo apt install python3-pip -y
sudo apt install python3-venv -y
sudo apt install python3-dev -y
sudo apt-get install libcairo2-dev -y
sudo apt-get install python3-tk python3-dev -y
pip3 install Flask
pip3 install flask_cors
pip3 install pyautogui
pip3 install SpeechRecognition
pip3 install pydub
pip3 install selenium
python3 -m venv venv
# source venv/bin/activate
pip3 install xlrd
pip3 install -r requirements.txt
pip install PyPDF2
pip install matplotlib
pip install scipy
sudo apt install sqlite3 -y


echo "Dependencias Instaladas"


