from tensorflow.keras.models import load_model
import os, io,  numpy as np, requests
from PIL import Image

os.environ["TF_ENABLE_ONEDNN_OPTS"] = '0'
os.environ["TF_CPP_MIN_LOG_LEVEL"] = '2'

kelas = {'hazard': 0,
        'kaca': 1,
        'kardus': 2,
        'kertas': 3,
        'logam': 4,
        'organic': 5,
        'plastik': 6,
        'recyclabe': 7,
        'residu': 8}

model = load_model("models/model_ep_33_vacc_0.8826530575752258.keras")

def process_image(image):
    image = image.resize((224, 224))
    image_array = np.array(image) / 255.0
    image_array = np.expand_dims(image_array, axis=0)
    # Perform prediction using the loaded model
    # return classes
    return image_array

file = Image.open("img\kertas.jpg")
# array_image = process_image(file)
# history = model.predict(array_image)
print(file)

