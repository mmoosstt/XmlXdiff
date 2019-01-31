import os
import sys
import subprocess
import svgwrite

root_path = __file__[:__file__.rfind('\\')]

python_path = sys.exec_prefix

cmd_set_env1 = "set MYPYPATH={python_path}\\Lib\\site-packages\n".format(
    python_path=python_path)
cmd_mypy = "{python_path}\\Scripts\\mypy.exe --config-file {path}\\tests\\mypy\\mypy.ini {path}\\lib\\XmlXdiff\n".format(
    python_path=python_path,
    path=root_path)

_process = subprocess.Popen('cmd', stdin=subprocess.PIPE,
                            shell=False, cwd=root_path)
#_process.stdin.write(cmd_set_env1.encode('utf-8'))
_process.stdin.write(cmd_mypy.encode('utf-8'))
_process.communicate()

_process.wait()
