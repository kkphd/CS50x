// CS50 Fall 2020
// Problem Set 1
// Author: kkphd

#include <stdio.h>
#include <cs50.h>

long length(long number);
long luhns(long number);
long split_sum(long number);

int main(void)
{
    long cc = get_long("Number: ");

    int digits = length(cc);

    if ((digits < 13) || (digits > 16))
    {
      printf("INVALID\n");
      return 0;
    }

    long total_sum = luhns(cc);

    if (total_sum % 10 == 0)
    {
        if ((cc >= 340000000000000) && (cc < 350000000000000))
        {
            printf("AMEX\n");
        }
        else if ((cc >= 370000000000000) && (cc < 380000000000000))
        {
            printf("AMEX\n");
        }
        else if ((cc >= (5100000000000000)) && (cc < (5600000000000000)))
        {
            printf("MASTERCARD\n");
        }
        else if ((cc >= (4000000000000)) && (cc < (5000000000000)))
        {
            printf("VISA\n");
        }
        else if ((cc >= (4000000000000000)) && (cc < (5000000000000000)))
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }
}

long length(long number)
{
    int count = 0;
    do
    {
        number /= 10;
        count++;
    }
    while (number != 0);
    return count;
}

long luhns(long number)
{
    int remain = 0;
    int sum1 = 0;
    int sum2 = 0;
    int i = 1;
    do
    {
        if ((i % 2) == 0)
        {
            remain = number % 10;
            sum1 += split_sum(remain);
        }
        else
        {
            sum1 += number % 10;
        }
        number /= 10;
        i++;
    }
    while (number > 0);
    return sum1;
}

long split_sum(long number)
{
    number *= 2;
    if (number < 10)
    {
        return number;
    }

    int ones = number % 10;
    number /= 10;
    int tens = number % 10;
    int total = ones + tens;
    return total;
}