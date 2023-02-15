import os
import pandas as pd
from constants import CHARS_PATH, CSV_PATH

def get_chars():
  if os.path.isfile(CHARS_PATH):
    with open(CHARS_PATH, "r", encoding="utf-8") as f:
      chars = list(f.read())
      return chars
  
  db = pd.read_csv(CSV_PATH)
  text = db['text'].str.cat(sep='\n')

  with open(CHARS_PATH, "w", encoding="utf-8") as f:
    f.write(text)

  return  sorted(list(set(text)))

chars = get_chars()
stoi = { ch:i for i,ch in enumerate(chars) }
itos = { i:ch for i,ch in enumerate(chars) }
encode = lambda s: [stoi[c] for c in s] # encoder: take a string, output a list of integers
decode = lambda l: ''.join([itos[i] for i in l]) # decoder: take a list of integers, output a string