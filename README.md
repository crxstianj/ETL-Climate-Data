# ETL de Datos Climáticos de México

Pipeline ETL en Python para extraer, transformar y almacenar datos climáticos históricos de los estados de México utilizando una API externa y MongoDB.

## Descripción

Este proyecto implementa un proceso de **Extracción, Transformación y Carga (ETL)** que obtiene datos climáticos diarios desde una API, los procesa para generar métricas mensuales agregadas y los almacena en MongoDB para su análisis posterior.

El script procesa información climática de los estados de México desde 2020 hasta la fecha actual, manteniendo los registros actualizados sin duplicados.

---

## Objetivo

- Obtener datos climáticos históricos de los estados de México.
- Transformar datos diarios en métricas mensuales.
- Almacenar datos estructurados en MongoDB.
- Mantener actualización incremental automática.

---

## Flujo del Pipeline


API climática → Extracción → Transformación → Agregación mensual → MongoDB


### Extracción
- Consumo de API mediante solicitudes HTTP.
- Obtención de datos diarios por estado.
- Validación de respuesta de la API.

### Transformación
- Limpieza y validación de datos.
- Conversión a DataFrame con Pandas.
- Agregación mensual de:
  - temperatura máxima promedio
  - temperatura mínima promedio
  - temperatura media
  - humedad relativa promedio

### Carga
- Inserción y actualización de datos en MongoDB.
- Uso de `upsert` para evitar duplicados.
- Actualización incremental por estado y fecha.

---

## Tecnologías utilizadas

- Python
- Pandas
- MongoDB
- Requests (API REST)
- python-dotenv
- Certifi

---

## Variables procesadas

- Temperatura máxima
- Temperatura mínima
- Temperatura promedio
- Humedad relativa promedio

Frecuencia de almacenamiento: **mensual por estado**.

---

## Estructura del proyecto

.  
├── etl_weather.py  
├── .env  
└── README.md


---

## Instalación

### 1. Clonar repositorio

git clone <repo-url>
cd <repo>

###2. Instalar dependencias
pip install pandas pymongo requests python-dotenv certifi

###3. Configurar variables de entorno

Crear archivo .env con:

MONGODB_URI=tu_uri_mongodb
DB_NAME=nombre_base_datos
COLLECTION_NAME=nombre_coleccion
###Uso

Ejecutar el script:

python etl_weather.py

El programa:

obtiene datos desde 2020 hasta la fecha actual

procesa información de todos los estados de México

actualiza registros automáticamente en MongoDB

Ejemplo de registro almacenado
{
  "estado": "Guanajuato",
  "fecha": "2024-05",
  "temperatura_max_promedio": 29.3,
  "temperatura_min_promedio": 14.2,
  "temperatura_promedio": 21.7,
  "humedad_promedio": 65.1
}
Posibles mejoras

Contenerización con Docker

Orquestación del pipeline

API para consulta de datos

Visualización de información

Programación automática de ejecuciones

Autor

Cristian Jesús Silva Medel
