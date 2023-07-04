# Longevity prediction
This project was inspired by an off-hand comment by Balaji Srinivasan in his
[podcast with Lex
Fridman](https://www.youtube.com/watch?v=VeH7qKZr0WI&ab_channel=LexFridman).

F(picture of face, age) = life exectancy

The methodology is to collect a large dataset of pictures of faces and their dates, along with the
dates of birth and death of the people in the picture. Then train a neural network to predict age of death.

This could be a cool thing people use to get feedback on their own
health.


#Known limitations
The dataset is heavily skewed towards older people, so I'm not sure how well it
performs on pictures of younger people.

#How to use this code
The models are small enough that you can train on CPU, but I recommend running
on a GPU (I did my training on a Quadro M4000, takes about 10 minutes for 15
epochs which is more than enough).

``` python train.py ```
