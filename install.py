import os
import sys
import subprocess

root_path = __file__[:__file__.rfind('\\')]

python_path = sys.exec_prefix
cmd = "{python_path}\\python.exe -m pip install {path}\\dist\\XmlXdiff-0.1-py3-none-any.whl".format(
    python_path=python_path,
    path=root_path)

subprocess.Popen(cmd, shell=False, cwd=root_path)
