#! /usr/bin/env python

import sys, string, langid, grammar_check, enchant, re, json, nltk, time
import os.path
import numpy as np
# from cross_validation import ModelSelector
from syllables_en import count as count_syllables
from nltk.tokenize import sent_tokenize, WhitespaceTokenizer
from sklearn.svm import SVC as SVM
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression, LogisticRegressionCV #, SGDClassifier
from sklearn.metrics import accuracy_score

MIN_WORDS_PER_DOC = 3
LABELS_FILE = "labels.json" # "labels.json"
TRAIN_FEATURES_DIR = "train_features"
VALIDATE_FEATURES_DIR = "validate_features"
TRAIN_DATA_DIR = "train_data"
VALIDATE_DATA_DIR = "validate_data"
TEST_DATA_DIR = "test_data"
GRID_SEARCH_RESULTS_FILE = "grid_search.txt"
OPTIMAL_KERNEL = "linear"
# C = 100
C = 10
SOLVER = "lbfgs"

# source: http://stackoverflow.com/a/7160778
# modified so protocol is optional.
url_regex = re.compile(
    r'(^(?:http|ftp)s?://)?' # http:// or https:// (optional)
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' # domain...
    r'localhost|' # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
    r'(?::\d+)?' # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

space_or_num_regex = re.compile(r'(\d|\s)+')
proper_noun_regex = re.compile(r'^([0-9]|[A-Z][a-z0-9]+)')

punctuation_table = dict.fromkeys(map(ord, string.punctuation))

grammar_tool = grammar_check.LanguageTool('en-US')
spelling_tool = enchant.Dict('en_US')

tokenizer = WhitespaceTokenizer()

def get_sentences (doc):
    return sent_tokenize(doc)

def get_words (sentence):
    sentence = sentence.strip()

    words = []
    for token in tokenizer.tokenize(sentence):
        token = token.decode("utf-8")

        # remove urls
        modified = re.sub(url_regex, '', token)
        # remove punctuation
        modified = modified.translate(punctuation_table)
        # remove proper nouns
        modified = re.sub(proper_noun_regex, '', modified)
        # remove whitespace and standalone numbers
        modified = re.sub(space_or_num_regex, '', modified)

        if len(modified):
            words.append(token) 

    return words

def get_metrics (doc):
    global grammar_tool

    # initialize dict
    metrics = [
        'syllables', 'words', 'spelling_errors', 'grammar_errors', 'sentences'
    ]
    res = { metric: 0 for metric in metrics }

    # initial parse
    sentences = get_sentences(doc)
    # words = []

    # get metrics
    num_sentences = len(sentences)
    res['sentences'] = num_sentences
    for sentence in sentences:
        try:
            try:
                res['grammar_errors'] += len(grammar_tool.check(sentence))
            except Exception as e:
                print "grammar tool failed: {}".format(e)
                print "reinitializing grammar tool.."
                grammar_tool = grammar_check.LanguageTool('en-US')
                time.sleep(0.1)

            words_for_sentence = get_words(sentence)
            res['words'] += len(words_for_sentence)
            # words.append(words_for_sentence)

            for word in words_for_sentence:
                try:
                    # handle trailing punctuation for spellchecker
                    if word[-1] in string.punctuation:
                        word = word[:-1]
                    res['syllables'] += count_syllables(word)
                    if not spelling_tool.check(word):
                        res['spelling_errors'] += 1
                except Exception as e:
                    print "inner exception:", e
                    continue
        except Exception as e:
            print "outer exception:", e
            continue

    if res['words'] == 0:
        print "discarding...", doc

    return res #, sentences, words

def get_features (metrics):
    num_sentences = metrics['sentences']

    # document is too short
    if (num_sentences == 0 or metrics['words'] < MIN_WORDS_PER_DOC):
        return None

    res = []
    num_sentences = float(num_sentences)

    # `syllables_per_word`: count the total number of syllables and divide by
    # total number of words
    res.append(metrics['syllables'] / float(metrics['words']))

    # `words_per_sentence`: count the total number of words and divide by total
    # number of sentences
    res.append(metrics['words'] / num_sentences)

    # `spelling_errors_per_sentence`: count the total number of spelling errors
    # and divide by total number of sentences
    res.append(metrics['spelling_errors'] / num_sentences)

    # `grammer_errors_per_sentence`: count the total number of grammer errors
    # and divide by total number of sentences
    res.append(metrics['grammar_errors'] / num_sentences)

    return np.array(res)

# given a list of docs (body of text), parse into tokens
# if doc is too short, skip
# otherwise, use the tokens to build an example with the features:
# `syllables_per_word`: count the total number of syllables and divide by
# total number of words
# `words_per_sentence`: count the total number of words and divide by total
# number of sentences
# `spelling_errors_per_sentence`: count the total number of spelling
# errors and divide by total number of sentences
# `grammer_errors_per_sentence`: count the total number of
# grammer errors and divide by total number of sentences
def create_features (docs, labels):
    X, y = [], []
    non_english = 0
    too_short = 0

    for i, doc in enumerate(docs):
        # ignore if not english
        if langid.classify(doc)[0] != 'en':
            non_english += 1
            continue

        metrics = get_metrics(doc)
        features = get_features(metrics)
        if features is not None:
            X.append(features)
            y.append(labels[i])
        else:
            too_short += 1

    X = np.array(X)
    y = np.array(y)
    print X.shape, y.shape, non_english, too_short
    return X, y

# comments should be a nx1 list of strings
# labels should be a nx1 list of ints
# the ith label should correspond to the ith comment
def learn_classifier (X_train, y_train, kernel='best'):
    print "learning classifier..."
    clf = LogisticRegressionCV(
        Cs=list(np.power(10.0, np.arange(-10, 10))),
        penalty='l2',
        # scoring='roc_auc',
        cv=10, # kfolds with k=10
        random_state=42,
        max_iter=10000,
        fit_intercept=True,
        solver='lbfgs', #'newton-cg',
        tol=1e-4
    )

    # clf = LogisticRegression(C=C, solver=SOLVER)

    # clf = SGDClassifier(loss="log", n_iter=1000)

    # if kernel == 'best' and OPTIMAL_KERNEL:
    #     print "using kernel: {}".format(OPTIMAL_KERNEL)
    #     clf = SVM(C=C, kernel=OPTIMAL_KERNEL)
    # else:
    #     print "using default kernel"
    #     clf = SVM(C=C)

    clf.fit(X_train, y_train)
    print "done learning classifier"
    return clf

# chooses optimal kernel for svm
def optimal_kernel (X_train, y_train, X_validate, y_validate):
    best_kernel = None
    best_accuracy = 0
    for kernel in ['linear', 'rbf', 'poly', 'sigmoid']:
        classifier = learn_classifier(X_train, y_train, kernel)
        accuracy = classifier.score(X_validate, y_validate)
        if best_kernel is None or accuracy > best_accuracy:
            best_accuracy = accuracy
            best_kernel = kernel
        print kernel, ":", accuracy
    return best_kernel, best_accuracy

def optimal_hyperparams (X_train, y_train):
    print "running grid search..."
    clf = LogisticRegression()
    params = {
        "solver": ["lbfgs", "newton-cg", "sag"],
        "max_iter": [100, 1000, 10000],
        "multi_class": ["ovr", "multinomial"],
        "C": [0.001, 0.01, 0.1, 1, 10, 100, 1000]
    }
    classifier = GridSearchCV(clf, params)
    classifier.fit(X_train, y_train)
    best = classifier.best_params_
    print "best params:", best
    print "best score:", classifier.best_score_
    print "dumping results to file: {}...".format(GRID_SEARCH_RESULTS_FILE)
    with open(GRID_SEARCH_RESULTS_FILE, 'w') as f:
        f.write("{}".format(best))

## data/feature helpers

def read_features (feature_dir, label_map):
    print "reading from {}...".format(feature_dir)
    features = []
    for feature_file in label_map.keys():
        with open(os.path.join(feature_dir, feature_file), 'r') as f:
            features += json.load(f)

    features = zip(*features) # "unzip"
    X = np.array(features[0])
    y = np.array(features[1])
    return X, y

def read_raw_data (raw_dir, feature_dir, label_map):
    X, y = None, None
    for src, label in label_map.iteritems():
        filename = '{}.json'.format(src)
        filepath = os.path.join(raw_dir, filename)
        print "reading from {}...".format(filepath)
        with open(filepath, 'r') as f:
            curr = json.load(f)
            labels = [label]*len(curr)
            X_curr, y_curr = create_features(np.array(curr), np.array(labels))

            # save to file
            with open(os.path.join(feature_dir, filename), 'w') as g:
                json.dump(zip(X_curr.tolist(), y_curr), g)

            # aggregate results
            if X is None or y is None:
                X = X_curr
                y = y_curr
            else:
                X = np.concatenate((X, X_curr))
                y = np.concatenate((y, y_curr))
    return X, y

## wrappers 

def gen_train_features ():
    with open(LABELS_FILE, 'r') as f:
        label_map = json.load(f)

    print "generating features for training..."
    try:
        # try using pre-generated features if they exist
        X_train, y_train = read_features(TRAIN_FEATURES_DIR, label_map)
        print "features already generated"
    except:
        print "generating from raw data..."
        X_train, y_train = read_raw_data(TRAIN_DATA_DIR, TRAIN_FEATURES_DIR,
            label_map)

    print "done generating features for training"
    return X_train, y_train

def gen_validate_features ():
    with open(LABELS_FILE, 'r') as f:
        label_map = json.load(f)

    print "generating features for validation..."
    try:
        # try using pre-generated features if they exist
        X, y = read_features(VALIDATE_FEATURES_FILE)
        print "features already generated"
    except:
        print "generating from raw data..."
        X, y = read_raw_data(VALIDATE_DATA_DIR, VALIDATE_FEATURES_DIR,
            label_map)

    print "done generating features for validation"
    return X, y

def choose_optimal_kernel ():
    X_train, y_train = gen_train_features()
    X, y = gen_validate_features()

    print "choosing optimal kernel"
    print "this might take a while..."
    print optimal_kernel(X_train, y_train, X, y)

def choose_optimal_params ():
    X_train, y_train = gen_train_features()
    optimal_hyperparams(X_train, y_train)

def test ():
    X_train, y_train = gen_train_features()
    classifier = learn_classifier(X_train, y_train)

    print "testing on holdout set..."
    X, y = gen_validate_features()
    y_pred = classifier.predict(X)
    print "accuracy:", accuracy_score(y, y_pred)

def usage ():
    print "invalid options"

def main ():
    if len(sys.argv) < 2:
        usage()
    else:
        option = sys.argv[1]
        if option == "optimize_kernel":
            choose_optimal_kernel()
        elif option == "optimize_params":
            choose_optimal_params()
        elif option == "generate_features":
            gen_train_features()
            gen_validate_features()
        elif option == "test":
            test()

if __name__ == "__main__":
    main()
