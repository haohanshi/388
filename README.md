# 15388 Final Project

## Group Member:
Name: Mark Lee

Andrew ID: marklee

Name: Haohan Shi

Andrew ID: haohans

Name: Tianjun Ma

Andrew ID: tianjunm

## How to run our code:
Before starting, make sure that required packages are installed. We've put all the requirements in a txt file so that everything can be downloaded by calling the following command:
```terminal
pip install --requirements.txt
```
The main program can be run by running the main.py file in the repository. We only need one extra parameter to run the program during each step. 
First of all, we should optimize the model before we start working on the data by calling
```terminal
./main.py optimize_kernel
```
and
```terminal
./main.py optimize_params
```
Then, we can start generating features from the data we’ve collected:
```terminal
./main.py generate_features
```

This instruction will automatically generate the features from the pages we collected.
In the end, we can test our model:
```terminal
./main.py test
```
to render the result of prediction model.

## nbviewer link:

## Links to large files:
All the data we used for feature generating, training, validation and testing:

https://drive.google.com/drive/folders/0B3to2Ko7FJl1clVEelJ5OHY2SG8?usp=sharing

## Potential sources:
Statistics about demographics of various websites:

https://www.quora.com/What-are-the-demographics-of-Minecraft-players

http://www.ibtimes.com/audience-profiles-who-actually-reads-new-york-times-watches-fox-news-other-news-publications-1451828

https://pypi.python.org/pypi/pylinkgrammar

http://jetscram.com/blog/industry-news/social-media-user-statistics-and-age-demographics-2014/

http://sproutsocial.com/insights/new-social-media-demographics/

http://venturebeat.com/2012/08/22/social-media-demographics-stats-2012/


Reference we builidng grammar checker component for feature generation:

http://stackoverflow.com/questions/10252448/how-to-check-whether-a-sentence-is-correct-simple-grammar-check-in-python
https://github.com/dwyl/english-words

