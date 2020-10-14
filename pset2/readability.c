// CS50 Fall 2020
// Problem Set 2
// Author: kkphd

#include <stdio.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>
#include <math.h>

int count_letters(string c);
int count_words(string c);
int count_sent(string c);

int main(void)
{
    string input = get_string("Text: ");
    int letters = count_letters(input);
    int words = count_words(input);
    int sents = count_sent(input);

    // Coleman-Liau readability formula: index = 0.0588 * L - 0.296 * S - 15.8
    float index = ((5.88 * letters / words) - (29.6 * sents / words) - 15.8);

    // Print the appropriate grade level of the text provided.
    if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %.0f\n", round(index));
    }
}

// Separate functions for calculating the number of letters, words, and sentences in the text.
int count_letters(string c)
{
    int count = 0;
    for (int l = 0; l < strlen(c); l++)
    {
        if isalpha(c[l])
        {
            count++;
        }
    }
    return count;
}

int count_words(string c)
{
    int count = 0;
    for (int w = 0; w < strlen(c); w++)
    {
        if (c[w] == ' ')
        {
            count++;
        }
    }

    if (strlen(c) > 0) //for the last word.
    {
        count++;
    }
    return count;
}

int count_sent(string c)
{
    int count = 0;
    for (int s = 0; s < strlen(c); s++)
    {
        if ((c[s] == '.') || (c[s] == '!') || (c[s] == '?'))
        {
            count++;
        }
    }
    return count;
}