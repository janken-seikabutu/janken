from fastapi import APIRouter

import os
from os.path import join, dirname
from dotenv import load_dotenv

import boto3
from boto3.session import Session
from boto3.dynamodb.conditions import Key, Attr

import json
from pydantic import BaseModel
import time
import hashlib
import decimal

router = APIRouter()

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

session = Session(
  aws_access_key_id=os.environ["AWS_DYNAMODB_ACCESSKEY"],
  aws_secret_access_key=os.environ["AWS_DYNAMODB_SECRETKEY"],
  region_name=os.environ["AWS_DYNAMODB_REGION"])

dynamodb = session.resource("dynamodb")

@router.get("/user/get/{user_name}")
def get_users(user_name:str):
  table = dynamodb.Table("janken-users")
  result1 = table.scan(
    FilterExpression = Attr("name").eq(f"{user_name}")
  )

  # result2 = json.loads(result1)

  return result1

class User(BaseModel):
  name: str
  password: str

@router.post("/user/register")
def register_user(user:User):
  register_table = dynamodb.Table("janken-users")
  confilm = register_table.scan(
    FilterExpression = Attr("name").eq(f"{user.name}")
  )
  if confilm["Count"] == 0:
    register_pass_hash = hashlib.sha256()
    register_pass_hash.update(user.password.encode())
    response = register_table.put_item(
      Item={
        "name": user.name,
        "password": register_pass_hash.hexdigest(),
        "markov_id": 0,
        "game_count": 0,
        "previous_id": 0,
      }
    )
    return {"name":user.name, "markov_id":0, "game_count":0, "previous_id":0}
  return {"error":"そのユーザーはすでに登録されています。別のユーザー名で登録してください。"}

@router.post("/user/login")
def login_user(user:User):
  login_table = dynamodb.Table("janken-users")
  result = login_table.scan(
    FilterExpression = Attr("name").eq(f"{user.name}")
  )
  if result["Count"] != 0:
    login_pass_hash = hashlib.sha256()
    login_pass_hash.update(user.password.encode())
    if result["Items"][0]["password"] == login_pass_hash.hexdigest():
      markov_id = result["Items"][0]["markov_id"]
      game_count = result["Items"][0]["game_count"]
      previous_id = result["Items"][0]["previous_id"]
      return {"name":user.name, "markov_id":markov_id, "game_count":game_count, "previous_id":previous_id}
    else:
      return {"error":"パスワードが間違っています。"}
  return {"error":"ユーザー名が間違っています。登録したユーザー名を入力してください。登録がまだの場合はユーザー登録をしてください。"}
