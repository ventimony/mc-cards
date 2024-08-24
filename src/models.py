import json
import os

DIR = "PlayingCards_v0.1.0/assets/cards/models/item"

if __name__ == "__main__":
  os.makedirs(DIR, exist_ok=True)

  # Generate JSON files
  for suit in "dchs":
      for idx in range(1,14):
          # Create the data for the JSON file
          data = {
              "parent": "cards:item/base",
              "textures": {
                  "0": f"cards:item/{suit}_{idx:02}"
              }
          }
          
          # Define the filename
          filename = f"{suit}_{idx:02}.json"
          
          # Write the JSON file
          with open(os.path.join(DIR, filename), 'w') as json_file:
            json.dump(data, json_file, indent=2)

  print("Generated JSON files.")
