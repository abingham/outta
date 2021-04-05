from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from outta.parser import Parser

app = FastAPI()


class TranslationRequest(BaseModel):
    text: str


class Element(BaseModel):
    description: str
    text: str


@app.get("/", response_model=List[Element])
async def root(request: TranslationRequest):
    parser = Parser()
    return [
        Element(description=str(element), text=element.text)
        for element in parser.feed(request.text)
    ]
