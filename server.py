from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
import shutil
import uvicorn

app = FastAPI()

# Storage directory layout configuration
STORAGE_DIR = os.path.join(os.path.dirname(__file__), "cloud_storage")
os.makedirs(STORAGE_DIR, exist_ok=True)

USERS_DB = {}

class UserCredentials(BaseModel):
    username: str
    password: str

@app.post("/register")
async def register(user: UserCredentials):
    if user.username in USERS_DB:
        raise HTTPException(status_code=400, detail="Username already exists.")
    USERS_DB[user.username] = user.password
    return {"message": "Registration successful"}

@app.post("/login")
async def login(user: UserCredentials):
    if user.username not in USERS_DB or USERS_DB[user.username] != user.password:
        raise HTTPException(status_code=400, detail="Invalid username or password.")
    return {"message": "Login successful"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_location = os.path.join(STORAGE_DIR, file.filename)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        return {"message": f"Successfully uploaded {file.filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

# NEW: Fetch a list of all files sitting in the cloud storage folder
@app.get("/files")
async def list_files():
    try:
        files = os.listdir(STORAGE_DIR)
        return {"files": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# NEW: Allow users to download target items by name
@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(STORAGE_DIR, filename)
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename=filename, media_type='application/octet-stream')
    raise HTTPException(status_code=404, detail="File not found")

if __name__ == "__main__":
    # Host on 0.0.0.0 so anyone on your Wi-Fi/network connection can connect to your local IP!
    uvicorn.run(app, host="0.0.0.0", port=8000)