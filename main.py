from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from Utils.Funciones import (
    procesar_datos,
    developer,
    userdata,
    UserForGenre,
    best_developer_year,
    developer_reviews_analysis,
    get_recommendations
)
from Utils.Funciones import df_games, df_reviews, df_items
from Utils.Modelos import UserDataQuery, GenreQuery, YearQuery, GameRequest
from typing import List, Dict

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

# Cargar los datasets
#df_games = cargar_data1()
#df_reviews = cargar_data2()
#df_items = cargar_data3()

# Verifica que los DataFrames se hayan cargado correctamente
if df_games is None or df_reviews is None or df_items is None:
    raise RuntimeError("Error al cargar los datos, asegúrate de que los archivos existan y sean accesibles.")

class DeveloperQuery(BaseModel):
    desarrollador: str

@app.get("/developer/", response_model=List[Dict])
async def get_developer_info(desarrollador: str):  
    try:
        resultado = developer(desarrollador, df_games)
        if resultado.empty:
            raise HTTPException(status_code=404, detail="Desarrollador no encontrado o sin datos disponibles.")
        
        return resultado.to_dict(orient='records')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/userdata/", response_model=dict)
async def get_user_data(user_id: str):  
    try:
        user_data = userdata(user_id, df_items, df_reviews, df_games)
        if user_data['cantidad de items'] == 0:
            raise HTTPException(status_code=404, detail=f"No se encontraron datos para el usuario {user_id}")
        return user_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/user-for-genre/", response_model=dict)
async def get_user_for_genre(genero: str):  
    try:
        user_genre_data = UserForGenre(genero, df_items, df_games)
        if user_genre_data['Id del Usuario con más horas jugadas para el Género ' + genero] is None:
            raise HTTPException(status_code=404, detail=f"No se encontraron juegos para el género {genero}")
        return user_genre_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/best-developer-year/", response_model=list)
async def get_best_developer_year(año: int):  
    try:
        top_developers = best_developer_year(año, df_games, df_reviews)
        if isinstance(top_developers, dict) and "Error" in top_developers:
            raise HTTPException(status_code=404, detail=top_developers["Error"])
        return top_developers
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/developer-reviews-analysis/", response_model=dict)
async def get_developer_reviews_analysis(desarrollador: str):  
    try:
        result = developer_reviews_analysis(desarrollador, df_reviews, df_games)
        if isinstance(result, dict) and "No hay juegos disponibles para este desarrollador." in result.values():
            raise HTTPException(status_code=404, detail=result[desarrollador])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/recommendations")
async def recommend_games_get(game_title: str):
    if not game_title:
        raise HTTPException(status_code=400, detail="El título del videojuego es requerido.")

    try:
        recommendations = get_recommendations(game_title, df_games)
        if not recommendations:
            raise HTTPException(status_code=404, detail="No se encontraron recomendaciones.")
        
        return {"game_title": game_title, "recommendations": recommendations}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.post("/recommendations")
async def recommend_games_post(game_request: GameRequest):
    game_title = game_request.game_title
    if not game_title:
        raise HTTPException(status_code=400, detail="El título del videojuego es requerido.")

    try:
        recommendations = get_recommendations(game_title, df_games)
        if not recommendations:
            raise HTTPException(status_code=404, detail="No se encontraron recomendaciones.")
        
        return {"game_title": game_title, "recommendations": recommendations}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

if __name__ == "__main__":
    procesar_datos()  # Puedes mantener esto si es necesario

    # Iniciar la aplicación en el puerto 8000
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
