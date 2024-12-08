#! /bin/bash
conda create -n detective python=3.10 -y
echo "conda environment created"
conda activate detective
pip install -r requirements.txt
sudo chmod +x run.sh
./run.sh