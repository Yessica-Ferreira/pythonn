n = 10_000_000
es_primo = True
while True:
    n += 1
    es_primo = True

    for x in range(2, int(n ** 0.5) + 1):
        if n % x == 0:
            es_primo = False
            break

    if es_primo:
        print(f"El número primo es: {n}")
        