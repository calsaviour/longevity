import numpy as np
import torch

from train import _generate_dataset, _get_train_test_split


def rescale_model_output_to_years(model_output,
                                  train_max_life_expectancy,
                                  train_min_life_expectancy):
    rescaled =  model_output * (train_max_life_expectancy - train_min_life_expectancy) + train_min_life_expectancy
    return rescaled


if __name__ == '__main__': 
    dataset = _generate_dataset()
    train_dataset, test_dataset = _get_train_test_split(dataset)

    train_life_expectancies = [row[2].item() for row in train_dataset]

    train_max_life_expectancy = max(train_life_expectancies)
    train_min_life_expectancy = min(train_life_expectancies)

