from urllib.request import urlopen
from pprint import pprint
import bs4
import argparse

import gettext
import os
import sys

class ClientWeb(object):
    """Client web per descarregar les ofertes de Bang good"""
    
    def __init__(self):
        print(_("Initializing Web Client"))
        super(ClientWeb, self).__init__()

    def run(self):
        """Runs the functions in the correct order"""
        # agafar arguments
        link, path = self.parse_arguments()

        # descaregar-me html
        html = self.descarregar_html(link)

        # buscar deals
        results = self.buscar_deals(html)

        # imprimir resultat
        if path:
            self.store_result(path, results)
        else:
            print(_("Results:"))
            pprint(results)

    def parse_arguments(self):
        """Parses the arguments that the application accepts"""

        parser = argparse.ArgumentParser(description='Returns flash offers from Bang good web.')
        parser.add_argument('-l', '--link', dest='link', type=str, help='link to the web',
                            default='https://www.banggood.com/Flashdeals.html')
        parser.add_argument('-f', '--file', dest='file', type=str, help='path to the output file')

        args = parser.parse_args()

        return args.link, args.file

    def store_result(self, path, result):
        """Stores the result in the specified file with pprint format"""

        print(_("Storing results..."))
        f = open(path, 'w')
        pprint(result, f)
        f.close()

    def descarregar_html(self, link):
        """Gets the html of the page"""

        print(_("Downloading web HTML..."))
        f = urlopen(link)
        html = f.read()
        f.close()
        return html

    def buscar_deals(self, html):
        """Searches the multiple sets of offers and returns a list of lists"""

        print(_("Searching for the best deals..."))
        result = []
        arbre = bs4.BeautifulSoup(html, features='lxml')

        result.append(self.get_li_data_product_info(arbre, 'unbeatabledealsitem newdealsgoods'))
        result.append(self.get_li_data_product_info(arbre, 'brandweekdealsbox newdealsgoods'))

        return result

    def get_li_data_product_info(self, tree, class_name):
        """Searches for the information of one set of offers and returns a list of lists"""

        results = []
        unbeatable_deals_class = tree.find_all(class_=str(class_name))
        for deal_class in unbeatable_deals_class:
            unbeatable_deals = deal_class.find_all('li')
            for deal in unbeatable_deals:
                result = []

                title = []
                spans = deal.find(class_='title')
                for span in spans:
                    title = span.contents[0]
                result.append(title)

                price = self.price_span_content_search(deal, 'price')
                result.append(price)

                price_old = self.price_span_content_search(deal, 'price_old')
                result.append(price_old)

                results.append(result)

        return results

    def price_span_content_search(self, parent, class_name):
        """Searches for the content in a price span type and returns a string"""

        content = []
        spans = parent.find(class_=str(class_name))
        for span in spans:
            content = span
        return content


if __name__ == "__main__":
    appdir = os.path.dirname(sys.argv[0])
    appdir = os.path.abspath(appdir)
    localedir = os.path.join(appdir, "locales")

    gettext.install("dealgetter", localedir, "utf-8")

    print(_("This Code is deprecated as the web recently changed :("))
    c = ClientWeb()
    c.run()
