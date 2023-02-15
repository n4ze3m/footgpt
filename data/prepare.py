import requests
import os
import numpy as np
from datasets import load_dataset
from utils.converter import encode
from constants import CHARS_PATH, CSV_PATH, GDRIVE_ID


## COPY PASTE FROM https://stackoverflow.com/questions/38511444/python-download-files-from-google-drive-using-url
def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)




if not os.path.exists(CSV_PATH):
    download_file_from_google_drive(GDRIVE_ID, CSV_PATH)


# Load dataset from CSV file
dataset = load_dataset("csv", data_files=CSV_PATH)


split_dataset = dataset["train"].train_test_split(test_size=0.3, seed=2357, shuffle=True)
split_dataset['val'] = split_dataset.pop('test')


num_proc = 1

def process(dataset):
    ids = encode(dataset["text"])
    out = {'ids': ids, 'len': len(ids)}
    return out


tokenized = split_dataset.map(
    process,
    remove_columns=['text'],
    desc="Running tokenizer on dataset",
    num_proc=num_proc,
)

for split, dset in tokenized.items():
    arr_len = np.sum(dset['len'])
    filename =  f'data/{split}.bin'
    dtype = np.uint16
    arr = np.memmap(filename, dtype=dtype, mode='w+', shape=(arr_len,))

    print(f"writing {filename}...")
    idx = 0
    for example in dset:
        arr[idx : idx + example['len']] = example['ids']
        idx += example['len']
    arr.flush()
