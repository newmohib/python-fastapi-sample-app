from fastapi import FastAPI
from . routers import user, course, auth

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(user.router)
app.include_router(course.router)
app.include_router(auth.router)

