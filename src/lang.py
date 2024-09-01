import json
import os

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

if __name__ == "__main__":
  os.makedirs(DIR, exist_ok=True)

  locale = {
    f"card.{idx}": get_name(idx)
    for idx in range(56)
  }
  
  with open(os.path.join(DIR, FILE), 'w') as file:
    file.write(json.dumps(locale, indent=1))

  print("Generated locale")
