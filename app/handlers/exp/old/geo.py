def gen(n):
    i = -1
    while n - 1 > i:
        i += 1
        yield i


def gen_dict(n):
    for i in range(n):
        yield str(i), str(i+1)


a = [i + 1 for i in range(10)]

print(a)
print(gen(10))
m = gen(10)
for i in m:
    print(i)
print([i for i in gen(10)])
my_dictionary: dict = {f"key_{i1}": f"value_{i2}" for i1, i2 in gen_dict(3)}
print(my_dictionary)
m: dict = {"Хуй": 1}
print(m)
