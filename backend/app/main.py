from fastapi import FastAPI

app = FastAPI(
    title="AssetFlow API",
    description="Enterprise Asset Management System",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "success": True,
        "message": "AssetFlow Backend Running"
    }