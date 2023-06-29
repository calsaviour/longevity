import tqdm
import time
import pandas as pd
from wikidata import get_wikidata
from wikipedia_parser import download_wiki_image, FOLDER_PATH


if __name__ == '__main__': 
    df = get_wikidata()
    import pdb;pdb.set_trace() 
    #df = pd.read_pickle("df_0515.pkl")
    errors = []

    for i in tqdm.tqdm(range(len(df))):
        try:
            url = df['wikipedia_url'][i]
            birth_year = int(df['date_of_birth'][i].split('-')[0])
            death_year = int(df['date_of_death'][i].split('-')[0])
            person_name = df['person_name'][i].replace(" ","_")
            download_wiki_image(url, birth_year, death_year, person_name)
        except:
            errors.append(url)
            print(len(errors))


