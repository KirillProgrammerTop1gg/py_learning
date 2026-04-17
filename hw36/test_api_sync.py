import requests, time

TOTAL_REQUESTS_QUANTITY = 1000
url = "http://127.0.0.1:8000/participants"

start_time = round(time.time(), 2)

for i in range(TOTAL_REQUESTS_QUANTITY):
    res = requests.post(
        url,
        json={
            "name": "nick",
            "email": f"example{i+1}@test.com",
            "age": 17,
            "event": "yoga",
        },
    )

print(f"Work time: {round(time.time(), 2)-start_time}s")
