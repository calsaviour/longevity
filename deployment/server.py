from flask import Flask, request
import torch
import torchvision.transforms as transforms
from PIL import Image
import io

from longevity.modelling.model import preprocess

app = Flask(__name__)

model = torch.load('model.pt')
model.eval()


@app.route('/predict', methods=['POST'])
def predict():
    image = request.files['file']  # get the image
    image = Image.open(io.BytesIO(image.read()))
    image = preprocess(image)  # apply the transformations

    # add an extra dimension and send the image through the model
    output = model(image.unsqueeze(0)) 
    _, predicted = torch.max(output, 1)

    # return the predicted class
    return {'prediction': predicted.item()}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

