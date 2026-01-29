import sys

def suma(num1, num2):
    return num1 + num2

try:
    nums = sys.argv

    num1 = int(nums[1])
    num2 = int(nums[2])

    print(suma(num1, num2))

except:
    print("Ha habido un error")