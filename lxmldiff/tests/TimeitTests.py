import timeit


print(timeit.timeit(setup="import lxmldiff.xDiffCore as api",
                    stmt="api.xDiffExecutor().run()", 
                    number = 10))