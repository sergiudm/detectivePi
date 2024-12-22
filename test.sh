#!/bin/bash

PYTHON_INTERPRETER=$(which python3)
echo "Current Python interpreter: $PYTHON_INTERPRETER"

sudo $PYTHON_INTERPRETER -m detective.modules.music_player