from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from app.config import merge_config

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/effective-config")
def effective_config(set: List[str] = Query(default=[])):
    cli_overrides = {}
    for item in set:
        if "=" in item:
            key, value = item.split("=", 1)
            cli_overrides[key] = value

    return merge_config(cli_overrides)
