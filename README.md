# Longevity prediction
This project was inspired by an off-hand comment by Balaji Srinivasan in his
[podcast with Lex
Fridman](https://www.youtube.com/watch?v=VeH7qKZr0WI&ab_channel=LexFridman).

F(picture of face, age) = life exectancy

The methodology is to collect a large dataset of pictures of faces and their dates, along with the
dates of birth and death of the people in the picture. Then train a neural network to predict age of death.

This could be a cool thing people use to get feedback on their own
health.

# Known limitations
1. The dataset is heavily skewed towards older people, so I'm not sure how well it
performs on pictures of younger people.

2. When generating the dataset I simplified myself the work so all dates are just
years (I didn't bother with the month or day of the year, so at best this can
only ever be accurate to the year).

3. I've done very little optimization: there is a lot of room for performance
   improvements

Other possible problems: I haven't thought hard about data leakage, so maybe
something is off here.


# High level technical overview
1. [Wikidata's API](query.wikidata.org) to generate the dataset (plus a bit of
   scraping).
2. I used pre-trained models as the initialisation of my neural nets,
ensembling different pre-trained models improves performance.
3. The target variable is a min-max scaled delta-life expectancy (subtracted
   the mean life expectancy, this is a big improvement on just predicting
min-max scaled life expectancy).


The models are small enough that you can train on CPU, but I recommend running
on a GPU (I did my training on a Quadro M4000, takes about 10 minutes for 15
epochs which is more than enough).
