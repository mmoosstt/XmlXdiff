import unittest
import sys
import os
import io

sys.stdout = io.StringIO()

sys.path.append(os.path.abspath("./tests"))
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
test_suite.addTest(CompareAll('test11'))

test_runner = unittest.TextTestRunner(verbosity=2)
res = test_runner.run(test_suite)

sys.stdout.flush()
sys.stdout.seek(0)

f = open('./tests/GeneralTests.CompareAll.txt', 'w')
f.write(sys.stdout.read())
f.close()