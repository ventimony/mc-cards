import json
import os

ROOT = "PlayingCards/assets"
DIR = f"{ROOT}/cards/models/item"

SUITS = ["diamond", "club", "heart", "spade"]
RED = ["diamond", "heart"]

def gen_item(out: str, name: str, textures: dict[str, str], namespace: str, type: str = "item", parent: str = "base", ext: str = "json"):
  """Generate an item model that derives from a parent model in a given namespace.

  Args:
    out (str): The output directory for the model file
    name (str): Name of the model file
    textures (dict[str, str]): Texture key mapping
    namespace (str): Namespace for the model. e.g. 'minecraft'
    type (str, optional): The model type. e.g. 'block' or 'item'. Defaults to "item".
    parent (str, optional): Name of the parent model. Defaults to "base".
    ext (str, optional): The output file extension. Defaults to "json".
  """

  prefix = f"{namespace}:{type}"

  # Create the data for the JSON file
  data = {
    "parent": f"{prefix}/{parent}",
    "textures": textures
  }
  
  # Define the filename
  filename = f"{name}.{ext}"
  
  # Write the JSON file
  with open(os.path.join(out, filename), 'w') as json_file:
    json.dump(data, json_file, indent=2)


def gen_items(out: str, items: list[tuple[str, dict[str, str]]], namespace: str = "cards", type: str = "item", parent: str = "base", ext: str = "json"):
  """Generate the item model files

  Args:
    out (str): path of the models/items directory
  """
  os.makedirs(out, exist_ok=True)

  # Generate JSON files
  for (name, textures) in items:
    gen_item(out, name, textures, namespace, type, parent, ext)
  
  print("Generated item models files.")

def get_textures(suit: str, value: int, version: str = "0.1"):
  match version:
    case "0.2" | "0.2.1":
      match suit:
        case _ if suit in SUITS:
          colour = "r" if suit in RED else "b"

          textures = {
            "value": f"cards:item/value/{colour}_{value:02}",
            "suit": f"cards:item/suit/{suit}"
            }
        case "blank":
          textures = {
            "value": "cards:item/empty",
            "suit": "cards:item/empty"
            }
        case _:
          textures = {
            "value": "cards:item/empty",
            "suit": f"cards:item/{suit}"
            }
          
    case _:
      textures = {"0": f"cards:item/{suit}_{value:02}"}
  
  return textures

def gen_model_case(suit: str, value: int, prefix: str, version: str = "0.2"):
  if suit in SUITS:
    model = f"{prefix}/{suit}/{suit}_{value:02}"
    when = f"{suit}.{value:02}"
  else:
    model = f"{prefix}/{suit}"
    when = f"{suit}"
  
  match version:
    case "0.2.1":
      # display contexts
      # first-person: large
      # third: base + blank
      # head: base (+ band?)
      # gui: base
      # ground: base
      # fixed: large

      model = {
        "model": {
            "type": "minecraft:select",
            "property": "minecraft:display_context",
            "fallback": { # base
              "type": "minecraft:model",
              "model": model
            },
            "cases": gen_display_contexts(model, prefix, version)
          },
        "when": when
      }

      return model

  return {
    "model": {
        "type": "minecraft:model",
        "model": model
      },
    "when": when
  }

def gen_display_contexts(model: str, prefix: str, version: str = "0.2"):
  return [gen_display_context(context, model, prefix, version) for context in [
    "blank", # thirdperson
    "large", # firstperson, fixed
    ]]

def gen_display_context(context: str, model: str, prefix: str, version: str = "0.2"):
  match context:
    case "blank":
      ctx = ["thirdperson_lefthand", "thirdperson_righthand"]
      ctx_model = {
        "type": "minecraft:model",
        "model": f"{prefix}/blank"
      }
    case "large":
      ctx = ["firstperson_lefthand", "firstperson_righthand", "fixed"]
      ctx_model = {
        "type": "minecraft:model",
        "model": f"{model}_l"
      }    
    case _:
      ctx = context
      ctx_model = {
        "type": "minecraft:model",
        "model": model
      } 

  return {
    "model": ctx_model,
    "when": ctx
  }

def gen_model_cases(prefix: str, cards: list[tuple[str, int, str]], version: str = "0.2"):
  return [gen_model_case(suit, card, prefix, version) for (suit, card, _) in cards]

def gen_model(assets: str, name: str, cards: list[tuple[str, int, str]], version: str = "0.1", start: int = 52000, filter: str | list[str] = "cards"):
  """Generate the model file that overrides the vanilla model
  
  Pre 1.21.4: <namespace>/models/item
  1.21.4+: <namespace>/items
  """
  filename = f"{name}.json"
  prefix = "cards:item"
  
  match version:
    case "0.2" | "0.2.1":
      out = "minecraft/items"

      model = {
        "model": {
          "type": "minecraft:select",
          "property": "minecraft:custom_model_data",
          "fallback": {
            "type": "minecraft:model",
            "model": f"minecraft:item/{name}"
          },
          "cases": [{
            "model": {
              "type": "minecraft:select",
              "property": "minecraft:custom_model_data",
              "index": 1,
              "fallback": {
                "type": "minecraft:model",
                "model": f"{prefix}/blank"
              },
              "cases": gen_model_cases(prefix, cards, version),
            },
            "when": filter
          }]
        }
      }
          
    case _:
      out = "minecraft/models/item"
      
      names = ["base"] + \
              [f"{suit}_{idx:02}" for suit in "dchs" for idx in range(1,14)] + \
              ["joker_red", "joker_black", "back"]

      model = {
        "parent": "minecraft:item/generated",
        "textures": {
          "layer0": f"minecraft:item/{name}"
        },
        "overrides": [
          { 
            "predicate": {"custom_model_data": start + idx}, 
            "model": f"cards:item/{card}"
            }
          for (idx, card) in enumerate(names)
        ]
      }
  
  os.makedirs(f"{assets}/{out}", exist_ok=True)

  # Write the JSON file
  with open(os.path.join(assets, out, filename), 'w') as json_file:
    json.dump(model, json_file, indent=2)

  print("Generated overriding model.")

def gen_cards(out: str, version: str):
  cards = ["blank", "joker_red", "joker_black", "back"]
  cards = [(card, 0, card) for card in cards]

  match version:
    case "0.2" | "0.2.1":
      for suit in SUITS:
        os.makedirs(f"{out}/{suit}", exist_ok=True)
      
      cards += [(suit, idx, f"{suit}/{suit}_{idx:02}") for suit in SUITS for idx in range(1,14)]
    
    case _:
      cards += [(suit, idx, f"{suit}_{idx:02}") for suit in "dchs" for idx in range(1,14)]
  
  
  items = [(name, get_textures(suit, card, version)) for (suit, card, name) in cards]
  gen_items(out, items)

  items_large = [(f"{name}_l", get_textures(suit, card, version)) for (suit, card, name) in cards]
  gen_items(out, items_large, parent="large")
  gen_model(ROOT, "paper", cards, version)

if __name__ == "__main__":
  gen_cards(DIR, "0.2.1")
