import math
import numpy as np
import torch

from train import _generate_dataset, _get_train_test_split


def rescale_model_output_to_years(mse,
                                  train_max_life_expectancy,
                                  train_min_life_expectancy):
    rmse = math.sqrt(mse)
    rescaled =  rmse * (train_max_life_expectancy - train_min_life_expectancy)
    return rescaled


if __name__ == '__main__': 
    dataset = _generate_dataset()
    train_dataset, test_dataset = _get_train_test_split(dataset)

    train_life_expectancies = [row[2].item() for row in train_dataset]

    max_lex = max(train_life_expectancies)
    min_lex = min(train_life_expectancies)
    
    mean_mse = 0.06292656314531728
    random_mse = 0.19728467289926574



