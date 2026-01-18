from fastapi import FastAPI
from fastapi import UploadFile, HTTPException
import pandas as pd
import uvicorn
from models import TerroristModel
from db import db
from pymongo import errors

app = FastAPI()
db_object = db()


@app.post("/top-threats")
def foo(file: UploadFile | None = None):
    if not file:
        raise HTTPException(status_code=400, detail="No file provided")
    if file.content_type != "text/csv":
        raise HTTPException(status_code=400, detail="Invalid CSV file")
    try:
        client = db_object.get_connection()
        client.admin.command('ping')
    except errors.ConnectionFailure:
        raise HTTPException(status_code=503, detail="Database unavailable")
    df = pd.read_csv(file.file)
    df = df.sort_values(by=["rate_danger"], ascending=False)
    result = df.head(5)
    count = result.shape[0]
    raw_dict = df.to_dict("records")
    try:
        clean_data = [TerroristModel(**row).model_dump() for row in raw_dict]
    except Exception as e:
        raise HTTPException(status_code=422, detail=e)

    db_object.insert_to_top_threats(clean_data)
    return {"count": count,
            "top": clean_data}


if __name__ == "__main__":
    uvicorn.run(app)
