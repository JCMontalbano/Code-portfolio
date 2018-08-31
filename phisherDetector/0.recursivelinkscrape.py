#example call:
#search rapid7 structure to gather 10,000 links:
#python3 recursivelinkscrape.py https://rapid7.com rapid7 10000 

#it finds github properties, offsite hosted libraries, etc which are 
#still a structured part of the organization's internet presence
#ie https://travis-ci.org showing up for rapid7. 
#I blacklisted web.archive.org because it prevents the unlimited scan
# from terminating.
#The scraper also finds procedurally generated lists; we could probably 
# procedurally solve their list generating protocols from this data

#next step with this data is in 1.recursiveTextScan.py, which collects 
#the text from these links. You don't actually need to run this script.
#This script preserves the outward-pointing link list as a procedurally generated csv
#the name from the procedurally generated outlink csv is used as a cue in the next stage, 
#when I use the outlinks to pull a list of related ngrams as a counter-filter for the most
#common ngrams in the rapid7 site; this allows to avoid false positives on in-industry links
#by targeting word choices specific to the target company.
import pandas as pd
import sys
import requests
from bs4 import BeautifulSoup as bs

#arg1: target URL, arg2: keyword limiter, arg3: result limit, set limit=0 for unlimited search
#_URL='https://rapid7.com';_KEY='rapid7';_LIMIT=10000
_URL=sys.argv[1];_KEY=sys.argv[2];_LIMIT=int(sys.argv[3])
linkname=str(_KEY)+'.'+str(_LIMIT)+'.links.csv'
outlinkname=str(_KEY)+'.'+str(_LIMIT)+'.outlinks.csv'
errlinkname=str(_KEY)+'.'+str(_LIMIT)+'.errlinks.csv'
#blacklist=[] #put the empty blacklist on 
blacklist='web.archive.org' #filter out links including these phrases
#blacklist allows it to avoid falling into recursive scrapes of 
#internet-recorders like web.archive.org

def getLinks(url,filterKey):
	howManyLinks=0
	try:
		print('*** Getting links from:'+url+' ***')
		response = requests.get(url)
		data = response.text
		soup = bs(data, 'lxml')
		#links = []
		for links in soup.find_all('a'):
			link = links.get('href')
			if (link is not None) and (link.startswith('http')) and (str(filterKey) in link) and (link not in linklist) and blacklist not in link: #awkward blacklist, only allows 1 term rn
				howManyLinks+=1
				linklist.append(link)
				print('Adding in-network link:'+link)
			if (link is not None) and (link.startswith('http')) and (str(filterKey) not in link) and (link not in outlinklist):
				outlinklist.append(link)
				print('Adding out-network link:'+link)
	except Exception as ex:
		print(ex)
		print('Adding error-generating link: '+url)
		errorlist.append(url)
	return howManyLinks
	
def getRecursiveUnlimited(url,filterKey):
	count=0
	getLinks(_URL,_KEY) #initiate list
	totalLinks=len(linklist)
	for link in linklist:
		newLinks=getLinks(link,_KEY)
		count+=1
		totalLinks+=newLinks
		percentcomplete=(count/totalLinks)
		percentstring='{:.1%}'.format(percentcomplete)
		print('Total links found: '+str(len(linklist))+'\t Links searched:'+str(count)+'\t Percent Complete:'+percentstring)
	#done=True

def getRecursiveLimited(url,filterKey,limit):
	count=0
	getLinks(_URL,_KEY) #initiate list
	totalLinks=len(linklist)
	for link in linklist:
		newLinks=getLinks(link,_KEY)
		totalLinks+=newLinks
		count+=1
		percentcomplete=(count/limit);percentstring='{:.1%}'.format(percentcomplete)
		print('Total links found: '+str(len(linklist))+'\t Links scanned:'+str(count)+'\t Percent Complete:'+percentstring)
		if totalLinks>limit:break
	
##############################
#operating code begins below:#
##############################
linklist,outlinklist,errorlist=[],[],[]

if _LIMIT==0: #if the limit=0, use unlimited length fcn
	getRecursiveUnlimited(_URL,_KEY)
else:
	getRecursiveLimited(_URL,_KEY,_LIMIT)
#while done==False:
#	ContinueRecursive(_URL,_KEY)

print('Linklist length:'+str(len(linklist)))
linkDF=pd.DataFrame()
linkDF['links']=linklist
linkDF.to_csv(linkname)
print('Outward-pointing linklist length:'+str(len(outlinklist)))
outlinkDF=pd.DataFrame()
outlinkDF['outlinks']=outlinklist
outlinkDF.to_csv(outlinkname)
print('Error-generating linklist length:'+str(len(errorlist)))
errlinkDF=pd.DataFrame()
errlinkDF['errlinks']=errorlist
errlinkDF.to_csv(errlinkname)
