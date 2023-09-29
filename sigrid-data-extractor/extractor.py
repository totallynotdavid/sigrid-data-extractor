import json
import requests
import pandas as pd

# Constantes y variables globales
BASE_URL = "https://sigrid.cenepred.gob.pe/arcgis/rest/services/Cartografia_Peligros/MapServer/5020100/query"
FILE_NAME_CSV = "output.csv"
FILE_NAME_EXCEL = "output.xlsx"

def build_url(params):
    """
    Construye la URL completa para realizar la solicitud al API.

    :param params: Parámetros para incluir en la URL.
    :return: URL completa.
    """
    geometry = params.pop("geometry", None)
    url = BASE_URL + "?" + "&".join(f"{key}={value}" for key, value in params.items())
    if geometry:
        url += "&geometry=" + json.dumps(geometry)
    return url

def fetch_data(url):
    """
    Obtiene los datos de la URL dada.

    :param url: URL de la cual obtener los datos.
    :return: Datos obtenidos.
    """
    response = requests.get(url)
    data = response.json()
    return data["features"]

def process_data(data):
    """
    Procesa los datos obtenidos.

    :param data: Datos brutos a procesar.
    :return: Datos procesados.
    """
    processed_data = []
    for feature in data:
        processed_data.append(feature["attributes"])
    return processed_data

def save_to_csv(data, file_name):
    """
    Guarda los datos dados en un archivo CSV.

    :param data: Datos a guardar.
    :param file_name: Nombre del archivo donde guardar los datos.
    """
    df = pd.DataFrame(data)
    df.to_csv(file_name, index=False, encoding="utf-8")

def save_to_excel(data, file_name):
    """
    Guarda los datos dados en un archivo Excel.

    :param data: Datos a guardar.
    :param file_name: Nombre del archivo donde guardar los datos.
    """
    df = pd.DataFrame(data)
    df.to_excel(file_name, index=False, engine='openpyxl')

def main():
    params = {
        "f": "json",
        "where": "1%3D1",
        "returnGeometry": "true",
        "spatialRel": "esriSpatialRelIntersects",
        "geometryType": "esriGeometryPolygon",
        "inSR": "102100",
        "outFields": "*",
        "outSR": "102100",
        "geometry": {
            "rings": [[
                [-8974049.114116076, -2211885.176650285],
                [-8974049.114116076, 128922.37755433063],
                [-7721704.842692081, 128922.37755433063],
                [-7721704.842692081, -2211885.176650285],
                [-8974049.114116076, -2211885.176650285]
            ]],
            "spatialReference": {"wkid": 102100}
        }
    }
    
    # Construir URL para obtener datos
    url = build_url(params)
    data = fetch_data(url)

    # Procesar los datos obtenidos
    processed_data = process_data(data)

    save_to_csv(processed_data, FILE_NAME_CSV)
    save_to_excel(processed_data, FILE_NAME_EXCEL)

    print(f"Datos guardados en {FILE_NAME_CSV} y {FILE_NAME_EXCEL}.")

if __name__ == "__main__":
    main()
