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

        # imprimir resultat
        if path:
            self.store_result(path, html)
        else:
            print(html)

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


if __name__ == "__main__":
    c = ClientWeb()
    c.run()