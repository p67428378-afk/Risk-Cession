import hmac
import hashlib
import os
from config import Config

class SecurityService:
    """
    Service responsible for validating the X-Reinsurance-Hmac header.
    This implementation uses HMAC-SHA256 for validation.
    """
    def __init__(self):
        self.hmac_secret_key = Config.HMAC_SECRET_KEY.encode('utf-8')

    def validateHmacHeader(self, header_value: str, request_body: bytes) -> bool:
        """
        Validates the X-Reinsurance-Hmac header against the request body.

        Args:
            header_value (str): The value of the 'X-Reinsurance-Hmac' header.
            request_body (bytes): The raw request body as bytes.

        Returns:
            bool: True if the HMAC is valid, False otherwise.
        """
        if not header_value:
            return False

        # Calculate HMAC-SHA256 of the request body
        calculated_hmac = hmac.new(
            self.hmac_secret_key,
            request_body,
            hashlib.sha256
        ).hexdigest()

        # Compare the calculated HMAC with the provided header value
        # Using hmac.compare_digest for constant-time comparison to prevent timing attacks
        return hmac.compare_digest(calculated_hmac, header_value)