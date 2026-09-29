lst = [1, 2, 3, 'ali', 'reza', True, 1, 1.5]


cnumber = 50
i = 3
while i:
    a = int(input("enter a number: "))
    if a == cnumber:
        print("you win")
        break
    else:
        print("try again")
    i -= 1
else:
    print("Game over")