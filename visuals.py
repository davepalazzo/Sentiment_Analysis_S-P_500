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


def get_GDP_visual(df):
    '''Returns dataframe used in ploting the gdp trend over time
     '''
    USA = np.array(df[df['Data Source'] == 'United States'])
    gdp_USA = pd.DataFrame(USA, columns=['Country Name', 'Country COde', 'Indicator Name', 'Indicator Code',
                                                 '1960','1961','1962','1963','1964','1965','1966','1967','1968','1969',
                                                 '1970','1971','1972','1973','1974','1975','1976','1977','1978','1979',
                                                 '1980','1981','1982','1983','1984','1985','1986','1987','1988','1989',
                                                 '1990','1991','1992','1993','1994','1995','1996','1997','1998','1999',
                                                 '2000','2001','2002','2003','2004','2005','2006','2007','2008','2009',
                                                 '2010','2011','2012','2013','2014','2015','2016','2017','2018'])

    gdp_USA = gdp_USA.drop(columns=['Country Name','Country COde','Indicator Name','Indicator Code','1960','1961','1962',
                                   '1963','1964','1965','1966','1967','1968','1969', '1970','1971','1972','1973','1974',
                                   '1975','1976','1977','1978','1979', '1980','1981','1982','1983','1984','1985','1986',
                                   '1987','1988','1989', '1990','1991','1992','1993','1994','1995','1996','1997','1998',
                                   '1999', '2000','2001','2002','2003','2004','2005','2006','2018'])

    gdp_USA_trans = gdp_USA.transpose()
    gdp_USA_trans = gdp_USA_trans.rename(columns={0:'GDP'})
    return gdp_USA_trans
