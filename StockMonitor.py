"""
Created Aug. 6 2018
Branden Lisk
NASDAQ Stock Monitor in python 3.6.2

This command line program allows the user to:
-Obtain real-time information about a stock, sourced from Yahoo Finance
-Search an up-to-date dictionary by stock name or stock symbol
-Add stocks to monitoring for comparison. This data is saved to a file and is available
the next time the user opens the program

Data scraped from ca.finance.yahoo.com and nasdaqtrader.com
"""

import sys
import urllib.request
import re
import os

# Define dictionaries containing stock names and symbols
stockDictNames = {} #This dictionary has stock NAMES as the key
stockDictSymbols = {} #This dictionary has stock SYMBOLS as the key

## This method compiles all stock symbols and names into a dictionary
def createStockDict():
  #Data sourced from ftp source of nasdaqtrader.com
  stockListFile = urllib.request.urlopen('ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt')
  stockData = stockListFile.read().decode('utf-8')
  stockTuples = re.findall(r'\n(\w+)\|([\w\s,.]*)', stockData)
  
  for data in stockTuples:
    stockDictNames[data[1]] = data[0]
    stockDictSymbols[data[0]] = data[1]
  
## This method allows the dictionary to be searched by name or symbol, prints the results
## Takes two parameters: The string that is being searched, and the boolean flag
## boolean flag: True if searching by name, False if searching by symbol
def searchDict(searchString, nameFlag):
  resultList = [] #initialize the list to store results of the search
  foundResult = False
  
  if nameFlag: #if searching by name:
    for name in stockDictNames:
      if name.startswith(searchString):
        foundResult = True
        resultList.append(name + '- ' + stockDictNames[name])
  else: #if searching by symbol:
    for symbol in stockDictSymbols:
      if symbol.startswith(searchString):
        foundResult = True
        resultList.append(symbol + ' - ' + stockDictSymbols[symbol])
  
  if foundResult: #print all results of the search
    print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nFound %d Results:' %(len(resultList)))
    for result in resultList:
      print (result)
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
  else:
    print ('\n~~~~~~~~~~~~~~~~~~\nNo Results Found\n~~~~~~~~~~~~~~~~~~')
  

## This method fetches the url data of the stock from Yahoo Finance, and scrapes certain data
## Takes one parameter: (a string) the full stock symbol of any stock. Prints the result.
def printStockData(stockName):
  try:
    url = 'https://ca.finance.yahoo.com/quote/'+stockName+'?p='+stockName
    stockFile = urllib.request.urlopen(url)
    html = stockFile.read().decode('utf-8')
    
    #Current Price
    #use regular expressions to scrape data
    closeMatch = re.search(r'"regularMarketPrice":\{"raw":([\w.]+)', html)
    closePrice = (closeMatch.group(1))
    
    #Previous Close Price
    previousMatch = re.search(r'"regularMarketPreviousClose":\{"raw":([\w.]+)', html)
    previousPrice = (previousMatch.group(1))
    
    #Market Cap
    capMatch = re.search(r'"marketCap":\{"raw":[\w.]+,"fmt":"([\w.]+)', html)
    marketCap = (capMatch.group(1))
    
    ##This section prints all stock info
    print (
    '''
  ---------------------------------
    Stock: %s
    Current stock price: $%s
    Previous close price: $%s
    Market cap: %s
  ---------------------------------'''
    % (stockName, closePrice, previousPrice, marketCap))
  except:
    print('\nInvalid stock symbol, please enter the full stock symbol.')


###### NOTE: The following methods are for modifying the save file 'stockSave.txt',
#            which is used to save stock monitoring data.

## This method returns all stocks from the file as a list
## Takes no parameters, returns a list
def returnFile():
  stockList = []
  f = open('stockSave.txt', 'r') #open the file for reading
  for line in f: #append each items to a list
    stockList.append(line[:-1]) #splice each string, to remove the '\n' on each of the lines
  return stockList

## This method deletes a current stock from the file
## Takes one parameter: a full symbol of a stock
## NOTE: This method should only be used when there are items in the file
def deleteStockFromFile(stockSymbol):
  f = open('stockSave.txt', 'r')
  stockList = []
  for line in f: #add all items from file to a list
    stockList.append(line)
  stockList.remove(stockSymbol+'\n') #remove item from list
  f.close()
  f = open('stockSave.txt', 'w')
  for item in stockList: #write new list back into file
    f.write(item)
  f.close()

## This method adds a stock name to the file
## Take one parameter (a string): a full symbol of a stock
def addStockToFile(stockSymbol):
  f = open('stockSave.txt', 'a')
  f.write(stockSymbol + '\n')
  f.close()

#######

def main():
  createStockDict() #call the method to create the initial dictionaries of the stocks
  #check if file already exists. If not, create the initial save file
  if os.path.exists('stockSave.txt') == False:
    f = open('stockSave.txt', 'w') #create the initial file
    f.close()
  
  #This prints the intro to the program
  print(
  '''
----------------------------------------
  Welcome to the NASDAQ Stock Monitor!
----------------------------------------''')
  quit = False #This defines the quite flag, so if the user enters 'quit', the program exits
  while quit == False:
    #This prints the menu that prompts the user to enter a selection
    print(
      '''
-------------------------------------------
  Enter the number of an option below:
  1. Obtain data about a stock
  2. Search for a stock by name
  3. Search for a stock by symbol
  4. Enter Stock Monitoring Mode
    
  Type the word 'quit' to quit
-------------------------------------------
    ''')
    option = str(input("Enter choice: ")) #prompt the user for a choice using command line input; convert to string
    
    #1.Obtain data about a stock:
    if option == '1':
      back = False #define back flag
      while back == False:
        stockName = input("\nEnter a stock symbol, or type 'back' to return to the main menu: ") #prompt for a stock name
        if stockName.lower() == 'back': #test if user wants to go back to previous menu
          back = True
        else:
          if stockName.upper() in stockDictSymbols: #test if the entered stock exists by comparing it to the dictionary
            printStockData(stockName.upper()) #calls method to print info about a stock
          else: #if stock does not exists, print message to inform user
            print ('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nStock not found, enter a complete stock symbol.\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
          
    #2.Search for a stock by name:
    elif option == '2':
      back = False
      while back == False:
        search = input("\nEnter first letters of stock name, or type 'back' to return to the main menu: ")
        if search.lower() == 'back':
          back = True
        else:
          searchDict(search, True) #calls method to search the appropriate dictionary
          
    #3.Search for a stock by symbol:
    elif option == '3':
      back = False
      while back == False:
        search = input("\nEnter the first part, or the complete stock symbol, or type 'back' to return to the main menu: ")
        if search.lower() == 'back':
          back = True
        else:
          searchDict(search.upper(), False) #calls method to search the appropriate dictionary
          
    #4.Enter Stock Monitoring Mode
    elif option == '4':
      back = False
      while back == False:
        print ('\nCurrent Stock Monitoring:')
        for stock in returnFile(): #call method to return a list of all strings in the file
          printStockData(stock) #call method to print stock data about each stock in the file
        
        #prompt for user to enter a stock
        search = input("\nEnter a stock symbol to be added or deleted, or type 'back' to return to the main menu: ")
        if search.lower() == 'back':
          back = True
        else:
          if search.upper() in stockDictSymbols: #test if the entered stock exists by comparing it to the dictionary
            if search.upper() in returnFile(): #test if stock is already being monitored
              #if so, delete it from the file and print the delete message
              deleteStockFromFile(search.upper())
              print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'+search.upper()+' deleted from monitoring\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            else:
              #if not, add it to the file and print the added message
              addStockToFile(search.upper())
              print('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n'+search.upper()+' added to monitoring\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
          else: #if stock does not exists, print message to inform user
            print ('\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nStock not found, enter a complete stock symbol.\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            
    #Option to quit program
    elif option.lower() == 'quit':
      print('Exiting Program...')
      quit = True
      
    #Any other invalid choices
    else:
      print('\nInvalid Option. Try Again')
  
  
  

if __name__ == '__main__': ##standard code
  main()