# Analyzing-movie-plots-with-Elasticsearch-and-Python

## Instructions for running system 
Requirements: csv file with the movie plots, Elasticsearch running on localhost:9200, Kibana, Python IDE, Python libraries – elasticsearch, pandas, requests, json.
To run the program run the python file names main.py with the movie plots file in the same directory 

## Indexing
Using the pandas library, I uploaded the csv file to python and converted it to a dataframe. After doing some data analysis, I ran into the first problem - that there where Nan values, as well string values “unknown” and “Unknown”. To get around this I decided to drop the rows with these values. To get the  1000 samples I decided to use the df.sample() function to get a sample of 1000 random rows from the dataframe. At this point I ran into another issue since I needed to convert the dataframe to json to index it in Elasticsearch. To accomplish this, I used the df.to_json() function in conjunction with the json.loads() function. And finally, to upload the data I traverse it with a for loop and upload each document individually.

## Tokenization and Normalization
To tokenize the data as well as lowercase it, I used an elastic analyzer, that includes a lowercase tokenizer. To index it I used the elasticsearch python API indices.create() function

## Selecting Keywords

For stop word removal I used the “stop” filter in an elasticsearch analyzer, which removes English stop words. For the ngram extraction I used the “ngram” type tokenizer with length 3 (for getting trigrams). Finally, for the tfidf scores, I configured the similarity module to use the BM25 type which is a TF/IDF based similarity that has built-in tf normalization.

## Stemming or Morphological Analysis 
To add stemming to the analyzer I added the stemmer filter.

## Searching 
Outputs for examples might not be the same every time since the index has 1000 random movies.
Search example 1: Searching for movies where cast contains Francis
Search example 2: Searching for Movie where Director name starts with T
Search example 3: Searching for Movie about soldiers, but more importance on the title of the movie
 
## Possible improvements
* More usage of Elasticsearch together with python. During the testing of the analyzers, I used the Kibana Dev Tools to test the analyzers, because I could not get the elasticsearch _analyze to work with the request library in python.
* More customized analyzer. The analyzer that I have uses already available filters and tokenizers. This could be improved upon by adding custom scripts for filtering
* UI For searching – allowing the user to search using the terming or even better a GUI could turn this into a real search engine
