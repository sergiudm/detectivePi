import sys
import os

def add_path():  
    # 使用os.path.join确保路径的正确性，并替换环境变量
    path_to_add = os.path.join(os.environ['HOME'], os.environ['USER'], 'detectivePy')

    # 将路径添加到sys.path
    sys.path.append(path_to_add)

