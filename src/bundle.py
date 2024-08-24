import json
import os

DIR = "PlayingCards_datapack_v0.1.0/data/cards/function"
FILE = "deck.mcfunction"

if __name__ == "__main__":
  os.makedirs(DIR, exist_ok=True)

  start = 52000
  items = ", ".join([
    json.dumps(
      {
        "id": "minecraft:carved_pumpkin", 
        "count": 1, 
        "components": {"minecraft:custom_model_data": idx}
        })
    for idx in range(52001, 52053)
  ])

  func = f"give @s minecraft:bundle[minecraft:bundle_contents=[{items}]] 1" 
  
  with open(os.path.join(DIR, FILE), 'w') as file:
    file.write(func)

  print("Generated function")
