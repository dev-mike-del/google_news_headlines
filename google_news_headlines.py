#!/usr/bin/env python3

from datetime import datetime, timezone
import itertools
import json

# Beautiful Soup is a Python library for pulling data out of HTML and XML files.
from bs4 import BeautifulSoup

import pandas as pd

# Requests is a Python HTTP library
import requests

# lxml is a Python library which allows for easy handling of XML and HTML files.
import lxml


class GoogleNewsHeadlines(object):
    """docstring for GoogleNewsHeadlines"""
    def __init__(self):
        super(GoogleNewsHeadlines, self).__init__()
        r = requests.get('https://news.google.com/')
        soup = BeautifulSoup(r.text, 'lxml')
        self.source = soup.findAll(True, {'class':['DY5T1d', 'wEwyrc']})
        self.timestamp = datetime.now(timezone.utc)
        # This list is to filter out any words (str) that are single letters
        self.alphabet_list = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p',
                    'q','r','s','t','u','v','w','x','y','z']

        # This list is to filter out any numbers that may appear in the text
        self.string_numbers_list = ['0','1','2','3','4','5','6','7','8','9']

        # This list is to filter out and punctuation from the word_count function
        self.punctuation_list = ['.', ',', '!', '?', ';', ':', '"', '\'', '[', ']', '{', '}',
                       '\\', '|', '=', '+', '‒', '–', '—', '―', '(', ')', '*', '~', '&']

        # This list is to filter out any unwanted words from the word_count function
        self.ignore_word_list = ['', 'a', 'about', 'after', 'all', 'amid', 'an', 'and', 
                            'are', 'as', 'at', 'be', 'but', 'by', 'can', 'could', 
                            'during', 'for', 'from', 'get', 'gets', 'has', 'have', 
                            'he', 'his', 'how', 'if', 'in', 'is', 'it', 'it\'s', 
                            'new', 'news', 'not', 'of', 'on', 'or', 'out', 'says', 
                            'takes', 'than', 'that', 'the', 'this', 'to', 'was', 
                            'will', 'what', 'when', 'with', 'who', 'why', 'won\'t',]

        # This lambda funciton is used to check if a word (str) is unicode
        self.isascii = lambda s: len(s) == len(s.encode())

        self.num_of_headlines = len(self.source) / 2


    def _as_dict(self):
        results = {}
        index = 0
        iter_source =  iter(self.source)

        for headlines in iter_source:
            org = next(iter_source)
            results[index] = (headlines.text, org.text, self.num_of_headlines, self.timestamp,)
            index += 1

        return results


    def _as_json(self):
        return json.dumps(self._as_dict(),default=str)


    def _as_pandas_dataframe(self):
        results = []
        iter_source =  iter(self.source)
        for headline in iter_source:
            org = next(iter_source)
            results.append([self.timestamp, 
                              headline.text, 
                              org.text, 
                              self.num_of_headlines])
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', None)
        colNames = ['headline',
                    'organization',
                    'number_of_headlines',
                    'timestamp',
                    ]
        df = pd.DataFrame(data = results, columns = colNames)
        return df

    def _as_table_schema_json(self):
        df = self._as_pandas_dataframe()
        df['timestamp'] = pd.to_datetime(df.timestamp.astype(str))
        return df.to_json(orient='table')


    def word_count(self):
        source = self._as_dict()
        results = {}
        index = 0
        clean_words_list = []

        raw_words_list = [headline[1][1].split() for headline in source.items()]
        words_list = list(itertools.chain.from_iterable(raw_words_list))
        lowercased_words_list = [headline.lower() for headline in words_list]

        for word in lowercased_words_list:
            if word[0] in self.punctuation_list:
                word = word.replace(word[0], '')
            elif word[-1] in self.punctuation_list:
                word = word.replace(word[-1], '')
            if (word not in self.ignore_word_list and
                word not in self.punctuation_list and
                word not in self.alphabet_list and 
                word not in self.string_numbers_list and
                self.isascii(word) == True):
                clean_words_list.append(word.lower())


        num_of_words = len(clean_words_list)
        for i in list(set(clean_words_list)):
            word = max(set(clean_words_list), 
                key = clean_words_list.count)
            appearances =  clean_words_list.count(word)
            results[index] = {'word': word, 
                              'appearances': appearances,
                              'number_of_words': num_of_words,
                              'timestamp': self.timestamp}
            clean_words_list = list(
                filter((word).__ne__, clean_words_list))
            index += 1

        return results


    def word_count_as_json(self):
        return json.dumps(self.word_count(), default=str)
        


def main():
    data = GoogleNewsHeadlines()
    print(data._as_json())


if __name__ == '__main__':
    main()

