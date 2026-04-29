
print("hello world")
num = input("say a word you like: ")
num2 = int(input("say a number you like: "))
print(f"you love {num} and {num2}")

def sum_func(c, d):   # renamed (avoid using 'sum')
    return c + d

a = 2
b = 3
print(f"2 plus 3 is equal to {a + b}")

c = int(input("say a number: "))
d = int(input("say another number: "))
print(f"{c} plus {d} is equal to {sum_func(c, d)}")

print("my name is sigma boy")

def idk(a, b, c):
    return a + b + c

a = 1
b = 2
c = 3
print(f"abc {idk(a, b, c)}")

print("i am sigma")

def sayhi(name):
    return "hi " + name

hello = input("say your name: ")
print(sayhi(hello))