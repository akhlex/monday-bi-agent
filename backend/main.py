from fastapi import FastAPI
from pydantic import BaseModel
from agent import process_query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    question: str


@app.post("/query")
def query_agent(q: Query):

    answer = process_query(q.question)

    return {"answer": answer}