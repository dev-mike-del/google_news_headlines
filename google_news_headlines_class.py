#!/usr/bin/env python3

from datetime import datetime, timezone

# Beautiful Soup is a Python library for pulling data out of HTML and XML files.
from bs4 import BeautifulSoup

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


    def _as_dict(self):
        results = {}
        index = 0
        iter_source =  iter(self.source)

        for headlines in iter_source:
            org = next(iter_source)
            results[index] = (self.timestamp, headlines.text, org.text)
            index += 1

        return results


    def word_count(self):
        return self._as_dict()


def main():
    data = GoogleNewsHeadlines()
    print(data._as_dict())


if __name__ == '__main__':
    main()

