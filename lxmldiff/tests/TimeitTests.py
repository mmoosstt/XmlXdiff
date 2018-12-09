import timeit

print(timeit.timeit("api.getChildren(api._xml1, api._root1,  api._pathes1, api._hashes1)", number = 1000, setup="import lxmldiff.xdiffCore as api"))
print(timeit.timeit("api.getChildren2(api._xml1, api._root1,  api._pathes1, api._hashes1)", number = 1000, setup="import lxmldiff.xdiffCore as api"))