# coding:utf-8
# Author:  mmoosstt -- github
# Purpose: timing analysis for XmlXdiff
# Created: 01.01.2019
# Copyright (C) 2019, diponaut@gmx.de
# License: TBD

import cProfile
import sys
import unittest
import os
import XmlXdiff.XDiffer as api
sys.path.append(os.path.abspath("./tests"))
from GeneralTests import CompareAll

test_suite = unittest.TestSuite()
test_suite.addTest(CompareAll('test9'))
test_runner = unittest.TextTestRunner(verbosity=2)

_x = cProfile.run('test_runner.run(test_suite)')

i = 0
