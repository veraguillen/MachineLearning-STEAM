# Sistema de Recomendación de Videojuegos/ #steam/ # HENRY


### Tabla de Contenidos

- [Descripción](#descripción)
- [Funcionalidades](#funcionalidades)
- [Tecnologías Utilizadas](#tecnologías-utilizadas)
- [Instalación](#instalación)
- [Uso de la Aplicación](#uso-de-la-aplicación)
- [Análisis Exploratorio de Datos (EDA)](#análisis-exploratorio-de-datos-eda)
- [Desarrollo de la API](#desarrollo-de-la-api)
  - [Endpoints](#endpoints)
- [Modelo de Machine Learning](#modelo-de-machine-learning)
- [Despliegue](#despliegue)
- [Contribuciones](#contribuciones)


## Descripción

Este sistema de recomendación utiliza técnicas de aprendizaje automático para sugerir videojuegos similares a los que ya te gustan. Basado en un modelo de similitud del coseno que analiza características como género y descripciones, ofrece una lista personalizada de títulos que podrían interesarte. ¡Descubre nuevos juegos y explora el mundo del entretenimiento digital de manera más inteligente! 🎮✨

### Funcionalidades

- **Recomendación de Juegos:** Basada en la similitud del coseno.
- **Análisis de Sentimiento:** Procesa reseñas de usuarios para mejorar las recomendaciones.
- **API Rápida:** Desarrollada con FastAPI para proporcionar un servicio eficiente.
- **Despliegue en Docker:** Incluye un Dockerfile para facilitar el despliegue en cualquier entorno compatible.

### Tecnologías Utilizadas

- **Backend:** [FastAPI](https://fastapi.tiangolo.com/)
- **Machine Learning:** [scikit-learn](https://scikit-learn.org/)
- **Análisis de Sentimiento:** [nltk](https://www.nltk.org/)
- **Docker:** [Docker](https://www.docker.com/)

## Instalación

Sigue estos pasos para instalar y configurar el proyecto en tu máquina local:

1. **Clona el Repositorio:**
    ```bash
    git clone https://github.com/veraguillen/Proyecto-Machine.git
    ```

2. **Navega al Directorio del Proyecto:**
    ```bash
    cd tu_repositorio
    ```

3. **Crea y Activa un Entorno Virtual:**
    ```bash
    python -m venv venv
    venv\Scripts\activate  # Windows
    # o
    source venv/bin/activate  # macOS/Linux
    ```

4. **Instala las Dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

5. **Configura los Datos:** Asegúrate de que la configuración esté correcta en el archivo correspondiente.

6. **Ejecuta la Aplicación:**
    ```bash
    uvicorn main:app --reload
    ```

### Uso de la Aplicación

Accede a [http://localhost:8000/docs](http://localhost:8000/docs) para la documentación interactiva de la API. 🖥️

### Análisis Exploratorio de Datos (EDA)

Cuenta con un EDA para entender mejor la distribución y relaciones en el dataset, que incluye:

- Visualizaciones de la distribución de géneros.
- Análisis de la cantidad de reseñas y su correlación con las calificaciones.
- Identificación de patrones para el desarrollo del modelo.

### Desarrollo de la API

La API, esta desarrollada con FastAPI, y permiten realizar diversas consultas sobre los datos.  

#### EJEMPLO:

1. **Cantidad de Items y Contenido Free por Año según Desarrolladora**
   - **Método:** `GET`
   - **Ruta:** `/developer`
   - **Parámetros:** `desarrollador`
   - **Ejemplo de retorno:**
     ```json
     {
       "Año": 2023,
       "Cantidad de Items": 50,
       "Contenido Free": "27%"
     }
     ```

## Modelo de Machine Learning

Se implementa un modelo de recomendación utilizando **similitud del coseno**, midiendo cuán similares son las características de los videojuegos. El modelo toma como entrada el nombre de un videojuego y devuelve una lista de 5 recomendaciones similares.

### Entrenamiento del Modelo

Se entrenó con un conjunto de datos que incluye:

- ***Género:*** Categorías de cada videojuego.
- **Price:** precio de cada videojuego.
- **Specs:** Especificaciones de los videojuegos.

Los datos son preprocesados para crear un **vector de características** que se utiliza para calcular la similitud.

### Uso en la API

La funcionalidad de recomendación se implementa a través de un endpoint que permite a los usuarios ingresar el nombre de un videojuego, respondiendo con cinco juegos recomendados.



### Despliegue

El proyecto está configurado para ser desplegado en **Render** utilizando un contenedor de **Docker**. Asegúrate de tener Docker instalado y configurado en tu entorno. 


### Contribuciones:
Si deseas contribuir a este proyecto, siéntete libre de hacer un fork y enviar un pull request.


### Autores
Vera Guillén - Contacto: LinkedIn.