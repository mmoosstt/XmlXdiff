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


_path1 = '<insert xml filepath 1>'
_path2 = '<insert xml filepath 1>'

x = DrawXmlDiff(_path1, _path2)
x.save()
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

## open issues ##
 * xdiff cost rating for matching couples
 * performance analysis and improvements (different hash algorithms, ...)
 * rework xml elements identification readability/performance issues

## documentation ##
![Tests](./doc/tests.md "Executed Tests")
