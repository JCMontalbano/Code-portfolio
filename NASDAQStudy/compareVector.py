#python3 compareVector.py JulyFANG 
import pandas as pd
import sys
import os
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
import matplotlib.dates as mdates

#output=sys.argv[1]
output='JulyFANG'
controloutput=str('control'+output+'.csv')
targetoutput=str('target'+output+'.csv')
if os.path.isfile(controloutput)==False:
	print('Target DFs not found :(')
	exit() 

controlDF=pd.read_csv(controloutput,index_col=0, parse_dates=['time'])
targetDF=pd.read_csv(targetoutput,index_col=0, parse_dates=['time'])

#init lists
timelist=targetDF.time
tVectorlist=[]
cVectorlist=[]
cSTDlist=[]
VectorRatiolist=[]

for row in targetDF.iterrows():
	values=row[1][1:]
	rowAverage=values.mean()
	tVectorlist.append(rowAverage)#address row except for date somehow

for row in controlDF.iterrows():
	values=row[1][1:]	
	rowAverage=values.mean()
	rowSTD=values.std()
	cVectorlist.append(rowAverage)
	cSTDlist.append(rowSTD)

DF=pd.DataFrame()
DF['date']=timelist
DF['TVector']=tVectorlist
DF['CVector']=cVectorlist
DF['CSTD']=cSTDlist

for row in DF.iterrows():
	TVector=row[1][1]
	CVector=row[1][2]
	VectorRatio=TVector/CVector
	VectorRatiolist.append(VectorRatio)	

DF['VRatio']=VectorRatiolist

plt.title('Change in target group \n'+str(list(targetDF.columns)[1:])+'\n relative to control group')

# format the ticks
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator())

maxRat=DF.VRatio.max()
for row in DF.iterrows():
	date=row[1][0]
	ratio=abs(row[1][4])/maxRat #take abs() so it works regardless of negatives
	#print(ratio)
	plt.axvspan(date, date+dt.timedelta(days=1), color='red', alpha=ratio)

plt.plot(DF['date'],DF['CVector'], color='grey', linewidth=7.0)
for column in targetDF.columns[1:]:
	plt.plot(DF['date'],targetDF[column],color='black', linewidth=0.7)

plt.xticks(rotation=90)
filename=output+'.png'
plt.savefig(filename)
