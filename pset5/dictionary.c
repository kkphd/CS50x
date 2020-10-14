// CS50 Fall 2020
// Problem Set 5
// Author: kkphd

// Implements a dictionary's functionality

#include <stdbool.h>
#include "dictionary.h"
#include <cs50.h>
#include <strings.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>
#include <ctype.h>
#include <stdio.h>

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
// Determined size of hash table using a load factor value of 0.75:
// (Number of factors or elements in the table / number of entries or locations)
// https://stackoverflow.com/questions/10901752/what-is-the-significance-of-load-factor-in-hashmap
// Default dictionary contains 143091 words * 4/3. Value rounded up to the nearest prime number.
const unsigned int N = 190793;

// Hash table head (size 0 in the beginning since it's not pointing to anything)
node *table[N];

// Keep track of the words added to the dictionary
int count = 0;

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    char word[LENGTH + 1];

    // Open dictionary file
    FILE *dict = fopen(dictionary, "r");
    if (dict == NULL)
    {
        return false;
    }

    // Read strings from file one at a time
    while (fscanf(dict, "%s\n", word) != EOF)
    {
        // Create a new node for each word
        node *n = malloc(sizeof(node));
        if (n == NULL)
        {
            fclose(dict);
            return false;
        }

        // Copy the word into the node
        strcpy(n->word, word);
        n->next = NULL;

        // Hash word to obtain an index
        unsigned int index = hash(word);

        // Set the new node's next pointer to the first element in the linked list
        n->next = table[index];

        // Make the new node the head of the linked list
        table[index] = n;
        count++;
    }
    fclose(dict);
    return true;
}

// Hashes word to a number
// Use polynomial string hashing:
// https://cp-algorithms.com/string/string-hashing.html
// https://advancedweb.dev/polynomial-rolling-hash
// https://www.cs.umd.edu/class/fall2019/cmsc420-0201/Lects/lect10-hash-basics.pdf
unsigned int hash(const char *word)
{
    int base = 13;
    unsigned int index = 0;

    for (int i = 0; i < (LENGTH + 1); i++)
    {
        char lower = tolower(*word);
        int converted = atoi(&lower);
        index = (index * base + converted) % N;
    }
    return index;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    if (count > 0)
    {
        return count;
    }
    else
    {
        return 0;
    }
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // Determine the index of the word in the hash table
    unsigned int index = hash(word);

    // Access linked list at that index in the hash table
    node *cursor = table[index];

    // Traverse linked list and look for word
    while (cursor != NULL)
    {
        if (strcasecmp(cursor->word, word) == 0)
        {
            return true;
        }
        else
        {
            cursor = cursor->next;
        }
    }
    return false;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];

        while (cursor != NULL)
        {
            node *tmp = cursor;
            cursor = cursor->next;
            free(tmp);
        }
    }
    return true;
}
