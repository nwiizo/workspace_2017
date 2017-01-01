def prime_is(q):
    i = 2
    table = []
    while i * i <= q:
        while q % i == 0:
            q /= i
            table.append(i)
        i += 1
    if q > 1:
        table.append(q)
    return table
