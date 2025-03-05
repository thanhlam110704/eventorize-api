import hashlib
import hmac
import time

from utils import http_client

from .config import settings


class PayOSApi:
    def __init__(self, client_id, api_key, checksum_key, cancel_url, return_url) -> None:
        self.url = "https://api-merchant.payos.vn/v2/payment-requests"
        self.client_id = client_id
        self.api_key = api_key
        self.checksum_key = checksum_key
        self.cancel_url = cancel_url
        self.return_url = return_url

        self.headers = {}
        self.headers["x-client-id"] = self.client_id
        self.headers["x-api-key"] = self.api_key

    def generate_signature(self, order_code: int, amount: int, description: str, return_url: str):
        data_str = f"amount={amount}&cancelUrl={self.cancel_url}&description={description}&orderCode={order_code}&returnUrl={return_url}"
        return hmac.new(self.checksum_key.encode("utf-8"), msg=data_str.encode("utf-8"), digestmod=hashlib.sha256).hexdigest()

    def round_to_int(self, amount: float) -> int:
        return int(round(amount))

    async def create_payment_link(self, order_id: str, order_code: int, amount: int):
        amount = self.round_to_int(amount=amount)
        return_url = f"{self.return_url}/{order_id}"
        # description max length is 25 characters
        description = f"TT đơn hàng EVT{order_code}"
        signature = self.generate_signature(order_code=order_code, amount=amount, description=description, return_url=return_url)
        payload = {
            "orderCode": order_code,
            "amount": amount,
            "description": description,
            "returnUrl": return_url,
            "cancelUrl": self.cancel_url,
            "expiredAt": int(time.time()) + 600,
            "signature": signature,
        }
        response = await http_client.post(url=self.url, json=payload, headers=self.headers)
        response = response.json()
        result = {}
        if response.get("code") != "00" or not response.get("data"):
            result["status"] = "failed"
            return result

        result["status"] = "success"
        result["qr_code"] = response["data"]["qrCode"]
        result["qr_data_url"] = response["data"]["checkoutUrl"]
        return result

    async def get_payment_information(self, order_code: int):
        url = f"{self.url}/{order_code}"
        response = await http_client.get(url=url, headers=self.headers)
        response = response.json()
        result = {}
        if response.get("code") != "00" or not response.get("data"):
            result["status"] = "failed"
            return result

        result["status"] = "success"
        result["qr_id"] = response["data"]["id"]
        result["qr_status"] = response["data"]["status"]
        result["amount"] = response["data"]["amount"]
        result["amount_paid"] = response["data"]["amountPaid"]
        result["amount_remaining"] = response["data"]["amountRemaining"]
        return result

    async def cancel_payment(self, order_code: int):
        url = f"{self.url}/{order_code}/cancel"
        response = await http_client.post(url=url, headers=self.headers)
        response = response.json()
        result = {}
        if response.get("code") != "00" or not response.get("data"):
            result["status"] = "failed"
            return result

        result["status"] = "success"
        result["qr_id"] = response["data"]["id"]
        result["qr_status"] = response["data"]["status"]
        return result

    async def get_checkout_url(self, order_code: int):
        url = f"{self.url}/{order_code}"
        response = await http_client.get(url=url, headers=self.headers)
        response = response.json()
        result = {}
        if response.get("code") != "00" or not response.get("data"):
            result["status"] = "failed"
            return result
        if response["data"]["status"] == "CANCELLED":
            result["status"] = "failed"
            return result
        result["status"] = "success"
        result["qr_data_url"] = f'https://pay.payos.vn/web/{response["data"]["id"]}'
        return result


payos_api = PayOSApi(
    client_id=settings.client_id_payos, api_key=settings.api_key_payos, checksum_key=settings.checksum_key_payos, cancel_url=settings.cancel_url_payos, return_url=settings.return_url_payos
)
