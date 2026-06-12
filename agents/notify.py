import base64
import os
import smtplib
import urllib.parse
import urllib.request
from datetime import date
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

TODAY = str(date.today())
TO_EMAIL = "christhian.cp@gmail.com"
TO_PHONE = "+16465122550"
SWARM_FILE = f"output/woodys_swarm_{TODAY}.md"

GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD")
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_FROM_NUMBER = os.environ.get("TWILIO_FROM_NUMBER")

with open(SWARM_FILE) as f:
    content = f.read()

# --- Email via Gmail SMTP ---
msg = MIMEMultipart()
msg["From"] = TO_EMAIL
msg["To"] = TO_EMAIL
msg["Subject"] = f"Woody's Daily Marketing Kit — {TODAY}"
msg.attach(MIMEText(content, "plain"))

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(TO_EMAIL, GMAIL_APP_PASSWORD)
    server.send_message(msg)

print("Email sent")

# --- SMS via Twilio REST API ---
sms_body = (
    f"Woody's marketing kit for {TODAY} is ready! "
    "5 sections: social posts, pitch scripts, email templates, "
    "objection responses & 7-day content calendar. Check your email for the full kit."
)

url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json"
data = urllib.parse.urlencode({"From": TWILIO_FROM_NUMBER, "To": TO_PHONE, "Body": sms_body}).encode()
credentials = base64.b64encode(f"{TWILIO_ACCOUNT_SID}:{TWILIO_AUTH_TOKEN}".encode()).decode()
req = urllib.request.Request(url, data=data, headers={"Authorization": f"Basic {credentials}"})
urllib.request.urlopen(req)

print("SMS sent")
