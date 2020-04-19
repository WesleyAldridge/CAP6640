v#!/usr/bin/env bash

# requires elevation
# this script will set venv so that dependencies do not need
# to be maintained in Github

echo "*******************************************************"
echo "Creating python virtual environment, fetching libraries"
echo "and dependencies."
echo "*******************************************************"

sudo apt install libffi-dev libnacl-dev python3-dev

directory_name=${PWD##*/}
cd ..
python3 -m venv ${directory_name}
cd ${directory_name}
source ./bin/activate
pip3 install discord.py
pip3 install -U setuptools
pip3 install tensorflow
pip3 install keras
pip3 install nltk
unset directory_name

echo "******************************************"
echo "Do not forget to run \"source bin/activate\""
echo "******************************************"



