from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def status_ok():
    return {"status": "OK"}
