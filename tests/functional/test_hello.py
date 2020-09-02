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

name1 = "Tom"
height1 = 1.90
weight1 = 80

name2 = "Katy"
height2 = 1.70
weight2 = 80

name3 = "Bob"
height3 = 2
weight3 = 150

def bmi_calculator(name, height, weight):
    bmi = weight / (height ** 2)

    print("Индекс массы тела:" + str(bmi))

    if bmi < 25:
        return name + " не имеет лишнего веса"
    else:
        return name + " имеет лишний вес"

bmi1 = bmi_calculator(name1, height1, weight1)
bmi2 = bmi_calculator(name2, height2, weight2)
bmi3 = bmi_calculator(name3, height3, weight3)
