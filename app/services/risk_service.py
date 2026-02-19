class RiskService:

    @staticmethod
    def calculate_risk(confidence, domain_age, ssl_status):

        risk = confidence * 100

        if domain_age and domain_age < 30:
            risk += 15

        if not ssl_status:
            risk += 10

        return min(int(risk), 100)


    @staticmethod
    def get_threat_level(risk_score):

        if risk_score >= 80:
            return "High"
        elif risk_score >= 50:
            return "Medium"
        else:
            return "Low"
