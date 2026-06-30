import hmac
import hashlib
import json
from fastapi import HTTPException, Request
from src.config import settings

class WebhookVerifier:
    @staticmethod
    def verify_github_signature(signature: str, payload: bytes) -> bool:
        if not signature:
            return False

        signature = signature.replace("sha256=", "")
        expected_signature = hmac.new(
            settings.WEBHOOK_SECRET.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()

        return hmac.compare_digest(signature, expected_signature)

    @staticmethod
    async def extract_webhook_data(request: Request) -> dict:
        payload = await request.body()
        signature = request.headers.get("X-Hub-Signature-256", "")

        if not WebhookVerifier.verify_github_signature(signature, payload):
            raise HTTPException(status_code=401, detail="Invalid GitHub signature")

        try:
            data = json.loads(payload)
            return data
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON payload")
