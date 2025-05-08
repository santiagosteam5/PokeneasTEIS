from flask import Flask, render_template_string, jsonify
import os
import random
from pokeneas import pokeneas
from .utils import get_docker_id

app = Flask(__name__)

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)

S3_BUCKET = os.getenv("S3_BUCKET")

@app.route('/')
def get_pokeneas():
    pokenea = random.choice(pokenea)
    return jsonify({
        "id": pokenea["Id"],
        "nombre": pokenea["Nombre"],
        "altura": pokenea["Altura"],
        "habilidad": pokenea["Habilidad"],
        "contenedor": get_docker_id()
    })

@app.route('/imagenes')
def mostrar_imagenes():
    objects = s3.list_objects_v2(Bucket=S3_BUCKET)

    image_urls = []
    for obj in objects.get('Contents', []):
        key = obj['Key']
        url = f"https://{S3_BUCKET}.s3.amazonaws.com/{key}"
        image_urls.append(url)

    picked_image = random.choice(image_urls) if image_urls else None

    html = """
    <h1>Imágenes desde S3</h1>
        <div>
            <img src="{{ picked_image }}" style="max-width:300px;"><br>
            <small>{{ picked_image }}</small>
        </div>
    """
    return render_template_string(html, image_urls=image_urls)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
