import coverage
import unittest
import sys
import os
import io

sys.path.append(os.path.abspath("./tests"))
cov = coverage.Coverage()
cov.start()

from test_general import CompareAllXmls, ReportModule, CompareAllJsons

test_suite = unittest.TestSuite()
# test_suite.addTest(ReportModule('testXSvgColoredText'))
# test_suite.addTest(ReportModule('testXSvgCompact'))
# test_suite.addTest(ReportModule('testXSvgColorOnly'))
test_suite.addTest(CompareAllXmls('test1'))
test_suite.addTest(CompareAllXmls('test2'))
test_suite.addTest(CompareAllXmls('test3'))
test_suite.addTest(CompareAllXmls('test4'))
test_suite.addTest(CompareAllXmls('test5'))
test_suite.addTest(CompareAllXmls('test6'))
test_suite.addTest(CompareAllXmls('test7'))
test_suite.addTest(CompareAllXmls('test8'))
test_suite.addTest(CompareAllXmls('test9'))
test_suite.addTest(CompareAllJsons('test15'))

test_runner = unittest.TextTestRunner(verbosity=2)
res = test_runner.run(test_suite)

cov.stop()
cov.save()
cov.html_report(directory="./tests/coverage",
                omit=['./tests/*',
                      'pyscript'])

with open("./tests/GeneralTests.Coverage.txt", "w") as f:
    cov.report(file=f,
               omit=['./tests/*',
                     'pyscript'])
