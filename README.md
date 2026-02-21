ETL de Datos Climáticos de México

Pipeline ETL desarrollado en Python para la extracción, transformación y almacenamiento de datos climáticos históricos de los estados de México utilizando una API externa y MongoDB.

Descripción

Este proyecto implementa un proceso automatizado de Extracción, Transformación y Carga (ETL) que obtiene datos climáticos diarios, los procesa para generar métricas mensuales agregadas y los almacena en una base de datos NoSQL para su análisis posterior.

El pipeline permite mantener datos actualizados de variables meteorológicas clave como temperatura y humedad para los 31 estados de México.

Objetivo

Construir una solución automatizada para:

Obtener datos climáticos históricos desde 2020 hasta la fecha.

Procesar y agregar información diaria en métricas mensuales.

Almacenar datos estructurados en MongoDB.

Mantener actualización incremental sin duplicados.

Arquitectura del Pipeline
API Climática → Extracción → Transformación → Agregación Mensual → MongoDB
Fases del ETL
1. Extracción

Consumo de API climática mediante solicitudes HTTP.

Obtención de datos diarios por estado.

Manejo de errores en respuesta de API.

2. Transformación

Limpieza y validación de datos.

Conversión a DataFrame con Pandas.

Agregación mensual de métricas:

Temperatura máxima promedio

Temperatura mínima promedio

Temperatura media

Humedad relativa promedio

3. Carga

Inserción en MongoDB.

Actualización incremental mediante upsert.

Prevención de duplicados por estado y fecha.

Tecnologías Utilizadas

Python

Pandas — procesamiento y transformación de datos

MongoDB — almacenamiento NoSQL

Requests — consumo de API REST

python-dotenv — gestión de variables de entorno

Certifi — conexión segura TLS

Variables Climáticas Procesadas

Temperatura máxima

Temperatura mínima

Temperatura promedio

Humedad relativa promedio

Frecuencia final de almacenamiento: mensual por estado.

Estructura del Proyecto
.
├── etl_weather.py
├── .env
└── README.md
Configuración
1. Clonar repositorio
git clone <repo-url>
cd <repo>
2. Instalar dependencias
pip install pandas pymongo requests python-dotenv certifi
3. Configurar variables de entorno

Crear archivo .env:

MONGODB_URI=tu_uri_mongodb
DB_NAME=nombre_base_datos
COLLECTION_NAME=nombre_coleccion
Ejecución
python etl_weather.py

El script:

procesa datos de todos los estados de México

obtiene información desde 2020 hasta la fecha actual

actualiza registros automáticamente en MongoDB

Ejemplo de Documento en MongoDB
{
  "estado": "Guanajuato",
  "fecha": "2024-05",
  "temperatura_max_promedio": 29.3,
  "temperatura_min_promedio": 14.2,
  "temperatura_promedio": 21.7,
  "humedad_promedio": 65.1
}
Características Técnicas Destacadas

Pipeline ETL automatizado

Agregación temporal de datos climáticos

Actualización incremental de registros

Manejo de errores en consumo de API

Procesamiento de datos a escala nacional

Posibles Mejoras Futuras

Contenerización con Docker

Orquestación del pipeline (Airflow)

API de consulta de datos

Sistema de caché con Redis

Visualización interactiva de datos

Programación automática de ejecuciones

Autor

Cristian Jesús Silva Medel
