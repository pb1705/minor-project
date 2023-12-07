from flask import Flask, request, jsonify, json,send_file
from flask_cors import CORS,cross_origin
import pandas as pd
import numpy as np
import pickle
import cv2
from io import BytesIO
# from bson import ObjectId
from tqdm import tqdm
# from PIL import Image

from skimage.feature import local_binary_pattern
import os



app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

count=0
classnames = ['ali', 'daksh', 'khan', 'prath', 'raj']
#load model pickel file
with open('.\model\model_saved.unknown', 'rb') as f:
    model = pickle.load(f)


def preprocess_images_single(images):
    preprocessed_images = []
    for image in tqdm(images):
        image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        image = cv2.resize(image, dsize=(150,150))


    return np.array(image)


def extract_lbp_single(image):
    lbp = local_binary_pattern(image, P=8, R=1)
    return lbp


def create_histogram_single(image, sub_images_num, bins_per_sub_images):
    grid = np.arange(0, image.shape[1]+1, image.shape[1]//sub_images_num)

    sub_image_histograms = []

    for i in range(1, len(grid)):
        for j in range(1, len(grid)):
            sub_image = image[grid[i-1]:grid[i], grid[j-1]:grid[j]]

            sub_image_histogram = np.histogram(sub_image, bins=bins_per_sub_images)[0]
            sub_image_histograms.append(sub_image_histogram)

    histogram = np.array(sub_image_histograms).flatten()

    return histogram




@app.route('/',  methods = ['GET', 'POST'])
def main():
    return "hi"

@app.route('/getClass', methods = ['POST'])
def getClass():

    global count
    # file = request.files['file']
    # file.save(".\\files\sample.jpg", "")
    cv_img = []
    # demo_image = cv2.imread(".\\files\sample.jpg")
           # Get the file from the request
    file = request.files['file']

        # Read the file content as bytes
    file_content = file.read()

        # Use BytesIO to create a file-like object from the bytes
    file_stream = BytesIO(file_content)

        # Use cv2.imdecode to decode the image from the file-like object
    demo_image = cv2.imdecode(np.frombuffer(file_stream.read(), np.uint8), 1)
    cv_img.append(demo_image)
    demo_image = preprocess_images_single(cv_img)
    demo_image_test_lbp = extract_lbp_single(demo_image)
    # print(demo_image_test_lbp)
    
    demo_image_test_hist = create_histogram_single(demo_image_test_lbp, sub_images_num=3, bins_per_sub_images=64)
    
    demo_image_test_hist_reshaped = demo_image_test_hist.reshape(1,-1)
    count+=1
    prediction = model.predict(demo_image_test_hist_reshaped)
    cv2.imwrite('./files/saved'+str(count)+".jpg", demo_image_test_lbp)
    response_data = {
        'class': classnames[prediction[0]],
        'count': count
    }

    return jsonify(response_data)
    

    # return "skndvnjsvn"

    
@app.route('/get_processed_image', methods=['GET','POST'])

def get_processed_image():
    try:
        if request.method == 'POST':
            # For POST request, get the filename from the request
            filename = request.form['filename']
        elif request.method == 'GET':
            # For GET request, get the filename from the URL
            filename = request.args.get('filename')
        else:
            return jsonify({'error': 'Invalid request method'})

        # Use the filename to construct the file path
        

        # Send the processed image as a response
        return send_file("./files/saved"+filename+".jpg", mimetype='image/jpeg')

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__=='__main__':  
    app.run(debug=True, port ='5000')