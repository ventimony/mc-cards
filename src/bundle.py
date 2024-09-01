import json
import os

DIR = "PlayingCards_datapack/data/cards/function"
FILE = "deck_t.mcfunction"

if __name__ == "__main__":
  os.makedirs(DIR, exist_ok=True)

  start = 52000
  items = ", ".join([
    json.dumps(
      {
        "id": "minecraft:paper", 
        "count": 1, 
        "components": {"minecraft:custom_model_data": idx}
        })
    for idx in range(52001, 52053)
  ])

  func = f"give @s minecraft:bundle[minecraft:bundle_contents=[{items}]] 1" 
  
  with open(os.path.join(DIR, FILE), 'w') as file:
    file.write(func)

  print("Generated function")
