# def f1():
#     print("Hello1")
#     print("Hello2")
#
# def f2(x):
#     return 2*x
#
# def f3(x,y):
#     return x + y
#
# a = f3(5,7)
#
# print(a)
#
# def f4(some_argument):
#     print(some_argument)
#     print("test")
# f4(10)
#
# def f5():
#     return 5
#
# b = f5()
#
# print(b)

# def f7(x):
#     print(x)
#     print("test")
#     return 3*x
#
# a = f7(10)
# print(a)
#
# name1 = "Tom"
# height1 = 1.90
# weight1 = 80
#
# name2 = "Katy"
# height2 = 1.70
# weight2 = 80
#
# name3 = "Bob"
# height3 = 2
# weight3 = 150
#
# def bmi_calculator(name, height, weight):
#     bmi = weight / (height ** 2)
#
#     print("Индекс массы тела:" + str(bmi))
#
#     if bmi < 25:
#         return name + " не имеет лишнего веса"
#     else:
#         return name + " имеет лишний вес"
#
# bmi1 = bmi_calculator(name1, height1, weight1)
# bmi2 = bmi_calculator(name2, height2, weight2)
# bmi3 = bmi_calculator(name3, height3, weight3)



# def convert(milles):
#     return milles * 1.609
#
# kilommetrs = convert(1)
#
# print(kilommetrs)
#
#
# def area(a, b):
#     return a * b
#
# s = area(2, 6)
#
# print(s)
#
#
#
# namber = 5
#
# def is_evevn(x):
#
#     if x % 2 == 0:
#         return "Это число четное"
#     else:
#         return "Это число нечетное"
#
# n = is_evevn(8)
#
# print(n)

a = [3, 5, 10]

print(a)

a.append(1)

print(a)

a.append("test")

print(a)

a.append([5,7])

print(a)

a.pop()
print(a)

print(a[1])

a[0] = 100
print(a)

b = ["hello", "bya", "hey"]

temp = b[0]
b[0] = b[2]
b[2] = temp

print(b)

b[0], b[2] = b[2], b[0]
print(b)