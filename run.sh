#!/bin/bash

PYTHON_INTERPRETER=$(which python3)
echo "Current Python interpreter: $PYTHON_INTERPRETER"
cd detective/
sudo $PYTHON_INTERPRETER main.py