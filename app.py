# app.py
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

app = Flask(__name__, static_folder="static", static_url_path="/")
CORS(app)
MONGODB_URI = "mongodb+srv://glouloudorra7:2VMbnEHFf1uiwvLU@cluster0.z6ezz9f.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(MONGODB_URI)
db = client["pawmatch"]
pets_col = db["pets"]

def load_pets():
    pets = list(pets_col.find())
    for p in pets:
        # convert ObjectId to string for JSON
        p["_id"] = str(p["_id"])
    return pets

def build_tfidf(pets):
    descriptions = [p.get("description", "") for p in pets]
    if len(descriptions) == 0:
        return None, None
    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf = vectorizer.fit_transform(descriptions)
    return vectorizer, tfidf

@app.route("/")
def index():
    # serves static/index.html
    return app.send_static_file("index.html")

@app.route("/api/pets", methods=["GET"])
def api_pets():
    pets = load_pets()
    return jsonify(pets)

@app.route("/api/recommend", methods=["POST"])
def api_recommend():
    prefs = request.get_json() or {}
    # Load pets & build TF-IDF
    pets = load_pets()
    vectorizer, tfidf = build_tfidf(pets)

    # Build a small text query from the user's preferences
    parts = []
    if prefs.get("home_size"): parts.append(prefs["home_size"])
    if prefs.get("activity"): parts.append(prefs["activity"])
    if prefs.get("experience"): parts.append(prefs["experience"])
    if prefs.get("allergies"): parts.append(prefs["allergies"])
    user_query = " ".join(parts).strip()

    if tfidf is not None and user_query:
        qv = vectorizer.transform([user_query])
        sims = cosine_similarity(qv, tfidf).flatten()
    else:
        sims = np.zeros(len(pets))

    # Attribute-based scoring function
    def attr_score(pet):
        score = 0.0
        # home size fit
        size_map = {"small": 1, "medium": 2, "large": 3, "very-large": 4}
        pet_size_str = str(pet.get("size", "Medium")).lower()
        pet_size_num = size_map.get(pet_size_str, 2)
        home_num = size_map.get(prefs.get("home_size", "medium"), 2)
        diff = abs(home_num - pet_size_num)
        size_score = max(0, 1 - (diff * 0.25))  # 1 when perfect, lower when mismatch
        score += size_score * 0.25

        # allergies
        allergies = prefs.get("allergies", "none")
        if allergies == "severe":
            score += 0.25 if pet.get("hypoallergenic", False) else 0.0
        else:
            score += 0.15

        # activity match
        a_map = {"low": 1, "moderate": 2, "high": 3}
        pet_activity = a_map.get(pet.get("activity", "moderate"), 2)
        user_activity = a_map.get(prefs.get("activity", "moderate"), 2)
        act_diff = 1 - (abs(user_activity - pet_activity) / 2)  # from 0..1
        score += max(0, act_diff) * 0.2

        # kids compatibility
        has_kids = prefs.get("has_kids", False)
        if has_kids:
            score += 0.15 if pet.get("good_with_children", False) else 0.0
        else:
            score += 0.05

        # experience requirement
        if prefs.get("experience") == "none" and pet.get("needs_experience", False):
            score *= 0.6

        return score

    attr_scores = np.array([attr_score(p) for p in pets])
    # normalize sims
    if len(sims) > 0 and sims.max() != sims.min():
        sims_norm = (sims - sims.min()) / (sims.max() - sims.min())
    else:
        sims_norm = np.zeros_like(sims)

    final = 0.6 * attr_scores + 0.4 * sims_norm
    if final.max() > 0:
        final_pct = (final / final.max()) * 100
    else:
        final_pct = final * 100

    # attach match value and return sorted list
    for i, p in enumerate(pets):
        p["match"] = int(final_pct[i])

    pets_sorted = sorted(pets, key=lambda x: x["match"], reverse=True)
    return jsonify(pets_sorted[:10])

if __name__ == "__main__":
    app.run(debug=True)
