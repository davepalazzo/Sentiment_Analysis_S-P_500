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
    for i in range(len(df['X'])):
        polarity_score = []
        for t in df['X'][i]:
            polarity_score.append(t[1])
        df['X'][i] = polarity_score
    return df
