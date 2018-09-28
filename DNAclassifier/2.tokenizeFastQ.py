#Example call:
#long: python3 2.tokenizeFastQ.py ecolimotifs1020.csv paerugmotifs1020.csv Ecoli.FLX.fna paerug1.fastq ecoli.paerug.full.csv 0
#short: python3 2.tokenizeFastQ.py ecolimotifs1020.csv paerugmotifs1020.csv Ecoli.FLX.fna paerug1.fastq ecoli.paerug.100k.csv 100000

#This script takes 2 motif frequency files prepared in 1.learnMotifs.py, 
#loads 2 raw sequence data files, and counts them for frequencies
#Arg 1: first motif frequency list; Arg 2: second motif list
#Arg 3: first FastQ sequencing data; Arg 4: second fastQ sequencing data
#Arg 5: output tokenized DF, prepped for training in 3.TrainDNAClassifier.py
#############################################

import HTSeq, sys, os.path, itertools
import pandas as pd

#############################
#	FUNCTIONS				#
#############################

def openDNA(filename):
	extension=os.path.splitext(filename)[1]
	if extension in ['.fna','.fasta','.ffn','.faa','.frn']:
		print('File '+filename+' is type FastA.')
		file=HTSeq.FastaReader(filename)
		num_lines=sum(1 for line in open(filename))
	elif extension in ['.fq','.fastq']:
		print('File '+filename+' is type FastQ.')
		file=HTSeq.FastqReader(filename)
		num_lines=int(sum(1 for line in open(filename))/4) #1/4 of lines are sequencesy in fastQ
	else: raise Exception('Unknown file type, exiting.')
	return file, num_lines

def motifList(motifdata): #loads the CSVs from 1.learnMotifs.py as lists
	motifDF=pd.read_csv(motifdata)
	motifList=[]
	for column in motifDF.columns:
		for row in motifDF[column].iteritems():
			motif=row[1]
			motifList.append(motif)
	return motifList

#this processes a fastA or fastQ file for its ngrams
def tokenizeSamples(fastFile,howManyReads,targetlist,whichSample):
	print('Counting ')
	readCount=0
	CombinedReadString=''
	for read in itertools.islice(fastFile,howManyReads):
		readCount+=1
		direct=str(read) #DNA is double-stranded, so we do both ways
		reverse=str(read.get_reverse_complement())
		if readCount%1000!=0: #combine 1k reads together
			CombinedReadString=CombinedReadString+direct+reverse
		if readCount%1000==0: #after combining 1k, tokenize
			row=tokenizeDNARead(CombinedReadString, targetlist)
			#row2=tokenizeDNARead(reverse, targetlist)
			#row=[x+y for x,y in zip(row1,row2)] #produces 1 row for direct and reverse combined
			row.append(whichSample) #tags the row with the source, for training
			VectorDF.loc[len(VectorDF)]=row 
			percentcomplete=(readCount/howManyReads);percentstring='{:%}'.format(percentcomplete)
			print(row)
			print('Counting reads, '+str(percentstring)+' complete')
		if depth!=0: #if depth is limited, break at the limit
			if (readCount/1000)>=(depth/1000):break

def tokenizeDNARead(targetString,mList):
	#count this read for each in the motif list
	row=[]
	for motif in mList: #this fcn accepts motifLists of arbitrary length
		motifCount=targetString.count(motif)
		#print(motif)
		#print(motifCount)
		row.append(motifCount)
	#return a row to put in the VectorDF
	return row


##############################
#operating code begins below:#
##############################
#motifdata1='ecolimotifs1020.csv';motifdata2='paerugmotifs1020.csv'
#SequenceData1='Ecoli.FLX.fna';SequenceData2='paerug.fastq'
#outputVectorDF='ecoli.paerug.tokens.csv'

motifdata1=sys.argv[1];motifdata2=sys.argv[2]
SequenceData1=sys.argv[3];SequenceData2=sys.argv[4] #the sequence data, fastA or fastQ
outputVectorDF=sys.argv[5];depth=int(sys.argv[6]) #0=unlimited

file1,num_lines1=openDNA(SequenceData1)
file2,num_lines2=openDNA(SequenceData2)

motifs1=motifList(motifdata1)
motifs2=motifList(motifdata2)#load both motifs files from 1.learnMotifs.py as lists
motifsList1=list(set(motifs1)-set(motifs2))[:100] #counter-filter lists to strengthen binary classification
motifsList2=list(set(motifs2)-set(motifs1))[:100]
motifsList=motifsList1+motifsList2
print('motifsList:'+str(len(motifsList))+', motifsList1:'+str(len(motifsList1))+', motifsList2:'+str(len(motifsList2)))
VectorDF=pd.DataFrame() #make vectorDF

for motif in motifsList:
		VectorDF[str(motif)]=motif 
		#makes empty DF with the correct headings

VectorDF['sample']=[]

tokenizeSamples(file1,num_lines1,motifsList,0)
tokenizeSamples(file2,num_lines2,motifsList,1)
#tokenizeMotifs directly modifies the existing global var 'VectorDF' 
#hence there is no var assignment here

VectorDF.to_csv(outputVectorDF)
