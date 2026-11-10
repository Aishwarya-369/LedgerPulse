import requests
from requests.auth import HTTPBasicAuth
from backend.app.config import settings

class PayPalService:
    def __init__(self):
        self.base_url = settings.PAYPAL_BASE_URL
        self.client_id = settings.PAYPAL_CLIENT_ID
        self.client_secret = settings.PAYPAL_CLIENT_SECRET

    def get_access_token(self) -> str:
        url = f"{self.base_url}/v1/oauth2/token"
        headers = {
            "Accept": "application/json",
            "Accept-Language": "en_US"
        }
        data = {"grant_type": "client_credentials"}
        response = requests.post(
            url,
            auth=HTTPBasicAuth(self.client_id, self.client_secret),
            headers=headers,
            data=data,
            timeout=10
        )
        if response.status_code != 200:
            raise Exception(f"Failed to fetch PayPal token: {response.text}")
        return response.json()["access_token"]

    def create_order(self, amount: float, currency: str = "USD") -> str:
        token = self.get_access_token()
        url = f"{self.base_url}/v2/checkout/orders"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        payload = {
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "amount": {
                        "currency_code": currency,
                        "value": f"{amount:.2f}"
                    }
                }
            ]
        }
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        if response.status_code not in (200, 201):
            raise Exception(f"Failed to create PayPal order: {response.text}")
        return response.json()["id"]

    def capture_order(self, order_id: str) -> dict:
        token = self.get_access_token()
        url = f"{self.base_url}/v2/checkout/orders/{order_id}/capture"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }
        response = requests.post(url, headers=headers, json={}, timeout=10)
        if response.status_code not in (200, 201):
            raise Exception(f"Failed to capture PayPal order: {response.text}")
        return response.json()

paypal_service = PayPalService()
