# from fastapi import FastAPI
# import boto3

# app = FastAPI()
# s3 = boto3.client('s3')
# bucket = "app-runner-entrada-luis"

# @app.get("/")
# def read_file():
#     input_key = "entrada/mensaje.txt"
#     output_key = "salida/resultado.txt"

#     # Obtener contenido
#     response = s3.get_object(Bucket=bucket, Key=input_key)
#     content = response['Body'].read().decode('utf-8')

#     # Crear salida
#     resultado = content + "\nProcesado correctamente por FastAPI."
#     s3.put_object(Bucket=bucket, Key=output_key, Body=resultado)

#     return {"message": "¡Procesado con éxito!"}


from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import boto3

app = FastAPI()
s3 = boto3.client('s3')
bucket = "app-runner-entrada-luis"
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def read_file(request: Request):
    input_key = "entrada/mensaje.txt"
    output_key = "salida/resultado.txt"

    # Leer contenido del archivo
    response = s3.get_object(Bucket=bucket, Key=input_key)
    content = response['Body'].read().decode('utf-8')

    # Procesar: convertir a mayúsculas y añadir mensaje
    resultado = content.upper() + "\nPROCESADO CORRECTAMENTE POR FASTAPI."

    # Guardar en carpeta de salida
    s3.put_object(Bucket=bucket, Key=output_key, Body=resultado)

    # URL pública del archivo
    s3_url = f"https://{bucket}.s3.us-east-2.amazonaws.com/{output_key}"

    # Renderizar la plantilla
    return templates.TemplateResponse("resultado.html", {"request": request, "s3_url": s3_url})
