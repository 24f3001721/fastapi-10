from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the CSV file from the same directory as app.py
df = pd.read_csv("q-fastapi.csv")

@app.get("/api")
def get_students(class_filter: list[str] | None = Query(default=None, alias="class")):
    result = df

    if class_filter:
        result = result[result["class"].astype(str).isin(class_filter)]

    return result.to_dict(orient="records")
