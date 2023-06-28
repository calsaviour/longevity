
def rescale_model_output_to_years(model_output,
                                  train_max_life_expectancy,
                                  train_min_life_expectancy):
    rescaled =  model_output * (train_max_life_expectancy - train_min_life_expectancy) + train_min_life_expectancy
    return rescaled
