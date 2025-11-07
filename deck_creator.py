import json
import base64

def generate_deck_code(defids):
    """
    Takes up to 12 card defIds (strings) and generates a Marvel Snap deck code.
    """

    clean_ids = []
    for cid in defids:
        # Normalize
        cid = str(cid).strip().replace(" ", "").replace("_", "")
        if cid:
            clean_ids.append(cid)

    if len(clean_ids) < 12:
        print(f"⚠️ Warning: only {len(clean_ids)} cards received. Padding.")
        clean_ids += ["Unknown"] * (12 - len(clean_ids))

    clean_ids = clean_ids[:12]

    deck_obj = {"Cards": [{"CardDefId": cid} for cid in clean_ids]}
    deck_str = json.dumps(deck_obj, separators=(",", ":"))
    deck_code = base64.b64encode(deck_str.encode("utf-8")).decode("utf-8")

    print(f"✅ Generated deck code for {len(clean_ids)} cards.")
    return deck_code
