from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from outta.parser import Parser
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TranslationRequest(BaseModel):
    text: str


class Element(BaseModel):
    description: str
    text: str


@app.get("/", response_model=List[Element])
async def root(text: str):
    parser = Parser()
    return [
        Element(description=str(element), text=repr(element.text)[1:-1])
        for element in parser.feed(text)
    ]
