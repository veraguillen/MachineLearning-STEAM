from pydantic import BaseModel

class DeveloperQuery(BaseModel):
    desarrollador: str  


class UserDataQuery(BaseModel):
    user_id: str


class GenreQuery(BaseModel):
    genero: str


class YearQuery(BaseModel):
    año: int


class GameRequest(BaseModel):
    game_title: str