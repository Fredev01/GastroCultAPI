from fastapi import APIRouter, Depends, HTTPException
from google.genai import types

from app.features.ai_recipe.models.recipe_info import RecipeInfo, RecipeRequest
from app.share.gemini import GeminiClient
from app.share.gemini.config import GeminiConfigImpl
from app.share.gemini.model import GeminiModel
from utils.extract_json import extract_json_from_ia_response
from utils.recipe_prompt import recipe_search_prompt


recipes_router = APIRouter(
    prefix="/recipes",
    tags=["recipes"],
)

gemini_client = GeminiClient(GeminiConfigImpl()).get_client()
model = GeminiModel.GEMINI_2_5_PRO
tools = [
    types.Tool(googleSearch=types.GoogleSearch(
    )),
]
generate_content_config = types.GenerateContentConfig(
    thinking_config=types.ThinkingConfig(
        thinking_budget=-1,
    ),
    tools=tools,
    response_mime_type="text/plain",
)


@recipes_router.post("/search")
async def search_recipes(
    request: RecipeRequest,
):
    """
    Search for recipes based on the provided location.
    """
    try:
        prompt = recipe_search_prompt(request.location)

        response = gemini_client.models.generate_content(
            model=model,
            contents=prompt,
            config=generate_content_config,
        )
        print(f"Response: {response.text}")
        if not response.text:
            raise HTTPException(
                status_code=400, detail="No response from model")
        recipes = extract_json_from_ia_response(response.text)

        return {"recipes": recipes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
