# CS50 Fall 2020
# Problem Set 6
# Author: kkphd

import math

def prompt():
    while True:
        try:
            dollars = input("Change owed: ")
            converted = int(float(dollars) * 100)
            if converted > 0:
                return converted
        except:
            print("Value must be a positive number.")

def calc(money):
    count = 0
    quarters = 0
    dimes = 0
    nickels = 0
    pennies = 0

    while money >= 25:
        quarters = money // 25
        money -= (quarters * 25)
        count += quarters

    while money < 25 and money >= 10:
        dimes = money // 10
        money -= (dimes * 10)
        count += dimes

    while money < 10 and money >= 5:
        nickels = money // 5
        money -= (nickels * 5)
        count += nickels

    while money < 5 and money >= 1:
        pennies = money // 1
        money -= pennies
        count += pennies

    print(count)

answer = prompt()
calc(answer)