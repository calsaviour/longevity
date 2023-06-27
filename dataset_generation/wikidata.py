import sys
import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON

endpoint_url = "https://query.wikidata.org/sparql"

query = """SELECT ?person ?personLabel ?date_of_birth ?date_of_death ?image ?wikipediaUrl WHERE {
  ?person wdt:P31 wd:Q5;
          wdt:P569 ?date_of_birth;
          wdt:P570 ?date_of_death;
          wdt:P18 ?image;
  FILTER(YEAR(?date_of_death) = 2023)
  ?article schema:about ?person;
           schema:isPartOf <https://en.wikipedia.org/>.  
  BIND(IRI(STR(?article)) AS ?wikipediaUrl)
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }

  }
LIMIT 10"""


def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


def dict_to_dataframe(dict_list):
    processed_dicts = []
    for d in dict_list:
        processed_dict = {}
        processed_dict['person'] = d['person']['value']
        processed_dict['date_of_death'] = d['date_of_death']['value']
        processed_dict['image'] = d['image']['value']
        processed_dict['date_of_birth'] = d['date_of_birth']['value']
        processed_dict['personLabel'] = d['personLabel']['value']
        processed_dict['wikipediaUrl'] = d['wikipediaUrl']['value']
        processed_dicts.append(processed_dict)
    return pd.DataFrame(processed_dicts)

results = get_results(endpoint_url, query)
df = dict_to_dataframe(results["results"]["bindings"])
