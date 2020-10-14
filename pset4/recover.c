// CS50 Fall 2020
// Problem Set 4
// Author: kkphd

#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover image\n");
        return 1;
    }

    FILE *pointer = fopen(argv[1], "r");

    if (pointer == NULL)
    {
        return 1;
    }

    // Set the block size to 512.
    unsigned char buffer[512];

    // Count the number of files you've processed. This will be used for naming each jpeg file.
    int count = 0;

    // Prepare a string of 8 bytes for the file name (which includes an extra byte for '\0').
    char filename[8];
    FILE *img = NULL;

    while (fread(buffer, sizeof(buffer), sizeof(char), pointer) != 0)
    {
        // Check if you''ve encountered a new jpeg file.
        if ((buffer[0] == 0xff) && (buffer[1] == 0xd8) && (buffer[2] == 0xff) && (buffer[3] & 0xf0) == 0xe0)
        {
            // If it's not the first file, then close the current image file.
            if (img != NULL)
            {
                fclose(img);
            }

            // Create new files in ascending order (beginning with 000).
            sprintf(filename, "%03i.jpg", count);
            img = fopen(filename, "w");
            count++;
        }

        // Continue writing to the existing jpeg file.
        if (img != NULL)
        {
            fwrite(&buffer, sizeof(buffer), sizeof(char), img);
        }
    }

    // Close the open files to prevent a memory leak.
    fclose(img);
    fclose(pointer);
    return 0;
}
