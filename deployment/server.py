from flask import Flask, request
import torch
import torchvision.transforms as transforms
from PIL import Image
import io

from longevity.modelling.model import preprocess

app = Flask(__name__)

model = torch.load('longevity/deployments/model.pt')
model.eval()

@app.route('/predict', methods=['POST'])
def predict():
    image = request.files['file']
    age = float(request.form.get('age'))

    image = Image.open(io.BytesIO(image.read()))
    image = preprocess(image)

    age_tensor = torch.tensor([age]).unsqueeze(0)
    output = model(image.unsqueeze(0), age_tensor)
    prediction = output.item()
    return {'prediction': prediction}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

