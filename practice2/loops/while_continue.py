i = 1
while i <= 5:
    if i == 3:
        i += 1
        continue
    print(i)
    i += 1

i = 1
while i <= 10:
    if i % 2 == 0:
        i += 1
        continue
    print(i)
    i += 1

i = 1
while i <= 12:
    if i % 3 == 0:
        i += 1
        continue
    print(i)
    i += 1

i = 0
s = 0
while i < 5:
    x = int(input())
    if x < 0:
        i += 1
        continue
    s += x
    i += 1
print(s)

i = 0
while i < 3:
    w = input()
    if w == "0":
        i += 1
        continue
    print(w)
    i += 1
