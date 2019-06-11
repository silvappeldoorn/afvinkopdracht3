from Bio import Entrez
import requests
from bs4 import BeautifulSoup
import pandas as pd


def search(query):
    Entrez.email = 'your.email@example.com'
    handle = Entrez.esearch(db='pubmed',
                            sort='relevance',
                            retmax='2',
                            retmode='xml',
                            term=query)
    results = Entrez.read(handle)
    return results


def fetch_details(id_list):
    ids = ','.join(id_list)
    Entrez.email = 'your.email@example.com'
    handle = Entrez.efetch(db='pubmed',
                           retmode='xml',
                           id=ids)
    results = Entrez.read(handle)
    return results


def get_table():
    res = requests.get("https://echa.europa.eu/web/guest/information-on-chemicals/pre-registered-substances")
    soup = BeautifulSoup(res.content, 'lxml')
    table = soup.find_all('table')[0]
    df = pd.read_html(str(table))
    # print(df)
    df = df[0]
    namen = df["Name"].tolist()
    syns = df["Synonyms"].tolist()
    # print(namen)
    return namen


def main():
    namen = get_table()
    for item in namen:
        print(item)
        item = item.replace("'", "")
        item = item.replace("(", "")
        item = item.replace(")", "")
        results = search(item)
        id_list = results['IdList']
        papers = fetch_details(id_list)
        for i, paper in enumerate(papers['PubmedArticle']): print(
            "%d) %s" % (i + 1, paper['MedlineCitation']['Article']['ArticleTitle']))


main()
