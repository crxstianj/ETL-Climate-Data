import os
import requests
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
import pandas as pd
import certifi

# Cargar variables de entorno
load_dotenv()

estados_mexico = [
    {"nombre": "Aguascalientes", "lat": 21.8823, "lon": -102.2826},
    {"nombre": "Baja California", "lat": 32.6545, "lon": -115.4670},
    {"nombre": "Baja California Sur", "lat": 24.1426, "lon": -110.3128},
    {"nombre": "Campeche", "lat": 19.8301, "lon": -90.5349},
    {"nombre": "Chiapas", "lat": 16.7538, "lon": -93.1162},
    {"nombre": "Chihuahua", "lat": 28.6353, "lon": -106.0889},
    {"nombre": "Coahuila", "lat": 25.4383, "lon": -101.0000},
    {"nombre": "Colima", "lat": 19.2452, "lon": -103.7241},
    {"nombre": "Durango", "lat": 24.0277, "lon": -104.6532},
    {"nombre": "Guanajuato", "lat": 21.0181, "lon": -101.2591},
    {"nombre": "Guerrero", "lat": 17.5514, "lon": -99.5058},
    {"nombre": "Hidalgo", "lat": 20.0911, "lon": -98.7624},
    {"nombre": "Jalisco", "lat": 20.6597, "lon": -103.3496},
    {"nombre": "México", "lat": 19.2826, "lon": -99.6557},
    {"nombre": "Michoacán", "lat": 19.7039, "lon": -101.1925},
    {"nombre": "Morelos", "lat": 18.6813, "lon": -99.1013},
    {"nombre": "Nayarit", "lat": 21.7514, "lon": -104.8455},
    {"nombre": "Nuevo León", "lat": 25.5922, "lon": -99.9962},
    {"nombre": "Oaxaca", "lat": 17.0732, "lon": -96.7266},
    {"nombre": "Puebla", "lat": 19.0414, "lon": -98.2063},
    {"nombre": "Querétaro", "lat": 20.5888, "lon": -100.3899},
    {"nombre": "Quintana Roo", "lat": 18.5036, "lon": -88.3050},
    {"nombre": "San Luis Potosí", "lat": 22.1510, "lon": -100.9740},
    {"nombre": "Sinaloa", "lat": 24.8074, "lon": -107.3940},
    {"nombre": "Sonora", "lat": 29.0729, "lon": -110.9559},
    {"nombre": "Tabasco", "lat": 17.8409, "lon": -92.6189},
    {"nombre": "Tamaulipas", "lat": 24.2669, "lon": -98.8363},
    {"nombre": "Tlaxcala", "lat": 19.3182, "lon": -98.2375},
    {"nombre": "Veracruz", "lat": 19.1738, "lon": -96.1342},
    {"nombre": "Yucatán", "lat": 20.7099, "lon": -89.0943},
    {"nombre": "Zacatecas", "lat": 22.7709, "lon": -102.5832}
]


def extract_weather_data(lat, lon, start_date, end_date):
    url = "https://climate-api.open-meteo.com/v1/climate"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "models": "CMCC_CM2_VHR4",
        "daily": ["temperature_2m_max", "temperature_2m_min", "temperature_2m_mean", "relative_humidity_2m_mean"],
        "timezone": "America/Mexico_City"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error en la API: {response.status_code}, Respuesta: {response.text}")


# Transformacion
def transform_data(raw_data, estado):
    daily_data = raw_data.get("daily", {})
    required_keys = ["time", "temperature_2m_max", "temperature_2m_min",
                     "temperature_2m_mean", "relative_humidity_2m_mean"]
    for key in required_keys:
        if key not in daily_data:
            raise ValueError(f"Falta la clave en la respuesta de la API: {key}")
    df = pd.DataFrame({
        "fecha": daily_data["time"],
        "temperatura_max": daily_data["temperature_2m_max"],
        "temperatura_min": daily_data["temperature_2m_min"],
        "temperatura_promedio": daily_data["temperature_2m_mean"],
        "humedad": daily_data["relative_humidity_2m_mean"]
    })
    df["fecha"] = pd.to_datetime(df["fecha"])
    df_mensual = df.resample('ME', on='fecha').mean().reset_index()

    transformed = []
    for _, row in df_mensual.iterrows():
        record = {
            "fecha": row["fecha"].strftime("%Y-%m"),
            "estado": estado,
            "temperatura_max_promedio": row["temperatura_max"],
            "temperatura_min_promedio": row["temperatura_min"],
            "temperatura_promedio": row["temperatura_promedio"],
            "humedad_promedio": row["humedad"]
        }
        transformed.append(record)
    return transformed


# Carga
def load_to_mongodb(data):
    client = MongoClient(os.getenv("MONGODB_URI"), tlsCAFile=certifi.where())
    db = client[os.getenv("DB_NAME")]
    collection = db[os.getenv("COLLECTION_NAME")]
    for record in data:
        collection.update_one(
            {"estado": record["estado"], "fecha": record["fecha"]},
            {"$set": record},
            upsert=True
        )
    print(f"{len(data)} registros insertados o actualizados")
    client.close()


if __name__ == "__main__":
    start_date = "2020-01-01"
    end_date = datetime.today().strftime("%Y-%m-%d")

    for estado in estados_mexico:
        try:
            raw_data = extract_weather_data(estado["lat"], estado["lon"], start_date, end_date)
            clean_data = transform_data(raw_data, estado["nombre"])
            load_to_mongodb(clean_data)
            print(f"Datos de {estado['nombre']} cargados correctamente.")
        except Exception as e:
            print(f"Error con {estado['nombre']}: {str(e)}")
