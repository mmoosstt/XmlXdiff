import os
import sys
import subprocess
import shutil

try:
    shutil.rmtree('build')
except FileNotFoundError:
    pass

root_path = __file__[:__file__.rfind('\\')]

python_path = sys.exec_prefix
cmd = "{python_path}\\python.exe setup.py bdist_wheel".format(
    python_path=python_path)

subprocess.Popen(cmd, shell=False, cwd=root_path)
