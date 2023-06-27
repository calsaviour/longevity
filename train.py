import torch
from torch import nn
from torch.utils.data import Dataset, DataLoader
from torchvision import models, transforms
import cv2
import glob
import numpy as np
import matplotlib.pyplot as plt

# Preprocessing for images
preprocess = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

class FaceAgeDataset(Dataset):
    def __init__(self, image_paths, ages, life_expectancies):
        self.image_paths = image_paths
        self.ages = ages
        self.life_expectancies = life_expectancies

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        img_path = self.image_paths[idx]
        img = cv2.imread(img_path)
        img = preprocess(img)

        age = self.ages[idx]
        life_expectancy = self.life_expectancies[idx]

        return img, torch.tensor([age]).float(), torch.tensor([life_expectancy]).float()


class FaceAgeModel(nn.Module):
    def __init__(self):
        super(FaceAgeModel, self).__init__()

        self.cnn = models.resnet50(pretrained=True)
        for param in self.cnn.parameters():
            param.requires_grad = False

        self.cnn.fc = nn.Linear(self.cnn.fc.in_features, 500)
        self.fc1 = nn.Linear(501, 250)  # 500 for image features + 1 for age
        self.fc2 = nn.Linear(250, 1)

    def forward(self, img, age):
        x1 = self.cnn(img)
        x = torch.cat((x1, age), dim=1)
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x


if __name__ == '__main__': 
    image_paths = glob.glob('dataset/*.jpg')

    image_dates = [int(p.split('date:')[-1][:-4]) for p in image_paths]
    death_dates = [int(p.split('death:')[-1][:4]) for p in image_paths]
    birth_dates = [int(p.split('birth:')[-1][:4]) for p in image_paths]
    ages = [img_date - birth_date for img_date, birth_date in zip(image_dates, birth_dates)]
    life_expectancies = [death - date for death, date in zip(death_dates, image_dates)]

    dataset = FaceAgeDataset(image_paths, ages, life_expectancies)
    dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = FaceAgeModel().to(device)

    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    losses = []

    # Training loop
    for epoch in range(30):  # epochs
        for imgs, age, target in dataloader:
            imgs = imgs.to(device)
            age = age.to(device)
            target = target.to(device)

            optimizer.zero_grad()

            output = model(imgs, age)
            loss = criterion(output, target)
            losses.append(loss.item())
            loss.backward()
            optimizer.step()

        print(f"Epoch {epoch+1}, Loss: {loss.item()}")
    plt.plot(losses)
    plt.show()

