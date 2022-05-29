import argparse
from _crawler import Crawler

parser = argparse.ArgumentParser(description="get page info")

parser.add_argument("-u", "--url", help="get the information of a page")
parser.add_argument("-e", "--export", action='store_true', help="(optionnal) export the report to a file")
parser.add_argument("--user")
parser.add_argument("--password")

args = parser.parse_args()
print(args.url)
if args.url:

    if args.url.startswith("http"):
        
        crawler = Crawler(args.url)

        numbers_of_urls=crawler.nombre_url()
        
        export = ""

        export+="nombre d'urls : " + str(numbers_of_urls)
        export+="\n\nurls pointant sur le même domaine : " + "\n\t - ".join(crawler.urls_interne)
        export+="\n\nurls pointant sur un domaine differents : " + "\n\t - ".join(crawler.urls_externe)
        export+="\n\nurls non trouvées : " + "\n\t - ".join(crawler.urls_404)
        export+="\n\nurls contenant un formulaire : " + "\n\t - ".join(crawler.urls_form)
        export+="\n\nurls demandant un mot de passe : " + "\n\t - ".join(crawler.urls_protected)

        print(export)

        if args.export:
            