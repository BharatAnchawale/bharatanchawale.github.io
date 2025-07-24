from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from storage.minio_client import upload_to_minio, download_from_minio
from processing.video_converter import encrypt_video, decrypt_video
import os
import uuid
import tempfile

app = FastAPI()

# TEMP key store (use secure vault in prod)
KEY_STORE = {}

@app.post("/upload/")
async def upload_video(file: UploadFile = File(...)):
    if not file.filename.endswith((".mp4", ".mov", ".avi", ".mkv")):
        raise HTTPException(status_code=400, detail="Unsupported file format")

    # Save uploaded file to temp
    temp_input = tempfile.NamedTemporaryFile(delete=False)
    temp_input.write(await file.read())
    temp_input.close()

    # Encrypt and save encrypted output
    temp_encrypted = tempfile.NamedTemporaryFile(delete=False, suffix=".enc")
    key = encrypt_video(temp_input.name, temp_encrypted.name)

    # Unique filename to avoid clashes
    video_id = str(uuid.uuid4())
    minio_filename = f"{video_id}.enc"

    # Upload to MinIO
    upload_to_minio(temp_encrypted.name, minio_filename)

    # Store key for decryption (simplified for now)
    KEY_STORE[video_id] = key

    # Cleanup
    os.remove(temp_input.name)
    os.remove(temp_encrypted.name)

    return {"message": "Upload successful", "video_id": video_id}

@app.get("/download/{video_id}")
def download_video(video_id: str):
    minio_filename = f"{video_id}.enc"
    key = KEY_STORE.get(video_id)

    if not key:
        raise HTTPException(status_code=404, detail="Key not found")

    temp_encrypted = tempfile.NamedTemporaryFile(delete=False)
    download_from_minio(minio_filename, temp_encrypted.name)

    temp_decrypted = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    decrypt_video(temp_encrypted.name, temp_decrypted.name, key)

    def iterfile():
        with open(temp_decrypted.name, mode="rb") as file_like:
            yield from file_like
        os.remove(temp_encrypted.name)
        os.remove(temp_decrypted.name)

    return StreamingResponse(iterfile(), media_type="video/mp4")
