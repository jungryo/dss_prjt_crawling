import requests, json

def send_msg(webhook_url, msg, channel="#dss", username="맛집봇"):
    payload = {"channel":channel, "username":username, "text":msg}
    requests.post(webhook_url, data = json.dumps(payload))
