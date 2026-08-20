# n = int(input("enter a number: "))
n = 11

# if n % 2 == 0:
#     print("even")
# else:
#     print("odd")

# print("odd" if n % 2 else "even")

def is_even(num1: int=0, num2: int=0) -> int:
    """Get tow numbers and returns sum of them.

    Args:
        num1 (int): first number.
        num2 (int): second number.

    Returns:
        int: num1 + num2
    """
    return num1 + num2


number = int(input())
print(is_even(number))