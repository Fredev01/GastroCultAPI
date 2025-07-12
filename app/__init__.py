from fastapi import FastAPI
from app.features.ai_recipe import recipes_router
from starlette.middleware.cors import CORSMiddleware
app = FastAPI()

# Lista de orígenes permitidos
origins = [
    "http://localhost:3000",
    "http://localhost:5173"
    # agrega aquí el dominio de producción, e.g. "https://tu-dominio.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # orígenes permitidos
    allow_credentials=True,           # si permites enviar cookies o credenciales
    allow_methods=["GET", "POST", "PUT", "DELETE",
                   "OPTIONS"],  # métodos permitidos
    allow_headers=["*"],              # cabeceras permitidas
)
app.include_router(recipes_router)


@app.get("/")
def get_index():
    return {"message": "API"}
