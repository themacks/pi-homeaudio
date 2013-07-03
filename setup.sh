#!/bin/bash

echo "Getting webpy..."
git clone https://github.com/webpy/webpy.git
touch ./webpy/__init__.py

echo "Installing flup..."
sudo apt-get install python-setuptools
sudo easy_install flup
