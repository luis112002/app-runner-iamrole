from fastapi import FastAPI
import boto3
import os

app = FastAPI()

BUCKET_NAME = "app-runner-entrada-luis"
ENTRADA = "entrada/mensaje.txt"
SALIDA = "salida/resultado.txt"

@app.get("/")
def procesar_archivo():
    s3 = boto3.client("s3")

    try:
        # Leer el archivo de entrada
        obj = s3.get_object(Bucket=BUCKET_NAME, Key=ENTRADA)
        contenido = obj["Body"].read().decode("utf-8")

        # Modificar el contenido
        nuevo_contenido = f"{contenido}\nProcesado correctamente por FastAPI."

        # Subir el nuevo archivo
        s3.put_object(Bucket=BUCKET_NAME, Key=SALIDA, Body=nuevo_contenido.encode("utf-8"))

        return {"mensaje": "Archivo procesado con éxito", "contenido_original": contenido}
    except Exception as e:
        return {"error": str(e)}

