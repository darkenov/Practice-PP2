x = 5
print(x > 0 and x < 10)

y = 5
print(y < 5 or y > 10)

z = 5
print(not(z > 3 and z < 10))

d=5
print(not(d>10 or d>4))

f = ["apple", "banana"]
u = ["apple", "banana"]
k = f
print(f is k)
print(f is u)
print(f == u)

text = "Hello World"
print("H" in text)
print("hello" in text)
print("z" not in text)

print(6 & 3)
print(6 | 3)
print(6 ^ 3)

#Multiplication * has higher precedence than addition +, and therefore multiplications are evaluated before additions:

print(100 + 5 * 3)