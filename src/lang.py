import json
import os

from collections.abc import Callable

DIR = "PlayingCards/assets/cards/lang"
FILE = "en_us.json"

VAL = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
SUIT = "♠♥♣♦"

def get_name(idx: int) -> str:
  match idx:
    case 0:
      return "Blank"
    case 53:
      return "Red Joker"
    case 54:
      return "Black Joker"
    case 55:
      return "Misprint"

  return f"{SUIT[(idx-1)//13]} {VAL[(idx-1)%13]}"

def create_locale(locale: str, out: str, *, namespace: str = "card", indexer: Callable[[int], str] = get_name):
  os.makedirs(out, exist_ok=True)

  locale = {
    f"{namespace}.{idx}": indexer(idx)
    for idx in range(56)
  }
  
  with open(os.path.join(out, f"{locale}.json"), 'w') as file:
    file.write(json.dumps(locale, indent=1))

  print("Generated {locale} in {out}")

if __name__ == "__main__":
  create_locale("en_us", DIR)
