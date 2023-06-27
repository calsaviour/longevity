import tqdm
import time
from wikipedia_parser import parse_wiki_page

if __name__ == '__main__': 
    with open("links.txt", "r") as f:
        wiki_pages = f.readlines()

    for link in tqdm.tqdm(wiki_pages):
        try:
            parse_wiki_page(link)
            time.sleep(0.1)
        except:
            print("Error: ", link)
            pass

