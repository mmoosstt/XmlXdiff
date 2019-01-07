import re


def readmeUpdatePerformanceInfo():

    _path_readme = './README.md'
    _path_report = './tests/GeneralTests.CompareAll.txt'

    _performance_str = """
[//]: # (insert_performance_start)

```
{insert}
```

[//]: # (insert_performance_end)
"""

    _re_performance = """
\[//\]: # \(insert_performance_start\)
.*
\[//\]: # \(insert_performance_end\)
"""

    with open(_path_readme, "r") as f:
        _content = f.read()

    _md_performance = re.findall(_re_performance, _content, re.M | re.S)[0]

    with open(_path_report, 'r') as f:
        _performance_unittest = f.read()

    _content = _content.replace(_md_performance,
                                _performance_str.format(insert=_performance_unittest))

    with open(_path_readme, "w") as f:
        _content = f.write(_content)


def readmeUpdateCoverageInfo():

    _path_readme = './README.md'
    _path_report = './tests/GeneralTests.Coverage.txt'

    _performance_str = """
[//]: # (insert_coverage_start)

```
{insert}
```

[//]: # (insert_coverage_end)
"""

    _re_performance = """
\[//\]: # \(insert_coverage_start\)
.*
\[//\]: # \(insert_coverage_end\)
"""

    with open(_path_readme, "r") as f:
        _content = f.read()

    _md_performance = re.findall(_re_performance, _content, re.M | re.S)[0]

    with open(_path_report, 'r') as f:
        _performance_unittest = f.read()

    _content = _content.replace(_md_performance,
                                _performance_str.format(insert=_performance_unittest))

    with open(_path_readme, "w") as f:
        _content = f.write(_content)


readmeUpdatePerformanceInfo()
readmeUpdateCoverageInfo()
