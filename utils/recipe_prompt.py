def recipe_search_prompt(location: str) -> str:
    """
    Generate a prompt for searching recipes based on the provided location.
    """
    return f"""\
        Genera una lista de al menos 20 recetas tradicionales de {location}.
        Para cada receta, incluye:
        - El nombre del platillo
        - Una breve descripción
        - Una lista de ingredientes con sus cantidades
        - Una lista de instrucciones de preparación

        Devuelve la información en formato JSON con la siguiente estructura:
        [
        {{
            "name": "Nombre del platillo",
            "description": "Breve descripción del platillo",
            "ingredients": [
            {{
                "name": "Nombre del ingrediente",
                "quantity": "Cantidad del ingrediente"
            }},
            ...
            ],
            "preparation": [
            "Instrucción 1",
            "Instrucción 2",
            ...
            ]
        }},
        ...
        ]"""
