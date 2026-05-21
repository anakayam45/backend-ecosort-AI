from tensorflow.keras.models import load_model
import os, io,  numpy as np, requests
from PIL import Image

os.environ["TF_ENABLE_ONEDNN_OPTS"] = '0'
os.environ["TF_CPP_MIN_LOG_LEVEL"] = '2'

kelas = { 0: 'hazard',
         1: 'kaca',
         2: 'kardus',
         3: 'kertas',
         4: 'logam',
         5: 'organic',
         6: 'plastik',
         7: 'recyclabe',
         8: 'residu'}

model = load_model("models/model_ep_33_vacc_0.8826530575752258.keras")

def process_image(image):
    image = image.resize((224, 224))
    image_array = np.array(image) / 255.0
    image_array = np.expand_dims(image_array, axis=0)
    # Perform prediction using the loaded model
    # return classes
    return image_array

file = Image.open("img/residu.jpg")

array_image = process_image(file)
history = model.predict(array_image)
print(kelas[history.argmax()-1])