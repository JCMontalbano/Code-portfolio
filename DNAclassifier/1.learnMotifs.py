#example call:
#long: python3 1.learnMotifs.py motifs_escherica_coli.txt motifs_pseudomonas_aeruginosa.txt ecolimotifs1020.csv paerugmotifs1020.csv

#This script accepts large single line sequence files, and scans them for the most common recurring motifs
#Arg 1: first motif trainer; Arg 2: second motif trainer
#Arg3: output motiflist for Arg1; Arg4: output motiflist for Arg2
#############################################

import HTSeq, sys
from nltk import FreqDist
from collections import Counter
import pandas as pd

#############################
#	FUNCTIONS				#
#############################

def tokenizeDNARead(targetString,chunkLength,outputList,limit):
	mystring=str(targetString) #to prevent modifying the strings
	while len(mystring)>chunkLength: #stop when <1 chunk remains
		newMotif = mystring[:chunkLength]
		outputList.append(newMotif) #replace with tokenize dict-adding code
		mystring = mystring[1:] #only advances the string by 1 to get all possible strings
		if len(mystring)%10000==0:
			print('Scanning for '+str(chunkLength)+'-BP motifs, '+str(len(mystring))+' bases remaining.')
		if limit!=0: #unlimited
			if len(outputList)>=limit:break

def FreqList(targetFreq, listlength): #gets the most frequently recurring listlength in the frequency list
	newoligolist=[]
	count=0
	for oligo in targetFreq.most_common():
		count+=1
		newoligolist.append(oligo[0])
		if count>listlength:break
	print(newoligolist)
	return newoligolist

##############################
#operating code begins below:#
##############################

#sample filenames for debugging:
#filename1='ecoli1.fna';filename2='paerug1.fna'
#output1='ecolimotifsShort.csv';output2='paerugmotifsShort.csv'
filename1=sys.argv[1];filename2=sys.argv[2] 
output1=sys.argv[3];output2=sys.argv[4] 

with open(filename1) as data1:motifs1=data1.readlines()

with open(filename2) as data2:motifs2=data2.readlines()

depth=0 #for debugging, 0=unlimited, 
#otherwise it stops after int(depth) base pairs

#you can uncomment these, to get more detail, but it takes much longer
#because right now it re-runs the whole genome sample every time
s1m10=[]
tokenizeDNARead(motifs1[0],10,s1m10,depth)
s1m10=FreqList(FreqDist(s1m10),100)
s1m20=[]
tokenizeDNARead(motifs1,20,s1m20,depth)
s1m20=FreqList(FreqDist(s1m20),100)
#s1m40=[]
#tokenizeDNARead(motifs1,40,s1m40,depth)
#s1m40=FreqList(FreqDist(s1m40),100)
#s1m60=[]
#tokenizeDNARead(motifs1,60,s1m60,depth)
#s1m60=FreqList(FreqDist(s1m60),100)
#s1m80=[]
#tokenizeDNARead(motifs1,80,s1m80,depth)
#s1m80=FreqList(FreqDist(s1m80),100)

s2m10=[]
tokenizeDNARead(motifs2,10,s2m10,depth)
s2m10=FreqList(FreqDist(s2m10),100)
s2m20=[]
tokenizeDNARead(motifs1,20,s2m20,depth)
s2m20=FreqList(FreqDist(s2m20),100)
#s2m40=[]
#tokenizeDNARead(motifs1,40,s2m40,depth)
#s2m40=FreqList(FreqDist(s2m40),100)
#s2m60=[]
#tokenizeDNARead(motifs2,60,s2m60,depth)
#s2m60=FreqList(FreqDist(s2m60),100)
#s2m80=[]
#tokenizeDNARead(motifs1,80,s2m80,depth)
#s2m80=FreqList(FreqDist(s2m80),100)

DF1=pd.DataFrame()
DF1['m10']=s1m10
DF1['m20']=s1m20
#DF1['m40']=s1m40
#DF1['m60']=s1m60
#DF1['m80']=s1m80
DF2=pd.DataFrame()
DF2['m10']=s2m10
DF2['m20']=s2m20
#DF2['m40']=s2m40
#DF2['m60']=s2m60
#DF2['m80']=s2m80

DF1.to_csv(output1)
DF2.to_csv(output2)