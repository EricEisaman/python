import math

def sameDigits(left, right, count):
    if count == 0:
        return True
    if left % 10 != right % 10:
        return False
    return sameDigits(left // 10, right // 10, count - 1)

def isDuplicatedNumber(n):
    if n <= 0:
        return False
    num_digits = int(math.log10(n) + 1)
    if num_digits % 2 != 0:
        return False
    half = num_digits // 2
    divisor = 10 ** half
    return sameDigits(n // divisor, n % divisor, half)

# local helper - you can't name it `assert` in Python, it's a keyword
def check(condition, label):
    if condition:
        print(f"{label}: PASS")
    else:
        print(f"{label}: FAIL")

def testIsDuplicatedNumber():
    check(isDuplicatedNumber(11) == True, "isDuplicatedNumber(11) == True")
    check(isDuplicatedNumber(55) == True, "isDuplicatedNumber(55) == True")
    check(isDuplicatedNumber(123123) == True, "isDuplicatedNumber(123123) == True")
    check(isDuplicatedNumber(123) == False, "isDuplicatedNumber(123) == False")
    check(isDuplicatedNumber(1221) == False, "isDuplicatedNumber(1221) == False")
    check(isDuplicatedNumber(12312) == False, "isDuplicatedNumber(12312) == False")
    check(isDuplicatedNumber(121212) == False, "isDuplicatedNumber(121212) == False")
    check(isDuplicatedNumber(1) == False, "isDuplicatedNumber(1) == False")
    check(isDuplicatedNumber(0) == False, "isDuplicatedNumber(0) == False")
    
def main():
    testIsDuplicatedNumber()

main()