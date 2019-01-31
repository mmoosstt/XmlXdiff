import coverage
import unittest
import sys
import os
import io

sys.path.append(os.path.abspath("./tests"))
cov = coverage.Coverage()
cov.start()

from GeneralTests import CompareAll
test_suite = unittest.TestSuite()
test_suite.addTest(CompareAll('test1'))
test_suite.addTest(CompareAll('test2'))
test_suite.addTest(CompareAll('test3'))
test_suite.addTest(CompareAll('test4'))
test_suite.addTest(CompareAll('test5'))
test_suite.addTest(CompareAll('test6'))
test_suite.addTest(CompareAll('test7'))
test_suite.addTest(CompareAll('test8'))
test_suite.addTest(CompareAll('test9'))

test_runner = unittest.TextTestRunner(verbosity=2)
res = test_runner.run(test_suite)

cov.stop()
cov.save()
cov.html_report(directory="./tests/coverage",
                omit=['./tests/*',
                      'pyscript'])

with open("./tests/GeneralTests.Coverage.txt", "w") as f:
    cov.report(file=f,
               omit=['./tests/*'])
