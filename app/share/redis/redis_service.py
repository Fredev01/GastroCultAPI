import json
import os
from typing import Optional, Any
import redis
from redis.exceptions import ConnectionError, RedisError
from dotenv import load_dotenv


class RedisService:
    _instance = None
    _initialized = False

    def __new__(cls, url: str = None):
        if cls._instance is None:
            cls._instance = super(RedisService, cls).__new__(cls)
        return cls._instance

    def __init__(self, url: str = None):
        # Evitar reinicialización múltiple
        if self._initialized:
            return

        load_dotenv()
        self.url = url or os.getenv("REDIS_URL", "redis://localhost:6379")
        self.client = None
        self._connect()
        self._initialized = True

    def _connect(self):
        """Establece conexión con Redis"""
        try:
            self.client = redis.from_url(self.url, decode_responses=True)
            # Test de conexión
            self.client.ping()
            print(f"✅ Conexión exitosa a Redis: {self.url}")
        except ConnectionError as e:
            print(f"❌ Error conectando a Redis: {e}")
            self.client = None
        except Exception as e:
            print(f"❌ Error inesperado con Redis: {e}")
            self.client = None

    def is_connected(self) -> bool:
        """Verifica si Redis está conectado"""
        if not self.client:
            return False
        try:
            return self.client.ping()
        except:
            return False

    def get_recipe_cache(self, location: str) -> Optional[dict]:
        """
        Obtiene los datos de recetas desde Redis usando location como clave
        """
        if not self.is_connected():
            return None

        try:
            key = f"recipe:{location.lower().strip()}"
            cached_data = self.client.get(key)

            if cached_data:
                print(f"📋 Cache HIT para location: {location}")
                return json.loads(cached_data)
            else:
                print(f"❌ Cache MISS para location: {location}")
                return None

        except (RedisError, json.JSONDecodeError) as e:
            print(f"❌ Error obteniendo cache para {location}: {e}")
            return None

    def set_recipe_cache(self, location: str, recipes: Any, ttl: int = 3600) -> bool:
        """
        Guarda datos de recetas en Redis

        Args:
            location: Ubicación (clave única)
            recipes: Datos de recetas a guardar
            ttl: Tiempo de vida en segundos (default: 1 hora)
        """
        if not self.is_connected():
            return False

        # Validar que recipes tenga contenido
        if not recipes or (isinstance(recipes, (list, dict)) and len(recipes) == 0):
            print(f"⚠️ No se guardará cache para {location}: sin contenido")
            return False

        try:
            key = f"recipe:{location.lower().strip()}"
            data = json.dumps(recipes, ensure_ascii=False)

            result = self.client.setex(key, ttl, data)

            if result:
                print(f"💾 Cache guardado para location: {location}")
                return True
            else:
                print(f"❌ Error guardando cache para location: {location}")
                return False

        except (RedisError, json.JSONEncodeError) as e:
            print(f"❌ Error guardando cache para {location}: {e}")
            return False

    def delete_recipe_cache(self, location: str) -> bool:
        """Elimina cache de recetas para una ubicación específica"""
        if not self.is_connected():
            return False

        try:
            key = f"recipe:{location.lower().strip()}"
            result = self.client.delete(key)
            print(f"🗑️ Cache eliminado para location: {location}")
            return result > 0
        except RedisError as e:
            print(f"❌ Error eliminando cache para {location}: {e}")
            return False

    def get_cache_info(self) -> dict:
        """Información del estado del cache"""
        if not self.is_connected():
            return {"connected": False}

        try:
            info = self.client.info()
            return {
                "connected": True,
                "used_memory": info.get("used_memory_human", "N/A"),
                "total_keys": self.client.dbsize(),
                "redis_version": info.get("redis_version", "N/A")
            }
        except RedisError as e:
            return {"connected": False, "error": str(e)}

    @classmethod
    def get_instance(cls, url: str = None):
        """Método alternativo para obtener la instancia (más explícito)"""
        return cls(url)


# Función para obtener la instancia global
def get_redis_service() -> RedisService:
    return RedisService()
