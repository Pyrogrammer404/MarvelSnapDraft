import json
import os
from flask import Flask, render_template, request, session, redirect, jsonify, url_for
from deck_creator import generate_deck_code
import threading
import subprocess

def update_cards_json():
    try:
        print("🔄 Updating cards_enriched.json from Untapped.gg...")
        subprocess.run(
            ["python", "Card_Details_write.py"],
            check=True
        )
        print("✅ cards_enriched.json updated successfully.")
    except Exception as e:
        print("⚠️ Could not update cards_enriched.json:", e)
threading.Thread(target=update_cards_json, daemon=True).start()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.secret_key = "supersecretkey"

# Load cards
with open("cards_enriched.json", "r", encoding="utf-8") as f:
    all_cards = json.load(f)


# --- Utility Functions ---
def load_bans():
    try:
        with open("bans.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_bans(bans):
    with open("bans.json", "w") as f:
        json.dump(bans, f, indent=2)


def load_history():
    try:
        if not os.path.exists("history.json"):
            return []
        with open("history.json", "r", encoding="utf-8") as f:
            data = f.read().strip()
            if not data:  # empty file
                return []
            return json.loads(data)
    except (json.JSONDecodeError, FileNotFoundError):
        return []



def save_history(deck):
    history = load_history()
    history.append(deck)
    if len(history) > 3:
        history = history[-3:]
    with open("history.json", "w") as f:
        json.dump(history, f, indent=2)


# --- Routes ---
@app.route("/")
def main_menu():
    return render_template("index.html")


@app.route("/bans")
def bans():
    return render_template("bans.html", all_cards=all_cards)


@app.route("/save_bans", methods=["POST"])
def save_bans_route():
    ban_card = request.form.get("bans")
    bans = load_bans()
    if ban_card and ban_card not in bans:
        bans.append(ban_card)
        save_bans(bans)
    return redirect(url_for("draft"))


@app.route("/draft")
def draft():
    session["draft"] = []
    return render_template("draft.html")


@app.route("/history")
def history():
    return render_template("history.html", history=load_history())

@app.route("/api/deckcode", methods=["POST"])
def generate_deck():
    data = request.get_json()
    cards = data.get("cards", [])
    if not cards:
        return jsonify({"error": "No cards provided"}), 400

    # map card names to defIds
    defIds = [c["defId"] for c in all_cards if c["name"] in cards]
    deck_code = generate_deck_code(defIds)
    return jsonify({"deck_code": deck_code})

@app.route("/feedback")
def feedback():
    return render_template("feedback.html")

@app.route("/api/feedback", methods=["POST"])
def api_feedback():
    data = request.get_json()
    fb = data.get("feedback", "").strip()
    if not fb:
        return jsonify({"error": "Empty feedback"}), 400

    with open("feedbacks.txt", "a", encoding="utf-8") as f:
        f.write(f"{fb}\n")

    print("📝 Feedback saved:", fb)
    return jsonify({"success": True}), 200



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
