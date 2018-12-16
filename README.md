# XmlXdiff #
 - generating nice plots of differences between xml files
 - general comparison without grammatical information
 - playground for performance analysis
 
# Used Prinziples #

## Implementation
 - creating an hashed tree representation of each element
 - each element is identified by it's xml path and a hash

|comparison results|xml1|xml2|
|---|---|---|
|ElementUnchanged|   |   |
|ElementChanged|   |   |
|ElementDeleted|   |   |
|ElementAdded|   |   |
|ElementMoved|   |   |
|ElementTagConsitency|   |   |
|ElementTextAttributeValueConsitency|   |   |
|ElementTagAttributeNameConsitency|   |   |
|ElementUnknown|   |   |   |   |
|ElementVerified|   |   |

<figure>
	<img src="./doc/example_diff_a_b.svg" alt="example svg output">
	<figcaption>example showing differences between xml's</figcaption>
</figure>

## To Be Investigated/Implemented
 - xdiff cost rating for moved and deleted leafs
 - gravity spline for moved elements
 - performance analysis and improvements (different hash algorithms, ...)
 - figure out how to create a general python package
 
# Inspired by xml-diff #
## Compare two XML files in unordered manner #

XML has been used to transfer hierarchical data. 
In most of those cases, the ordered relation between sibling 
nodes not important - only ancestor relation is important.

The [X-Diff](http://pages.cs.wisc.edu/~yuanwang/xdiff.html) algorithm 
describes how two XML documents can be effectively compared in an unordered
manner.




## License #
