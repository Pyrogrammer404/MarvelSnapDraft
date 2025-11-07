import json
import base64

def generate_deck_code(defids):
    """
    Takes a list of up to 12 card defIds (strings) and generates a Marvel Snap deck code
    compatible with DeckCodes.chat long format.
    """

    # If fewer than 12 cards, pad with dummy placeholders for safety
    if len(defids) < 12:
        print(f"⚠️ Warning: only received {len(defids)} cards. Padding with placeholders.")
        defids += ["Unknown"] * (12 - len(defids))

    # Trim if somehow more than 12
    defids = defids[:12]

    # Build JSON object
    deck_obj = {"Cards": [{"CardDefId": cid} for cid in defids]}

    # Convert to compact JSON string
    deck_str = json.dumps(deck_obj, separators=(",", ":"))

    # Encode to Base64
    deck_code = base64.b64encode(deck_str.encode("utf-8")).decode("utf-8")

    print("✅ Generated deck code successfully.")
    return deck_code
