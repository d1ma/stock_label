"""
util.py


utilities for nlp tasks for this project: tokenizing by sentence, building 
a tree of the sentence, etc.



"""
import nltk
import string

parser = nltk.data.load('tokenizers/punkt/english.pickle')
filter_ascii = lambda s: filter(lambda x: x in string.printable, s)
regex = "\[\[(.*?)\]\]"
comma_int = r'[1-9]{1}\d{0,2}(?:,\d{3}){1,5}'
