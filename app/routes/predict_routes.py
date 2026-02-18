from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

predict_bp = Blueprint("predict", __name__)


@predict_bp.route("/predict", methods=["POST"])
@jwt_required()
def predict():

    current_user = get_jwt_identity()

    url = request.json.get("url")

    if not url:
        return {"message": "URL is required"}, 400

    # TODO: Replace this with your ML model prediction
    prediction = "Safe URL"

    return jsonify({
        "user_id": current_user,
        "url": url,
        "prediction": prediction
    }), 200
