wiki_pages = [
	"https://en.wikipedia.org/wiki/Albert_Einstein",
	"https://en.wikipedia.org/wiki/Steve_Jobs",
	"https://en.wikipedia.org/wiki/Mother_Teresa",
	"https://en.wikipedia.org/wiki/Martin_Luther_King_Jr.",
	"https://en.wikipedia.org/wiki/Marilyn_Monroe",
	"https://en.wikipedia.org/wiki/John_F._Kennedy",
	"https://en.wikipedia.org/wiki/Nelson_Mandela",
	"https://en.wikipedia.org/wiki/Elvis_Presley",
	"https://en.wikipedia.org/wiki/Anne_Frank",
	"https://en.wikipedia.org/wiki/Pablo_Picasso",
	"https://en.wikipedia.org/wiki/Mario_Artali",
	"https://en.wikipedia.org/wiki/Francisco_Bozinovic",
	"https://en.wikipedia.org/wiki/Martin_Davis_(mathematician)",
	"https://en.wikipedia.org/wiki/Elena_Huelva",
	"https://en.wikipedia.org/wiki/John_McCaina",
    "https://en.wikipedia.org/wiki/George_Frazier_(pitcher)",
    "https://en.wikipedia.org/wiki/Doris_Stockhausen",
    "https://en.wikipedia.org/wiki/Diane_Rowe",
    "https://en.wikipedia.org/wiki/Daniel_Ellsberg"]


import requests
from bs4 import BeautifulSoup
import tqdm
import time


def get_people_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    base_url = 'https://en.wikipedia.org'

    people_links = []
    all_links = soup.find_all('a', href=True)[:1000]

    for link in tqdm.tqdm(all_links):
        if '/wiki/' in link['href'] and ':' not in link['href']:
            time.sleep(0.3)
            # This is a Wikipedia page link, but we don't know if it's a person's page.
            # Let's check by sending a request to the page and looking for a birth date.
            possible_person_link = base_url + link['href']
            possible_person_page = requests.get(possible_person_link)
            soup_person = BeautifulSoup(possible_person_page.text, 'html.parser')
            bday = soup_person.find('span', {'class' : 'bday'})
            if bday:
                # This page has a birth date, so it's likely a person's page.
                people_links.append(possible_person_link)
    
    return people_links
