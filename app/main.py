from fastapi import FastAPI
from . import database, models
from .routers import user, blog, auth

app = FastAPI()

models.Base.metadata.create_all(database.engine)


app.include_router(auth.router)
app.include_router(blog.router)
app.include_router(user.router)
