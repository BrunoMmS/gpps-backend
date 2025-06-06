from fastapi import APIRouter, File, UploadFile, HTTPException, status
from typing import Optional
import os
import shutil

uploader_router = APIRouter(prefix="/upload", tags=["Upload"])
upload_directory = "uploaded_files"

@uploader_router.post("/")
async def upload_multiple_files(files: list[UploadFile] = File(...)):
    os.makedirs(upload_directory, exist_ok=True)
    uploaded_files = []
    for file in files:
        file_location = os.path.join(upload_directory, file.filename)
        try:
            with open(file_location, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            uploaded_files.append({"filename": file.filename, "info": f"El archivo '{file.filename}' se subió correctamente."})
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"No se pudo subir el archivo '{file.filename}': {e}")
        finally:
            file.file.close()
    return {"files": uploaded_files}