#example call:
#python3 2.countersample.py rapid7 10000
#############################################
#This script does the same text scan as in 1.recursiveTextScan.py, 
#but now it is scanning the out-of-network links generated before.
import pandas as pd
import sys

import urllib.request
import requests
from bs4 import BeautifulSoup as bs
from bs4.element import Comment
from nltk import word_tokenize

#procedurally generated filenames which work through the whole process:
#_KEY='rapid7';_LIMIT=10000 #these must address a previously produced scan file
_KEY=sys.argv[1];_LIMIT=sys.argv[2] 
inputname=str(_KEY)+'.'+str(_LIMIT)+'.scan.csv' #'scan' differentiates linklist from linklist with text included
outlinkname=str(_KEY)+'.'+str(_LIMIT)+'.outlinks.csv'
outlinkScanOutput=str(_KEY)+'.'+str(_LIMIT)+'.outScan.csv'
errlinkname=str(_KEY)+'.'+str(_LIMIT)+'.errlinks.csv'

#The below are functions to recursively scrape links, and the text of those links:
def getLinksAntiScan(url,filterKey):
	howManyLinks=0
	try:
		print('*** Getting links from:'+url+' ***')
		response = requests.get(url)
		data = response.text
		soup = bs(data, 'lxml')
		#links = []
		for links in soup.find_all('a'):
			link = links.get('href')
			if (link is not None) and (link.startswith('http')) and (str(filterKey) not in link) and (link not in outlinklist):
				outlinklist.append(link)
				howManyLinks+=1
				print('Adding out-network link:'+link)
	except Exception as ex:
		print(ex)
		print('Adding error-generating link: '+url)
		#errorlist.append(url)
	return howManyLinks

def AntiScanRecursive(filterKey,limit): #'anti-scan' filters in the opposite direction from the filterkey, and starts with an existing outlinkDF
	totalLinks=len(outlinklist)
	antiScanDF=pd.DataFrame(columns=['link','text'])
	count=0
	for link in outlinklist:
		newText=getText(link)
		newLinks=getLinksAntiScan(link,_KEY)
		totalLinks+=newLinks
		count+=1#needs to not count upunless it gets a hit, this with try:
		percentcomplete=(count/limit);percentstring='{:.1%}'.format(percentcomplete)
		#add a row to the DF
		row=[link,newText]
		antiScanDF.loc[len(antiScanDF)]=row
		print('Outward-pointing links found: '+str(len(outlinklist))+'\t Outward-pointing links scanned:'+str(count)+'\t Percent Complete:'+percentstring)
		if count>limit:break
		if count%1000==0: #save the DF every 1000 links
			print('Saving backup:')
			antiScanDF.to_csv(outlinkScanOutput)
	return antiScanDF

def tag_visible_text(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def getText(url):
	try:
		html = urllib.request.urlopen(url).read()
		soup = bs(html, 'html.parser')
		texts = soup.findAll(text=True)
		visible_texts = filter(tag_visible_text, texts)  
		return u" ".join(t.strip() for t in visible_texts)
	except Exception as ex:
		print(ex)
		print('Adding error-generating link: '+url)
		return '' #it has to return the empty text		errorlist.append(url)

##############################
#operating code begins below:#
##############################

scanDF=pd.read_csv(inputname,index_col=0)
outlinkDF=pd.read_csv(outlinkname,index_col=0)
errorDF=pd.read_csv(errlinkname,index_col=0)
outlinklist=outlinkDF['outlinks']
errorlist=errorDF['errlinks']

controlScanLength=len(scanDF)*1.2
antiscanDF=AntiScanRecursive(_KEY,controlScanLength)
print('Anti-scan complete, saved to:'+outlinkScanOutput)
antiscanDF.to_csv(outlinkScanOutput)
