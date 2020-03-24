#!/usr/bin/env python3

# Beautiful Soup is a Python library for pulling data out of HTML and XML files.
# import the BeautifulSoup Python library according to these instructions: 
# http://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-beautiful-soup
# use this syntax as described on the documentation page: 
# http://www.crummy.com/software/BeautifulSoup/bs4/doc/#making-the-soup
from bs4 import BeautifulSoup

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


alphabet_list = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p',
            'q','r','s','t','u','v','w','x','y','z']

string_numbers_list = ['0','1','2','3','4','5','6','7','8','9']

punctuation_list = ['.', ',', '!', '?', ';', ':', '"', '\'', '[', ']', '{', '}',
               '\\', '|', '=', '+', '‒', '–', '—', '―', '(', ')', '*', '~', '&']

ignore_word_list = ['', 'a', 'about', 'after', 'all', 'amid', 'an', 'and', 
                    'are', 'as', 'at', 'be', 'but', 'by', 'can', 'could', 
                    'during', 'for', 'from', 'get', 'gets', 'has', 'have', 
                    'he', 'his', 'how', 'if', 'in', 'is', 'it', 'it\'s', 
                    'new', 'news', 'not', 'of', 'on', 'or', 'out', 'says', 
                    'takes', 'than', 'that', 'the', 'this', 'to', 'was', 
                    'will', 'what', 'when', 'with', 'who', 'why', 'won\'t',]

isascii = lambda s: len(s) == len(s.encode())

 
def word_count():
    """
    This function takes a url as the argument
    and returns the most common word found in that web page
    """
    # "load" a webpage 
    r = requests.get('https://news.google.com/')

    # decode the text of the HTML.
    # r comes from the requests request above
    soup = BeautifulSoup(r.text, 'lxml')

    # find all anchor tags with the class of "DYST1d".
    # The anchore tag with this tag contains
    # the news article headline and link
    anchor = soup.findAll("a", {"class": "DY5T1d"})

    words_list = []
    results = {}

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
            # This check if the word is in the ignore_word_list. If it's not,
            # it is added to word_list.
            if (word not in ignore_word_list and
                word not in punctuation_list and 
                word not in alphabet_list and 
                word not in string_numbers_list and
                isascii(word) == True):
                words_list.append(word.lower())

    counter = 1
    for i in list(set(words_list)):
        word = max(set(words_list), key = words_list.count)
        number_of_appearances =  words_list.count(word)
        results[counter] = {'word':word, 'appearances':number_of_appearances}
        counter += 1
        words_list = list(filter((word).__ne__, words_list))

    return results


   
def main():

    print('''
Hello and welcom to the Google News word count. 
This program returns the word count of all the words 
found on the Google New website.

Created by Michael Delgado (devmikedel@gmail.com)

(Please wait for the results)''')

    results = word_count()

    for result in results:
        print(f'{results[result]}')


if __name__ == '__main__':
    main()
