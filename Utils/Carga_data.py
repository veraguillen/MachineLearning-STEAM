import os
import pandas as pd

def cargar_datos_parquet(filepath):
    """
    Carga un archivo .parquet si existe, de lo contrario, muestra un mensaje de advertencia.
    """
    if os.path.exists(filepath):
        try:
            data = pd.read_parquet(filepath)
            print(f"Archivo {filepath} cargado con éxito.")
            return data
        except Exception as e:
            print(f"Error al cargar el archivo {filepath}: {e}")
    else:
        print(f"El archivo {filepath} no existe.")
    return None