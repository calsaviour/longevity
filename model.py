import torch
from torch import nn
from torch.utils.data import Dataset
from torchvision import models, transforms
import cv2
import numpy as np

from utils import min_max_scale

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
        self.targets = min_max_scale(life_expectancies)
        self.life_expectancies = life_expectancies

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        img_path = self.image_paths[idx]
        img = cv2.imread(img_path)
        img = preprocess(img)

        age = self.ages[idx]
        target = self.targets[idx]
        life_expectancy = self.life_expectancies[idx]

        return img, torch.tensor([age]).float(), torch.tensor([life_expectancy]).float(), torch.tensor([target]).float()


class FaceAgeModel(nn.Module):
    def __init__(self):
        super(FaceAgeModel, self).__init__()

        self.cnn = models.resnet50(pretrained=True)
        for param in self.cnn.parameters():
            param.requires_grad = False

        for param in self.cnn.layer3.parameters():
            param.requires_grad = True

        for param in self.cnn.layer4.parameters():
            param.requires_grad = True

        self.cnn.fc = nn.Linear(self.cnn.fc.in_features, 500)
        self.fc1 = nn.Linear(501, 250)  # 500 for image features + 1 for age
        self.fc2 = nn.Linear(250, 1)

    def forward(self, img, age):
        x1 = self.cnn(img)
        x = torch.cat((x1, age), dim=1)
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x


class DenseNetFaceAgeModel(nn.Module):
    def __init__(self):
        super(DenseNetFaceAgeModel, self).__init__()

        # Load pretrained DenseNet-121
        self.base_model = models.densenet121(pretrained=True)
        for param in self.base_model.parameters():
            param.requires_grad = False
        
        # Unfreeze the last dense block
        for param in self.base_model.features.denseblock4.parameters():
            param.requires_grad = True

        self.base_model.classifier = nn.Identity()  # Remove the classifier part of DenseNet
        
        # New layers
        self.fc1 = nn.Linear(1024+1, 512)  # 1024 for densenet features + 1 for age
        self.dropout = nn.Dropout(0.2)
        self.fc2 = nn.Linear(512, 128)
        self.fc3 = nn.Linear(128, 1)

    def forward(self, img, age):
        x1 = self.base_model(img)
        x = torch.cat((x1, age), dim=1)
        x = torch.relu(self.fc1(x))
        x = self.dropout(x)
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x


