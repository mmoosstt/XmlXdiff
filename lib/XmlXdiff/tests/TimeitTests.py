import timeit


print(timeit.timeit(setup="import xDiffXml.xDiffCore as api",
                    stmt="api.xDiffExecutor().run()", 
                    number = 10))