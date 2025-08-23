import tensorflow as tf
import os
import numpy as np
from django.conf import settings
from tensorflow.keras.preprocessing import image

# Path to the saved CNN model
MODEL_PATH = os.path.join(settings.BASE_DIR, "ML_model", "milk_quality_classifier", "milk_quality_classifier.keras")

# Load once at startup
milk_model = tf.keras.models.load_model(MODEL_PATH)

CLASSES = ["blue good", "pink moderate", "cream spoil"]

def predict_milk_quality(img_path):
    img = image.load_img(img_path, target_size=(128, 128))
    img_array = image.img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    predictions = milk_model.predict(img_array)
    class_index = np.argmax(predictions[0])
    return CLASSES[class_index]
