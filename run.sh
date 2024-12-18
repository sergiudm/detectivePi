#!/bin/bash

# 切换到你希望的工作目录，替换下面的路径为你的实际路径
# WORKING_DIRECTORY="$HOME/$USER/detectivePy"
# cd "$WORKING_DIRECTORY"

# # 检查目录是否成功切换
# if [ $? -eq 0 ]; then
#     echo "Changed directory to $WORKING_DIRECTORY"
# else
#     echo "Failed to change directory to $WORKING_DIRECTORY"
#     exit 1
# fi



# 查找并使用 python3 解释器
PYTHON_INTERPRETER=$(which python3)
echo "Current Python interpreter: $PYTHON_INTERPRETER"
$PYTHON_INTERPRETER path.py add_path 
# 使用找到的解释器执行 main.py
sudo $PYTHON_INTERPRETER main.py
1