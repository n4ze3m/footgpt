from constants import *

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.distributions import Categorical


class Head(nn.Module):
    def __init__(self, head_size):
        super().__init__()
        self.key = nn.Linear(n_embed, head_size, bias=False)
        self.query = nn.Linear(n_embed, head_size, bias=False)
        self.value = nn.Linear(n_embed, head_size, bias=False)
        self.register_buffer('trail', torch.tril(torch.ones(block_size, block_size)))
        self.droupout = nn.Dropout(dropout)
    
    def forward(self, X):
        B, T, C = X.shape
        k = self.key(X) # (B,T,H)
        q = self.query(X) # (B,T,H)

        wei = q @ k.transpose(-2, -1) * C ** -0.5 # (B,T,T)
        wei = wei.masked_fill(self.trail[:T,:T] == 0, float('-inf'))
        wei = F.softmax(wei, dim=-1) # (B,T,T)
        wei = self.droupout(wei)
        
        v = self.value(X) # (B,T,H)
        out = wei @ v # (B,T,H)
        return out

class MultiHeadAttention(nn.Module):
    def __init__(self, n_heads, head_size):
        super().__init__()
        self.heads = nn.ModuleList([Head(head_size) for _ in range(n_heads)])
        self.proj = nn.Linear(n_embed, n_embed)
        self.droupout = nn.Dropout(dropout)
    
    def forward(self, X):
        out =  torch.cat([h(X) for h in self.heads], dim=-1)
        out = self.proj(out)
        out = self.droupout(out)
        return out

class FeedForward(nn.Module):
    def __init__(self, n_embed):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(n_embed,  4 * n_embed),
            nn.ReLU(),
            nn.Linear(4 * n_embed, n_embed),
            nn.Dropout(dropout)
        )

    def forward(self, X):
        return self.net(X)

class Block(nn.Module):

    def __init__(self, n_embed, n_head):
        super().__init__()
        head_size = n_embed // n_head
        self.sa = MultiHeadAttention(n_head, head_size)
        self.ffwd = FeedForward(n_embed)
        self.ln1 = nn.LayerNorm(n_embed)
        self.ln2 = nn.LayerNorm(n_embed)


    def forward(self, x):
        x = x + self.sa(self.ln1(x))
        x = x + self.ffwd(self.ln2(x))
        return x


class GPT(nn.Module):

    def __init__(self):
        super().__init__()
        self.token_embedding_table = nn.Embedding(vocab_size, n_embed)
        self.position_embedding_table = nn.Embedding(block_size, n_embed)
        self.blocks = nn.Sequential(
            *[Block(n_embed, n_head=n_head) for _ in range(n_layer)],
        )
        self.ln_f = nn.LayerNorm(n_embed)
        self.lang_head = nn.Linear(n_embed, vocab_size)

    def forward(self, idx, targets=None):
        B, T = idx.shape
        # idx and targets are both (B,T) tensor of integers
        token_emb = self.token_embedding_table(idx) # (B,T,C)
        pos_emb = self.position_embedding_table(torch.arange(T, device=device)) # (T,C)
        X = token_emb + pos_emb # (B,T,C)
        X = self.blocks(X) # (B,T,C)
        X = self.ln_f(X)
        logits = self.lang_head(X) # (B,T,VOCAB_SIZE)

        if targets is None:
            loss = None
        else:
            B, T, C = logits.shape
            logits = logits.view(B*T, C)
            targets = targets.view(B*T)
            loss = F.cross_entropy(logits, targets)

        return logits, loss

    def generate(self, idx, max_new_tokens, temperature=1.0, freq_penalty=0.0, top_p=None):
        """


        idx: (B, T) tensor of integers (eg. [[1,2,3,4,5]])
        max_new_tokens: number of tokens to generate (eg. 10)
        temperature: temperature for sampling (eg. 1.0) 
        freq_penalty: penalty for frequency of tokens (eg. 0.0)
        top_p: top-p sampling (eg. 0.9)

        returns: (B, T+max_new_tokens) tensor of integers


        """
        for _ in range(max_new_tokens):
            idx_cond = idx[:, -block_size:] # (B, T)
            logits, loss = self(idx_cond)
            logits = logits[:, -1, :] # becomes (B, C)
            logits /= temperature
            freq = torch.bincount(idx.view(-1), minlength=vocab_size).unsqueeze(0)
            probs = F.softmax(logits - freq_penalty*freq, dim=-1) # (B, C)

            if top_p is not None:
                sorted_probs, sorted_indices = torch.sort(probs, descending=True)
                cum_probs = torch.cumsum(sorted_probs, dim=1)
                sorted_indices_to_remove = cum_probs > top_p
                sorted_indices_to_remove[:, 1:] = sorted_indices_to_remove[:, :-1].clone()
                sorted_indices_to_remove[:, 0] = 0
                for i in range(sorted_probs.shape[0]):
                    indices_to_remove = sorted_indices[i, sorted_indices_to_remove[i]]
                    probs[i, indices_to_remove] = 0
                probs = probs / probs.sum(dim=-1, keepdim=True)

            idx_next = torch.multinomial(probs, num_samples=1) # (B, 1)
            idx = torch.cat((idx, idx_next), dim=1) # (B, T+1)
        return idx