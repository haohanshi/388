import string, langid, grammar_check, enchant, re, json, nltk, time
# import scipy.sparse as sp
import numpy as np
from svm import SVM
from cross_validation import ModelSelector
from syllables_en import count as count_syllables
from nltk.tokenize import sent_tokenize, WhitespaceTokenizer

MIN_WORDS_PER_DOC = 3

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
                time.sleep(0.2)

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

    X = np.matrix(X)
    y = np.array(y)
    print X.shape, len(y), non_english, too_short
    return X, y

# comments should be a nx1 list of strings
# labels should be a nx1 list of ints
# the ith label should correspond to the ith comment
def learn_classifier (X_train, y_train):
    # perform grid search to learn hyperparameters
    # we use [ 0.1, 1, 10 ] for learning rate search space,
    # and [ 0.01, 0.1, 1, 10 ] for regularization
    ms = ModelSelector(X_train, y_train, np.arange(X_train.shape[0]), 4, 100)
    lr, reg = ms.grid_search(np.logspace(-1,1,3), np.logspace(-2,1,4))
    err, svm = ms.test(lr, reg)
    print "learned hyperparams:", lr, reg, "error:", err
    return svm

def run ():
    print "learning classifier..."
    with open('labels.json', 'r') as f:
        label_map = json.load(f)

    docs = []
    labels = []
    for filename, label in label_map.iteritems():
        with open('data_70/{}_70.json'.format(filename), 'r') as f:
            curr = json.load(f)[:200]
            docs += curr
            labels += [label]*len(curr)

    X_train, y_train = create_features(np.array(docs), np.array(labels)) 

    with open('test_features', 'w') as f:
        json.dump(zip(X_train.tolist(), labels), f)

    svm = learn_classifier(X_train, y_train)
    print "done learning classifier"

    # test on holdout set
    print "testing on holdout set..."
    docs = []
    labels = []
    for filename, label in label_map.iteritems():
        with open('data_30/{}_30.json'.format(filename), 'r') as f:
            curr = json.load(f)
            docs += curr
            labels += [label]*len(curr)

    X, y = create_features(np.array(docs), np.array(labels))
    predicted_y = np.array(svm.predict(X))

    with open('predictions', 'w') as f:
        json.dump(predicted_y.tolist(), f)

    err = (predicted_y != y).sum()
    total = float(len(docs))

    print "done testing on holdout set"
    print "error:", err / total
