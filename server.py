import os
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles

# Disable Swagger UI
app = FastAPI(docs_url=None, redoc_url=None)

# Create cloud_storage folder on the server if it doesn't exist
STORAGE_DIR = "cloud_storage"
os.makedirs(STORAGE_DIR, exist_ok=True)

# Mount cloud_storage directory so files can be publicly downloaded
app.mount("/download", StaticFiles(directory=STORAGE_DIR), name="download")

# --- Backend Endpoints ---

@app.post("/register")
async def register(username: str = Form(""), password: str = Form("")):
    return {"message": f"User '{username}' registered successfully!"}

@app.post("/login")
async def login(username: str = Form(""), password: str = Form("")):
    return {"message": f"Welcome back, {username}!"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(STORAGE_DIR, file.filename)
    
    # Save the file permanently on the cloud server
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
        
    download_url = f"/download/{file.filename}"
    return {
        "filename": file.filename, 
        "status": "File uploaded successfully!",
        "download_url": download_url
    }

@app.get("/files")
async def list_files():
    """Returns a list of all files currently stored on the cloud server."""
    files = os.listdir(STORAGE_DIR)
    return {"files": files}

# --- Interactive Web Dashboard ---

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
            :root {
                --bg-color: #121212;
                --card-bg: #1e1e1e;
                --text-color: #ffffff;
                --subtext-color: #b0b0b0;
                --input-bg: #2d2d2d;
                --accent-color: #4CAF50;
                --border-color: #333333;
            }

            [data-theme="light"] {
                --bg-color: #f4f6f8;
                --card-bg: #ffffff;
                --text-color: #1a1a1a;
                --subtext-color: #666666;
                --input-bg: #f0f0f0;
                --accent-color: #2e7d32;
                --border-color: #dddddd;
            }

            body {
                background-color: var(--bg-color);
                color: var(--text-color);
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                margin: 0;
                padding: 20px;
                display: flex;
                flex-direction: column;
                align-items: center;
                transition: background-color 0.3s, color 0.3s;
            }

            .header {
                width: 100%;
                max-width: 600px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 20px;
            }

            .card {
                background-color: var(--card-bg);
                padding: 25px;
                border-radius: 12px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.2);
                width: 100%;
                max-width: 600px;
                margin-bottom: 20px;
                border: 1px solid var(--border-color);
                box-sizing: border-box;
            }

            .status {
                color: var(--accent-color);
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 15px;
            }

            .tab-buttons {
                display: flex;
                gap: 10px;
                margin-bottom: 20px;
            }

            .tab-btn {
                flex: 1;
                padding: 10px;
                border: none;
                background-color: var(--input-bg);
                color: var(--text-color);
                border-radius: 6px;
                cursor: pointer;
                font-weight: bold;
            }

            .tab-btn.active {
                background-color: var(--accent-color);
                color: white;
            }

            form {
                display: flex;
                flex-direction: column;
                gap: 15px;
            }

            input[type="text"], input[type="password"], input[type="file"] {
                padding: 12px;
                border-radius: 6px;
                border: 1px solid var(--border-color);
                background-color: var(--input-bg);
                color: var(--text-color);
                box-sizing: border-box;
                width: 100%;
            }

            button.submit-btn {
                padding: 12px;
                border: none;
                border-radius: 6px;
                background-color: var(--accent-color);
                color: white;
                font-weight: bold;
                cursor: pointer;
                font-size: 15px;
            }

            .theme-toggle {
                background: none;
                border: 1px solid var(--border-color);
                color: var(--text-color);
                padding: 8px 12px;
                border-radius: 20px;
                cursor: pointer;
                font-size: 14px;
            }

            .response-box {
                margin-top: 15px;
                padding: 10px;
                border-radius: 6px;
                background-color: var(--input-bg);
                font-size: 14px;
                display: none;
                word-break: break-all;
            }

            .file-list {
                margin-top: 15px;
                list-style: none;
                padding: 0;
            }

            .file-item {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 10px;
                background-color: var(--input-bg);
                border-radius: 6px;
                margin-bottom: 8px;
            }

            .file-item a {
                color: var(--accent-color);
                text-decoration: none;
                font-weight: bold;
            }
        </style>
    </head>
    <body>

        <div class="header">
            <h2>ARNOD CLOUD SYSTEM</h2>
            <button class="theme-toggle" onclick="toggleTheme()">🌓 Switch Theme</button>
        </div>

        <div class="card">
            <div class="status">Cloud Backend Active & Healthy ✅</div>
            <p style="color: var(--subtext-color);">Public Cloud Storage & User Dashboard</p>
            
            <div class="tab-buttons">
                <button class="tab-btn active" onclick="showTab('login')">Sign In</button>
                <button class="tab-btn" onclick="showTab('register')">Create Account</button>
                <button class="tab-btn" onclick="showTab('upload')">Cloud Storage</button>
            </div>

            <!-- Login Form -->
            <form id="loginForm" onsubmit="handleForm(event, '/login')">
                <input type="text" name="username" placeholder="Username" required>
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit" class="submit-btn">Sign In</button>
            </form>

            <!-- Register Form -->
            <form id="registerForm" style="display: none;" onsubmit="handleForm(event, '/register')">
                <input type="text" name="username" placeholder="Choose Username" required>
                <input type="password" name="password" placeholder="Choose Password" required>
                <button type="submit" class="submit-btn">Create Account</button>
            </form>

            <!-- File Upload Form -->
            <div id="uploadSection" style="display: none;">
                <form onsubmit="handleFileUpload(event)">
                    <input type="file" name="file" required>
                    <button type="submit" class="submit-btn">Upload to Public Cloud</button>
                </form>

                <h3 style="margin-top: 25px;">Available Cloud Files:</h3>
                <ul id="fileList" class="file-list">Loading files...</ul>
            </div>

            <div id="responseBox" class="response-box"></div>
        </div>

        <script>
            function toggleTheme() {
                const currentTheme = document.body.getAttribute('data-theme');
                document.body.setAttribute('data-theme', currentTheme === 'light' ? 'dark' : 'light');
            }

            function showTab(tabName) {
                document.getElementById('loginForm').style.display = tabName === 'login' ? 'flex' : 'none';
                document.getElementById('registerForm').style.display = tabName === 'register' ? 'flex' : 'none';
                document.getElementById('uploadSection').style.display = tabName === 'upload' ? 'block' : 'none';
                
                const buttons = document.querySelectorAll('.tab-btn');
                buttons.forEach(btn => btn.classList.remove('active'));
                event.target.classList.add('active');

                if (tabName === 'upload') {
                    loadCloudFiles();
                }
            }

            async function handleForm(event, endpoint) {
                event.preventDefault();
                const formData = new FormData(event.target);
                const responseBox = document.getElementById('responseBox');
                
                try {
                    const res = await fetch(endpoint, { method: 'POST', body: formData });
                    const data = await res.json();
                    responseBox.style.display = 'block';
                    responseBox.style.color = '#4CAF50';
                    responseBox.innerText = data.message;
                } catch (err) {
                    responseBox.style.display = 'block';
                    responseBox.style.color = '#f44336';
                    responseBox.innerText = "Error connecting to backend.";
                }
            }

            async function handleFileUpload(event) {
                event.preventDefault();
                const formData = new FormData(event.target);
                const responseBox = document.getElementById('responseBox');
                
                try {
                    const res = await fetch('/upload', { method: 'POST', body: formData });
                    const data = await res.json();
                    responseBox.style.display = 'block';
                    responseBox.style.color = '#4CAF50';
                    responseBox.innerText = `${data.status} Saved as ${data.filename}`;
                    loadCloudFiles(); // Refresh file list automatically
                } catch (err) {
                    responseBox.style.display = 'block';
                    responseBox.style.color = '#f44336';
                    responseBox.innerText = "Upload failed.";
                }
            }

            async function loadCloudFiles() {
                const fileList = document.getElementById('fileList');
                try {
                    const res = await fetch('/files');
                    const data = await res.json();
                    fileList.innerHTML = '';
                    
                    if (data.files.length === 0) {
                        fileList.innerHTML = '<p style="color: var(--subtext-color);">No files uploaded yet.</p>';
                        return;
                    }

                    data.files.forEach(filename => {
                        const li = document.createElement('li');
                        li.className = 'file-item';
                        li.innerHTML = `
                            <span>📄 ${filename}</span>
                            <a href="/download/${filename}" download target="_blank">Download 📥</a>
                        `;
                        fileList.appendChild(li);
                    });
                } catch (err) {
                    fileList.innerHTML = '<p style="color: red;">Failed to load files.</p>';
                }
            }
        </script>

    </body>
    </html>
    """
