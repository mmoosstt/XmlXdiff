import itertools

def powerset(s):
    x = len(s)
    for i in range (1 << x):
        yield [s[j] for j in range(x) if (i & (1 << j))]

def shouldcont (list1, list2):
    if len(list1) != len(list2):
        return False
    return True

if __name__ == '__main__':
    a = [1, 2, 3]
    b = ['a', 'b', 'c']

    aset = set(a)
    bset = set(b)

    for asub in powerset(a):
        for bsub in powerset(b):
            if shouldcont (asub, bsub):
                asubset = set(asub)
                bsubset = set(bsub)

                adiff = aset - asubset
                bdiff = bset - bsubset

                prod = itertools.product(asub, bsub)

                for p in itertools.permutations(asub):
                    print zip(p, bsub)
                    print list(adiff)
                    print list(bdiff)
                    print '----------------------------------'
