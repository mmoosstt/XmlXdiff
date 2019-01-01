# coding:utf-8
# Author:  mmoosstt -- github
# Purpose: timing analysis for XmlXdiff
# Created: 01.01.2019
# Copyright (C) 2019, Moritz Ost
# License: TBD


import timeit


print(timeit.timeit(setup="import xDiffXml.xDiffCore as api",
                    stmt="api.xDiffExecutor().run()",
                    number=10))
