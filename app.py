from flask import Flask, render_template, jsonify
import json, random, os

app = Flask(__name__)

DATA_FILE = os.getenv("TIPS_FILE", "tips.json")
with open(DATA_FILE, "r", encoding="utf-8") as f:
    TIPS = json.load(f)

@app.get("/")
def home():
    tip = random.choice(TIPS)
    return render_template("index.html", tip=tip)

@app.get("/api/tip")
def api_tip():
    return jsonify(random.choice(TIPS))

@app.get("/healthz")
def healthz():
    return jsonify(status="ok")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
