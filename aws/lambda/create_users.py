import json
def create_users(event, context):
  return {
    "statusCode": 200,
    "body": json.dumps('create users')
  }
