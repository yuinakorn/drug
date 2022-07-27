from typing import Union, List

from fastapi import FastAPI, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from starlette import status

import models
import os
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from dotenv import dotenv_values

from fastapi.middleware.cors import CORSMiddleware

config_env = {
    **dotenv_values(".env"),  # load local file development variables
    **os.environ,  # override loaded values with system environment variables
}

app = FastAPI()

origins = [
    config_env["ORIGINS_URL_1"],
    config_env["ORIGINS_URL_2"],
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=[config_env["ALLOW_METHODS"]],
    allow_headers=[config_env["ALLOW_HEADERS"]],
)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class DrugAllergy(BaseModel):
    cid: str = Field(min_length=1, max_length=13, required=True)
    dname: str = Field(min_length=1, max_length=100)


@app.get("/", status_code=200, tags=["Read"])
async def root():
    return {"message": "Hello API"}


@app.get("/drug/allergy/{cid}/t/{token}", tags=["Read"])
async def read_drug_allergy(cid: str, token: str, db: Session = Depends(get_db)):
    drug_name = []
    drug_alg_cid = await db.query(models.DrugAllergy).filter(models.DrugAllergy.cid == cid).first()

    # if cid is not a number, return error
    if not cid.isdigit():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="CID must be a number")

    # if cid length is not 13, return error
    elif len(cid) != 13:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="CID must be 13 characters long")

    # if cid is not in the database, return error
    elif drug_alg_cid is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="CID not found")

    # if cid is in the database, return cid
    else:
        drug_allergy = db.query(models.DrugAllergy.dname) \
            .filter(models.DrugAllergy.cid == cid) \
            .group_by(models.DrugAllergy.dname).all()

        # for i in drug_allergy:
        #    drug_name.append(i[0].replace(" ", ""))

        if drug_allergy:
            return {"cid": cid, "drug_allergy": [drug_allergy.dname for drug_allergy in drug_allergy]}

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Something went wrong!")
