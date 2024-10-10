from pydantic import BaseModel

class DeveloperQuery(BaseModel):
    desarrollador: str  # Mantener el nombre correcto de la propiedad


class UserDataQuery(BaseModel):
    user_id: str


class GenreQuery(BaseModel):
    genero: str


class YearQuery(BaseModel):
    año: int



# Clase para recibir el cuerpo de la solicitud POST
class GameRequest(BaseModel):
    game_title: str