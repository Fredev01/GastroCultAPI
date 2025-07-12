import json
import re
from fastapi import APIRouter, Depends, HTTPException
from google.genai import types

from app.features.ai_recipe.models.recipe_info import RecipeInfo, RecipeRequest
from app.share.gemini import GeminiClient
from app.share.gemini.config import GeminiConfigImpl
from app.share.gemini.model import GeminiModel


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
        prompt = f"""\
            Genera una lista de al menos 20 recetas tradicionales de {request.location}.
            Para cada receta, incluye:
            - El nombre del platillo
            - Una breve descripción
            - Una lista de ingredientes con sus cantidades
            - Una lista de instrucciones de preparación

            Devuelve la información en formato JSON con la siguiente estructura:
            [
            {{
                "nombre": "Nombre del platillo",
                "descripcion": "Breve descripción del platillo",
                "ingredientes": [
                {{
                    "nombre": "Nombre del ingrediente",
                    "cantidad": "Cantidad del ingrediente"
                }},
                ...
                ],
                "preparacion": [
                "Instrucción 1",
                "Instrucción 2",
                ...
                ]
            }},
            ...
            ]
        """

        response = gemini_client.models.generate_content(
            model=model,
            contents=prompt,
            config=generate_content_config,
        )
        print(f"Response: {response.text}")
        match = re.search(
            r"```json\s*(\[.*?\])\s*```", response.text, re.DOTALL)
        if not match:
            raise HTTPException(
                status_code=400, detail="Invalid response format")
        json_content = match.group(1)
        print(f"JSON content: {json_content}")
        recipes = json.loads(json_content)

        return {"recipes": recipes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
