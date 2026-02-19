from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from app.services.model_service import ModelService
from app.services.feature_extraction_service import FeatureExtractionService
from app.services.domain_service import DomainService
from app.services.ssl_service import SSLService
from app.services.url_intelligence_service import URLIntelligenceService
from app.services.risk_service import RiskService
from app.extensions import mongo


# 🔥 DEFINE BLUEPRINT FIRST
predict_bp = Blueprint("predict", __name__)

# 🔥 LOAD MODEL AFTER
model_service = ModelService()


@predict_bp.route("/predict", methods=["POST"])
@jwt_required()
def predict():

    data = request.get_json()
    url = data.get("url")

    if not url:
        return jsonify({"message": "URL is required"}), 400

    try:
        # 1️⃣ Extract features
        features = FeatureExtractionService.extract_features(url)

        # 2️⃣ ML Prediction
        prediction, confidence = model_service.predict(features)
        classification = "Phishing" if prediction == 1 else "Legitimate"

        # 3️⃣ Domain Age
        domain_age = DomainService.get_domain_age(url)

        # 4️⃣ SSL
        ssl_status = SSLService.check_ssl(url)

        # 5️⃣ URL Intelligence
        url_type = URLIntelligenceService.detect_url_type(url)
        flags = URLIntelligenceService.get_additional_flags(url)

        # 6️⃣ Risk + Threat
        risk_score = None
        threat_level = None
        explanation = []

        if classification == "Phishing":
            risk_score = RiskService.calculate_risk(
                confidence,
                domain_age,
                ssl_status
            )

            threat_level = RiskService.get_threat_level(risk_score)

            if domain_age and domain_age < 30:
                explanation.append("Domain is newly registered")

            if not ssl_status:
                explanation.append("Website does not use HTTPS")

            if flags["suspicious_keywords"]:
                explanation.append("Contains suspicious keywords")

            if flags["ip_address_used"]:
                explanation.append("Uses IP address instead of domain")

        return jsonify({
            "url": url,
            "classification": classification,
            "confidence": round(confidence * 100, 2),
            "risk_score": risk_score,
            "threat_level": threat_level,
            "ssl_certified": ssl_status,
            "domain_age_days": domain_age,
            "url_type": url_type,
            "flags": {
                "ip_address_used": flags["ip_address_used"],
                "too_many_subdomains": flags["too_many_subdomains"],
                "contains_suspicious_keyword": bool(flags["suspicious_keywords"])
            },
            "explanation": explanation
        }), 200

    except Exception as e:
        return jsonify({
            "message": "Prediction failed",
            "error": str(e)
        }), 500
