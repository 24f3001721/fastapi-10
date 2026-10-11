from pathlib import Path

import pandas as pd
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load the CSV file from the same directory as app.py
CSV_FILE = Path(__file__).parent / "q-fastapi.csv"
df = pd.read_csv(CSV_FILE)

# Keep the original column names and row order
df = df[["studentId", "class"]]


@app.get("/api")
def get_students(
    class_: list[str] | None = Query(default=None, alias="class")
):
    students = df

    # Filter by one or more requested classes
    if class_:
        students = students[students["class"].isin(class_)]

    # Return the required JSON structure
    return {
        "students": students.to_dict(orient="records")
    }
