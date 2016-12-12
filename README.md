# Prediction of Education Level from User Comments

[nbviewer](http://nbviewer.jupyter.org/github/markblee/388/blob/master/edlevel.ipynb?flush_cache=true)

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
The bulk of the functionality is contained in `main.py`. Currently, we have
pre-generated all the features in `train_features` (for training),
`validate_features` (for validating the model), and `test_features` (holdout set
used for testing).

To train the LogisticRegressionCV model and test on `test_features`:
```terminal
./main.py test
```

If using SVM, the following can be used to determine the optimal kernel based on
the training set:
```terminal
./main.py optimize_kernel
```

If using LogisticRegression as model, the following will perform a grid search
to find optimal hyperparams based on the training set:
```terminal
./main.py optimize_params
```

It is also possible to re-generate the features on a different set of raw data.
To do so, update the data in `test_data`, `train_data`, and `validate_data`, and
update the `test_labels.json`, `train_labels.json` and `validate_labels.json`
files appropriately. Then, the following can be used to generate new features:
```terminal
./main.py generate_features
```

## Links to large files:
Contains the data we used for feature generating, training, validation and
testing (requires Andrew email account):  
https://drive.google.com/drive/folders/0B3to2Ko7FJl1clVEelJ5OHY2SG8?usp=sharing

## References:
Social media demographics:
- https://www.quora.com/What-are-the-demographics-of-Minecraft-players
- http://jetscram.com/blog/industry-news/social-media-user-statistics-and-age-demographics-2014/
- http://sproutsocial.com/insights/new-social-media-demographics/
- http://venturebeat.com/2012/08/22/social-media-demographics-stats-2012/
- http://www.ibtimes.com/audience-profiles-who-actually-reads-new-york-times-watches-fox-news-other-news-publications-1451828
