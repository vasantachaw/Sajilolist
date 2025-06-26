# authentication/mixsins.py

import vonage
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class MessageHandler:
    def __init__(self, phone_number, otp) -> None:
        self.phone_number = phone_number
        self.otp = otp

    def send_otp_on_phone(self):
        try:
            client = vonage.Client(key=settings.VONAGE_API_KEY, secret=settings.VONAGE_API_SECRET)
            sms = vonage.Sms(client)
            response = sms.send_message({
                "from": "VonageOTP",  # Ensure this is allowed in your region
                "to": self.phone_number,
                "text": f"Your Sajilolist OTP is {self.otp}"
            })

            logger.debug(f"Vonage response: {response}")  # For debugging

            message_info = response["messages"][0]
            if message_info["status"] == "0":
                logger.info(f"OTP sent to {self.phone_number} (message-id: {message_info['message-id']})")
                return message_info["message-id"]
            else:
                logger.error(f"Vonage error sending OTP to {self.phone_number}: {message_info['error-text']}")
                return None

        except Exception as e:
            logger.exception(f"Exception in send_otp_on_phone: {e}")
            return None
