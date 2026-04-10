def hexDigits(num: int):
    return len(hex(num))-2


print(hexDigits(0))
print(hexDigits(1))
print(hexDigits(10))
print(hexDigits(16))
print(hexDigits(17))
print(hexDigits(100))
print(hexDigits(1000))