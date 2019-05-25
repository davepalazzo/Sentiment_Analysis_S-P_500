import requests
from bs4 import BeautifulSoup as bsoup
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


