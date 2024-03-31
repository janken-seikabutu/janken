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

router = APIRouter()

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

session = Session(
  aws_access_key_id=os.environ["AWS_DYNAMODB_ACCESSKEY"],
  aws_secret_access_key=os.environ["AWS_DYNAMODB_SECRETKEY"],
  region_name=os.environ["AWS_DYNAMODB_REGION"])

dynamodb = session.resource("dynamodb")

router = APIRouter()

class Store(BaseModel):
  name:str
  hand:str
  result:str
  game_count:int
  previous_id:int
  markov_id:int

@router.post("/game/1")
def score_store(store:Store):
  score_table = dynamodb.Table("janken-scores")
  count_scores = score_table.scan()
  score_id = count_scores["Count"] + 1
  response_score = score_table.put_item(
    Item={
      "id": score_id,
      "user_name": store.name,
      "hand": store.hand,
      "result": store.result,
      "game_id": 1,
    }
  )

  user_table = dynamodb.Table("janken-users")
  response_user = user_table.get_item(
    Key={
      "name": store.name,
    }
  )
  markov_id = store.markov_id
  markov_table = dynamodb.Table("janken-markov")
  
  if markov_id == 0:
    count_markov = markov_table.scan()
    markov_table.put_item(
      Item={
        "id":count_markov["Count"] + 1,
        "user_name": store.name,
        "gw-g":0,
        "gw-c":0,
        "gw-p":0,
        "gl-g":0,
        "gl-c":0,
        "gl-p":0,
        "gd-g":0,
        "gd-c":0,
        "gd-p":0,
        "cw-g":0,
        "cw-c":0,
        "cw-p":0,
        "cl-g":0,
        "cl-c":0,
        "cl-p":0,
        "cd-g":0,
        "cd-c":0,
        "cd-p":0,
        "pw-g":0,
        "pw-c":0,
        "pw-p":0,
        "pl-g":0,
        "pl-c":0,
        "pl-p":0,
        "pd-g":0,
        "pd-c":0,
        "pd-p":0,
      }
    )
    markov_id = count_markov["Count"] + 1
  
  else:
    previous_result = score_table.get_item(
      Key={"id": store.previous_id},
    )
    count_markov = markov_table.get_item(
      Key={"id":markov_id}
    )
    attribut_name = previous_result["Item"]["hand"] + previous_result["Item"]["result"] + "-" + store.hand
    markov_table.update_item(
      Key = {"id":markov_id},
      UpdateExpression = "set #result = :count",
      ExpressionAttributeNames = {"#result":attribut_name},
      ExpressionAttributeValues = {":count" : count_markov["Item"][f"{attribut_name}"] + 1}
    )
  
  user_table = dynamodb.Table("janken-users")
  response_update_user = user_table.update_item(
    Key = {"name":store.name},
    UpdateExpression = "set previous_id = :previous_id, game_count = :game_count, markov_id = :markov_id",
    ExpressionAttributeValues = {":previous_id" : score_id, ":game_count" : store.game_count + 1, ":markov_id" : markov_id},
  )

  return {"previous_id":score_id, "game_count":store.game_count + 1, "markov_id":markov_id}
