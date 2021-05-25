from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def index():
    return {"data": {"name": "Stephano"}}


@app.get("/about")
def about():
    return {"data": {"page": "about"}}
