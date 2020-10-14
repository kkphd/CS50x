// CS50 Fall 2020
// Problem Set 4
// Author: kkphd

#include "helpers.h"
#include <math.h>
#include <stdio.h>

void swap(RGBTRIPLE *a, RGBTRIPLE *b);

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int red = image[i][j].rgbtRed;
            int green = image[i][j].rgbtGreen;
            int blue = image[i][j].rgbtBlue;
            int average = round((red + green + blue)/3.0);

            image[i][j].rgbtRed = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtBlue = average;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int red = image[i][j].rgbtRed;
            int green = image[i][j].rgbtGreen;
            int blue = image[i][j].rgbtBlue;

            int sepia_red = round(.393*red + .769*green + .189*blue);
            {
                if (sepia_red > 255)
                {
                    sepia_red = 255;
                }
            }

            int sepia_green = round(.349*red + .686*green + .168*blue);
            {
                if (sepia_green > 255)
                {
                    sepia_green = 255;
                }
            }

            int sepia_blue = round(.272*red + .534*green + .131*blue);
            {
                if (sepia_blue > 255)
                {
                    sepia_blue = 255;
                }
            }

            image[i][j].rgbtRed = sepia_red;
            image[i][j].rgbtGreen = sepia_green;
            image[i][j].rgbtBlue = sepia_blue;
        }
    }
    return;
}

// Reflect image
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        int l = 0;
        int r = width - 1;
        while (l < r)
        {
            swap(&image[i][l], &image[i][r]);
            l++;
            r--;
        }
    }
}

void swap(RGBTRIPLE *r, RGBTRIPLE *l)
{
    RGBTRIPLE temp = *r;
    *r = *l;
    *l = temp;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int position[9][2] = { {-1, -1}, {-1, 0}, {-1, 1}, {0, 0}, {0, -1}, {0, 1}, {1, -1}, {1, 0}, {1, 1} };
            int blue_sum = 0;
            int green_sum = 0;
            int red_sum = 0;
            float count = 0;

            for (int p = 0; p < 9; p++)
            {
                int row = position[p][0] + i;
                int col = position[p][1] + j;

                if ((row < height) && (row >= 0) && (col < width) && (col >=0))
                {
                    blue_sum += copy[row][col].rgbtBlue;
                    green_sum += copy[row][col].rgbtGreen;
                    red_sum += copy[row][col].rgbtRed;
                    count++;
                }
            }

            int blue_avg = round(blue_sum / count);
            int green_avg = round(green_sum / count);
            int red_avg = round(red_sum / count);

            image[i][j].rgbtBlue = blue_avg;
            image[i][j].rgbtGreen = green_avg;
            image[i][j].rgbtRed = red_avg;
        }
    }
    return;
}