import os

from twilio.rest import Client


def send_to_phone(pdf_url):
    twilio_sid = os.environ.get("TWILIO_SID")
    twilio_token = os.environ.get("TWILIO_TOKEN")
    client = Client(twilio_sid, password=twilio_token)
    from_whatsapp_number = "whatsapp:+14155238886"
    to_whatsapp_number = "whatsapp:+14046425216"
    message = client.messages.create(
        body="Current Covid-19 data",
        media_url=[pdf_url],
        from_=from_whatsapp_number,
        to=to_whatsapp_number
    )
