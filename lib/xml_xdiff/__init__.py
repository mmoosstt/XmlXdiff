"""
 coding:utf-8
 Author:  mmoosstt -- github
 Purpose: root module
 Created: 01.01.2019
 Copyright (C) 2019, diponaut@gmx.de
 License: TBD
"""

import os


def getPath():
    """
    return: path of the model __init__.py is located in.
    """

    return __file__.replace('\\__init__.py', "")
