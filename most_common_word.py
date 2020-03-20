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


alphabet_list = [' ','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p',
            'q','r','s','t','u','v','w','x','y','z']

string_numbers_list = ['0','1','2','3','4','5','6','7','8','9']

punctuation_list = ['.', ',', '!', '?', ';', ':', '"', '\'', '[', ']', '{', '}',
               '\\', '|', '=', '+', '-', '(', ')', '*', '~']

ignore_word_list = ['a', 'and', 'if', 'is', 'to', 'be', 'can', 'not', 'the']

output = []
 
def most_common_word(url):
    """
    This function takes a url as the argument
    and returns the most common word found in that web page
    """
    # "load" a webpage 
    r = requests.get(url)

    # decode the text of the HTML.
    # r comes from the requests request above
    soup = BeautifulSoup(r.text, 'lxml')

    # find all anchor tags with the class of "DYST1d".
    # The anchore tag with this tag contains
    # the news article headline and link
    anchor = soup.findAll("a", {"class": "DY5T1d"})

    words = []
    # results = {}
    # counter = 0

    for obj in anchor:
        for obj_text in obj:
            for obj_word in obj_text.split():
                if obj_word not in ignore_word_list:
                    words.append(obj_word)

        
    most_common_word = max(set(words), key = words.count)
    number_of_appearances =  words.count(most_common_word)

    return f'The most common word is "{most_common_word}". It appears {number_of_appearances} times.'

def main():
    print(most_common_word('https://news.google.com/'))

if __name__ == '__main__':
    main()