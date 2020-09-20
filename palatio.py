import re
import spacy

import nltk
#nltk.download('popular')
from nltk.corpus import words

import pandas as pd
import itertools
import json


# We have pre-sorted the 'Food' column in ascending order to be able to apply binary search for optimization
def search(ingredient, food_column):
  low = 0
  high = len(food_column) - 1
  while (low <= high): 
      mid = (low + high) // 2
  
      if (ingredient == food_column[mid] or ingredient in food_column[mid]):
          return mid
      elif (ingredient < food_column[mid]):
          high = mid - 1
      else:
          low = mid + 1

  return -1



def search_database(ingredients_list, food_column, data, food_allergy_mapping):
  index = 0
  while index < len(ingredients_list):
      ingredient = ingredients_list[index]
      res = search(ingredient, food_column)
      if res != -1:
        food_allergy_mapping[ingredient] = data['Allergy'][res]
        ingredients_list.remove(ingredient)
      
      index += 1



def palatio(raw_text):
    raw_text_modified = re.sub('(ingredients)|([\/\n\.:])| ([\d]*)', ' ', raw_text.lower()).strip()

    nlp = spacy.load('en_core_web_sm')
    doc = nlp(raw_text_modified)

    # Lemmatizing the ingredients
    ingredients_list = sorted(list(set([token.lemma_ for token in doc if not token.is_punct and not token.is_stop and not token.is_space and str(token.lemma_) in words.words()])))

    data = pd.read_csv('FoodData.csv')
    # Lowercasing the data
    data = data.apply(lambda x: x.astype(str).str.lower())

    # Storing the values of 'Food' column in a list
    food_column = data['Food'].values.tolist()

    ingredients_list_copy = ingredients_list[:]
    food_allergy_mapping = {}

    # Generating permutations of size two of the ingredients
    ingredients_list_copy = list(itertools.permutations(ingredients_list, 2))
    for index in range(len(ingredients_list_copy)):
        ingredients_list_copy[index] = ' '.join(ingredients_list_copy[index])

    # Searching for permutations of ingredients first
    search_database(ingredients_list_copy, food_column, data, food_allergy_mapping)
    # Searching for individual ingredients
    search_database(ingredients_list, food_column, data, food_allergy_mapping)


    json_output = json.dumps(food_allergy_mapping)
    return json_output





