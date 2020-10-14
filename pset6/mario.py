# CS50 Fall 2020
# Problem Set 6
# Author: kkphd

def prompt():
    while True:
        try:
            size = input("Height: ")
            converted = int(size)
            if converted > 0 and converted < 9:
                return converted
        except:
            print("Value must be a number.")

def blocks(height):
    for row in range(height):
        for space in range(height - row - 1):
            print(" ", end="")
        print("#" * (row + 1))

answer = prompt()
blocks(answer)