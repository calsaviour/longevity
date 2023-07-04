# Longevity prediction
This project was inspired by an off-hand comment by Balaji Srinivasan in his
[podcast with Lex
Fridman](https://www.youtube.com/watch?v=VeH7qKZr0WI&ab_channel=LexFridman).

F(picture of face, age) = life exectancy

The methodology is to collect a large dataset of pictures of faces and their dates, along with the
dates of birth and death of the people in the picture. Then train a neural network to predict age of death.

This could be a cool thing people use to get feedback on their own
health.

# Performance
A ResNet-50 gets to sub-1 year accuracy for life expectancy on the test set.

| Model | Best test loss | Estimated precision (years) | Git hash |
|---------|---------|---------|---------|
| ResNet-50 (last block un-frozen)   | 0.007870   | 0.08   | 5e0fb47a6c00118495dca9ba6   |
# Known limitations
1. The dataset is heavily skewed towards older people, so I'm not sure how well it
performs on pictures of younger people.

2. When generating the dataset I simplified myself the work so all dates are just
years (I didn't bother with the month or day of the year, so at best this can
only ever be accurate to the year).

3. Some pictures in the dataset (I estimate <2%) have more than one person in
   them, which is "corrupt" data.

3. I've done very little optimization: there is a lot of room for performance
   improvements

Other possible problems: I haven't thought hard about data leakage, so maybe
something is off here.


# High level technical overview
1. [Wikidata's API](query.wikidata.org) to generate the dataset (plus a bit of
   scraping): dataset_v2 has ~5000 examples. I also have dataset_v3 with about
14k examples, but haven't used it yet.
2. I used pre-trained models as the initialisation of my neural nets,
ensembling different pre-trained models improves performance.
3. The target variable is a min-max scaled delta-life expectancy (subtracted
   the mean life expectancy, this is a big improvement on just predicting
min-max scaled life expectancy).


The models are small enough that you can train on CPU, but I recommend running
on a GPU (I did my training on a Quadro M4000, takes about 10 minutes for 15
epochs which is more than enough).

Some details on dataset cleaning: a lot of the results returned by the wikidata
API (see exact query in ```dataset_generation/wikidata.py```) had pictures that
were stamps of the person, not actual pictures. The way this came up is that
when running the dataset generation / scraping code, the year of death and the
year of the picture would be the same. It seems important to remove these data
before using a new dataset, but I'm not sure what the performance hit would be
from them.




