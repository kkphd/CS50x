// CS50 Fall 2020
// Problem Set 1
// Author: kkphd

#include <stdio.h>
#include <cs50.h>

int main(void)
{
    // Initialize the height variable until it meets the conditions below.
    int h;
    do
    {
        h = get_int("Height: ");
    }
    while (h > 8 || h < 1);

    // Create the loop for each row.
    for (int r = 0; r < h; r++)
    {
        // Create the loop for blank spaces and columns within each row.
        for (int s = 0; s < h - r - 1; s++)
        {
            printf(" ");
        }
        for (int c = 0; c <= r; c++)
        {
            printf("#");
        }

        printf("  ");

        for (int c = 0; c <= r; c++)
        {
            printf("#");
        }
        // Proceed to the next line.
        printf("\n");
    }
}

