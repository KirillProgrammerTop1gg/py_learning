from fastapi import File, FastAPI, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os, uuid, re
from pathlib import Path
from PIL import Image
from datetime import datetime

app = FastAPI()

MAX_FILE_SIZE = 5 * 1024 * 1024
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png"]
CHUNK_SIZE = 1024 * 1024

os.makedirs("photos", exist_ok=True)

def sanitize_filename(filename: str) -> str:
    stem = Path(filename).stem
    suffix = Path(filename).suffix
    clean_stem = re.sub(r'[^\w\-]', '', stem)
    if not clean_stem:
        clean_stem = "file"
    clean_stem = clean_stem[:50]
    unique_id = uuid.uuid4().hex[:8]
    return f"{clean_stem}_{unique_id}{suffix}"


def validate_image(file_path: Path) -> bool:
    try:
        with Image.open(file_path) as image:
            image.verify()
        return True
    except Exception:
        return False


@app.post("/photos/upload/", status_code=201)
async def upload_verified_image(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Недопустимий формат файлу. Дозволені: {', '.join(ALLOWED_IMAGE_TYPES)}"
        )

    safe_filename = sanitize_filename(file.filename)
    file_path = Path("photos") / safe_filename

    total_size = 0
    try:
        with open(file_path, "wb") as f:
            while chunk := await file.read(CHUNK_SIZE):
                total_size += len(chunk)
                if total_size > MAX_FILE_SIZE:
                    f.close()
                    file_path.unlink(missing_ok=True)
                    raise HTTPException(
                        status_code=413,
                        detail="Файл занадто великий. Максимальний розмір: 5MB"
                    )
                f.write(chunk)
    except HTTPException:
        raise
    except Exception as e:
        file_path.unlink(missing_ok=True)
        raise HTTPException(status_code=500, detail=f"Не вдалося зберегти файл: {str(e)}")

    if not validate_image(file_path):
        file_path.unlink(missing_ok=True)
        raise HTTPException(
            status_code=400,
            detail="Файл пошкоджений або не є зображенням"
        )

    return {
        "message": "Зображення перевірено та збережено",
        "filename": safe_filename,
        "public_url": f"/photos/{safe_filename}"
    }


@app.get("/photos/list/")
async def list_photos():
    photos_dir = Path("photos")
    
    files = [
        f for f in photos_dir.iterdir()
        if f.is_file() and f.suffix.lower() in (".jpg", ".jpeg", ".png")
    ]
    
    files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
    
    return {
        "total": len(files),
        "photos": [
            {
                "filename": f.name,
                "public_url": f"/photos/{f.name}",
                "uploaded_at": datetime.fromtimestamp(f.stat().st_mtime).isoformat()
            }
            for f in files
        ]
    }

@app.get("/photos/{filename}")
async def get_photo(filename: str):
    safe_name = Path(filename).name
    file_path = Path("photos") / safe_name

    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="Фото не знайдено")

    suffix = file_path.suffix.lower()
    media_type = "image/jpeg" if suffix in (".jpg", ".jpeg") else "image/png"

    return FileResponse(path=file_path, media_type=media_type)