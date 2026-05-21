import os, io,  numpy as np, requests
import threading
from flask import Flask, request, jsonify, render_template
from PIL import Image
from tensorflow.keras.models import load_model

os.environ["TF_ENABLE_ONEDNN_OPTS"] = '0'
os.environ["TF_CPP_MIN_LOG_LEVEL"] = '2'

model = None

kelas = { 0: 'hazard',
         1: 'kaca',
         2: 'kardus',
         3: 'kertas',
         4: 'logam',
         5: 'organic',
         6: 'plastik',
         7: 'recyclabe',
         8: 'residu'}

try:
    model = load_model('models/model_ep_33_vacc_0.8826530575752258.keras')
    print("===== Model loaded successfully =====")
except Exception as e:
    print(f"===== Error loading model =====")
    print(str(e))


def process_image(image):
    image = image.resize((224, 224))
    image_array = np.array(image) / 255.0
    image_array = np.expand_dims(image_array, axis=0)
    # Perform prediction using the loaded model
    # return classes
    return image_array


app = Flask(__name__)
model_locked = threading.Lock()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/ambil_data', methods=['GET'])
def hello():
    return jsonify({'message': 'id_proses, waktu, tipesampah, akurasi'})

@app.route('/predict_url', methods=['POST'])
def predict_url():
    process_id = request.form.get('process_id')
    image_url = request.form.get('image_url')
    if not process_id or not image_url:
        return jsonify({'error': 'Missing process_id or image_url'}), 400
    
    try:
        with model_locked:
            response = requests.get(image_url)
            response.raise_for_status()
            image = Image.open(io.BytesIO(response.content))
            image_array = process_image(image)
            history = model.predict(image_array)
        return jsonify({'classes': kelas[history.argmax()-1], 'process_id': process_id}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/predict_image', methods=['POST'])
def predict_image():
    process_id = request.form.get('process_id')

    # if request.content_type not in ['image/jpeg', 'image/png', 'image/jpg']:
    #     return jsonify({'error': 'Invalid file type'}), 400 // error handling for file type, but currently not working, need to be fixed later

    file = request.files['file']

    if not process_id or not file:
        return jsonify({'error': 'Missing process_id or file'}), 400
    
    try:
        with model_locked:
            image_bytes = file.read()
            image = Image.open(io.BytesIO(image_bytes))
            image_array = process_image(image)
            history = model.predict(image_array)
        return jsonify({'classes': kelas[history.argmax()-1], 'process_id': process_id}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

# how to run:
# run this comand: uvicorn app:app --reload