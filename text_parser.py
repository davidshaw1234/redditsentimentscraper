#this module will take a string and return a list of tickers in the post
#does not care about company names, as only big companies tend to have their names fully said on reddit
import pandas as pd
#from nltk.corpus import stopwords
#from nltk.tokenize import word_tokenize

#import spacy


#nlp = spacy.load("en_core_web_sm")


#list of tickers to be analyzed
tickerinfo = []
data = pd.read_csv('NYSE-NASDAQ-TICKERS.csv')
tickerinfo = list(data.ticker)


#helper method
#takes a list of str as input and returns a list containing unique valid tickers
def getTickerList(l):
    returnList = []
    for value in l:
        if value.upper() in tickerinfo:
            returnList.append(value.upper())
    #converts to a set to remove duplicates then reconverts to list
    return list(set(returnList))

#helper method
#returns a string containing spaces where punctuation was, does not remove $ unless specified with True input
def symbol_remover(strinput,removeDollar):
    if removeDollar:
        chars = "!@#%^&*()-_=+[]}{\|;:<>,./?1234567890$"
        for c in chars:
            if c in strinput:
                strinput = strinput.replace(c,' ')
        return strinput.replace('"',' ').replace("'"," ")
    else:
        chars = "!@#%^&*()-_=+[]}{\|;:<>,./?1234567890"
        for c in chars:
            if c in strinput:
                strinput = strinput.replace(c,' ')
        return strinput.replace('"',' ').replace("'"," ")
    
    
#helper method
#nltk library
#takes a list of str and returns a list of str
#removes stopwords
def remove_stopwords(l):
    return_list = []
    stop_words = set(stopwords.words('english'))
    for word in l:
        if word.lower() not in stop_words:
            return_list.append(word)
    return return_list


#helper method
#returns true if input str is in nyse or nasdaq, false ow
def isOnEx(strinput):
    if strinput.upper() in tickerinfo:
        return True
    else:
        return False




#FUNCTION TO USE version1
#takes input a str
#returns a list containing tickers in the str, will return an empty list if no tickers are found
def ticker_parse1(strinput):
    strinput = symbol_remover(strinput,False)
    firstlist = strinput.split()

    secondlist = []
    for word in firstlist:
        if len(word) <=6:
            secondlist.append(word)

    potent_ticker_v_1 = []
    for word in secondlist:
        if '$' in word and len(word) > 1:
            potent_ticker_v_1.append(word.replace('$','').upper())
        elif word.isupper():
            potent_ticker_v_1.append(word)
        else:
            next
    return getTickerList(potent_ticker_v_1)


#FUNCTION TO USE version2
def ticker_parse2(strinput):
    strinput = symbol_remover(strinput.lower(),True)
    firstlist = strinput.split()

    secondlist = remove_stopwords(firstlist)
    thirdlist = []
    for word in secondlist:
        if len(word) <=6:
            thirdlist.append(word)
    return getTickerList(thirdlist)

#FUNCTION TO USE version3 <<<<< CURRENTLY USING
#third ticker method, ignores single letter stock tickers unless they have $ in front of them
def ticker_parse3(strinput):
    strinput = symbol_remover(strinput,False)
    firstlist = strinput.split()
    #first filter
    secondlist = []
    for word in firstlist:
        if len(word) <=6 and len(word) > 1:
            secondlist.append(word)


    potent_ticker_v_1 = []
    #second filter
    for word in secondlist:
        if '$' in word and len(word) > 1:
            potent_ticker_v_1.append(word.replace('$','').upper())
        elif word.isupper() and len(word) > 1:
            potent_ticker_v_1.append(word)
        elif isOnEx(word):
            potent_ticker_v_1.append(word)
        else:
            next
    #final filter
    return getTickerList(potent_ticker_v_1)

