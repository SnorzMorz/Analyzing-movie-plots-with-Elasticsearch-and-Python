# -----------------------------------------------------------
# CE306 - Information Retrieval - Assignment 1
# VAIVO58002
# -----------------------------------------------------------

from elasticsearch import Elasticsearch, helpers
import requests, json, os
import pandas as pd
import logging  # for debugging purposes

es = Elasticsearch("http://localhost:9200")  # Initiating instance of ElasticSearch
print(es.info())
uri = 'http://localhost:9200'  # For connecting to ElasticSearch

headers = {'content-type': 'application/json'}

# -----------------------------------------------------------
# Part 1 - Creating index in ElasticSearch with analyzer, tokenizer and case folding
# -----------------------------------------------------------


request_body_setup = {
    "settings": {
        "analysis": {
            "analyzer": {
                "my_custom_analyzer2": {
                    "type": "custom",
                    "tokenizer": "my_tokenizer",
                    "filter": ["asciifolding"]
                }
            },
            "tokenizer": {
                "my_tokenizer": {
                    "type": "lowercase" # Lowercase tokenizer
                }
            }
        }
    }
}

print(es.indices.create(index='index_part_1', body=request_body_setup))

# -----------------------------------------------------------
# Part 2 - Preparing Dataset
# -----------------------------------------------------------


df = pd.read_csv('wiki_movie_plots_deduped.csv')  # Reading to Dataframe from CSV
df = df[df.Director != "Unknown"]  # Removing rows with unknown values
df = df[df.Genre != "unknown"]
df = df.dropna(axis='rows')
df_1000 = df.sample(n=1000)  # Taking 1000 random rows form cleaned dataset

print(df_1000.head())

movie_plots_json_str = df_1000.to_json(orient='records')  # Converting df to Json string
movie_plots_json = json.loads(movie_plots_json_str)  # Converting Json string to Json

# -----------------------------------------------------------
# Part 3 - Adding stopwords removal, tfidf with similarity module, ngrams (trigrams in this case)
# -----------------------------------------------------------

request_body_setup = {
    "settings": {
        "analysis": {
            "analyzer": {
                "my_analyzer": {
                    "tokenizer": "my_tokenizer",
                    "filter": ["asciifolding", "stop", "lowercase"]  # Stopwords filter, lowercase filter
                }
            },
            "tokenizer": {
                "my_tokenizer": {
                    "type": "ngram",  # N-gram tokenizer
                    "min_gram": 3,
                    "max_gram": 3,
                    "token_chars": [
                        "letter",
                        "digit"
                    ]
                }
            }
        },
        "similarity": {
            "default": {
                "type": "BM25"  # TF/IDF based similarity that has built-in tf normalization
            }
        }
    }
}

print(es.indices.create(index='index_part_3', body=request_body_setup))

# -----------------------------------------------------------
# Part 4 - Adding Stemming
# -----------------------------------------------------------

request_body_setup = {
    "settings": {
        "analysis": {
            "analyzer": {
                "my_analyzer": {
                    "tokenizer": "my_tokenizer",
                    "filter": ["asciifolding", "stop", "lowercase", "stemmer"]  # stemmer filter
                }
            },
            "tokenizer": {
                "my_tokenizer": {
                    "type": "whitespace"
                }
            }
        },
        "similarity": {
            "default": {
                "type": "BM25"  # TF/IDF based similarity that has built-in tf normalization
            }
        }
    }
}

print(es.indices.create(index='index_part_final', body=request_body_setup))

# -----------------------------------------------------------
# Part 5 - Adding data to index
# -----------------------------------------------------------

i = 1
for item in movie_plots_json:  # Adding each json document to ElasticSearch index
    es.index(index='index_part_4', id=i, body=item)
    i = i + 1

# -----------------------------------------------------------
# Part 6 - Example Searching
# -----------------------------------------------------------


q1 = {  # Query 1 - Searching for movies where cast contains Francis
    "query": {
        "match": {
            "Cast": {
                "query": "Francis"
            }
        }
    }
}

resp = es.search(index="index_part_4", body=q1)
print("Query 1 - Searching for movies where cast contains Francis")
print("Got %d Hits:" % resp['hits']['total']['value'])
for hit in resp['hits']['hits']:
    print(hit["_score"], hit["_source"])

q2 = {  # Example Query 2 - Searching for Movie where Director name starts with T
    "query": {
        "wildcard": {
            "Director": "t*"
        }
    }
}

resp = es.search(index="index_part_4", body=q2)
print("Query 2 - Searching for Movie where Director name starts with T")
print("Got %d Hits:" % resp['hits']['total']['value'])
for hit in resp['hits']['hits']:
    print(hit["_score"], hit["_source"])

q3 = {  # Example Query 3 - Searching for Movie about soldiers, but more importance on the title of the movie
    "query": {
        "multi_match": {
            "query": "soldier",
            "fields": ["Title^2", "Plot"]
        }
    }
}

resp = es.search(index="index_part_4", body=q3)
print("Example Query 3 - Searching for Movie about soldiers, but more importance on the tile of the movie")
print("Got %d Hits:" % resp['hits']['total']['value'])
for hit in resp['hits']['hits']:
    print(hit["_score"], hit["_source"])
