from flask import Blueprint, jsonify
from app.extensions import mongo

analytics_bp = Blueprint("analytics", __name__)


# ==========================
# LIVE PERFORMANCE
# ==========================
@analytics_bp.route("/live-performance", methods=["GET"])
def live_performance():

    history = list(mongo.db.history.find())

    total = len(history)
    phishing = sum(1 for h in history if h.get("prediction") == "Phishing")
    safe = total - phishing

    accuracy = 0
    if total > 0:
        correct = sum(1 for h in history if h.get("prediction") == h.get("actual"))
        accuracy = correct / total

    return jsonify({
        "total": total,
        "phishing": phishing,
        "safe": safe,
        "accuracy": round(accuracy, 2)
    })


# ==========================
# TREND DATA
# ==========================
@analytics_bp.route("/trend", methods=["GET"])
def trend():

    history = list(mongo.db.history.find().sort("timestamp", -1).limit(10))

    history.reverse()

    trend_data = []

    for i, item in enumerate(history):
        trend_data.append({
            "index": i + 1,
            "phishing": 1 if item.get("prediction") == "Phishing" else 0,
            "safe": 1 if item.get("prediction") == "Legitimate" else 0
        })

    return jsonify(trend_data)