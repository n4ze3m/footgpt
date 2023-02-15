import torch

batch_size = 64 
block_size = 256
max_iters = 10000
eval_interval = 500
learning_rate = 3e-3
device = 'cuda' if torch.cuda.is_available() else 'cpu'
eval_iters = 200
n_embed = 384
dropout = 0.2
n_layer = 6
n_head = 6
vocab_size=1006 

MODEL_PATH = 'model/fgpt.pt'
CSV_PATH = "data/football_data.csv"
GDRIVE_ID = ""

CHARS_PATH="data/chars.txt"