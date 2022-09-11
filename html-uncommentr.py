from bs4 import BeautifulSoup as BS
from bs4 import Comment
import argparse
import requests
import sys


def extract(url, iscontext):
    try:
        response = requests.get(url)
        
        if response.status_code != requests.codes.ok:
            print(f'Got a response code {response.status_code}. Exiting...')
            sys.exit(-2)

        html = response.text
        bs = BS(html, 'html.parser')
        comments = bs.find_all(string=lambda text: isinstance(text, Comment))

        for comment in comments:
            if iscontext:
                print(comment.parent)
                print('-' * 50)
            else:
                print(comment)
                print('-' * 50)
    except requests.exceptions.MissingSchema:
        print(f'Schema is missing, did you mean http://{url} ?')
        sys.exit(-3)
    except requests.exceptions.ConnectionError:
        print(f'Unable to connect to the website at {url}')
        sys.exit(-1)


def main():
    parser = argparse.ArgumentParser(description='A little script to extract comments from web pages.')
    parser.add_argument('url')
    parser.add_argument('-c', '--context', default=False, action='store_true', help='Gives the HTML context for each comment')

    args = parser.parse_args()
    extract(args.url, args.context)


if __name__ == '__main__':
    main()