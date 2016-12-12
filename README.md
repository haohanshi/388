# Prediction of Education Level

## Group Member:
**Name**: Mark Lee  
**Andrew ID**: marklee

**Name**: Haohan Shi  
**Andrew ID**: haohans

**Name**: Tianjun Ma  
**Andrew ID**: tianjunm

## How to run our code:
Before starting, make sure that required packages are installed:
```terminal
pip install -r requirements.txt
```
The main program can be run by running the main.py file in the repository.
If using SVM as model, the following will find the optimal kernel:
```terminal
./main.py optimize_kernel
```
If using LogisticRegression as model, the following will find optimal hyperparams:
```terminal
./main.py optimize_params
```
To generate the features used in training (already pre-generated in repo):
```terminal
./main.py generate_features
```
To test the model with LogisticRegressionCV:
```terminal
./main.py test
```

## nbviewer link:

## Links to large files:
All the data we used for feature generating, training, validation and testing (use andrew email account):

https://drive.google.com/drive/folders/0B3to2Ko7FJl1clVEelJ5OHY2SG8?usp=sharing

## Potential sources:
Age distribution for Minecraft Player:

https://www.quora.com/What-are-the-demographics-of-Minecraft-players

Age distribution for social media:

http://jetscram.com/blog/industry-news/social-media-user-statistics-and-age-demographics-2014/

http://sproutsocial.com/insights/new-social-media-demographics/

http://venturebeat.com/2012/08/22/social-media-demographics-stats-2012/

http://www.ibtimes.com/audience-profiles-who-actually-reads-new-york-times-watches-fox-news-other-news-publications-1451828

Python bindings for Link Grammar system:

https://pypi.python.org/pypi/pylinkgrammar

Reference we builidng grammar checker component for feature generation:

http://stackoverflow.com/questions/10252448/how-to-check-whether-a-sentence-is-correct-simple-grammar-check-in-python
https://github.com/dwyl/english-words

