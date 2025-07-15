e# GastroCultApi 🍽️

Una API de FastAPI que utiliza inteligencia artificial para generar recetas culinarias basadas en ubicaciones geográficas específicas.

## 📋 Descripción

GastroCultApi es una aplicación web que combina la potencia de FastAPI con la inteligencia artificial de Google Gemini para crear recetas culinarias personalizadas. La API permite a los usuarios obtener recetas tradicionales y auténticas basadas en una ubicación o región específica.

## ✨ Características

- **Generación de recetas con IA**: Utiliza Google Gemini para crear recetas únicas
- **Recetas basadas en ubicación**: Genera recetas tradicionales según la región especificada
- **API RESTful**: Interfaz limpia y fácil de usar
- **Validación de datos**: Utiliza Pydantic para validación robusta
- **Configuración flexible**: Sistema de configuración basado en variables de entorno

## 🏗️ Arquitectura del Proyecto

```
GastroCultApi/
├── app/
│   ├── features/
│   │   ├── ai_recipe/
│   │   │   ├── models/
│   │   │   │   └── recipe_info.py      # Modelos de datos para recetas
│   │   │   └── __init__.py
│   │   └── events/
│   ├── share/
│   │   ├── config/
│   │   │   └── __init__.py             # Configuración base
│   │   └── gemini/
│   │       ├── config.py               # Configuración de Gemini
│   │       ├── model.py                # Modelos de Gemini
│   │       └── __init__.py
│   ├── main.py                         # Punto de entrada de la aplicación
│   └── __init__.py
├── requirements.txt                    # Dependencias del proyecto
└── venv/                              # Entorno virtual
```

## 🚀 Instalación

### Prerrequisitos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos de instalación

1. **Clonar el repositorio**

   ```bash
   git clone <url-del-repositorio>
   cd GastroCultApi
   ```

2. **Crear entorno virtual**

   ```bash
   python -m venv venv
   source venv/bin/activate  # En Linux/Mac
   # o
   venv\Scripts\activate     # En Windows
   ```

3. **Instalar dependencias**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**

   Crea un archivo `.env` en la raíz del proyecto:

   ```env
   GEMINI_API_KEY=tu_api_key_de_google_gemini
   ```

   ```env
   REDIS_URL=redis://localhost:6379
   ```

5. **Levantar la BD redis**

   ```bash
   docker compose up -d
   ```

6. **Ejecutar la aplicación**
   ```bash
    fastapi dev app
   ```

## 🔧 Configuración

### Variables de Entorno

| Variable         | Descripción              | Requerida |
| ---------------- | ------------------------ | --------- |
| `GEMINI_API_KEY` | API Key de Google Gemini | Sí        |

### Obtener API Key de Google Gemini

1. Ve a [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Crea una nueva API key
3. Copia la key y agrégala a tu archivo `.env`

## 📖 Uso

### Endpoints Disponibles

#### Generar Receta por Ubicación

**POST** `/recipes/generate`

Genera una receta basada en la ubicación especificada.

**Request Body:**

```json
{
  "location": "México"
}
```

**Response:**

```json
{
  "recipe": {
    "title": "Tacos al Pastor",
    "description": "Tacos tradicionales mexicanos con carne de cerdo marinada",
    "ingredients": [
      {
        "name": "Carne de cerdo",
        "quantity": "500g"
      },
      {
        "name": "Piña",
        "quantity": "1 taza"
      }
    ],
    "instructions": [
      "Marinar la carne con especias",
      "Cocinar en plancha caliente",
      "Servir en tortillas de maíz"
    ]
  }
}
```

## 🧪 Testing

Para ejecutar las pruebas:

```bash
pytest
```

## 📦 Dependencias

- **FastAPI**: Framework web moderno y rápido
- **python-dotenv**: Carga de variables de entorno
- **pytest**: Framework de testing
- **google-genai**: Cliente oficial de Google Gemini AI
- **Pydantic**: Validación de datos y serialización

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 🆘 Soporte

Si tienes alguna pregunta o problema, por favor:

1. Revisa la documentación
2. Busca en los issues existentes
3. Crea un nuevo issue con detalles del problema

## 🔮 Roadmap

- [ ] Añadir más endpoints para diferentes tipos de recetas
- [ ] Implementar caché para mejorar el rendimiento
- [ ] Añadir autenticación de usuarios
- [ ] Crear interfaz web
- [ ] Soporte para múltiples idiomas
- [ ] Integración con bases de datos de ingredientes

---

**Desarrollado con ❤️ usando FastAPI y Google Gemini AI**
