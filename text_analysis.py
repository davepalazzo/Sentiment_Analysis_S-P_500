from textblob import TextBlob
import pandas as pd
import numpy as np
from sklearn.model_selection import KFold
import xgboost as xgb
from sklearn.metrics import mean_absolute_error

def text_analysis_wordall(df):
    '''Function takes in a df and look at the text of each word to find the polarity and subjectivity score,
    and returns the word and its scores only if polarity does not equal 0.'''

    df['X'] = df['X'].map(lambda x: x.split(' '))
    for i in range(len(df['X'])):
        score = []
        for word in df['X'][i]:
            if word != '.':
                blob = TextBlob(word)
                sent = blob.sentiment
                # eliminate words with no polarity
                if sent.polarity != 0.0:
                    score.append((word,sent.polarity,sent.subjectivity))
        df['X'][i] = score
    return df

def text_analysis_sentenceall(df):
    '''Function takes in a df and look at the text of each sentence to find the polarity and subjectivity score,
    and returns the word and its scores only if polarity does not equal 0.'''

    df['X'] = df['X'].map(lambda x: x.split('.'))
    for i in range(len(df['X'])):
        score = []
        for s in df['X'][i]:
            blob = TextBlob(s)
            sent = blob.sentiment
            # eliminate words with no polarity
            if sent.polarity != 0.0:
                score.append((s,sent.polarity,sent.subjectivity))
        df['X'][i] = score
    return df

def get_polarity(df):
    '''Function takes in a df of a list of words, and their scores (polarity
    and subjectivity). It pulls only the polarity of that word into a df.'''

    for i in range(len(df['X'])):
        polarity_score = []
        for t in df['X'][i]:
            polarity_score.append(t[1])
        df['X'][i] = polarity_score
    return df

def low_subjectivity(df):
    '''Function takes in a df of a list of words, and their scores (polarity
    and subjectivity). It pulls only the polarity of that word with a
    subjectivity of less than 0.9 into a df.'''

    for i in range(len(df['X'])):
        polarity_score = []
        for t in df['X'][i]:
            # if subjectivity of the word is less that 0.9
            if t[2] < 0.9:
                polarity_score.append(t[1])
        df['X'][i] = polarity_score
    return df

def model_analysis(X,y):
    '''Takes in X and y and runs a XGBoost Model'''

    kfold = KFold(n_splits=5, shuffle=True, random_state=2)
    kf = KFold(n_splits=5, random_state=2, shuffle=True)

    for train_index, test_index in kf.split(X):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]

    if len(X_train.shape) == 1:
        # change the array dimmensions
        X_train = X_train[:, np.newaxis]
        X_test = X_test[:, np.newaxis]

    xgb_reg = xgb.XGBRegressor(max_depth=6,n_estimators=300, n_jobs=-1, subsample=.7,random_seed=3)
    xgb_fit = xgb_reg.fit(X_train,y_train)
    score = xgb_reg.score(X_test,y_test)
    y_pred = xgb_reg.predict(X_test)
    MAE = mean_absolute_error(y_test, y_pred)

    return xgb_reg,xgb_fit,score,y_pred,MAE,y_test
