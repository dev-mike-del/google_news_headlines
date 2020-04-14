#!/usr/bin/env python3

from datetime import datetime, timezone

# Beautiful Soup is a Python library for pulling data out of HTML and XML files.
# import the BeautifulSoup Python library according to these instructions: 
# http://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup
# use this syntax as described on the documentation page: 
# http://www.crummy.com/software/BeautifulSoup/bs4/doc/#making-the-soup
from bs4 import BeautifulSoup

import pandas as pd

# Requests is a Python HTTP library, released under the Apache License 2.0. 
# The goal of the project is to make HTTP requests simpler and more 
# human-friendly. The current version is 2.23.0
# import the requests Python library for programmatically making HTTP requests
# after installing it according to these instructions: 
# http://docs.python-requests.org/en/latest/user/install/#install
import requests

# lxml is a Python library which allows for easy handling of XML and HTML files.
# BeautifulSoup can employ lxml as a parser
# import lxml according to these instructions:
# https://lxml.de/installation.html
import lxml

# This list is to filter out any words (str) that are single letters
alphabet_list = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p',
            'q','r','s','t','u','v','w','x','y','z']

# This list is to filter out any numbers that may appear in the text
string_numbers_list = ['0','1','2','3','4','5','6','7','8','9']

# This list is to filter out and punctuation from the word_count function
punctuation_list = ['.', ',', '!', '?', ';', ':', '"', '\'', '[', ']', '{', '}',
               '\\', '|', '=', '+', '‒', '–', '—', '―', '(', ')', '*', '~', '&']

# This list is to filter out any unwanted words from the word_count function
ignore_word_list = ['', 'a', 'about', 'after', 'all', 'amid', 'an', 'and', 
                    'are', 'as', 'at', 'be', 'but', 'by', 'can', 'could', 
                    'during', 'for', 'from', 'get', 'gets', 'has', 'have', 
                    'he', 'his', 'how', 'if', 'in', 'is', 'it', 'it\'s', 
                    'new', 'news', 'not', 'of', 'on', 'or', 'out', 'says', 
                    'takes', 'than', 'that', 'the', 'this', 'to', 'was', 
                    'will', 'what', 'when', 'with', 'who', 'why', 'won\'t',]

# This lambda funciton is used to check if a word (str) is unicode
isascii = lambda s: len(s) == len(s.encode())

def word_count():
    """
    This function takes a url as the argument
    and returns the most common word found in that web page
    """
    timestamp = datetime.now(timezone.utc)

    # "load" a webpage 
    r = requests.get('https://news.google.com/')

    # decode the text of the HTML.
    # r comes from the requests request above
    soup = BeautifulSoup(r.text, 'lxml')

    # find all anchor tags with the class of "DYST1d".
    # The anchore tag with this tag contains
    # the news article headline and link
    anchor = soup.findAll("a", {"class": "DY5T1d"})

    num_of_articles = len(anchor)

    # This list is for all the words (str) that appear in the text
    words_list = []

    # This list is for the results that are returned from the 
    # word_count function
    results = []

    # This extracts the individual anchor tags from the BeautifulSoup element 
    # of anchor tags
    for obj in anchor:
        # This extracts the text from the anchor tag
        for word in obj.text.split():
            word = word.lower()
            # This check if the first letter of the word is in the 
            # punctuation_list. If it is, the function replaces the letter 
            # with an empty string (that we later remove).
            if word[0] in punctuation_list:
                word = word.replace(word[0], '')
            # This check if the last letter of the word is in the 
            # punctuation_list. If it is, the function replaces the letter 
            # with an empty string (that we later remove).
            elif word[-1] in punctuation_list:
                word = word.replace(word[-1], '')
            # This checks if the word is in the exclution lists and if the 
            # word is unicode. If it's not, it is added to word_list.
            if (word not in ignore_word_list and
                word not in punctuation_list and 
                word not in alphabet_list and 
                word not in string_numbers_list and
                isascii(word) == True):
                words_list.append(word.lower())

    num_of_words = len(words_list)

    # This loop dedupes the word list and adds each word and the number of 
    # appearances to the results dictionary. Additionally, it adds a key 
    # (index) as the key for each word.
    for i in list(set(words_list)):
        word = max(set(words_list), key = words_list.count)
        appearances =  words_list.count(word)
        results.append([word, appearances, num_of_words, num_of_articles, timestamp])
        words_list = list(filter((word).__ne__, words_list))

    colNames = ['word',
                'appearances',
                'number_of_words',
                'number_of_articles',
                'timestamp',
                ]

    df = pd.DataFrame(data = results, columns = colNames)

    # This returns the results gathered from this function
    return df

def main():

    # Opening welcome statement
    print('''
Hello and welcome to the Google News word count. 
This program returns the word count of all the words 
found on the Google New website.

Created by Michael Delgado (devmikedel@gmail.com)

(Please wait for the results)''')

    # This calls the word_count function and save the returned results in the 
    # variable results
    results = word_count()
    print(results)

    # # This loop prints out each dictionary item (one per line)
    # for result in results:
    #     print(f'{results[result]}')


if __name__ == '__main__':
    main()
