import json

def load_customers():
  with open("data/customers.json", "r") as file:
    return json.load(file)
