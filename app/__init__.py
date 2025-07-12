from fastapi import FastAPI
from app.features.ai_recipe import recipes_router
app = FastAPI()

app.include_router(recipes_router)


@app.get("/")
def get_index():
    return {"message": "API"}
