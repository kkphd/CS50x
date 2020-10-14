// CS50 Fall 2020
// Problem Set 2
// Author: kkphd

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <cs50.h>
#include <ctype.h>


int main(int argc, string argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    for (int i = 0; i < strlen(argv[1]); i++)
    {
        if (isdigit(argv[1][i]) == 0)
        {
            printf("Usage: ./caesar key\n");
            return 1;
        }
    }
    string k = argv[1];
    int key = atoi(k);
    string plain = get_string("plaintext:  ");

    printf("ciphertext: ");
    for (int letter = 0; letter < strlen(plain); letter++)
    {
        if (isupper(plain[letter])) // Convert uppercase letters.
        {
            // Convert ASCII to alphabetical index.
            int converted = (plain[letter] - 65);
            // Shift alphabetical index using the cipher formula above.
            // Convert the alphabetical index back to ASCII.
            int rotated = (converted + key) % 26 + 65;
            printf("%c", rotated);
        }
        else if (islower(plain[letter])) // Convert lowercase letters.
        {
            // Convert ASCII to alphabetical index.
            int converted = (plain[letter] - 97);
            // Shift alphabetical index using the cipher formula above.
            // Convert the alphabetical index back to ASCII.
            int rotated = (converted + key) % 26 + 97;
            printf("%c", rotated);
        }
        else
        {
            printf("%c", plain[letter]);
        }
    }
    printf("\n");
}