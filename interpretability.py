import math
import numpy as np
import torch

from train import _generate_dataset, _get_train_test_split


def rescale_model_output_to_years(mse,
                                  train_max_target,
                                  train_min_target):
    rmse = math.sqrt(mse)
    rescaled =  rmse * (train_max_target - train_min_target)
    return rescaled


if __name__ == '__main__': 
    dataset = _generate_dataset()
    train_dataset, test_dataset = _get_train_test_split(dataset)

    train_targets = [row[3].item() for row in train_dataset]

    max_target = max(train_life_expectancies)
    min_target = min(train_life_expectancies)

    rescale = lambda x: rescale_model_output_to_years(x, max_target, min_target)

    






    1/0


    train_images = [train_dataset.dataset.image_paths[i] for i in train_dataset.indices]
    train_lexs = [train_dataset.dataset.life_expectancies[i] for i in train_dataset.indices]
    

    def get_pic_year(f):
        return f.split('data:')[1][:4]

    def get_birth_year(f):
        return f.split('birth:')[1][:4]


    ixs = np.array([get_birth_year(f) == get_pic_year(f) for f in train_images])
    print(sum(ixs))
