import requests

res = requests.post(
    "http://127.0.0.1:1700/api/ai/inference",
    json={
        "msg": "Hi, how are you?",
    },
)

print(res.json(), res.status_code)
