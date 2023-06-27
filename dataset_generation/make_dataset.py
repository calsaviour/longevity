import tqdm
import time
from wikidata import get_wikidata
from wikipedia_parser import download_wiki_image, FOLDER_PATH


if __name__ == '__main__': 
    df = get_wikidata()

    for i in tqdm.tqdm(range(len(df))):
        time.sleep(0.5)
        url = df['wikipedia_url'][i]
        birth_year = df['date_of_birth'][i].split('-')[0]
        death_year = df['date_of_death'][i].split('-')[0]
        person_name = df['person_name'][i].replace(" ","_")
        path = f'{FOLDER_PATH}/dataset/{person_name}_birth:{birth_year}_death:{death_year}'
        try:
            download_wiki_image(url, path)
        except:
            print(url)
            import pdb; pdb.set_trace()



