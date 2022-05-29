from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.request import urlopen
import request

class Crawler:
    """
        
    """

    def __init__(self, url):
        self.url = url
        self.base_url = urlparse(url).netloc
        self.urls = []
        self.urls_404 = []
        self.urls_externe = []
        self.urls_interne = []
        self.urls_form = []
        self.urls_protected = []
        self.is_crawl = False
        self.crawl()

    def get_page(self, url):
        if urlparse(url).netloc == self.base_url:
            if url not in self.urls_interne:
                self.urls_interne.append(url)
            try:
                print("Récupération de la page {}".format(url))
                page = urlopen(url)
                if page.getcode() == 404:
                    self.urls_404.append(url)
                return page.read()
            except:
                print("Impossible de récupérer la page {}".format(url))
        else:
            print("l'URL externe {} ne sera pas analysée.".format(url))
            if url not in self.urls_externe:
                self.urls_externe.append(url)

    def retrieve_links(self, page):
        """
            Analyse la page et retourne toutes les URL's présentes dans les liens :
                - Ajoute les URL's à la liste self.urls si elle n'est pas présente dans url's visitees        
        """
        soup = BeautifulSoup(page, 'html.parser')
        links = soup.find_all('a', href=True)
        for link in links:
            if not link['href'].startswith('#'):
                # Si le lien commence par un # alors c'est une ancre et on peut l'ignorer
                if link['href'].startswith('/'):
                    # On reconstruit l'URL
                    link['href'] = self.url + link['href']
                    if link['href'] not in self.urls and urlparse(link['href']).netloc == self.base_url:
                        self.urls.append(link['href'])
                elif link['href'].startswith('http'):
                    self.urls.append(link['href'])
    
    def forms_links(self, page, url):
        soup = BeautifulSoup(page, 'html.parser')
        forms = soup.find_all('form')
        if len(forms) > 0:
            if url not in self.urls:
                self.urls.append(url)
    
    def protecteds_links(self, page, url):
        soup = BeautifulSoup(page, 'html.parser')
        print()
        inputs = soup.find_all('input')
        print(inputs)
        for input in inputs:
            if input["type"] == "password":
                if url not in self.urls:
                    self.urls.append(url)

    def nombre_url(self):
        """
            Retourne le nombre de pages trouvées
        """
        return len(self.urls)


    def crawl(self):
        # Premier appel sur self.url
        html = self.get_page(self.url)
        self.retrieve_links(html)

        # On itère sur la liste self.urls
        for url in self.urls:
            page = self.get_page(url)
            if page:
                self.forms_links(page, url)
                self.retrieve_links(page)
                self.protecteds_links(page, url)
        self.is_crawl = True
