import string, langid, grammar_check, enchant, re, json, nltk
import scipy.sparse as sp
import numpy as np
from svm import SVM
from syllables_en import count as count_syllables
from nltk.tokenize import sent_tokenize, word_tokenize

MIN_WORDS_PER_DOC = 5

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
proper_noun_regex = re.compile(r'\b[A-Z0-9]\S+')

punctuation_table = dict.fromkeys(map(ord, string.punctuation))

grammar_tool = grammar_check.LanguageTool('en-US')
spelling_tool = enchant.Dict('en_US')

def get_sentences (doc):
    return sent_tokenize(doc)

def get_words (sentence):
    sentence = sentence.strip()

    # remove links
    sentence = re.sub(url_regex, '', sentence)

    # remove proper nouns
    sentence = re.sub(proper_noun_regex, '', sentence)

    tokens = nltk.word_tokenize(sentence)
    words = []
    for token in tokens:
        without_punc = token.translate(punctuation_table)
        without_space_or_nums = re.sub(space_or_num_regex, '', without_punc)

        # ignore if word only consists of punctuations and numbers (e.g emoji)
        if len(without_space_or_nums):
            words.append(token) 

    return words

def get_metrics (doc):
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
        res['words'] += len(sentence)
        res['grammar_errors'] += len(grammar_tool.check(sentence))

        words_for_sentence = get_words(sentence)
        # words.append(words_for_sentence)

        for word in words_for_sentence:
            res['syllables'] += count_syllables(word)
            if not spelling_tool.check(word):
                res['spelling_errors'] += 1

    return res #, sentences, words

def get_features (metrics):
    # document is too short
    if (metrics['words'] < MIN_WORDS_PER_DOC):
        return None

    res = []
    num_sentences = float(metrics['sentences'])

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
def create_features (docs):
    X = []
    for doc in docs:
        # ignore if not english
        if langid.classify(doc)[0] != 'en':
            continue

        metrics = get_metrics(doc)
        features = get_features(metrics)
        if features:
            X.append(features)
    return sp.csr_matrix(X)

# comments should be a nx1 list of strings
# labels should be a nx1 list of ints
# the ith label should correspond to the ith comment
def learn_classifier (docs, labels):
    X, y = create_features(docs), labels
    svm = SVM(X, y, 1e-4)
    svm.train(niters=100, learning_rate=1)
    return svm

def validate (docs, labels):
    X, y = create_features(docs), labels
    ms = ModelSelector(X, y, np.arange(X.shape[0]), 3, 100)
    return ms.cross_validation(0.1, 1e-4)

def run ():
    with open('labels.json', 'r') as f:
        label_map = json.load(f)

    docs = []
    labels = []
    for filename,label in label_map.iteritems():
        with open('{}_70.json'.format(filename), 'r') as f:
            docs += json.load(f)
            labels += [label]*len(docs)

    docs = np.array(docs)
    labels = np.array(labels)
    print validate(docs, labels)

run()
