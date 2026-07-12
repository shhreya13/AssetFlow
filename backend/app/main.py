from fastapi import FastAPI

app = FastAPI(title="AssetFlow API")

@app.get("/")
def root():
    return {"message": "AssetFlow Backend Running"}