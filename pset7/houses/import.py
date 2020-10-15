# CS50 Fall 2020
# Problem Set 7
# Author: kkphd

from sys import argv
import csv
import cs50

def main():

    # Confirm user input
    argc = len(argv)
    if argc < 2:
        print("Enter CSV file")
        return 1;

    # Create an empty database
    open("students.db", "w").close()

    # Open the file for SQLite
    db = cs50.SQL("sqlite:///students.db")

    # Create a table to store the information
    db.execute("CREATE TABLE students (first TEXT, middle TEXT, last TEXT, house TEXT, birth NUMERIC)")

    # Open CSV
    with open(argv[1], 'r') as file:
        reader = csv.DictReader(file, delimiter=',')

        # Input rows from the CSV file into the SQL database
        for row in reader:
            n = row['name'].split(" ")

            # Parse through each name and separate into first, middle, and last names
            first = n[0]

            if len(n) > 2:
                middle = n[1]
                last = n[2]
            elif len(n) == 2:
                middle = None
                last = n[1]

            house = row['house']
            birth = int(row['birth'])

            db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)",
                first, middle, last, house, birth)

main()