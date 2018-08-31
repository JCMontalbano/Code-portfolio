#example call:
#python3 1.recursiveTextScan.py https://rapid7.com rapid7 10000
#############################################
#this script scans the text of the in-network links and saves it in 
#the output, which is a csv with two columns, link and its visible text
import pandas as pd
import sys
#for recursive link scrape
from bs4 import BeautifulSoup as bs
import requests
#for text scrape
from bs4.element import Comment
import urllib.request

#procedurally generated filenames which work through the whole process:
#_URL='https://rapid7.com';_KEY='rapid7';_LIMIT=10000
_URL=sys.argv[1];_KEY=sys.argv[2];_LIMIT=int(sys.argv[3])
output=str(_KEY)+'.'+str(_LIMIT)+'.scan.csv' #'scan' differentiates linklist from linklist with text included
outlinkname=str(_KEY)+'.'+str(_LIMIT)+'.outlinks.csv'
errlinkname=str(_KEY)+'.'+str(_LIMIT)+'.errlinks.csv'

#The below are functions to recursively scrape links:
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
			if (link is not None) and (link.startswith('http')) and (str(filterKey) in link) and (link not in linklist):
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
	
def scanRecursiveUnlimited(url,filterKey): #scans text and links
	linkDF=pd.DataFrame(columns=['link','text'])
	count=0
	getLinks(_URL,_KEY) #initiate list
	totalLinks=len(linklist)
	for link in linklist:
		newText=getText(link)
		newLinks=getLinks(link,_KEY)
		count+=1
		totalLinks+=newLinks
		percentcomplete=(count/totalLinks)
		#add a row to the DF
		row=[link,newText]
		linkDF.loc[len(linkDF)]=row
		percentstring='{:.1%}'.format(percentcomplete)
		print('Total links found: '+str(len(linklist))+'\t Links scanned:'+str(count)+'\t Percent Complete:'+percentstring)
		if count%1000==0: #save the DF every 1000 links
			print('Saving backup:')
			linkDF.to_csv(output)
	return linkDF

def scanRecursiveLimited(url,filterKey,limit): #scans text and links
	linkDF=pd.DataFrame(columns=['link','text'])
	count=0
	getLinks(_URL,_KEY) #initiate list
	totalLinks=len(linklist)
	for link in linklist:
		newText=getText(link)
		newLinks=getLinks(link,_KEY)
		totalLinks+=newLinks
		count+=1
		percentcomplete=(count/limit);percentstring='{:.1%}'.format(percentcomplete)
		#add a row to the DF
		row=[link,newText]
		linkDF.loc[len(linkDF)]=row
		print('Total links found: '+str(len(linklist))+'\t Links scanned:'+str(count)+'\t Percent Complete:'+percentstring)
		if totalLinks>limit:break
		if count%1000==0: #save the DF every 1000 links
			print('Saving backup:')
			linkDF.to_csv(output)
	return linkDF

#The below are functions to scrape visible text from a page:
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
		errorlist.append(url)
		return '' #it has to return the empty text
	


##############################
#operating code begins below:#
##############################


linklist,outlinklist,errorlist=[],[],[]

if _LIMIT==0: #if the limit=0, use unlimited length fcn
	scanDF=scanRecursiveUnlimited(_URL,_KEY)
else:
	scanDF=scanRecursiveLimited(_URL,_KEY,_LIMIT)
#while done==False:
#	ContinueRecursive(_URL,_KEY)

print('Linklist length:'+str(len(linklist)))
scanDF.to_csv(output)
print('Outward-pointing linklist length:'+str(len(outlinklist)))
outlinkDF=pd.DataFrame()
outlinkDF['outlinks']=outlinklist
outlinkDF.to_csv(outlinkname)
print('Error-generating linklist length:'+str(len(errorlist)))
errlinkDF=pd.DataFrame()
errlinkDF['errlinks']=errorlist
errlinkDF.to_csv(errlinkname)