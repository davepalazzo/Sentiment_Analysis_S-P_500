import requests
import edgar
import re
from bs4 import BeautifulSoup as bsoup
import pandas as pd
import numpy as np
from collections import defaultdict


def pullMDA(yearRange,compName, resLst, split_on = None):
    '''Pulls MD&A text from exhibit 13 SEC website
        Parameters: 1) yearRange - list of years
                    2) resLst - list of SEC websites
                    3) compName - string of company name
                    4) split_on - string to split on for MD&A
        Returns: Tuple with year and MD&A text
        '''
    output = defaultdict()
    for year in yearRange:
        for site in resLst:
            res = requests.get(site)
            soup = bsoup(res.content,'html.parser')
            text = soup.text
            if split_on:
                text = text.split(split_on)[1]
                output[year] = (compName,text)
                break
            else:
                output[year] = (compName,text)
                break
    return output


def divide_chunks(Lst, n):
    ''' Split list into successive n chunks'''
    for i in range(0, len(Lst), n):
        yield Lst[i:i + n]


def extractTable(soup):
    '''Extract the top ten companies from 1980-2013 '''
    table = []
    for div in soup.find_all('div', {'id':'sections'}):
        for a in div.find_all('div', {'class':'dataRow'}):
            for s in a.find_all('span', {'class': 'rowTitle'}):
                table+=s
    return(table)

def getComp(Lst):
    return [Lst[i::10] for i in range(10)]

# Yield successive n-sized
def divide_chunks(Lst, n):

    for i in range(0, len(Lst), n):
        yield Lst[i:i + n]


def annual_filings(name,ID,year,doc_num):
    '''This function finds the correct document'''
    # get filings from package
    company = edgar.Company(name,ID)
    tree = company.getAllFilings(filingType = "10-K")
    doc = edgar.getDocuments(tree, noOfDocuments=14)
    year = int(year)

    # search for the right document year
    d = doc_num
    while d < len(doc):

        filing = (re.sub('\\xa0|\\n',' ',doc[d]))
        # see if the document is amended
        if '10-K/A' in filing[1:15]:
            d += 1

        # if in the right fiscal year and remove the new lines and break
        elif re.search(r'FOR THE FISCAL YEAR ENDED\s*[0-9]*\s*[A-Z]*\s*'+str(year)+'|FOR THE\s*(FISCAL)? YEAR ENDED\s*(Commission File Number)?\W?\s*[A-Z]*\s*[0-9]*,\s*'+str(year),filing,re.IGNORECASE):
            filing = filing.replace('\n', '').replace('\t', '').replace('\r','').replace('Contents',' ').upper().split('ITEM ')
            break

        elif re.search(r'FOR THE FISCAL YEAR ENDED\s*[0-9]*\s*[A-Z]*\s*'+str(year+1)+'|FOR THE\s*(FISCAL)? YEAR ENDED\s*(Commission File Number)?\W?\s*[A-Z]*\s*[0-9]*,\s*'+str(year+1),filing,re.IGNORECASE):
            d += 1

        elif re.search(r'FOR THE FISCAL YEAR ENDED\s*[0-9]*\s*[A-Z]*\s*'+str(year-1)+'|FOR THE\s*(FISCAL)? YEAR ENDED\s*(Commission File Number)?\W?\s*[A-Z]*\s*[0-9]*,\s*'+str(year-1),filing,re.IGNORECASE):
            d -= 1
        # for Google doc #
        elif re.search(r'FOR THE\s*(FISCAL)? YEAR ENDED\s*\W?\s*[A-Z]*\s*[0-9]*,\s*'+str(year-2),filing,re.IGNORECASE):
            d -= 2

        else:
            return name,None

    new_doc = []
    start = []
    stop = []

    # remove characters from filing
    for item in filing:
        new_doc.append(re.sub('\\xa0*|(?<=[7-8])\W?s?','',item))
    for i in range(len(new_doc)):
        if re.search(r'7\s*\W?\.?\s*(AND 7A.)?(COMBINED)?\s*MANAGEMENT\W?\s*S\s*DISCUSSION\s*AND\s*ANALYSIS\s*OF\s*(CONSOLIDATED)?\s*FINANCIAL\s*CONDITION\S?\s*AND\s*RESULTS\s*OF\s*OPERATION\S?',new_doc[i]):
            start.append(i)
        if re.search(r'7\s*\W?\.?\s*MANAGEMENT\W?\s*S\s*DISCUSSION\s*AND\s*ANALYSIS\s*OF\s*RESULTS\s*OF\s*OPERATIONS\s*AND\s*FINANCIAL\s*CONDITION',new_doc[i]):
            start.append(i)
        if re.search(r'9\s*\W?\w?\.?\s*\W?\s*CONTROLS\s*AND\s*PROCEDURES',new_doc[i]):
            stop.append(i)

    return name,ID,start,stop,d


def MDA(name,ID,start_index,stop_index,doc_num,year):
    '''This function returns the MDA text of the 10-k filing using the indices provided and the correct document.'''
    # get filings from package
    company = edgar.Company(name,ID)
    tree = company.getAllFilings(filingType = "10-K")
    doc = edgar.getDocuments(tree, noOfDocuments=doc_num+1)

    if name == 'General Electric' and year > 2013:
        MDA= (re.sub('\\xa0|\\n',' ',doc[doc_num]))
        MDA = MDA.replace('\n', '').replace('\t', '').replace('\r','').replace('Contents',' ').split('GE '+str(year)+' FORM 10-K')

        new_doc = []
        for item in MDA:
            new_doc.append(re.sub('\\xa0*|(?<=[7-8])\W?s?','',item))

        for i in range(len(new_doc)):
            if re.search(r'MANAGEMENT\W?\s*S\s*DISCUSSION\s*AND\s*ANALYSIS\s*OF\s*FINANCIAL\s*CONDITION\s*AND\s*RESULTS\s*OF\s*OPERATIONS\s*\(MD',new_doc[i]):
                start_index = i
            if re.search(r'MANAGEMENT\W?\s*S\s*ANNUAL\s*REPORT\s*ON\s*INTERNAL\s*CONTROL\s*OVER\s*FINANCIAL\s*REPORTING',new_doc[i]):
                stop_index = i

        MDA_text = new_doc[start_index:stop_index]

        return name, MDA_text

    # create the same format used from the function above
    else:
        filing = (re.sub('\\xa0|\\n',' ',doc[doc_num]))
        filing = filing.replace('\n', '').replace('\t', '').replace('\r','').replace('Contents',' ').upper().split('ITEM ')
        new_doc = []
        for item in filing:
            new_doc.append(re.sub('\\xa0*|(?<=[7-8])\W?s?','',item))

    # find the text using the indices
    if len(start_index) == 2 and len(stop_index) == 2:
        if stop_index[-1] - start_index[-1] > 7:
            MDA_text = new_doc[start_index[1]:stop_index[1]]
        else:
            # for JP Morgan
            for i in range(len(new_doc)):
                if re.search(r'CONTENTS\s*FINANCIAL:\s+',new_doc[i]):
                    MDA_text = new_doc[i:]
                    return name,MDA_text
                 # for Chevron
                elif re.search(r'FINANCIAL TABLE OF\s*|BLANK\)\s*INDEX TO MANAGEMENT\W?S DISCUSSION AND ANALYSIS', new_doc[i]):
                    MDA_text = new_doc[i:]
                    return name,MDA_text
                  # for Exxon Mobil
                elif re.search(r'FINANCIAL SECTION\s+TABLE OF\s+CONTENTS\s+BUSINESS PROFILE',new_doc[i]):
                    MDA_text = new_doc[i:]
                    return name,MDA_text
                else:
                    MDA_text = None

    elif len(start_index) > 5:
        MDA_text = new_doc[start_index[-4]:stop_index[-1]]

    elif len(start_index) > 2:
        if stop_index[-1] - start_index[-1] > 4:
            MDA_text = new_doc[start_index[-1]:stop_index[-1]]
        elif stop_index[-1] > start_index[-1]:
            MDA_text = new_doc[start_index[-2]:stop_index[-1]]
        else:
            for i in range(len(new_doc)):
                # for Exxon Mobil
                if re.search(r'FINANCIAL SECTION\s+TABLE OF\s+CONTENTS\s+BUSINESS PROFILE',new_doc[i]):
                    MDA_text = new_doc[i:]
                    return name,MDA_text
                 # for Chevron 2013&2012
                elif re.search(r'FINANCIAL TABLE OF\s*|BLANK\)\s*INDEX TO MANAGEMENT\W?S DISCUSSION AND ANALYSIS',new_doc[i]):
                    MDA_text = new_doc[i:]
                    return name,MDA_text
                else:
                    MDA_text = None

    elif len(start_index) == 1 and stop_index[0] - start_index[0] > 8:
        if name != 'Wells Fargo':
            MDA_text = new_doc[start_index[0]:stop_index[0]]
        else:
            MDA_text = None

    else:
        MDA_text = None


    return name,MDA_text


def getXy(df, string=True):
    '''Input is the Cleaned_MDA df output is the dataframe used to run machine learning algorithms '''
    dic = defaultdict()
    for year in df:
        text = []
        for i in range(len(df)):
            text.extend(df[year][i][1])
        dic[year] = text

    df = pd.DataFrame.from_dict([dic])


    gdp = pd.read_csv('./Sentiment_Analysis_Project/gdp_annual.csv')
    USA = np.array(gdp[gdp['Data Source'] == 'United States'])
    gdp_USA = pd.DataFrame(USA, columns=['Country Name', 'Country COde', 'Indicator Name', 'Indicator Code',
                                                     '1960','1961','1962','1963','1964','1965','1966','1967','1968','1969',
                                                     '1970','1971','1972','1973','1974','1975','1976','1977','1978','1979',
                                                     '1980','1981','1982','1983','1984','1985','1986','1987','1988','1989',
                                                     '1990','1991','1992','1993','1994','1995','1996','1997','1998','1999',
                                                     '2000','2001','2002','2003','2004','2005','2006','2007','2008','2009',
                                                     '2010','2011','2012','2013','2014','2015','2016','2017','2018'])
    gdp_USA = gdp_USA.drop(columns=['Country Name', 'Country COde', 'Indicator Name', 'Indicator Code','1960','1961','1962','1963','1964','1965','1966','1967','1968','1969',
                                                     '1970','1971','1972','1973','1974','1975','1976','1977','1978','1979',
                                                     '1980','1981','1982','1983','1984','1985','1986','1987','1988','1989',
                                                     '1990','1991','1992','1993','1994','1995','1996','1997','1998','1999',
                                                     '2000','2001','2002','2003','2004','2005','2006','2018'])

    y = gdp_USA.transpose()
    X = df.transpose()
    result = pd.concat([X,y],axis=1)
    dataset = pd.DataFrame([np.array(X[0]),np.array(y[0])],columns=['2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017'])
    df = dataset.transpose()
    df.columns=['X','y']
    if string:
        df['X'] = df['X'].map(lambda x: ' '.join(x))
        return df
    else:
        return df
