# CS50 Fall 2020
# Problem Set 7
# Author: kkphd

from sys import argv
import cs50

def main():

    # Confirm user input
    argc = len(argv)
    if argc < 2:
        print("Enter house name")
        return 1;

    house_input = argv[1]

    db = cs50.SQL("sqlite:///students.db")
    data = db.execute('SELECT * FROM students WHERE house = ? ORDER BY last ASC, first ASC', house_input)

    for row in data:
        first = row['first']
        last = row['last']
        birth = str(row['birth'])

        if row['middle'] == None:
            print(first + " " + last + ", born " + birth)
        else:
            middle = row['middle']
            print(first + " " + middle + " " + last + ", born " + birth)

main()