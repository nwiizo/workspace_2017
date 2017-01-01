def is_prime(q): 
    i = 2
    while i <=q:
        if q % i == 0:
            return False
        i += 1
    return True
