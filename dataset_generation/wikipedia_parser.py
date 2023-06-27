import requests
import re
import os
from bs4 import BeautifulSoup


FOLDER_PATH = os.getcwd()
HEADER = {'User-Agent': 'scraping a few hundred images for a personal project, contact: thomasrialan@gmail.com'}


def parse_wiki_page(url):
    person_name = url.split('/')[-1]
    rows = _get_info_box_rows(url)
    year_of_birth, year_of_death = _get_year_of_birth_and_death(rows)
    path = f'{FOLDER_PATH}/dataset/{person_name}_birth:{year_of_birth}_death:{year_of_death}'
    year_of_img = download_wiki_image(url, path)
    return year_of_birth, year_of_death, year_of_img


def download_wiki_image(url, path):
    response = requests.get(url, headers=HEADER)
    assert response.status_code == 200
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')
    table = soup.find('table', {'class': 'infobox'})
    assert table, "Could not find the infobox."
    img = table.find('img')
    assert img, "Could not find the image."
    year_of_img = _get_year_of_image(img)
    img_url = 'https:' + img.get('src')
    response = requests.get(img_url, stream=True, headers=HEADER)
    response.raise_for_status()
    img_path = path + f'_date:{year_of_img}.jpg'
    with open(img_path, 'wb') as out_file:
        out_file.write(response.content)
    return year_of_img


def _get_year_of_image(img):
    img_caption = img.get('alt')
    if img_caption is None:
        subsequent_div = img.find_next_sibling('div')
        img_caption = subsequent_div.text
    assert img_caption, "Could not find the image caption."
    if len(_find_dates(img_caption)):
        year_of_img = int(_find_dates(img_caption)[0][:4])
    elif _find_year(img_caption):
        year_of_img = _find_year(img_caption)
    assert year_of_img, "Could not find the year of the image."
    return year_of_img


def _get_year_of_birth_and_death(rows):
    for row in rows:
        header = row.find('th')
        if header:
            if 'born' in header.text.lower():
                dates = _find_dates(row.text)
                year_of_birth = int(dates[0].split('-')[0])
            if 'died' in header.text.lower():
                dates = _find_dates(row.text)
                year_of_death = int(dates[0].split('-')[0])
    return year_of_birth, year_of_death


def _get_info_box_rows(url):
    """ Pages of people have a box of info on the right side of the page. """
    response = requests.get(url, headers=HEADER)
    soup = BeautifulSoup(response.text, 'html.parser')
    infobox = soup.find('table', attrs={'class': 'infobox'})

    if infobox is None:
        print("Could not find the infobox.")
        return None

    rows = infobox.find_all('tr')
    return rows


def _find_dates(input_string):
    """ Find dates formatted as YYYY-MM-DD in a string. """
    pattern = r'\b(\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12][0-9]|3[01]))\b'
    return re.findall(pattern, input_string)


def _find_year(input_string):
    match = re.search(r'\b(19[0-9]{2}|20[0-9]{2})\b', input_string)
    assert match, "Could not find a year."
    return int(match.group())
