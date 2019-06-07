"""
 coding:utf-8
 Author:  mmoosstt -- github
 Purpose: inteface for diffx
 Created: 01.01.2019
 Copyright (C) 2019, diponaut@gmx.de
 License: TBD
"""

import os


def get_path():
    """
    get folder path of diffx independent from deployment.
    purpose unittesting/debugging

    return: path 
    """

    return __file__.replace('\\__init__.py', "")
