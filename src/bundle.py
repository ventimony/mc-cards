from argparse import ArgumentParser
import os

DIR = "PlayingCards_datapack/data/cards/function"
FILE = "deck"


def build(directory: str, file: str, start: int = 52000, version: str = "old"):
  """Generates a mcfunction file that gives the player a custom filled bundle

  Args:
      directory (str): Output directory
      file (str): Function name
      start (int, optional): Starting index for model data. Defaults to 52000.
  """
  os.makedirs(directory, exist_ok=True)
  func = ""
  match version:
    case "new":
      pass
    case _:
      func = func_old(start)
  
  with open(os.path.join(directory, f"{file}.mcfunction"), 'w') as f:
    f.write(func)

  print(f"Generated function `{file}` in {directory} with {start=}")

def gen_items(items: list[str]):
  return ", ".join([
    f"""{{"id": "minecraft:paper", "count": 1, "components": {{"minecraft:custom_model_data": {start + idx}, "minecraft:item_name": '{{"translate":"card.{idx}"}}'}}}}""" for idx in idxs
  ])

def func(start: int):
  """Generates the function string for MC versions after 1.21.4
  Args:
      start (int): Starting index for model data.
  """

  """
    {"id":"minecraft:paper", "components": {"minecraft:custom_model_data":{\
    "strings": ["cards:clubs", "01"]\
    }\
  }\
}\
  """

  idxs = list(range(1, 53)) + [0, 53, 54, 55]
  items = ", ".join([
    f"""{{"id": "minecraft:paper", "count": 1, "components": {{"minecraft:custom_model_data": {start + idx}, "minecraft:item_name": '{{"translate":"card.{idx}"}}'}}}}""" for idx in idxs
  ])

  return f"give @s minecraft:bundle[minecraft:bundle_contents=[{items}]] 1" 

def func_old(start: int):
  """Generates the function string for MC versions before 1.21.4
  Args:
      start (int): Starting index for model data.
  """
  idxs = list(range(1, 53)) + [0, 53, 54, 55]
  items = ", ".join([
    f"""{{"id": "minecraft:paper", "count": 1, "components": {{"minecraft:custom_model_data": {start + idx}, "minecraft:item_name": '{{"translate":"card.{idx}"}}'}}}}""" for idx in idxs
  ])

  return f"give @s minecraft:bundle[minecraft:bundle_contents=[{items}]] 1" 

if __name__ == "__main__":
  parser = ArgumentParser()
  parser.add_argument("--out", help="Path of output directory", type=str, default=DIR)
  parser.add_argument("--file", help="Name of output file", type=str, default=FILE)
  parser.add_argument("--start", help="Starting index", type=int, default=52000)
  args = parser.parse_args()

  build(args.out, args.file, args.start)
