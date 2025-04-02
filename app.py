from fastapi import FastAPI
import boto3

app = FastAPI()
s3 = boto3.client('s3')
bucket = "app-runner-entrada-luis"

@app.get("/")
def read_file():
    input_key = "entrada/mensaje.txt"
    output_key = "salida/resultado.txt"

    # Obtener contenido
    response = s3.get_object(Bucket=bucket, Key=input_key)
    content = response['Body'].read().decode('utf-8')

    # Crear salida
    resultado = content + "\nProcesado correctamente por FastAPI."
    s3.put_object(Bucket=bucket, Key=output_key, Body=resultado)

    return {"message": "¡Procesado con éxito!"}
