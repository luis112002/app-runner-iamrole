from fastapi import FastAPI, HTTPException, Query
import boto3
import os

app = FastAPI()

# Cliente S3 usando el rol IAM (sin claves)
s3 = boto3.client("s3")

# Buckets de entrada y salida desde variables de entorno
BUCKET_IN = os.environ.get("BUCKET_IN")
BUCKET_OUT = os.environ.get("BUCKET_OUT")

@app.get("/")
def index():
    return {"mensaje": "API usando AWS SDK con IAM Role en App Runner"}

@app.get("/procesar-archivo")
def procesar_archivo(filename: str = Query(..., description="Nombre del archivo en BUCKET_IN")):
    try:
        # Leer archivo del bucket de entrada
        obj = s3.get_object(Bucket=BUCKET_IN, Key=filename)
        contenido = obj["Body"].read().decode("utf-8")

        # Procesamiento simple: convertir a mayúsculas
        contenido_procesado = contenido.upper()

        # Guardar archivo en el bucket de salida
        s3.put_object(
            Bucket=BUCKET_OUT,
            Key=f"procesado_{filename}",
            Body=contenido_procesado.encode("utf-8")
        )

        return {
            "mensaje": f"Archivo '{filename}' procesado y guardado como 'procesado_{filename}' en {BUCKET_OUT}"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
