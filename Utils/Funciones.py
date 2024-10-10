from Utils.Carga_data import cargar_datos_parquet
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


# Definir las rutas de los archivos .parquet
ruta_data_games = r'Datos_parquet/data_games.parquet'
ruta_data_review_user = r'Datos_parquet/data_review_user.parquet'
ruta_data_items = r'Datos_parquet/data_items.parquet'

# Cargar los archivos utilizando la función desde utils
df_games = cargar_datos_parquet(ruta_data_games)
df_reviews = cargar_datos_parquet(ruta_data_review_user)
df_items = cargar_datos_parquet(ruta_data_items)



def developer(desarrollador: str, df_games: pd.DataFrame):
    # Validar que df_games sea un DataFrame
    if not isinstance(df_games, pd.DataFrame):
        raise ValueError("El argumento df_games debe ser un DataFrame de pandas.")
    
    # Procesar el nombre del desarrollador
    desarrollador = desarrollador.lower().strip()
    
    # Verificar la existencia de la columna 'developer'
    if 'developer' not in df_games.columns:
        raise ValueError("El DataFrame no contiene la columna 'developer'.")

    # Filtrar los juegos del desarrollador
    juegos_filtrados = df_games[df_games['developer'].str.lower() == desarrollador]
    juegos_filtrados = juegos_filtrados.dropna(subset=['release_year', 'is_free'])

    # Manejo si no se encuentran juegos
    if juegos_filtrados.empty:
        return {desarrollador: "No se encontraron juegos para este desarrollador."}

    # Agrupar por año de lanzamiento
    agrupado_anio = juegos_filtrados.groupby('release_year').agg(
        total_items=('id', 'count'),
        total_free=('is_free', lambda x: (x == True).sum())
    )

    # Calcular porcentaje de contenido gratuito
    agrupado_anio['contenido_free'] = (agrupado_anio['total_free'] / agrupado_anio['total_items']) * 100
    agrupado_anio['contenido_free'] = agrupado_anio['contenido_free'].astype(float).astype(str) + '%'

    # Eliminar la columna total_free
    agrupado_anio = agrupado_anio.drop(columns=['total_free'])

    return agrupado_anio.reset_index()



class UserDataError(Exception):
    
    pass

def userdata(user_id: str, df_items: pd.DataFrame, df_reviews: pd.DataFrame, df_games: pd.DataFrame):
    # Validar que los DataFrames no estén vacíos
    for df, name in zip([df_items, df_reviews, df_games], ['df_items', 'df_reviews', 'df_games']):
        if df.empty:
            raise UserDataError(f"El DataFrame {name} está vacío.")
    
    # Filtrar los datos por el usuario dado
    items_usuario = df_items[df_items['user_id'] == user_id]
    reviews_usuario = df_reviews[df_reviews['user_id'] == user_id]
    
    # Comprobar si los datos de ítems están vacíos
    if items_usuario.empty:
        return {
            f"Usuario": user_id,
            'Dinero gastado': "$0.00",
            '% de recomendación': '0.00%',
            'cantidad de items': 0
        }

    # Comprobar si los datos de reseñas están vacíos
    if reviews_usuario.empty:
        pass  # Si no hay reseñas, se continúa sin hacer nada.

    # Combinar con el dataset de juegos para obtener precios
    items_con_precios = items_usuario.merge(df_games[['id', 'price', 'is_free']], left_on='item_id', right_on='id', how='left')
    
    # Verificar que el merge se hizo correctamente y hay datos
    if items_con_precios.empty:
        return {
            "Usuario": user_id,
            'Dinero gastado': "$0.00",
            '% de recomendación': '0.00%',
            'cantidad de items': 0
        }
    
    # Calcular el dinero gastado (solo ítems no gratuitos)
    dinero_gastado = items_con_precios[items_con_precios['is_free'] == False]['price'].sum()

    # Formatear el dinero gastado con el símbolo de dólar
    dinero_gastado_formateado = f"{dinero_gastado:,.2f} USD"

    # Calcular el total de ítems
    total_items = len(items_usuario)
    
    # Calcular el porcentaje de recomendación
    if len(reviews_usuario) > 0:
        porcentaje_recomendacion = (reviews_usuario['recommend'].sum() / len(reviews_usuario)) * 100
    else:
        porcentaje_recomendacion = 0  # Si no hay reseñas, el porcentaje es 0
    
    # Devolver los resultados en un diccionario con el nombre del usuario
    return {
        "Usuario": user_id,
        'Dinero gastado': dinero_gastado_formateado,
        'Porcentaje de recomendación': f"{porcentaje_recomendacion:.2f}%",
        'cantidad de items': total_items
    }




# Definir la función
def UserForGenre(genero: str, df_items: pd.DataFrame, df_games: pd.DataFrame):
    # Convertir a minúsculas para que la comparación no sea sensible a mayúsculas
    genero = genero.lower()
    
    # Filtrar juegos por el género dado
    juegos_genero = df_games[df_games['genre'].str.lower() == genero]
    
    # Unir los juegos filtrados con los ítems jugados por los usuarios (basado en item_id)
    juegos_con_horas = juegos_genero.merge(df_items, left_on='id', right_on='item_id', how='inner')
    
    # Verificar si hay datos después del merge
    if juegos_con_horas.empty:
        print(f"No se encontraron juegos para el género {genero}")
        return {f"Usuario con más horas jugadas para Género {genero}": None, 'Horas jugadas': []}

    # Validar que playtime_forever contenga solo valores numéricos
    juegos_con_horas = juegos_con_horas[pd.to_numeric(juegos_con_horas['playtime_forever'], errors='coerce').notna()]
    
    # Agrupar por usuario y sumar las horas jugadas
    horas_por_usuario = juegos_con_horas.groupby('user_id')['playtime_forever'].sum().reset_index()
    
    # Verificar si hay usuarios antes de proceder
    if horas_por_usuario.empty:
        print(f"No se encontraron horas jugadas válidas para el género {genero}")
        return {f"Usuario con más horas jugadas para Género {genero}": None, 'Horas jugadas': []}

    # Encontrar el usuario con más horas jugadas
    usuario_max_horas = horas_por_usuario.loc[horas_por_usuario['playtime_forever'].idxmax()]

    # Filtrar los juegos del usuario con más horas
    juegos_usuario = juegos_con_horas[juegos_con_horas['user_id'] == usuario_max_horas['user_id']]

    # Agrupar las horas jugadas por año de lanzamiento
    horas_por_año = juegos_usuario.groupby('release_year')['playtime_forever'].sum().reset_index()

    # Formatear la lista de acumulación por año
    acumulacion_por_año = [
        {"Año": int(row['release_year']), "Horas": int(row['playtime_forever'])}
        for _, row in horas_por_año.iterrows()
    ]

    # Devolver el usuario con más horas y las horas jugadas acumuladas por año
    return {
        f"Id del Usuario con más horas jugadas para el Género {genero}": usuario_max_horas['user_id'],
        'Horas jugadas': acumulacion_por_año
    }




# Definir la función
def best_developer_year(año: int, df_games: pd.DataFrame, df_reviews: pd.DataFrame):
    # Filtrar juegos para el año dado
    juegos_filtrados = df_games[df_games['release_year'] == año]
    
    # Si no hay juegos para el año dado
    if juegos_filtrados.empty:
        return {"Error": "No hay juegos lanzados en el año especificado."}

    # Obtener los item_ids de los juegos filtrados
    item_ids = juegos_filtrados['id'].tolist()

    # Filtrar reseñas que pertenecen a los juegos filtrados y que son recomendadas
    reseñas_filtradas = df_reviews[(df_reviews['item_id'].isin(item_ids)) & (df_reviews['recommend'] == True)]

    # Si no hay reseñas recomendadas para los juegos del año dado
    if reseñas_filtradas.empty:
        return {"Error": "No hay reseñas recomendadas para los juegos lanzados en el año especificado."}

    # Unir las reseñas con los juegos para obtener los desarrolladores
    reseñas_con_juegos = reseñas_filtradas.merge(df_games, left_on='item_id', right_on='id', how='inner')

    # Agrupar por desarrollador y contar la cantidad de reseñas recomendadas
    conteo_recomendaciones = reseñas_con_juegos.groupby('developer')['user_id'].count().reset_index(name='cantidad_recomendaciones')

    # Obtener el top 3 desarrolladores con más recomendaciones
    top_desarrolladores = conteo_recomendaciones.nlargest(3, 'cantidad_recomendaciones')

    # Convertir el resultado al formato requerido
    resultado = []
    for puesto, row in enumerate(top_desarrolladores.itertuples(), start=1):  # Enumerar desde 1
        resultado.append({
            f"Puesto {puesto}": {
                'Developer': row.developer,
                'Recomendaciones': row.cantidad_recomendaciones
            }
        })

    return resultado


def developer_reviews_analysis(desarrolladora: str, df_reviews: pd.DataFrame, df_games: pd.DataFrame):
    # Convertir a minúsculas para que la comparación no sea sensible a mayúsculas
    desarrolladora = desarrolladora.strip().lower()  # Eliminamos espacios extra también

    # Filtrar los juegos del desarrollador especificado
    juegos_desarrolladora = df_games[df_games['developer'].str.strip().str.lower() == desarrolladora]
    
    # Si no hay juegos para el desarrollador dado
    if juegos_desarrolladora.empty:
        return {desarrolladora: "No hay juegos lanzados por esta desarrolladora."}

    # Obtener los item_ids de los juegos filtrados
    item_ids = juegos_desarrolladora['id'].tolist()

    # Verificar si realmente se encontraron los juegos
    if not item_ids:
        return {desarrolladora: "No se encontraron juegos con un ID válido para esta desarrolladora."}

    # Filtrar reseñas que pertenecen a los juegos del desarrollador
    reseñas_filtradas = df_reviews[df_reviews['item_id'].isin(item_ids)]

    # Si no hay reseñas para los juegos de la desarrolladora
    if reseñas_filtradas.empty:
        return {desarrolladora: "No hay reseñas para los juegos de esta desarrolladora."}

    # Calcular el promedio de recomendaciones
    promedio_recomendaciones = reseñas_filtradas['recommend'].mean() * 100

    # Contar el número de reseñas
    total_reseñas = len(reseñas_filtradas)

    # Resultado final
    return {
        "Desarrolladora": desarrolladora,
        "Promedio de Recomendaciones": f"{promedio_recomendaciones:.2f}%",
        "Total de Reseñas": total_reseñas
    }




# Asumiendo que df_games es tu DataFrame cargado
# Verifica que la columna combined_features no tenga valores nulos
df_games = df_games.dropna(subset=['combined_features'])

# Inicializar el vectorizador y la matriz TF-IDF
vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = vectorizer.fit_transform(df_games['combined_features'])



def get_index_from_title(game_title, df_games):
    """
    Función para obtener el índice de un juego a partir de su título.
    """
    # Asegúrate de que el título esté en minúsculas y sin espacios extras
    game_title = game_title.lower().strip()
    
    # Buscar el índice del juego cuyo título coincide con game_title
    indices = df_games[df_games['app_name'].str.lower() == game_title].index
    
    # Verificar si hay coincidencias
    if not indices.empty:
        return indices[0]
    raise ValueError("Título no encontrado")

def get_recommendations(game_title, df_games):
    """
    Función para obtener recomendaciones basadas en la similitud del coseno.
    """
    try:
        # Obtener el índice del videojuego buscado por título
        idx = get_index_from_title(game_title, df_games)
        
        # Calcular la similitud del coseno
        cosine_sim = cosine_similarity(tfidf_matrix[idx], tfidf_matrix)
        
        # Enumerar los videojuegos y ordenarlos por similitud
        sim_scores = list(enumerate(cosine_sim[0]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Obtener los índices de los 5 videojuegos más similares
        game_indices = [i[0] for i in sim_scores[1:6]]
        
        # Devolver los nombres de los videojuegos recomendados
        return df_games['app_name'].iloc[game_indices].tolist()
    
    except ValueError:
        return ["No se encontró el videojuego en los datos"]

