from fastapi import FastAPI, Path, HTTPException
from concurrent.futures import ThreadPoolExecutor
import requests, time

app = FastAPI()

# jsonplaceholder не підтримує photos?userId=X
# Використовуємо photos?albumId=X через альбоми користувача


def get_json(url: str):
    try:
        r = requests.get(url, timeout=5)
        return r.json()
    except Exception:
        return None


try:
    r = requests.get("https://jsonplaceholder.typicode.com/users", timeout=5)
    all_user_ids = [x["id"] for x in r.json()]
except Exception:
    all_user_ids = []


@app.get("/user-dashboard/{user_id}")
def user_dashboard(user_id: int = Path(...)):
    if user_id not in all_user_ids:
        raise HTTPException(status_code=404, detail="User not found")
    start_time = time.perf_counter()
    urls = [
        f"https://jsonplaceholder.typicode.com/users/{user_id}",
        f"https://jsonplaceholder.typicode.com/users/{user_id}/posts",
        f"https://jsonplaceholder.typicode.com/users/{user_id}/albums",
    ]

    with ThreadPoolExecutor(max_workers=3) as executor:
        user, posts, albums = list(executor.map(get_json, urls))

    if albums:
        albums_urls = [
            f"https://jsonplaceholder.typicode.com/photos?albumId={album['id']}&_limit=10"
            for album in albums
        ]
        with ThreadPoolExecutor(max_workers=len(albums)) as executor:
            albums_with_photos = list(executor.map(get_json, albums_urls))

        photos_count = sum(
            [len(album) if album is not None else 0 for album in albums_with_photos]
        )
    else:
        photos_count = None

    elapsed = round(time.perf_counter() - start_time, 3)

    return {
        "user": {
            "id": user["id"],
            "name": user["name"],
            "username": user["username"],
            "email": user["email"],
        },
        "posts_count": len(posts) if posts is not None else None,
        "albums_count": len(albums) if albums is not None else None,
        "photos_count": photos_count,
        "elapsed_seconds": elapsed,
    }
