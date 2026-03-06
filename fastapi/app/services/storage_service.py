from fastapi import HTTPException, UploadFile, Depends
from app.dependencies.supabase import get_supabase
from typing import Annotated
from supabase import Client
from app.config import settings

def upload_user_profile_image(user_id: int, file: UploadFile, supabase: Annotated[Client, Depends(get_supabase)]):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Only images are allowed.")
    try:
        file_bytes = file.file.read()
        file_extension = file.filename.split(".")[-1] if "." in file.filename else "jpg"
        file_path = f"{user_id}/profile_image.{file_extension}"

        supabase.storage.from_(settings.bucket_name).upload(path=file_path, file=file_bytes, file_options={"content-type": file.content_type, "x-upsert": "true"})

        return supabase.storage.from_(settings.bucket_name).get_public_url(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
    finally:
        file.file.close()