# Predictions API

API to query and store predictions associated with sensors.

## Base URL

https://api.okshield.dev

---

## GET /predicciones

Retrieve predictions by sensor.

### Basic example

GET /predicciones?id_sensor=1

### With filters

GET /predicciones
  ?id_sensor=1
  &desde_objetivo=2025-11-27T00:00:00Z
  &hasta_objetivo=2025-11-28T00:00:00Z
  &emitido_desde=2025-11-26T00:00:00Z
  &emitido_hasta=2025-11-27T10:00:00Z
  &latest=true
  &order=desc
  &limit=50

### Parameters

| Parameter        | Description |
|------------------|------------|
| id_sensor        | Sensor ID |
| desde_objetivo   | Minimum target date |
| hasta_objetivo   | Maximum target date |
| emitido_desde    | Minimum emission date |
| emitido_hasta    | Maximum emission date |
| latest           | Returns only the latest prediction per target date |
| order            | asc or desc |
| limit            | Maximum number of results |

### Response (200)

{
  "ok": true,
  "data": [
    {
      "id_prediccion": 42,
      "id_sensor": 1,
      "fecha_objetivo": "2025-11-27T12:00:00+00:00",
      "valor_predicho": 23.5,
      "emitido_en": "2025-11-27T10:00:00+00:00"
    }
  ]
}

---

## POST /predicciones

Create one or multiple predictions.

### Headers

Content-Type: application/json

### Body (single prediction)

{
  "id_sensor": 1,
  "fecha_objetivo": "2025-11-27T12:00:00Z",
  "valor_predicho": 23.5,
  "emitido_en": "2025-11-27T10:00:00Z"
}

### Body (multiple predictions)

[
  {
    "id_sensor": 1,
    "fecha_objetivo": "2025-11-27T12:00:00Z",
    "valor_predicho": 23.5,
    "emitido_en": "2025-11-27T10:00:00Z"
  },
  {
    "id_sensor": 1,
    "fecha_objetivo": "2025-11-27T13:00:00Z",
    "valor_predicho": 24.0,
    "emitido_en": "2025-11-27T10:00:00Z"
  }
]

### Response (201)

{
  "ok": true,
  "data": {
    "insertados": 2
  }
}

---

## Examples with curl

### POST

curl -X POST "https://api.okshield.dev/predicciones" \
  -H "Content-Type: application/json" \
  -d '{"id_sensor":1,"fecha_objetivo":"2025-11-27T12:00:00Z","valor_predicho":23.5,"emitido_en":"2025-11-27T10:00:00Z"}'

### GET (latest by target date)

curl "https://api.okshield.dev/predicciones?id_sensor=1&latest=true&limit=20&order=desc"

---

## Notes

- Dates must be in ISO 8601 format.
- Use Z for UTC, e.g. 2025-11-27T12:00:00Z.
- latest=true returns only the latest prediction per fecha_objetivo, based on emitido_en.
