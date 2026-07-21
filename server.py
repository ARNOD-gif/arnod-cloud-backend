import flet as ft
import flet.fastapi as flet_fastapi
from fastapi import FastAPI, File, UploadFile

# 1. Create FastAPI app with Swagger UI completely DISABLED
app = FastAPI(docs_url=None, redoc_url=None)

# --- Your Existing Backend Endpoints ---

@app.post("/register")
async def register():
    return {"message": "User registered successfully"}

@app.post("/login")
async def login():
    return {"message": "User logged in successfully"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename, "status": "Uploaded successfully"}

# --- Your Custom Visual Web UI (Replaces Swagger) ---

def main(page: ft.Page):
    page.title = "ARNOD CLOUD SERVER"
    page.theme_mode = ft.ThemeMode.DARK
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    status_text = ft.Text(value="Cloud Backend Active & Healthy ✅", color="green", size=16)

    def on_keyboard_event(e: ft.KeyboardEvent):
        if e.key.lower() == "r":
            status_text.value = "Resetting application state..."
            status_text.color = "amber"
            page.update()

    page.on_keyboard_event = on_keyboard_event

    page.add(
        ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text("ARNOD CLOUD SYSTEM", size=28, weight=ft.FontWeight.BOLD),
                    status_text,
                    ft.Text("Welcome to the ARNOD Cloud Dashboard!", size=14, color="white70"),
                    ft.Text("Tip: Press 'R' on your keyboard to reset the view", size=12, color="gray")
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            ),
            padding=40,
            border_radius=10,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
        )
    )

# 2. Mount your Flet visual layout onto the root URL
app.mount("/", flet_fastapi.app(main))
