import torch
from torch.utils.data import DataLoader
from model import FaceAgeDataset, FaceAgeModel, DenseNetFaceAgeModel

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load the saved model weights
model1 = FaceAgeModel()
model1.load_state_dict(torch.load('model1.pth', map_location=device))
model1 = model1.to(device)
model1.eval()

model2 = DenseNetFaceAgeModel()
model2.load_state_dict(torch.load('model2.pth', map_location=device))
model2 = model2.to(device)
model2.eval()

# Load the test set
_, test_dataloader = get_dataloaders()  # You need to define this function or import from your script

# Define the loss
criterion = torch.nn.MSELoss()

# Evaluate the ensemble
test_loss = 0
with torch.no_grad():
    for imgs, age, _, target in test_dataloader:
        imgs = imgs.to(device)
        age = age.to(device)
        target = target.to(device)

        output1 = model1(imgs, age)
        output2 = model2(imgs, age)

        # Average the predictions of the two models
        ensemble_output = (output1 + output2) / 2.0

        loss = criterion(ensemble_output, target)
        test_loss += loss.item()

print(f"Test Loss of the ensemble: {test_loss / len(test_dataloader)}")
