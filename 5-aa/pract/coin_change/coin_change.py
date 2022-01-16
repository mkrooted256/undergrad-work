cache = {}

def coin_change(N, C):
    if N == 0:
        print(C, N, "-x", 1)
        return 1
    if len(C) == 0:
        print(C, N, "-x", 0)
        return 0

    h = (N,str(C)).__hash__()
    if h in cache:
        s = cache[h]
        print(C, N, "[]", s)
        return s

    s = 0
    C1 = C.copy()
    c0 = list(C)[-1]
    C1.remove(c0)

    if c0 <= N:
        s += coin_change(N-c0, C) 
    s += coin_change(N, C1)

    print(C, N, "->", s)
    cache[h] = s
    return s

print(coin_change(5, set([5,2,1])))

