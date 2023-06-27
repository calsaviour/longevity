from links import wiki_pages
from wikipedia_parser import parse_wiki_page

if __name__ == '__main__': 
    for link in wiki_pages:
        try:
            parse_wiki_page(link)
        except:
            print("Error: ", link)
            pass

