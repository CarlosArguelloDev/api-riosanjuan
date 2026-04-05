# API Río San Juan — Predicciones y Sensores

![Banner](assets/banner.png)

API robusta y escalable para consultar y almacenar mediciones y predicciones asociadas a sensores ambientales.

## Arquitectura del Proyecto

El proyecto ha sido refactorizado siguiendo una **arquitectura por capas** para facilitar su mantenimiento y escalabilidad:

- **`app/models`**: Definición de tablas y relaciones con SQLAlchemy ORM.
- **`app/services`**: Lógica de negocio pura (aislada de la capa HTTP).
- **`app/routes`**: Controladores (Blueprints) que manejan las peticiones y respuestas.
- **`app/schemas`**: Serialización y validación de datos.
- **`app/errors`**: Manejador global de errores (404, 400, 500) en formato JSON.

---

## Configuración y Ejecución

### Requisitos
- Python 3.14+
- PostgreSQL (Producción) / SQLite (Pruebas)

### Instalación Local
1. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Configurar variables de entorno (copiar `.env.example` a `.env`):
   ```bash
   FLASK_ENV=development
   DATABASE_URL=postgresql://usuario:password@localhost:5432/db_nombre
   ```
3. Ejecutar servidor de desarrollo:
   ```bash
   python wsgi.py
   ```

### Docker
```bash
docker build -t api-riosanjuan .
docker run -p 5000:5000 api-riosanjuan
```

---

## Documentación de la API (v1)

Todas las rutas están prefijadas con `/api/v1`.

### 1. Predicciones

#### GET /api/v1/predicciones
Obtener predicciones por sensor con filtros avanzados.

**Parámetros:**
| Parámetro | Descripción |
|---|---|
| `id_sensor` | (Obligatorio) ID del sensor. |
| `desde_objetivo` | Fecha objetivo mínima (ISO 8601). |
| `hasta_objetivo` | Fecha objetivo máxima. |
| `latest` | `true` para obtener solo la predicción más reciente por fecha. |

**Ejemplo:**
`GET /api/v1/predicciones?id_sensor=1&latest=true`

#### POST /api/v1/predicciones
Crear una o múltiples predicciones.

---

### 2. Mediciones

#### GET /api/v1/mediciones
Consultar historial de mediciones reales de un sensor.

#### POST /api/v1/mediciones
Subir mediciones (soporta carga masiva en JSON).

---

### 3. Catálogos
- `GET /api/v1/estaciones`: Listar todas las estaciones.
- `GET /api/v1/sensores`: Listar sensores (filtrable por `id_estacion`).
- `GET /api/v1/tipos_sensor`: Listar tipos de sensores disponibles.

---

## Pruebas (Testing)

Se utiliza `pytest` para asegurar la calidad del código. Los tests usan una base de datos SQLite en memoria.

```bash
pytest tests/ -v
```

---

## Notas
- Las fechas deben venir en formato **ISO 8601** (ej: `2025-11-27T12:00:00Z`).
- Toda respuesta de error incluye `{"ok": false, "error": "mensaje"}`.
