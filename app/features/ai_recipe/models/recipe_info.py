from pydantic import BaseModel, Field


class Ingredient(BaseModel):
    name: str
    quantity: str


class RecipeInfo(BaseModel):
    title: str
    description: str
    ingredients: list[Ingredient]
    instructions: list[str]


class RecipeInfoResponse(BaseModel):
    recipe: RecipeInfo


class RecipeRequest(BaseModel):
    location: str = Field(..., description="Lugar o región para buscar recetas",
                          min_length=1, max_length=100)
