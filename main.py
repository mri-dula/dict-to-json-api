from fastapi import FastAPI, Request, Depends, HTTPException
from exceptions import InvalidDictError
import converter
from pydantic import BaseModel
from config import Settings
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()
if os.environ.get("VERCEL"):
    settings = Settings(_env_file=None)
else:
    settings = Settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.allowed_origin],
    allow_methods=["*"],
    allow_headers=["*"],
)


class DictToConvert(BaseModel):
    text: str


@app.post("/api/convert_and_beautify")
def convert_and_beautify(payload: DictToConvert):
    try:
        return converter.convert(payload.text, beautify=True)
    except InvalidDictError as e:
        raise HTTPException(
            status_code=400, detail={"lineno": e.lineno, "line": e.line}
        )


@app.post("/api/convert_and_minify")
def convert_and_minify(payload: DictToConvert):
    try:
        return converter.convert(payload.text, beautify=False)
    except InvalidDictError as e:
        raise HTTPException(
            status_code=400, detail={"lineno": e.lineno, "line": e.line}
        )
