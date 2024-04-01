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

import random

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
  game_count = score_table.scan(
    FilterExpression = Attr("user_name").eq(f"{store.name}")
  )
  response_update_user = user_table.update_item(
    Key = {"name":store.name},
    UpdateExpression = "set previous_id = :previous_id, game_count = :game_count, markov_id = :markov_id",
    ExpressionAttributeValues = {":previous_id" : score_id, ":game_count" : game_count["Count"], ":markov_id" : markov_id},
  )

  return {"previous_id":score_id, "game_count":game_count["Count"], "markov_id":markov_id}

class Markov(BaseModel):
  name:str
  hand:str
  previous_id:int
  markov_id:int

@router.post("/game/2")
def markov_game(markov:Markov):
  score_table = dynamodb.Table("janken-scores")
  previous_result = score_table.get_item(
    Key={"id":markov.previous_id}
  )
  previous_hand_and_result = previous_result["Item"]["hand"] + previous_result["Item"]["result"] + "-"

  rock = previous_hand_and_result + "g"
  scissors = previous_hand_and_result + "c"
  paper = previous_hand_and_result + "p"

  markov_table = dynamodb.Table("janken-markov")
  markov_result = markov_table.get_item(
    Key = {"id":markov.markov_id}
  )

  count_rock = markov_result["Item"][f"{rock}"]
  count_scissors = markov_result["Item"][f"{scissors}"]
  count_paper = markov_result["Item"][f"{paper}"]

  counter = [count_rock, count_scissors, count_paper]
  max_index = [i for i, x in enumerate(counter) if x == max(counter)]

  hands = ["g", "c", "p"]
  choice_hand = random.choice(max_index)
  if choice_hand - 1 == -1:
    hand_ai = "p"
  else:
    hand_ai = hands[choice_hand - 1]

  game_result = ""

  if markov.hand == hand_ai:
    game_result = "d"
  elif markov.hand == "g":
    if hand_ai == "c":
      game_result = "w"
    else:
      game_result = "l"

  elif markov.hand == "c":
    if hand_ai == "p":
      game_result = "w"
    else:
      game_result = "l"

  else:
    if hand_ai == "g":
      game_result = "w"
    else:
      game_result = "l"
  
  attribut_name = previous_hand_and_result + markov.hand

  markov_table.update_item(
    Key = {"id":markov.markov_id},
    UpdateExpression = "set #result = :count",
    ExpressionAttributeNames = {"#result":attribut_name},
    ExpressionAttributeValues = {":count" : markov_result["Item"][f"{attribut_name}"] + 1}
  )

  count_scores = score_table.scan()
  score_id = count_scores["Count"] + 1
  score_table.put_item(
    Item={
      "id": score_id,
      "user_name": markov.name,
      "hand": markov.hand,
      "result": game_result,
      "game_id": 2,
    }
  )
  game_count = score_table.scan(
    FilterExpression = Attr("user_name").eq(f"{markov.name}")
  )

  user_table = dynamodb.Table("janken-users")
  user_table.update_item(
    Key = {"name":markov.name},
    UpdateExpression = "set previous_id = :previous_id, game_count = :game_count",
    ExpressionAttributeValues = {":previous_id" : score_id, ":game_count" : game_count["Count"]},
  )

  return {"previous_id":score_id, "game_count":game_count["Count"], "result":game_result, "hand_ai":hand_ai}

