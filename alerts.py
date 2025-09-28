import requests

def get_govt_alerts():
    try:
        url = "https://api.rootnet.in/covid19-in/notifications"
        r = requests.get(url)
        data = r.json()
        alerts = [item['title'] for item in data['data']['notifications'][:5]]
        return alerts
    except:
        return ["No alerts available currently."]
