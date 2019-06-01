from collections import defaultdict
import matplotlib.pyplot as plt
import pandas as pd

def getCompFreq(top10Comp):
    '''The following function creates a df of frequency counts of companies
    accross all years '''
    dd = defaultdict(int)
    # Count frequencies of each companies apperance in the top 10
    for year in top10Comp:
        for comp in range(len(top10Comp[year])):
            dd[top10Comp[year][comp][0]] += 1

    # Combine counts for duplicate companies
    dd['BERKSHIRE HATHAWAY'] += dd['Berkshire Hathaway Inc']
    dd['APPLE INC'] += dd['Apple Inc.']
    dd['EXXON MOBIL CORP'] += dd['Exxon Mobil Corp.']
    dd['MICROSOFT CORP'] += dd['Microsoft Corp.']
    dd['GENERAL ELECTRIC CO'] += dd['General Electric']
    dd['ALPHABET INC']+= dd['Alphabet Inc. Class A']
    dd['CHEVRON CORP'] += dd['Chevron Corp.']
    dd['JOHNSON & JOHNSON'] += dd['Johnson & Johnson']
    dd['WALMART INC'] += dd['Wal-Mart Stores Inc']
    dd['JPMORGAN CHASE & CO'] += dd['JPMorgan Chase & Co.']

    # Limit visual to companies that appear over 5 times
    dd1 = defaultdict(int)
    for key, value in dd.items():
        if value > 5:
            dd1[key] = value

    df = pd.DataFrame.from_dict(dd1, orient='index', columns=['count'])

    df.reset_index(level=0, inplace=True)

    df = df.sort_values(by=['count'])
    df.rename(columns= {'index': 'Company Name', 'count': 'Number of Years'},inplace=True)

    return df
