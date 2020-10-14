# CS50 Fall 2020
# Problem Set 6
# Author: kkphd

import re

def count_letter(text):
    count = 0

    for words in text:
        for letters in words:
            if letters.isalpha():
                count += 1
    return count

def count_word(text):
    count = len(text)
    return count

def count_sent(text):
    pattern = '[.!?]'
    modified = re.split(pattern, text)
    count = len(modified) - 1
    return count

def calc():
    response = input("Text: ")
    modified = response.split()

    letters = count_letter(modified)
    words = count_word(modified)
    sents = count_sent(response)

    # Coleman-Liau readability formula: index = 0.0588 * L - 0.296 * S - 15.8
    index = ((5.88 * letters / words) - (29.6 * sents / words) - 15.8)

    if index >= 16:
        print("Grade 16+")
    elif index < 1:
        print("Before Grade 1")
    else:
        print(f"Grade {round(index)}")

calc()