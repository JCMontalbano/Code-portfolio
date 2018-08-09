#python3 stockScrapeIEX.py JulyFANG 5 'FB AMZN NFLX GOOGL TWTR SNAP' '2018-07-01' '2018-08-06'
from datetime import datetime, timedelta
import time
import ast
import pandas as pd
from pandas import DataFrame
import pandas_datareader.data as web
import sys
import os

#check if file is done, exit program if yes
output=sys.argv[1]
controloutput=str('control'+output+'.csv')
targetoutput=str('target'+output+'.csv')
if os.path.isfile(controloutput)==True:
	exit() 

delay=int(sys.argv[2])
targetlist=sys.argv[3].split()
print('Target companies:'+str(targetlist))
#generate control list:
NASDAQ=pd.read_csv('NASDAQ.csv') #a list of nasdaq symbols
controllist=NASDAQ.sample(frac=50/len(NASDAQ))['Symbol'].tolist() #50 random symbols. NASDAQ length=3300, limits target list to 66 targets
print('Control companies:'+str(controllist))

startDT=datetime.strptime(sys.argv[4],'%Y-%m-%d')
endDT=datetime.strptime(sys.argv[5],'%Y-%m-%d')
print('Start date:'+str(startDT)+', end date:'+str(endDT))

DataSource='iex' #easy to change in pandas_datareader


#start the DF using the dates in the response. This matches non-trading days
outputDF=pd.DataFrame()
timelist=[]
timeDF=web.DataReader(controllist[0], DataSource, startDT, endDT)
for row in timeDF.iterrows():
	timeVal=datetime.strptime(row[0],'%Y-%m-%d') #parse as datetime
	timelist.append(timeVal)

#timelist=pd.date_range(start=startDT,end=endDT, freq='D')
print('Timelist length:'+(str(len(timelist))))
outputDF['time']=timelist
del(timeDF)
print('Length of default timelist:'+str(len(outputDF)))

def Vectorize(DF):
	VectorList=[]
	for row in DF.iterrows():
		openVal=float(row[1]['open'])
		closeVal=float(row[1]['close'])
		if openVal==0:
			deltaVal=0
		else: deltaVal=(closeVal/openVal)-1 #percent values
		VectorList.append(deltaVal) #append it to the list
	return(VectorList)

#for each company in the list, 
targetDF['time']=timelist
for company in targetlist:
	print(str(company))
	DF=web.DataReader(company, DataSource, startDT, endDT)	
	Vlist=Vectorize(DF)
	if len(Vlist)==len(targetDF):
		targetDF[company]=Vlist
	time.sleep(delay)

controlDF['time']=timelist
for company in controllist:
	print(str(company))
	DF=web.DataReader(company, DataSource, startDT, endDT)	
	Vlist=Vectorize(DF)
	if len(Vlist)==len(controlDF):
		controlDF[company]=Vlist
	time.sleep(delay)

targetDF.to_csv(targetoutput)
controlDF.to_csv(controloutput)

'''
date code for a fixed date using .now(), I should implement this as defaults in case of empty date-args:
endDT = datetime.now() #end of window is today
startDT=nowDT-timedelta(days=(2*365))
'''
