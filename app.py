import os, io,  numpy as np, requests
from flask import Flask, request, jsonify, render_template
from PIL import Image
from tensorflow.keras.models import load_model

status = "stuck"

try:
    model = load_model('model.h5')
    status = "ready"
except Exception as e:
    print(f"Error loading model: {e}")
    status = "error"


def process_image(image):
    image = image.resize((224, 224))
    image_array = np.array(image) / 255.0
    image_array = np.expand_dims(image_array, axis=0)
    # Perform prediction using the loaded model
    # return classes
    return None


app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/predict_url', methods=['POST'])
def predict_url():
    process_id = request.form.get('process_id')
    image_url = request.form.get('image_url')
    if not process_id or not image_url:
        return jsonify({'error': 'Missing process_id or image_url'}), 400
    
    try:
        response = requests.get(image_url)
        response.raise_for_status()
        image = Image.open(io.BytesIO(response.content))
        image_array = process_image(image)
        return jsonify({'message': 'Image processed successfully', 'process_id': process_id}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predict_image', methods=['POST'])
def predict_image():
    process_id = request.form.get('process_id')

    if request.content_type not in ['image/jpeg', 'image/png', 'image/jpg']:
        return jsonify({'error': 'Invalid file type'}), 400

    file = request.files['file']

    if not process_id or not file:
        return jsonify({'error': 'Missing process_id or file'}), 400
    
    try:
        image_bytes = file.read()
        image = Image.open(io.BytesIO(image_bytes))
        image_array = process_image(image)
        return jsonify({'message': 'Image processed successfully', 'process_id': process_id}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
