from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import os
from os.path import join, dirname
from dotenv import load_dotenv

import boto3
from boto3.session import Session
from boto3.dynamodb.conditions import Key, Attr

import time

from src.routers import db, user

app = FastAPI()

app.add_middleware(
  CORSMiddleware,
  allow_origins = ["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

app.include_router(db.router)
app.include_router(user.router)

@app.get("/")
def hello_world():
  now_time = time.time()
  return {"nowtime":now_time}
