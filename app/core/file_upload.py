import os
import uuid
from fastapi import UploadFile

def save_file(file: UploadFile, folder: str):
    os.makedirs(folder, exist_ok=True)

    extension = file.filename.split(".")[-1]

    filename = f"{uuid.uuid4()}.{extension}"
    filepath = os.path.join(folder, filename)

    with open(filepath, "wb") as buffer:
        buffer.write(file.file.read())


    return filepath
