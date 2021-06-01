from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
def index():
    return {"data": {"name": "Stephano"}}


@app.get("/blog/{id}")
def blog(id: int):
    return {"blog": id}


@app.get("/blog/{id}/comments")
def blog_comments(id: int):
    return {"blog": id, "comments": {"1", "2"}}


@app.get("/blog/{id}/status")
def blog_status(id: int):
    return {"blog": id, "status": "unpublished", "comments": {"1", "2"}}


class Post(BaseModel):
    name: str
    description: str
    content: str
    status: str = "unpublished"


@app.post("/post-creation/")
def createPost(post: Post):
    return post
