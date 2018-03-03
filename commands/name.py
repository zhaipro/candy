# coding: utf-8
import re

import requests


def main():
    r = requests.get('http://www.resgain.net/xmdq.html')
    links = re.findall('//\w+.resgain.net/name_list.html', r.text)
    for link in links:
        r = requests.get('http:' + link)
        for name in re.finditer('/name/(.+)\.html" class', r.text):
            print(name.group(1))


if __name__ == '__main__':
    main()
