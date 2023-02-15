from gpt import GPT
from constants import *
import torch
from utils.converter import encode, decode
from utils.clean import clean_text
from fastapi import FastAPI
from pydantic import BaseModel
from uvicorn import run
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

origins = ["*"]
methods = ["*"]
headers = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=methods,
    allow_headers=headers
)


model = GPT()
model.load_state_dict(torch.load(MODEL_PATH, map_location=device))
model.to(device)

class Generate(BaseModel):
    prompt: str
    max_new_tokens: int = 256
    temperature: float = 0.7
    top_p: float = 0.9
    freq_penalty: float = 0.0


@app.post("/generate")
def generate(generate: Generate):
    prompt = generate.prompt
    context = torch.tensor(encode(prompt), dtype=torch.long, device=device)
    context = context.unsqueeze(0)
    generated = decode(model.generate(context, max_new_tokens=generate.max_new_tokens, temperature=generate.temperature,
                                      top_p=generate.top_p, freq_penalty=generate.freq_penalty, )[0].tolist())
    return {
        "prompt": prompt,
        "generated": clean_text(generated)
    }

@app.get("/random")
def random():
    context = torch.randint(0, vocab_size, (1, 1), dtype=torch.long, device=device)
    generated = decode(model.generate(context, max_new_tokens=500, temperature=0.7, top_p=0.9, freq_penalty=0.0, )[0].tolist())
    return {
        "generated": clean_text(generated)
    }

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    run(app, host="0.0.0.0", port=port)