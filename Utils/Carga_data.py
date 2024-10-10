import pandas as pd
import os

def cargar_data1():
    ruta = r"C:\Users\veram\OneDrive\Escritorio\proyecto octubre\Datos parquet\data_games.parquet"
    return cargar_datos(ruta)

def cargar_data2():
    ruta = r"C:\Users\veram\OneDrive\Escritorio\proyecto octubre\Datos parquet\data_review_user.parquet"
    return cargar_datos(ruta)

def cargar_data3():
    ruta = r"C:\Users\veram\OneDrive\Escritorio\proyecto octubre\Datos parquet\data_items.parquet"
    return cargar_datos(ruta)

def cargar_datos(ruta):
    """Función auxiliar para cargar archivos parquet y manejar errores."""
    if os.path.exists(ruta):
        try:
            df = pd.read_parquet(ruta)
            return df
        except Exception as e:
            print(f"Error al cargar {ruta}: {e}")
            return None
    else:
        print(f"El archivo {ruta} no existe.")
        return None