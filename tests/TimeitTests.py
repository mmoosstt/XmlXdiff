# coding:utf-8
# Author:  mmoosstt -- github
# Purpose: timing analysis for XmlXdiff
# Created: 01.01.2019
# Copyright (C) 2019, diponaut@gmx.de
# License: TBD


import timeit


print(timeit.timeit(setup="import XmlXdiff.XDiffer as api",
                    stmt="api.XDiffExecutor().run()",
                    number=10))
