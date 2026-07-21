from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse

# Disable Swagger UI completely (/docs and /redoc will show 404)
app = FastAPI(docs_url=None, redoc_url=None)

# Your API Endpoints
@app.post("/register")
async def register():
    return {"message": "User registered successfully"}

@app.post("/login")
async def login():
    return {"message": "User logged in successfully"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename, "status": "Uploaded successfully"}

# Clean Dark-Mode Web Dashboard at root URL (/)
@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ARNOD CLOUD SERVER</title>
        <style>
            body {
                background-color: #121212;
                color: #ffffff;
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .card {
                background-color: #1e1e1e;
                padding: 40px;
                border-radius: 12px;
                box-shadow: 0 8px 16px rgba(0,0,0,0.5);
                text-align: center;
                max-width: 400px;
            }
            h1 {
                font-size: 26px;
                margin-bottom: 10px;
            }
            .status {
                color: #4CAF50;
                font-size: 18px;
                font-weight: bold;
                margin: 15px 0;
            }
            p {
                color: #b0b0b0;
                font-size: 14px;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>ARNOD CLOUD SYSTEM</h1>
            <div class="status">Cloud Backend Active & Healthy ✅</div>
            <p>Welcome to the ARNOD Cloud Dashboard!</p>
        </div>
    </body>
    </html>
    """
