from fastapi import FastAPI
from fastapi import UploadFile, HTTPException
import pandas as pd
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
    df = df.sort_values(by=["danger_rate"], ascending=False)
    result = df.head(5)
    count = result.shape[0]
    raw_dict = result.to_dict("records")
    try:
        clean_data_temp = [TerroristModel(**item).dict() for item in raw_dict]
        clean_data = [TerroristModel(**item).dict() for item in raw_dict]
    except Exception as e:
        raise HTTPException(status_code=422, detail=e)

    db_object.insert_to_top_threats(clean_data_temp)
    return {"count": count,
            "top": clean_data}
