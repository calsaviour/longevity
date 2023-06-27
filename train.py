import tqdm
import glob
import torch
import matplotlib.pyplot as plt
from torch.utils.data import DataLoader, random_split

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

    # Split the dataset into training and test sets
    test_ratio = 0.2  # Specifies what proportion of the dataset should be reserved for testing
    num_test = int(test_ratio * len(dataset))
    num_train = len(dataset) - num_test

    train_dataset, test_dataset = random_split(dataset, [num_train, num_test])

    # Define separate data loaders for the training and test sets
    train_dataloader = DataLoader(train_dataset, batch_size=1, shuffle=True)
    test_dataloader = DataLoader(test_dataset, batch_size=1, shuffle=False)

    import pdb;pdb.set_trace() 

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model = FaceAgeModel().to(device)

    criterion = torch.nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    losses = []

    # Training loop
    for epoch in range(N_EPOCHS):
        # Train
        model.train()
        for imgs, age, target in tqdm.tqdm(train_dataloader):
            imgs = imgs.to(device)
            age = age.to(device)
            target = target.to(device)

            optimizer.zero_grad()

            output = model(imgs, age)
            loss = criterion(output, target)
            losses.append(loss.item())
            loss.backward()
            optimizer.step()

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
        
        print(f"Epoch: {epoch+1}, Train Loss: {losses[-1]}, Test Loss: {test_loss / len(test_dataloader)}")
