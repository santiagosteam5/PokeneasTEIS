from flask import Flask, render_template_string, jsonify
import random
from .pokeneas import pokeneas
from .utils import get_docker_id

def create_app():
    app = Flask(__name__)
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

    @app.route('/')
    def get_pokeneas():
        pokenea = random.choice(pokeneas)
        return jsonify({
            "id": pokenea["Id"],
            "nombre": pokenea["Nombre"],
            "altura": pokenea["Altura"],
            "habilidad": pokenea["Habilidad"],
            "contenedor": get_docker_id()
        })

    @app.route('/imagenes')
    def mostrar_imagenes():
        image_urls = []
        for obj in pokeneas:
            key = obj['Nombre'].lower().replace(" ", "_")
            url = f"https://s3bucketwhydoesmybucketneedtohaveanuniquename.s3.us-east-1.amazonaws.com/{key}.jpg"
            url = f"https://s3bucketwhydoesmybucketneedtohaveanuniquename.s3.us-east-1.amazonaws.com/sillemon.jpg"
            image_urls.append(url)

        picked_image = random.choice(image_urls) if image_urls else None

        #prints para debug

        print(f"Picked image: {picked_image}")

        picked_name = picked_image.split('/')[-1] if picked_image else None
        picked_name = picked_name.split('.')[0] if picked_name else None
        picked_name = picked_name.capitalize()

        print(f"Picked name: {picked_name}")

        picked_frase = next((p["Frase filosófica"] for p in pokeneas if p["Nombre"] == picked_name), None)

        print(f"Picked frase: {picked_frase}")

        #no puedo cargar las imagenes de manera local, por lo que voy a hacer el test desde aws ahora

        html = """
        <h1>Imágenes desde S3</h1>
            <div>
                <img src="{{ picked_image }}" style="max-width:300px;"><br>
                <small>{{ picked_image }}</small>
                <p><strong>Frase:</strong> {{ picked_frase }}</p>
            </div>
        """
        return render_template_string(html, picked_image=picked_image, picked_frase=picked_frase)

    return app