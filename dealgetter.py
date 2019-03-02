from urllib.request import urlopen
import bs4
import argparse

class ClientWeb(object):
    """"Client web per descarregar les ofertes de Bang good"""
    def __init__(self):
        super(ClientWeb, self).__init__()
        pass

    def run(self):
        # agafar arguments
        link, path = self.parse_arguments()

        # descaregar-me html
        html = self.descarregar_html(link)

        # buscar deals
        results = self.buscar_deals(html)

        # imprimir resultat
        if path:
            self.store_result(path, html)
        else:
            print(results)

    def parse_arguments(self):
        parser = argparse.ArgumentParser(description='Returns flash offers from Bang good web.')
        parser.add_argument('-l', '--link', dest='link', type=str, help='link to the web',
                            default='https://www.banggood.com/Flashdeals.html')
        parser.add_argument('-f', '--file', dest='file', type=str, help='path to the output file')

        args = parser.parse_args()

        return args.link, args.file

    def store_result(self, path, result):
        f = open(path, 'w')
        f.write(str(result))
        f.close()

    def descarregar_html(self, link):
        f = urlopen(link)
        html = f.read()
        f.close()
        return html

    def buscar_deals(self, html):
        unbeatable_deals = []
        result = []
        arbre = bs4.BeautifulSoup(html, features='lxml')

        results = self.get_li_data_product_info(arbre)

        return results

    def get_li_data_product_info(self, tree):
        unbeatable_deals_class = tree.find_all(class_="unbeatabledealsitem newdealsgoods")
        for deal_class in unbeatable_deals_class:
            unbeatable_deals = deal_class.find_all('li')
        results = []
        for deal in unbeatable_deals:
            result = []
            # title = self.span_content_search(deal, class_='title')
            # result.append(title)

            title = []
            spans = deal.find(class_='title')
            for span in spans:
                title = span.contents
            result.append(title)

            price = []
            spans = deal.find(class_='price')
            for span in spans:
                price = span
            result.append(price)

            price = []
            spans = deal.find(class_='price_old')
            for span in spans:
                price_old = span

            result.append(price_old)

            results.append(result)

        return results


    def span_content_search(self, parent, class_name):
        for thing in parent:
            spans = thing.find(class_name)
            for span in spans:
                content = span.contents
            return content



if __name__ == "__main__":
    c = ClientWeb()
    c.run()