from fastapi import FastAPI
from . routers import user, course, auth
from . import models
from . database import engine
from . config import settings

models.Base.metadata.create_all(bind=engine)


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

