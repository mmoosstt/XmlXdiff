import timeit

print(timeit.timeit(setup="import lxmldiff.xdiffCore as api",
                    stmt="api.getChildren(api._xml1, api._root1,  api._pathes1, api._hashes1)", 
                    number = 1000))

print(timeit.timeit(setup="import lxmldiff.xdiffCore as api",
                    stmt="api.getChildren2(api._xml1, api._root1,  api._pathes1, api._hashes1, api.customElementHashAll)", 
                    number = 1000))