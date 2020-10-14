# CS50 Fall 2020
# Problem Set 6
# Author: kkphd

from sys import argv
import csv
import re

def main():

    argc = len(argv)
    if argc < 3:
        print("Usage: python dna.py data.csv sequence.txt")
        return 1;

    # Input the DNA sequence
    dna = open(argv[2], 'r')
    data = dna.read()

    # Read the database into a file
    person_dict = {}
    with open(argv[1], 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            count_string = str(row[1:])
            person_dict[count_string] = row[0]

    # Extract the header (remove the new line character ['\n'] in the last element)
    # This will prepare the STRs for search via regular expressions
    with open(argv[1], 'r') as file:
        header = next(file)
        header = header.split(',')
        header[-1] = header[-1].strip()
        header = header[1:len(header)]

    # Input the target STRs into an empty dictionary
    pattern = {}
    for head in header:
        pattern[head] = None

    # Create regular expressions to determine the longest string of the target STRs
    regex = []
    for head in header:
        # Add an extra set of parentheses to capture *all* iterations of the target STR sequence
        # (A single set of parentheses will only capture the *last* iteration and only return '1')
        regex.append('((' + head + ')+)')

    # Extract these STRs from the DNA sequence and input into 'match'
    count_list = []
    for pat, reg in zip(pattern, regex):
        # Maximum set to -99 arbitrarily
        maximum = -99
        match = re.compile(reg).findall(data)
        # Identify the largest sequence
        for m in match:
            if len(m[0]) > maximum:
                maximum = len(m[0])
        final = maximum // len(m[1])

        # Append matching STRs to count_list while ensuring each element in the list is converted to a string variable
        # (Both the individual elements of the list and the entire list itself must be in a string format -
        # This will match the DNA sequence serving as the key in person_dict dictionary above)
        if match:
            count_list.append(str(final))

    # As noted above, convert the entire list itself to a string variable
    count_string = str(count_list)

    # Return the matching value (person) for the key of interest (the target DNA sequence), if present
    if person_dict.get(count_string) != None:
        print(person_dict[count_string])
    else:
        print("No match")

main()