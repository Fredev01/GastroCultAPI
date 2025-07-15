from fastapi import APIRouter, Depends, HTTPException
from google.genai import types

from app.features.ai_recipe.models.recipe_info import RecipeInfo, RecipeRequest
from app.share.gemini import GeminiClient
from app.share.gemini.config import GeminiConfigImpl
from app.share.gemini.model import GeminiModel
from app.share.redis.redis_service import get_redis_service
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
redis_service = get_redis_service()


@recipes_router.post("/search")
async def search_recipes(
    request: RecipeRequest,
):
    """
    Search for recipes based on the provided location.
    Uses Redis cache to avoid repeated AI model calls.
    """
    try:
        location = request.location.strip()
        parts = location.split(",")
        municipality = parts[0].strip() if len(parts) > 0 else ""
        state = parts[1].strip() if len(parts) > 1 else ""
        if not municipality or not state:
            raise HTTPException(
                status_code=400, detail="Location must include municipality and state")
        location_formatted = f"{municipality}, {state}"

        # 1. Verificar si existe en cache
        cached_recipes = redis_service.get_recipe_cache(location_formatted)
        if cached_recipes:
            return {"recipes": cached_recipes, "from_cache": True}

        # 2. Si no existe en cache, consultar al modelo de IA
        prompt = recipe_search_prompt(location)

        response = gemini_client.models.generate_content(
            model=model,
            contents=prompt,
            config=generate_content_config,
        )

        if not response.text:
            raise HTTPException(
                status_code=400, detail="No response from model")

        # 3. Extraer recetas de la respuesta
        recipes = extract_json_from_ia_response(response.text)

        # 4. Guardar en cache solo si tiene contenido
        if recipes:
            redis_service.set_recipe_cache(
                location_formatted, recipes, ttl=3600)  # 1 hora

        return {"recipes": recipes, "from_cache": False}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
