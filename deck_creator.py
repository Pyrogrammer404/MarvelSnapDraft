import json
import base64

def generate_deck_code(defids):
    """
    Takes a list of 12 card defIds (strings) and generates a Marvel Snap deck code
    compatible with DeckCodes.chat long format.
    """
    if len(defids) != 12:
        raise ValueError("You must provide exactly 12 card defIds.")

    # Build JSON object
    deck_obj = {
        "Cards": [{"CardDefId": cid} for cid in defids]
    }

    # Convert to compact JSON string
    deck_str = json.dumps(deck_obj, separators=(',', ':'))

    # Encode to Base64
    deck_code = base64.b64encode(deck_str.encode('utf-8')).decode('utf-8')

    return deck_code

# Example usage
my_draft_defids = [
    "Abomination", "Sunspot", "IronMan", "CaptainAmerica",
    "SpiderMan", "Carnage", "Loki", "Hulk",
    "DoctorStrange", "MoonKnight", "Wolverine", "BlackWidow"
]

deck_code = generate_deck_code(my_draft_defids)
print("Deck Code:", deck_code)
