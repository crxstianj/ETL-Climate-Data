# ETL de Datos Climáticos de México

Pipeline ETL en Python para extraer, transformar y almacenar datos climáticos históricos de los estados de México utilizando una API externa (open meteo) y MongoDB.

## Descripción

Este proyecto implementa un proceso de **Extracción, Transformación y Carga (ETL)** que obtiene datos climáticos diarios desde una API, los procesa para generar métricas mensuales agregadas y los almacena en MongoDB para su análisis posterior.

El script procesa información climática de los estados de México desde 2020 hasta la fecha actual, manteniendo los registros actualizados sin duplicados.

---

## Flujo del Pipeline


API climática → Extracción → Transformación → Agregación mensual → MongoDB


### Extracción
- Consumo de API mediante solicitudes HTTP.

### Transformación
- Limpieza y validación de datos.
- Conversión temporal.

### Carga
- Inserción y actualización de datos en MongoDB.
- Manejo para evitar duplicados.


---

## Tecnologías utilizadas

- Python
- Pandas
- MongoDB
- Requests (API REST)
- python-dotenv
- Certifi

---

## Estructura del proyecto

```
.
├── etl_weather.py
├── .env
└── README.md
```

> Nota: Asegúrate de configurar el archivo `.env` con tus credenciales antes de ejecutar el proyecto.

---

## Instalación

### 1. Clonar repositorio

```
git clone <repo-url>
cd <repo>
```

### 2. Instalar dependencias

```
pip install pandas pymongo requests python-dotenv certifi
```

### 3. Configurar variables de entorno

Crear archivo `.env` con:

```
MONGODB_URI=tu_uri_mongodb
DB_NAME=nombre_base_datos
COLLECTION_NAME=nombre_coleccion
```

## Uso

Ejecutar el script:

```
python ETL.py
```

El programa:

- obtiene datos desde 2020 hasta la fecha actual
- procesa información de todos los estados de México
- actualiza registros automáticamente en MongoDB

## Ejemplo de registro almacenado

```json
{
  "estado": "Guanajuato",
  "fecha": "2024-05",
  "temperatura_max_promedio": 29.3,
  "temperatura_min_promedio": 14.2,
  "temperatura_promedio": 21.7,
  "humedad_promedio": 65.1
}
```

Autor  
Cristian Jesús Silva Medel
