i = 1
while i < 3:
    w = input()
    if w == "0":
        i += 1
        continue
    print(w)
    i += 1

s = 0
while True:
    x = int(input())
    if x == 0:
        break
    s += x
print(s)

i = 2
while i <= 100:
    if i % 7 == 0:
        print(i)
        break
    i += 1

while True:
    p = input()
    if p == "123":
        print("OK")
        break

a = list(map(int, input().split()))
i = 0
while i < len(a):
    if a[i] == 5:
        print("YES")
        break
    i += 1
