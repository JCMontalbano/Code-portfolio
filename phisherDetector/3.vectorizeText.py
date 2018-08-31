#example call:
#python3 3.vectorizeText.py rapid7 10000
#############################################
#This script takes the text scans from 1.recursiveTextScan.py 
#and 2.countersample.py, word-tokenizes them, counts the most 
#frequently occurring 1, 2, 3 and 4 word phrases, eliminates 
#duplicates, producing a list of 40 key ngrams. It then goes 
#through each list of text scans, counting key phrases and performing
#sentiment analysis. Each entry is tagged as coming from the in
#network or out-network scan with a binary value, 'whichCorpus'.
#The resulting two vectorized DFs are concatenated and saved to
#a single file, vectorOutput.
import pandas as pd
import sys
import datetime
#NLTK packages:
from nltk import word_tokenize, sent_tokenize, ngrams, FreqDist
from nltk.sentiment.vader import SentimentIntensityAnalyzer

#procedurally generated filenames which work through the whole process:
#_KEY='rapid7';_LIMIT=10000 #these must address a previously produced scan file
_KEY=sys.argv[1];_LIMIT=sys.argv[2] 
inScanName=str(_KEY)+'.'+str(_LIMIT)+'.scan.csv' #'scan' differentiates linklist from linklist with text included
outScanName=str(_KEY)+'.'+str(_LIMIT)+'.outScan.csv'
vectorOutput=str(_KEY)+'.'+str(_LIMIT)+'.vector.csv'
reportfile='ClassifierLog.txt'

#function for n<5 ngram counts
def ngramList(corpus):
	words=word_tokenize(corpus)
	print('Finding most frequent words...')
	gram1list=[]
	gram1=FreqDist(ngrams(words,1))
	freq1=FreqDist(gram1)
	count=0
	for ngram in freq1:
		count+=1
		gram1string=ngram[0]
		print(gram1string)
		gram1list.append(gram1string)
		if count>100:break
	print('Finding top bigrams...')
	gram2list=[]
	gram2=FreqDist(ngrams(words,2))
	freq2=FreqDist(gram2)
	count=0
	for ngram in freq2:
		count+=1
		gram2string=ngram[0]+' '+ngram[1]
		print(gram2string)
		gram2list.append(gram2string)
		if count>100:break
	print('Finding top trigrams...')
	gram3list=[]
	gram3=FreqDist(ngrams(words,3))
	freq3=FreqDist(gram3)
	count=0
	for ngram in freq3:
		count+=1
		gram3string=ngram[0]+' '+ngram[1]+' '+ngram[2]
		print(gram3string)
		gram3list.append(gram3string)
		if count>100:break
	print('Finding top tetragrams...')
	gram4list=[]
	gram4=FreqDist(ngrams(words,4))
	freq4=FreqDist(gram4)
	count=0
	for ngram in freq4:
		count+=1
		gram4string=ngram[0]+' '+ngram[1]+' '+ngram[2]+' '+ngram[2]
		print(gram4string)
		gram4list.append(gram4string)
		if count>100:break
	return(gram1list,gram2list,gram3list,gram4list)

#sentiment analysis, VADER = (Valence Aware Dictionary and sEntiment Reasoner)
def SentimentAnalyze(text):
	sentences=sent_tokenize(text)
	if len(sentences)>0:
		neulist=[];poslist=[];neglist=[];comlist=[]
		for sentence in sentences:
			ss = sid.polarity_scores(sentence)
			neulist.append(ss['neu'])
			poslist.append(ss['pos'])
			neglist.append(ss['neg'])
			comlist.append(ss['compound'])
		#get average values
		neu=sum(neulist)/len(neulist)
		pos=sum(poslist)/len(poslist)
		neg=sum(neglist)/len(neglist)
		compound=sum(comlist)/len(comlist)
	else:
		neg,pos,neu,compound=0,0,0,0
	return(neg,pos,neu,compound)

sid = SentimentIntensityAnalyzer() #initialize it

#function to tokenize a text corpus 
def tokenizeCorpus(corpusDF,whichCorpus):#whichCorpus should be int, 1 or 0
	VectorDF=pd.DataFrame(columns=['neg','pos','neu','compound',gramlist[0],
		gramlist[1],gramlist[2],gramlist[3],gramlist[4],gramlist[5],
		gramlist[6],gramlist[7],gramlist[8],gramlist[9],gramlist[10],
		gramlist[11],gramlist[12],gramlist[13],gramlist[14],gramlist[15],
		gramlist[16],gramlist[17],gramlist[18],gramlist[19],gramlist[20],
		gramlist[21],gramlist[22],gramlist[23],gramlist[24],gramlist[25],
		gramlist[26],gramlist[27],gramlist[28],gramlist[29],gramlist[30],
		gramlist[31],gramlist[32],gramlist[33],gramlist[34],gramlist[35],
		gramlist[36],gramlist[37],gramlist[38],gramlist[39],'AvgLength',
		'whichCorpus'])
	for page in corpusDF.iterrows():
		pagetext=page[1][1]
		row=[]
		neg,pos,neu,compound=SentimentAnalyze(pagetext)
		wtoken=word_tokenize(pagetext)
		key0=(wtoken.count(gramlist[0]))
		key1=(wtoken.count(gramlist[1]))
		key2=(wtoken.count(gramlist[2]))
		key3=(wtoken.count(gramlist[3]))
		key4=(wtoken.count(gramlist[4]))
		key5=(wtoken.count(gramlist[5]))
		key6=(wtoken.count(gramlist[6]))
		key7=(wtoken.count(gramlist[7]))
		key8=(wtoken.count(gramlist[8]))
		key9=(wtoken.count(gramlist[9]))
		key10=(wtoken.count(gramlist[10]))
		key11=(wtoken.count(gramlist[11]))
		key12=(wtoken.count(gramlist[12]))
		key13=(wtoken.count(gramlist[13]))
		key14=(wtoken.count(gramlist[14]))
		key15=(wtoken.count(gramlist[15]))
		key16=(wtoken.count(gramlist[16]))
		key17=(wtoken.count(gramlist[17]))
		key18=(wtoken.count(gramlist[18]))
		key19=(wtoken.count(gramlist[19]))
		key20=(wtoken.count(gramlist[20]))
		key21=(wtoken.count(gramlist[21]))
		key22=(wtoken.count(gramlist[22]))
		key23=(wtoken.count(gramlist[23]))
		key24=(wtoken.count(gramlist[24]))
		key25=(wtoken.count(gramlist[25]))
		key26=(wtoken.count(gramlist[26]))
		key27=(wtoken.count(gramlist[27]))
		key28=(wtoken.count(gramlist[28]))
		key29=(wtoken.count(gramlist[29]))
		key30=(wtoken.count(gramlist[30]))
		key31=(wtoken.count(gramlist[31]))
		key32=(wtoken.count(gramlist[32]))
		key33=(wtoken.count(gramlist[33]))
		key34=(wtoken.count(gramlist[34]))
		key35=(wtoken.count(gramlist[35]))
		key36=(wtoken.count(gramlist[36]))
		key37=(wtoken.count(gramlist[37]))
		key38=(wtoken.count(gramlist[38]))
		key39=(wtoken.count(gramlist[39]))
		#visible text registering as 0 sentences gives a divide-by-zero error, so we do this
		if len(sent_tokenize(pagetext))>0: 
			AvgLength= len(word_tokenize(pagetext))/len(sent_tokenize(pagetext)) #average sentence length, in words
		else:AvgLength=0
		row=[neg,pos,neu,compound,key0,key1,key2,key3,key4,key5,key6,key7,key8,
		key9,key10,key11,key12,key13,key14,key15,key16,key17,key18,key19,key20,
		key21,key22,key23,key24,key25,key26,key27,key28,key29,key30,key31,key32,
		key33,key34,key35,key36,key37,key38,key39,AvgLength,int(whichCorpus)]
		print(row)
		VectorDF.loc[len(VectorDF)]=row
	return VectorDF

##############################
#operating code begins below:#
##############################

#Load the text scan DFs for in-network and out-network links
inDF=pd.read_csv(inScanName,index_col=0)
inDF=inDF.applymap(str)
outDF=pd.read_csv(outScanName,index_col=0)
outDF=outDF.applymap(str)


#create a corpus of text for tokenizing
inCorpus='';outCorpus=''
print('Creating in-link text corpus...')
for text in inDF['text']:
	inCorpus=inCorpus+' '+text

print('Creating out-link text corpus...')
for text in outDF['text']:
	outCorpus=outCorpus+' '+text

#count word freqs
print('Counting words...')
in1gram,in2gram,in3gram,in4gram=ngramList(inCorpus)
out1gram,out2gram,out3gram,out4gram=ngramList(outCorpus)

#eliminate duplicates, select top 10 of each gram
gram1=list(set(in1gram)-set(out1gram))[:10]
gram2=list(set(in2gram)-set(out2gram))[:10]
gram3=list(set(in3gram)-set(out3gram))[:10]
gram4=list(set(in4gram)-set(out4gram))[:10]

gramlist=gram1+gram2+gram3+gram4

#tokenize both datasets and produce tokenized DFs for training inputs
inTokenDF=tokenizeCorpus(inDF,0)
outTokenDF=tokenizeCorpus(outDF,1)
vectorDF=pd.concat([inTokenDF,outTokenDF], axis=0)
vectorDF.to_csv(vectorOutput)
print('Done! '+vectorOutput+' saved.')
now=datetime.datetime.now().strftime('%m/%d/%y %H:%M')
open(reportfile,'a').write(str(now)+': Text vector complete for project '+vectorOutput+'\n')
open(reportfile,'a').write('Most common 1grams:'+str(gram1)+'\n')
open(reportfile,'a').write('Most common 2grams:'+str(gram2)+'\n')
open(reportfile,'a').write('Most common 3grams:'+str(gram3)+'\n')
open(reportfile,'a').write('Most common 4grams:'+str(gram4)+'\n')
