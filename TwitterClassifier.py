#This python script will pull tweets from two twitter accounts, which it accepts
#as arguments, write a brief report on the results, and then trains a neural net
#to distinguish the two.
#sample command: python3 TwitterClassifier.py realDonaldTrump DrJillStein reportfile.txt
import time
import sys
import pandas as pd
#Twitter scrape:
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import tweepy
#Natural Language Processing:
from nltk import word_tokenize, sent_tokenize
import string
from collections import Counter
#Neural networks:
import keras
from keras.layers import Dense
from keras.models import Sequential
from keras.utils import to_categorical
import datetime

#target1='realDonaldTrump'
#target2='DrJillStein'
#reportfile='reportfile.txt'
target1=sys.argv[1]
target2=sys.argv[2]
reportfile=sys.argv[3]

#Tweepy: collect sample tweets
ckey ='K7fyRPBdo3lHqsydEQm1UI9J1'
csecret = 'O4lldomxfzutFhgwlgjN01J8LaJvqhlYzjNt8Xr5kxKi85QpV2'
atoken = '1531086302-yDaRtB2uFlxwqGK7qwzKNYQuQpkBqPfA2lX5s4R'
asecret ='ajQ8gVN7pcs1pWyw2HjFwHQuow1NHdTji8iWypIVOKUWf'

auth = tweepy.OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

api = tweepy.API(auth)

def GetTweets(target):
    tweetlist=[]
    for tweet in tweepy.Cursor(api.user_timeline,screen_name=target,tweet_mode='extended').items():
        tweetlist.append(tweet.full_text)
        print(tweet.full_text)
    return(tweetlist)

print('Retrieving tweets for '+target1+' and '+target2)
targetlist1=GetTweets(target1)
targetlist2=GetTweets(target2)

#NLTK: vectorize tweets to 21 variables:

#count words and ID 10 most frequent non-stop words in each corpus
print('Counting most frequent words...')
bigString1=''
for tweet in targetlist1:
	bigString1=bigString1+' '+tweet

bigString2=''
for tweet in targetlist2:
	bigString2=bigString2+' '+tweet
#remove punctuation and numerals
bigString1 = bigString1.translate(str.maketrans('','',string.punctuation))
bigString1 = bigString1.translate(str.maketrans('','','1234567890'))
bigString2 = bigString2.translate(str.maketrans('','',string.punctuation))
bigString2 = bigString2.translate(str.maketrans('','','1234567890'))
#tokenize
bigtoken1=word_tokenize(bigString1);prefilter1=len(bigtoken1)
bigtoken2=word_tokenize(bigString2);prefilter2=len(bigtoken2)
#eliminate stopwords:
bigtoken1=[w for w in bigtoken1 if not w in stop_words]
bigtoken2=[w for w in bigtoken2 if not w in stop_words]
nonstop1=str(len(bigtoken1)/prefilter1).ljust(4)[:4]
nonstop2=str(len(bigtoken2)/prefilter2).ljust(4)[:4]

print(target1+' is '+nonstop1+' unique words.')
print(target2+' is '+nonstop2+' unique words.')

#count them
c1=Counter(bigtoken1)
c1=c1.most_common(10)
c2=Counter(bigtoken2)
c2=c2.most_common(10)

keywordlist=[]
keywordlist1=[]
keywordlist2=[]
for count in c1:
	keywordlist.append(count[0])
	keywordlist1.append(count[0])

for count in c2:
	keywordlist.append(count[0])
	keywordlist2.append(count[0])

print(target1+' most common words:'+str(keywordlist1))
print(target2+' most common words:'+str(keywordlist2))

#for each tweet in target1, then in target2:
VectorDF=pd.DataFrame(columns=['k0','k1','k2','k3','k4','k5','k6','k7','k8','k9','k10','k11','k12','k13','k14','k15','k16','k17','k18','k19','AvgLength','Target1'])
for tweet in targetlist1:
	row=[]
	wtoken=word_tokenize(tweet)
	key0=(wtoken.count(keywordlist[0]))
	key1=(wtoken.count(keywordlist[1]))
	key2=(wtoken.count(keywordlist[2]))
	key3=(wtoken.count(keywordlist[3]))
	key4=(wtoken.count(keywordlist[4]))
	key5=(wtoken.count(keywordlist[5]))
	key6=(wtoken.count(keywordlist[6]))
	key7=(wtoken.count(keywordlist[7]))
	key8=(wtoken.count(keywordlist[8]))
	key9=(wtoken.count(keywordlist[9]))
	key10=(wtoken.count(keywordlist[10]))
	key11=(wtoken.count(keywordlist[11]))
	key12=(wtoken.count(keywordlist[12]))
	key13=(wtoken.count(keywordlist[13]))
	key14=(wtoken.count(keywordlist[14]))
	key15=(wtoken.count(keywordlist[15]))
	key16=(wtoken.count(keywordlist[16]))
	key17=(wtoken.count(keywordlist[17]))
	key18=(wtoken.count(keywordlist[18]))
	key19=(wtoken.count(keywordlist[19]))
	AvgLength= len(word_tokenize(tweet))/len(sent_tokenize(tweet)) #average sentence length, in words
	row=[key0,key1,key2,key3,key4,key5,key6,key7,key8,key9,
	key10,key11,key12,key13,key14,key15,key16,key17,key18,key19,AvgLength,1]
	print(row)
	VectorDF.loc[len(VectorDF)]=row

for tweet in targetlist2:
	row=[]
	wtoken=word_tokenize(tweet)
	key0=(wtoken.count(keywordlist[0]))
	key1=(wtoken.count(keywordlist[1]))
	key2=(wtoken.count(keywordlist[2]))
	key3=(wtoken.count(keywordlist[3]))
	key4=(wtoken.count(keywordlist[4]))
	key5=(wtoken.count(keywordlist[5]))
	key6=(wtoken.count(keywordlist[6]))
	key7=(wtoken.count(keywordlist[7]))
	key8=(wtoken.count(keywordlist[8]))
	key9=(wtoken.count(keywordlist[9]))
	key10=(wtoken.count(keywordlist[10]))
	key11=(wtoken.count(keywordlist[11]))
	key12=(wtoken.count(keywordlist[12]))
	key13=(wtoken.count(keywordlist[13]))
	key14=(wtoken.count(keywordlist[14]))
	key15=(wtoken.count(keywordlist[15]))
	key16=(wtoken.count(keywordlist[16]))
	key17=(wtoken.count(keywordlist[17]))
	key18=(wtoken.count(keywordlist[18]))
	key19=(wtoken.count(keywordlist[19]))
	AvgLength= len(word_tokenize(tweet))/len(sent_tokenize(tweet)) #average sentence length, in words
	row=[key0,key1,key2,key3,key4,key5,key6,key7,key8,key9,
	key10,key11,key12,key13,key14,key15,key16,key17,key18,key19,AvgLength,0]
	print(row)
	VectorDF.loc[len(VectorDF)]=row

#TensorFlow: 
#load NLTK vectors as a target array
#select random 20% of array, 50% class balanced, load it as training data
#train a network using parameters until you get a target threshold
DF=VectorDF
targetcolumn='Target1'

#These parameters were useful for this approach in a different problem, but they don't
#appear very good, for this problem. These parameters need some work.
ratio=0.2 #we'll select 20% of the dataset
layerzlist=[20,22,25,28] #these need to hold the series of parameters we know tend to find solutions
nodezlist=[200,200,250] #4 and 3 are mutually prime, so it'll exhaustively hit all the possible combos
epochs=12
activator='relu'
losser='categorical_crossentropy' #these last 2 are hardcoded for now but can easily be changed

#we set the accuracy targets for this approach by 
targetacc=0.75
minacc=0.6

#function which selects a percent
def ClassBalance(TargetDF, ratio):
	targetDF1=TargetDF[TargetDF['Target1']==1]
	targetDF2=TargetDF[TargetDF['Target1']==0]
	n=int(len(TargetDF)*(ratio/2))
	targetDF1=targetDF1.sample(n=n)
	targetDF2=targetDF2.sample(n=n)
	returnDF=pd.concat([targetDF1,targetDF2], axis=0)
	returnDF=returnDF.sample(frac=1).reset_index(drop=True) #drop=True prevents .reset_index from creating a col with the old index entries
	return(returnDF)

def TrainNet(TargetDF, layerz, nodez, epochs, activator, losser):
	target=to_categorical(TargetDF[targetcolumn])
	predictors=TargetDF.drop([targetcolumn], axis=1).as_matrix()
	n_cols=predictors.shape[1]
	model=Sequential()
	model.add(Dense(nodez,activation=activator,input_shape=(n_cols,)))
	for layer in range(0,layerz):
		model.add(Dense(nodez,activation=activator))
	model.add(Dense(2,activation='softmax'))
	model.compile(optimizer='adam',loss=losser, metrics=['accuracy'])
	model_training=model.fit(predictors,target, epochs=epochs) #
	acc=model_training.history['acc'] #how do i get just the last value?
	loss=model_training.history['loss']
	acc=acc[-1]
	return(model,acc) 

#generate a dynamic neural network name:
now=datetime.datetime.now().strftime('%m%d%Y')
net_name=target1+'.'+target2+'.'+str(now)+'.h5'

print('Good luck!')
trainDF=ClassBalance(VectorDF,ratio) #class balance it, instance a new DF for this run
dropratio=0
new_net=False

while new_net==False:
	for layerz in layerzlist:
		for nodez in nodezlist:#will these lists cycle correctly? Yes
			model,acc=TrainNet(trainDF, layerz, nodez, epochs, activator, losser)
			if acc>(targetacc-dropratio): #if acc>target, name and save it and new_net=Tru
				new_net=True
				print('We did it!')
				model.save(net_name)
				open(reportfile,'a').write('\nSaving '+net_name+' ')
				now=datetime.datetime.now().strftime('%m/%d/%y %H:%M')
				open(reportfile,'a').write(str(now)+'\t Dataset:'+str(sys.argv[1])+'\t SeriesID:'+seriesID+'\t Ratio:'+str(posnegratio)+'\t Accuracy:'+str(acc)+'\t'+'Layers:'+str(layerz)+' Nodes:'+str(nodez)+' DF length:'+str(len(trainDF)))
			else: 
				del model
				trainDF=ClassBalance(VectorDF,ratio) #resample it
				trainDF=trainDF.sample(frac=1)
				if (targetacc-dropratio)>minacc:
					dropratio+=0.001
				print('Nope, dropratio is '+str(dropratio)+', new acc target is '+str(targetacc-dropratio))
				print('Layers:'+str(layerz)+' Nodes:'+str(nodez)+' trainDF length:'+str(len(trainDF)))
			if new_net==True:
				break
		if new_net==True:
			break


donetime=datetime.datetime.now().strftime('%d/%m/%y %H:%M')
print('Done at '+str(donetime)+' :D')


#After this script runs, you'll have a custom-named neural network.
#You'll then need a separate script to test that network, which will do the following:

#give the network the remaining 80% of NLTK vectors to predict on

#compare the network's predictions to the actuals:
	#take the higher value as its prediction
	#go through the 'target1' preds, if>0.5 pred=1, if<0.5 pred=0
	#go through the rows side by side, if target1 = target1 pred, True
	#take the % True as score

#Add 5 top words for each target to the report
#Append % True score to end of report
