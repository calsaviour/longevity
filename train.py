import tqdm
import glob
import torch
import matplotlib.pyplot as plt
import random
import numpy as np
from torch.utils.data import DataLoader, random_split
import matplotlib.pyplot as plt

from model import FaceAgeDataset, FaceAgeModel
from utils import min_max_scale


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

N_EPOCHS = 7
SEED = 7457769
LR = 1e-3
TEST_SET_RATIO = 0.2


def set_seed(seed):
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    np.random.seed(seed)
    random.seed(seed)


def generate_dataset():
    image_paths = glob.glob('dataset/*.jpg')
    image_dates = [int(p.split('date:')[-1][:-4]) for p in image_paths]
    death_dates = [int(p.split('death:')[-1][:4]) for p in image_paths]
    birth_dates = [int(p.split('birth:')[-1][:4]) for p in image_paths]
    ages = [img_date - birth_date for img_date, birth_date in zip(image_dates, birth_dates)]
    life_expectancies = [death - date for death, date in zip(death_dates, image_dates)]
    dataset = FaceAgeDataset(image_paths, ages, life_expectancies)
    return dataset


def get_train_test_split(dataset):
    num_test = int(TEST_SET_RATIO * len(dataset))
    num_train = len(dataset) - num_test
    train_dataset, test_dataset = random_split(dataset, [num_train, num_test],
                                               generator=torch.Generator().manual_seed(SEED))
    train_dataloader = DataLoader(train_dataset, batch_size=1, shuffle=True)
    test_dataloader = DataLoader(test_dataset, batch_size=1, shuffle=False)
    return train_dataloader, test_dataloader



if __name__ == '__main__': 
    set_seed(SEED)
    dataset = generate_dataset()
    train_dataloader, test_dataloader = get_train_test_split(dataset)

    model = FaceAgeModel().to(device)

    criterion = torch.nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=LR)

    train_losses = []
    test_losses = []

    # Training loop
    for epoch in range(N_EPOCHS):
        # Train
        model.train()
        train_loss = 0
        for imgs, age, target in tqdm.tqdm(train_dataloader):
            imgs = imgs.to(device)
            age = age.to(device)
            target = target.to(device)

            optimizer.zero_grad()

            output = model(imgs, age)
            loss = criterion(output, target)
            train_loss += loss.item()
            loss.backward()
            optimizer.step()
        train_losses.append(train_loss)

        # Evaluate
        model.eval()
        test_loss = 0
        with torch.no_grad():
            for imgs, age, target in test_dataloader:
                imgs = imgs.to(device)
                age = age.to(device)
                target = target.to(device)

                output = model(imgs, age)
                loss = criterion(output, target)
                test_loss += loss.item()
        test_losses.append(test_loss)
        
        print(f"Epoch: {epoch+1}, Train Loss: {train_loss / len(train_dataloader)}, Test Loss: {test_loss / len(test_dataloader)}")
    plt.plot(train_losses, 'r', label='train_loss')
    plt.plot(test_losses, 'g', label='test_loss')
    plt.show()

