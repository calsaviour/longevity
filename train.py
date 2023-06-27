import glob
import torch
import matplotlib.pyplot as plt
from torch.utils.data import DataLoader

from model import FaceAgeDataset, FaceAgeModel

N_EPOCHS = 3


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

    criterion = torch.nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    losses = []

    # Training loop
    for epoch in range(N_EPOCHS):
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

