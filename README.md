# XmlXdiff #

XmlXdiff was inspired by [X-Diff](http://www.inf.unibz.it/~nutt/Teaching/XMLDM1112/XMLDM1112Coursework/WangEtAl-ICDE2003.pdf "X-Diff: An Effective Change Detection Algorithm for XML Documents").

This is not a bullet prove library (till now). It s more a playground to get in touch with comparing tree structures and presenting the resulting in a charming way.

## dependencies ##
 * PySide2
 * svgwrite
 * lxml
 
## installation ##

```
python pip XmlXdiff
```

## fist step ##
```
from XmlXdiff.XReport import DrawXmlDiff

_xml1 = """<root><deleted>with content</deleted><unchanged/><changed name="test1" /></root>"""
_xml2 = """<root><unchanged/><changed name="test2" /><added/></root>"""

with open("test1.xml", "w") as f:
    f.write(_xml1)

with open("test2.xml", "w") as f:
    f.write(_xml2)

x = DrawXmlDiff("test1.xml", "test2.xml")
x.saveSvg('xdiff.svg')

```

# status quo #
![XmlXdiff example](https://github.com/mmoosstt/XmlXdiff/blob/master/tests/test1/xdiff_a_b.svg "XmlXdiff/tests/test1")

 
# implementation #
 
 Each xml element is identified by it's xpath and a hash calculated by selecting relevant information.
  
 1. mark all xml elements as changed
 1. mark unchanged xml elements
 1. mark moved xml elements
 1. mark xml elements identified by tag name and attribute names
 1. mark xml elements identified by attributes values and element text
 1. mark xml elements identified by tag name
 1. mark xml elements with xpath that do not exist in the other xml tree as added/deleted
 1. mark xml elements that have no child xml elements that are marked as changed as verified
 1. all xml elements that are still marked as changed have to be investigated
 
The selected order may change in future. This is still under investigation. 

## performance ##

[//]: # (insert_performance_start)

```
test1: delta_t=0.1219s xml_elements=63
test2: delta_t=0.0224s xml_elements=5
test3: delta_t=0.0196s xml_elements=4
test4: delta_t=0.1023s xml_elements=32
test5: delta_t=0.0728s xml_elements=34
test6: delta_t=0.0721s xml_elements=34
test7: delta_t=0.0189s xml_elements=8
test8: delta_t=0.1271s xml_elements=67
test9: delta_t=7.7058s xml_elements=6144
test11: delta_t=0.0746s xml_elements=34

```

[//]: # (insert_performance_end)

## open issues ##
 * xdiff cost rating for matching couples
 * performance analysis and improvements (different hash algorithms, ...)
 * rework xml elements identification readability/performance issues
 * if there are some users, improve interface

## documentation ##
![Tests](./doc/tests.md "Executed Tests")
