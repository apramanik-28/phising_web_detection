from app.extensions import mongo
from datetime import datetime

class HistoryService:

    @staticmethod
    def save_scan(user_id, url, result, confidence,
                  risk_score=None, domain_age=None,
                  ssl_status=None, url_type=None):

        mongo.db.history.insert_one({
            "user_id": user_id,
            "url": url,
            "result": result,
            "confidence": confidence,
            "risk_score": risk_score,
            "domain_age_days": domain_age,
            "ssl_certified": ssl_status,
            "url_type": url_type,
            "timestamp": datetime.utcnow()
        })
