#!/bin/bash

PYTHON_INTERPRETER=$(which python3)
echo "Current Python interpreter: $PYTHON_INTERPRETER"
cd detective/runner
sudo $PYTHON_INTERPRETER utils.py