import requests
import json

API_URL = "https://snapjson.untapped.gg/v2/latest/en/cards.json"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def fetch_cards():
    response = requests.get(API_URL, headers=HEADERS)
    response.raise_for_status()
    data = response.json()

    cards = []
    for card in data:
        # Only keep collectible cards
        if not card.get("collectible"):
            continue

        def_id = card.get("defId")
        name = card.get("name")
        cost = card.get("cost")
        power = card.get("power")
        description = card.get("description")

        # Build proper image URL
        # (Use the official Untapped static art endpoint)
        image_url = f"https://snapjson.untapped.gg/art/render/framebreak/common/256/{def_id}.webp"

        cards.append({
            "defId": def_id,
            "name": name,
            "cost": cost,
            "power": power,
            "description": description,
            "image": image_url,
            "collectible": True
        })

    return cards


def main():
    cards = fetch_cards()
    print(f"✅ Saved {len(cards)} collectible cards with images.")
    json_path = os.path.join("static", "data", "cards_enriched.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(cards, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
