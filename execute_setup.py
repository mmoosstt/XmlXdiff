import os
import sys
import subprocess
import shutil


root_path = __file__[:__file__.rfind('\\')]

python_path = sys.exec_prefix
cmd = "{python_path}\\python.exe setup.py bdist_wheel".format(
    python_path=python_path)

_ret = subprocess.Popen(cmd, shell=False, cwd=root_path)
_ret.wait()

try:
    shutil.rmtree('build')
except FileNotFoundError:
    pass

try:
    shutil.rmtree('{path}\\lib\\XmlXdiff.egg-info'.format(path=root_path))
except FileNotFoundError:
    pass
