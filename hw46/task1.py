from fastapi import FastAPI, Path, HTTPException
from concurrent.futures import ThreadPoolExecutor
import logging, requests, time

logger = logging.getLogger(__name__)

app = FastAPI()

# jsonplaceholder не підтримує photos?userId=X
# Використовуємо photos?albumId=X через альбоми користувача


def get_json(url: str):
    try:
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.Timeout:
        logger.error("Timeout fetching %s", url)
        return None
    except requests.exceptions.HTTPError as e:
        logger.error("HTTP %s for %s", e.response.status_code, url)
        if e.response.status_code == 404:
            raise
        return None
    except requests.exceptions.RequestException as e:
        logger.error("Request error for %s: %s", url, e)
        return None


@app.get("/user-dashboard/{user_id}")
def user_dashboard(user_id: int = Path(...)):
    start_time = time.perf_counter()
    urls = [
        f"https://jsonplaceholder.typicode.com/users/{user_id}",
        f"https://jsonplaceholder.typicode.com/users/{user_id}/posts",
        f"https://jsonplaceholder.typicode.com/users/{user_id}/albums",
    ]
    try:
        with ThreadPoolExecutor(max_workers=3) as executor:
            user, posts, albums = list(executor.map(get_json, urls))
    except requests.exceptions.HTTPError:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user is None:
        raise HTTPException(status_code=503, detail="Failed to fetch user data")

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
