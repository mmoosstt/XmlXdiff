import os
import sys
import subprocess

root_path = __file__[:__file__.rfind('\\')]

python_path = sys.exec_prefix

cmd_uninstall = "{python_path}\\python.exe -m pip uninstall XmlXdiff".format(
    python_path=python_path,
    path=root_path)

cmd_install = "{python_path}\\python.exe -m pip install {path}\\dist\\XmlXdiff-0.3.0-py3-none-any.whl".format(
    python_path=python_path,
    path=root_path)

_ret = subprocess.Popen(cmd_uninstall, shell=False, cwd=root_path)
_ret.wait()

subprocess.Popen(cmd_install, shell=False, cwd=root_path)
_ret.wait()
