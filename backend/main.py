from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent import process_query

app = FastAPI()

# CORS (needed for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    question: str


@app.get("/")
def root():
    return {"status": "Monday BI Agent running"}


@app.post("/query")
def query_agent(q: Query):

    answer = process_query(q.question)

    return {"answer": answer}