import argparse

import requests
from bs4 import BeautifulSoup

_cernbox_url = 'https://cernbox.cern.ch/index.php/s/9P8yC5FQcszSb9i'
_cernbox_url = 'https://cernbox.cern.ch/index.php/s/YBS6PhSyoLJPH5j'


def get_cernbox_webpage(url=_cernbox_url):
    request = requests.get(url)
    request.raise_for_status()
    soup = BeautifulSoup(request.content, 'html.parser')
    return soup


def get_datasets(soup: BeautifulSoup = get_cernbox_webpage()):
    print
    files = soup.find_all('td', {'class': 'filename ui-draggable'})
    print(files)


def download():
    """Entrypoint function to parse the arguments download a dataset from cernbox"""
    parser = argparse.ArgumentParser(description='Download an ALICE3 dataset from cernbox.')
    parser.add_argument('file', help='Location of the analysis results file to be plotted')


if __name__ == '__main__':
    download()
