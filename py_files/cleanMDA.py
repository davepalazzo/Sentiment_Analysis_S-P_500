import requests
from bs4 import BeautifulSoup as bsoup
from collections import defaultdict


def pullMDA(yearRange,compName, resLst):
    '''Pulls MD&A text from exhibit 13 SEC website
        Parameters: 1) yearRange - list of years
                    2) resLst - list of SEC websites
                    3) compName - string of company name
        Returns: Tuple with year and MD&A text
        '''
    output = defaultdict()
    for year in yearRange:
        for site in resLst:
            res = requests.get(site)
            soup = bsoup(res.content,'html.parser')
            text = soup.text
            output[year] = (compName,text)
            break
    return output
