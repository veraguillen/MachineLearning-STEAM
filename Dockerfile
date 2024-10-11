#imagen base de Python
FROM python:3.12-slim

#Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

#Copiamos los archivos necesarios al contenedor
COPY ./main.py /app
COPY ./Utils /app/Utils
COPY ./Datos_parquet /app/Datos_parquet

#Instalamos las dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#Exponemos el puerto 8000 para FastAPI
EXPOSE 8000

#Comando para ejecutar la aplicación
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]




