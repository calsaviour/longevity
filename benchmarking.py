import numpy as np
import torch
from torch.nn import MSELoss

from train import _generate_dataset, _get_train_test_split


if __name__ == '__main__': 
    dataset = _generate_dataset()
    train_dataset, test_dataset = _get_train_test_split(dataset)

    train_life_expectancies = [row[2].item() for row in train_dataset]
    test_life_expectancies = [row[2].item() for row in test_dataset]

    #Compute MSE Loss of the mean of the training set
    train_mean_life_expect = np.mean(train_life_expectancies)

    mean_guess_tensor = torch.tensor([train_mean_life_expect]*len(test_life_expectancies))
    mean_guess_loss_on_test = MSELoss()(mean_guess_tensor,
                                        torch.tensor(test_life_expectancies))

    #Compute MSE Loss of random guesses between min and max of training set
    min_life_expect = np.min(train_life_expectancies)
    max_life_expect = np.max(train_life_expectancies)

    random_guesses = np.random.uniform(min_life_expect, max_life_expect, 
                                       len(test_life_expectancies))
    random_guess_tensor = torch.tensor(random_guesses)

    random_guess_loss_on_test = MSELoss()(random_guess_tensor, 
                                          torch.tensor(test_life_expectancies))

    print(f"Mean guess loss: {mean_guess_loss_on_test}")
    print(f"Random guess loss: {random_guess_loss_on_test}")
