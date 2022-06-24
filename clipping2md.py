from asyncore import write
from genericpath import exists
from importlib.resources import path
from pydoc import cli
import sys
import os
import argparse

class book:
    def __init__(self, title, author, quote):
        self.title = title
        self.author = author
        self.quote = []
        self.quote.append(quote)
    
    def get_quote(self):
        return self.quote
    
    def get_title(self):
        return self.title


def get_file_content(file_path):
    with open(file_path, 'r') as f:
        return f.read()


def convert2books(content):
    clippings = content.split('==========')
    books = []
    for clipping in clippings:
        add_highlight2book(clipping, books)
    return books


def add_highlight2book(clipping, books):
    if clipping.replace('/\s+/g', '').strip() == '':
        return 
    
    bookTitle, info, newline, quote = clipping.strip().split('\n')
    cur_book = get_book_with_title(books, bookTitle)

    if cur_book is not None:
        cur_book.quote.append(quote)
    else:
        books.append(book(bookTitle, info, quote))


def get_book_with_title(books, book_Title):
    for book in books:
        if book.get_title() == book_Title:
            return book
    return None



def convert2md(out_path, books):
    for book in books:
        if len(book.get_quote()) > 0:
            title = book.get_title()
            remove_duplicate_quote(book)
            quote = book.get_quote()
            write2md(out_path, title, quote)
    pass


def write2md(out_path, title, quote):
    md_file = title + '.md'
    with open(out_path + md_file, 'w') as f:
        f.write('# ' + title + '\n')
        for q in quote:
            f.write('* ' + q + '\n')
    print('Converted ' + title + ' to ' + md_file)
    pass


def remove_duplicate_quote(book):
    quote = book.get_quote()
    quote = list(set(quote))
    book.quote = quote



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert a clipping file to a markdown file.')
    parser.add_argument('-i', '--input', help='Input file', required=True)
    args = parser.parse_args()

    input_file = args.input
    output_file = "./output/"

    if not os.path.isfile(input_file):
        print('Input file does not exist.')
        sys.exit(1)

    if  not os.path.exists(output_file):
        os.makedirs(output_file)
    
    books = convert2books(get_file_content(input_file))
    convert2md(output_file, books)
