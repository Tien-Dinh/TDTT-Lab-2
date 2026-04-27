from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.auth import router as auth_router
from routers.note import router as note_router

app = FastAPI(title="Note App Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to Note App API"}

app.include_router(auth_router)
app.include_router(note_router)

@app.get("/health")
def health():
    return {"status": "ok"}