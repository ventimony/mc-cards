from argparse import ArgumentParser
import os
import json

ROOT = "PlayingCards_datapack/data/cards"
DIR = f"{ROOT}/function"
FILE = "deck"
SUITS = ["diamond", "club", "heart", "spade"]

def get_cards():
  cards = [(suit, idx) for suit in SUITS for idx in range(1,14)]
  cards += [(card, 0) for card in ["blank", "joker_red", "joker_black", "back"]]

  idxs = list(range(1, 53)) + [0, 53, 54, 55]
  return cards, idxs

def build(directory: str, file: str, start: int = 52000, version: str = "0.2"):
  """Generates a mcfunction file that gives the player a custom filled bundle

  Args:
      directory (str): Output directory
      file (str): Function name
      start (int, optional): Starting index for model data. Defaults to 52000.
  """
  os.makedirs(directory, exist_ok=True)
  func = gen_func(version)
  
  with open(os.path.join(directory, f"{file}.mcfunction"), 'w') as f:
    f.write(func)

  print(f"Generated function `{file}` in {directory} with {start=}")

def get_model_data(card: tuple[str, int, int], start: int = 52000, version: str = "0.2"):
  match version:
    case "0.2":
      (suit, value, _) = card
      match suit:
        case _ if suit in SUITS:
          data = f"""{{"strings": ["cards","{suit}.{value:02}"]}}"""
        case _:
          data = f"""{{"strings": ["cards","{suit}"]}}"""
    case _:
      (_, _, idx) = card
      data = f"{start + idx}"

  return data

def get_model_data_recipe(card: tuple[str, int, int], start: int = 52000, version: str = "0.2"):
  match version:
    case "0.2":
      (suit, value, _) = card
      match suit:
        case _ if suit in SUITS:
          data = {"strings": ["cards",f"{suit}.{value:02}"]}
        case _:
          data = {"strings": ["cards", suit]}
    case _:
      (_, _, idx) = card
      data = f"{start + idx}"

  return data


def get_item_name(card: tuple[str, int, int], version: str = "0.2"):
  match version:
    case _:
      (_, _, idx) = card
      data = f"card.{idx}"

  return data

def get_equippable():
  return f"""{{"slot": "head"}}"""

def get_components(card: tuple[str, int, int], version: str = "0.2"):
  match version:
    case "0.2":
      data = f"""{{"minecraft:custom_model_data": {get_model_data(card, version)}, "minecraft:item_name": {{"translate":"{get_item_name(card, version)}"}}, "minecraft:equippable": {get_equippable()}}}"""
    case _:
      data = f"""{{"minecraft:custom_model_data": {get_model_data(card, version)}, "minecraft:item_name": '{{"translate":"{get_item_name(card, version)}"}}'}}"""
  
  return data

def gen_items(cards: list[tuple[str, int, int]], version: str = "0.2"):
  return ", \ \n".join([
    f"""{{"id": "minecraft:paper", "count": 1, "components": {get_components(card, version)}}}""" for card in cards
  ])

def gen_func(version: str = "0.2"):
  """Generates the function string for MC versions after 1.21.4
  Args:
      start (int): Starting index for model data.
  """
  idxs = list(range(1, 53)) + [0, 53, 54, 55]

  cards, idxs = get_cards()
  cards = [(suit, val, idx) for (suit, val), idx in zip(cards, idxs)]

  return f"give @s minecraft:bundle[minecraft:bundle_contents=[{gen_items(cards, version)}]] 1" 

def gen_contents(cards: list[tuple[str, int, int]], version: str = "0.2"):
  return [
    {
      "id": "minecraft:paper", 
      "count": 1, 
      "components": {
        "minecraft:custom_model_data": get_model_data_recipe(card, version),
        "minecraft:item_name": {
          "translate": get_item_name(card, version)
        },
        "minecraft:equippable": {"slot": "head"}
      }
    }
    for card in cards
  ]

def get_ingredients(version: str):
  match version:
    case "0.2":
      ingredients = ["minecraft:paper", "minecraft:red_dye", "minecraft:bundle", "minecraft:black_dye"]
    case _:
      ingredients = [{"item": "minecraft:paper"}, {"item": "minecraft:red_dye"}, {"item": "minecraft:bundle"}, {"item": "minecraft:black_dye"}]

  return ingredients

def gen_recipe(out: str, name: str, version: str = "0.2"):
  cards, idxs = get_cards()
  cards = [(suit, val, idx) for (suit, val), idx in zip(cards, idxs)]
  recipe = {
    "type": "minecraft:crafting_shapeless",
    "ingredients": get_ingredients(version),
    "result": {
        "id": "minecraft:bundle",
        "count": 1,
        "components": {
            "bundle_contents": gen_contents(cards, version)
        }
    }
  }
  os.makedirs(out, exist_ok=True)
  
  with open(os.path.join(out, f"{name}.json"), 'w') as json_file:
    json.dump(recipe, json_file, indent=2)

  print(f"Generated recipe `{name}` in {out}")

if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("--out", help="Path of output directory", type=str, default=DIR)
  parser.add_argument("--file", help="Name of output file", type=str, default=FILE)
  parser.add_argument("--start", help="Starting index", type=int, default=52000)
  args = parser.parse_args()

  build(args.out, args.file, args.start)
  gen_recipe(f"{ROOT}/recipe", "deck")
