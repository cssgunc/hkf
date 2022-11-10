from flask import Flask, request, Response,send_file
import numpy as np
from flask_cors import CORS
import base64
import cv2
from PIL import Image
from matplotlib import pyplot
from matplotlib.patches import Rectangle
from mtcnn.mtcnn import MTCNN

app = Flask(__name__)
CORS(app)


@app.route('/upload', methods=['POST'])
def fileUpload():
    processedImage = request.files['image'].read()

    return "Hello World"

if __name__ == '__main__':
    app.run()
