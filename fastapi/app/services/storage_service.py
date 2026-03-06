from fastapi import HTTPException, UploadFile, Depends
from app.dependencies.supabase import get_supabase
from typing import Annotated
from supabase import Client
from app.config import settings

def upload_user_profile_image(user_id: int, file: UploadFile, supabase: Annotated[Client, Depends(get_supabase)]):
    allowed_content_types = {"image/jpeg", "image/jpg", "image/png"}
    allowed_extensions = {"jpg", "jpeg", "png"}

    file_extension = file.filename.split(".")[-1].lower() if file.filename and "." in file.filename else ""
    if file.content_type not in allowed_content_types or file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPG, JPEG, and PNG are allowed.")

    try:
        file_bytes = file.file.read()
        file_path = f"{user_id}/profile_image.{file_extension}"

        supabase.storage.from_(settings.bucket_name).upload(path=file_path, file=file_bytes, file_options={"content-type": file.content_type, "x-upsert": "true"})

        return supabase.storage.from_(settings.bucket_name).get_public_url(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
    finally:
        file.file.close()