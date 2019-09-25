# diffx #

diffx was inspired by [X-Diff](http://www.inf.unibz.it/~nutt/Teaching/XMLDM1112/XMLDM1112Coursework/WangEtAl-ICDE2003.pdf "X-Diff: An Effective Change Detection Algorithm for XML Documents").

Since version 0.3.2 the distance cost's algorithm is replaced by parent-identification. This might by a wrong decision but the result's for huge xml documents (see. test 9) improved in performance and quality. 

This is not a bullet prove library (till now). It s more a playground to get in touch with comparing tree structures and presenting the resulting in a charming way.

## dependencies ##
 * PySide2
 * svgwrite
 * lxml
 * dicttoxml
 
## installation ##

```
python pip diffx
```

## fist step ##

### xml file example ###
```
from diffx import main

_xml1 = './simple/xml1.xml'
_xml2 = './simple/xml2.xml'

main.compare_xml(_xml1, _xml2)
main.save('./simple/diffx_file.svg')

```

### xml string example ###
```
from diffx import main

_xml1 = """<root><deleted>with content</deleted><unchanged/><changed name="test1" /></root>"""
_xml2 = """<root><unchanged/><changed name="test2" /><added/></root>"""

main.compare_xml(_xml1, _xml2)
main.save('./simple/diffx_string.svg')

```

### json file example ###
```
from diffx import main

json1 = './simple/xml1.json'
json2 = './simple/xml2.json'

main.compare_xml(json1, json2)
main.save('./simple/diffx_file.svg')

```

# status quo #
![diffx example](https://github.com/mmoosstt/XmlXdiff/blob/master/tests/test14/xdiff_a_b.svg "XmlXdiff/tests/test1")

 
# implementation #
 
 Each xml element is identified by it's xpath and a hash calculated by selecting relevant information. Start with the identification of huge xml blocks (changed/moved). Identification of parent elements by tag, text-pre, text-post, attribute-names and attribute-values. Parent xml blocks can contain further parent xml blocks.
 
```
 <tag attribute-name:"attribute-value" ...> 
 text-pre 
 	<... children ...>
 text-post
 </tag>
```

 1. mark all xml elements as changed
 1. iterate over parent blocks, starting with maximum children to parent blocks with less children
 1. mark unchanged xml elements of current parent
 1. mark moved xml elements of current parent
 1. mark xml elements identified by tag name and attribute names of the current parent
 1. mark xml elements identified by attributes values and element text of the current parent
 1. mark xml elements identified by tag name of the current parent
 1. mark xml elements with xpath that do not exist in the other xml tree as added/deleted of the current parent
 1. Repeat 3. till all xml elements are identified

All xml elements that are still marked as changed have to be investigated

## performance ##

[//]: # (insert_performance_start)

```
test1: delta_t=0.0699s xml_elements=63
test2: delta_t=0.0104s xml_elements=5
test3: delta_t=0.0154s xml_elements=10
test4: delta_t=0.0240s xml_elements=32
test5: delta_t=0.0258s xml_elements=34
test6: delta_t=0.0290s xml_elements=34
test7: delta_t=0.0124s xml_elements=8
test8: delta_t=0.1027s xml_elements=67
test9: delta_t=4.2290s xml_elements=6144
test11: delta_t=0.0298s xml_elements=34
test12: delta_t=0.0288s xml_elements=45
test13: delta_t=0.0442s xml_elements=75

```

[//]: # (insert_performance_end)

## coverage ##

[//]: # (insert_coverage_start)

```
Name                             Stmts   Miss  Cover
----------------------------------------------------
lib\diffx\__init__.py               34      5    85%
lib\diffx\base.py                  107      2    98%
lib\diffx\differ.py                170     14    92%
lib\diffx\hash.py                   71      0   100%
lib\diffx\svg\__init__.py            0      0   100%
lib\diffx\svg\coloured_text.py      21      0   100%
lib\diffx\svg\compact.py           340     34    90%
lib\diffx\svg\render_text.py        76      2    97%
lib\diffx\xpath.py                  54      3    94%
----------------------------------------------------
TOTAL                              873     60    93%

```

[//]: # (insert_coverage_end)

## open issues ##
 * performance analysis and improvements (different hash algorithms, ...)
 * if there are some users, improve interface
 * investigation of merge interfaces

## release notes ##
v1.1.0
* README.md updated
* main.compare_json implemented

v1.0.1
* README.md updated

v1.0.0
* XmlXdiff moved diffx
* ui improved diffx.main added as entry point
* code refactored - pythonic, pep8
* text block introduced
* performance improved
 
## documentation ##
![Tests](./doc/tests.md "Executed Tests")
