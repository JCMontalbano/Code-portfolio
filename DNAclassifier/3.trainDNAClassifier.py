#Example call:
#long: python3 3.trainDNAClassifier.py ecoli.paerug.25k.csv ecoli.paerug.h5

#This script takes 2 variables: 
#Arg1: tokenized reads from 2.tokenizeFastQ.py
#Arg2: name for the neural network produced

#It also re-samples from the data until it finds a working combination.
#############################################

import sys
import pandas as pd
import datetime
#Neural networks:
import time
import keras
from keras.layers import Dense
from keras.models import Sequential
from keras.utils import to_categorical

#########################
#	HYPERPARAMETERS 	#
#########################
#hyperparameters customize a neural network. I set them in the script
#to avoid cumbersome commands, which would result from making every
#one of them a sys.argv

#The targetacc, minacc and dropratio variables allow the user to tune
#the accuracy thresholds for faster vs more accurate networks.
targetacc=0.9 #the accuracy rate it starts looking for. This should always
#be higher than the class balance ratio.
minacc=0.8 #the minimum acceptable accuracy rate
dropchangerate=0.001 #the rate at which to decrement the target accuracy
#set dropchangerate=0 or minacc=targetacc to disable accuracy softening.

#I found these parameters doing parameter search for binary classifier with 
#similar variables, so I'm using them here for this demonstration. We can also 
#write a separate script to do a brute-force parameter grid search, and we should.
ratio=0.2 #we'll select 20% of the dataset
layerzlist=[20,22,25,28] #these need to hold the series of parameters we know tend to find solutions
nodezlist=[200,200,250] #4 and 3 are mutually prime, so it combinatorically hits all configurations
epochs=12
activator='relu'
losser='categorical_crossentropy' #these last 2 are hardcoded for now but can easily be changed

reportfile='DNAClassifierLog.txt'

#############################
#	FUNCTIONS				#
#############################

#function which selects a random sample balanced by argument 'ratio'
#The Class_Balance() function lets the user custom-tune class balances, 
# and outputs a balanced random sample.
def ClassBalance(TargetDF, ratio):
	targetDF1=TargetDF[TargetDF[targetcolumn]==1]
	targetDF2=TargetDF[TargetDF[targetcolumn]==0]
	n=int(len(TargetDF)*(ratio/2))
	targetDF1=targetDF1.sample(n=n)
	targetDF2=targetDF2.sample(n=n)
	returnDF=pd.concat([targetDF1,targetDF2], axis=0)
	returnDF=returnDF.sample(frac=1).reset_index(drop=True) #drop=True prevents .reset_index from creating a col with the old index entries
	return(returnDF)

#function which creates, trains, and assesses accuracy on a TensorFlow
#neural network using the provided hyperparameters.
def TrainNet(TargetDF, layers, nodes, epochs, activator, losser):
	target=to_categorical(TargetDF[targetcolumn])
	predictors=TargetDF.drop([targetcolumn], axis=1).as_matrix()
	n_cols=predictors.shape[1]
	model=Sequential()
	model.add(Dense(nodez,activation=activator,input_shape=(n_cols,)))
	for layer in range(0,layers):
		model.add(Dense(nodes,activation=activator))
	model.add(Dense(2,activation='softmax'))
	model.compile(optimizer='adam',loss=losser, metrics=['accuracy'])
	model_training=model.fit(predictors,target, epochs=epochs) #
	acc=model_training.history['acc'] #how do i get just the last value?
	loss=model_training.history['loss']
	acc=acc[-1]
	return(model,acc) 

##############################
#operating code begins below:#
##############################
vectorName=sys.argv[1];net_name=sys.argv[2]

VectorDF=pd.read_csv(vectorName)
targetcolumn='sample' #which corpus it came from? Line 102 in 2.tokenizeFastQ.py

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
				open(reportfile,'a').write('\nSaved '+net_name+' ')
				now=datetime.datetime.now().strftime('%m/%d/%y %H:%M')
				open(reportfile,'a').write(str(now)+'\t Accuracy:'+str(acc)+'\t'+'Layers:'+str(layerz)+' Nodes:'+str(nodez)+' DF length:'+str(len(trainDF)))
			else: 
				del model
				trainDF=ClassBalance(VectorDF,ratio) #resample it
				trainDF=trainDF.sample(frac=1)
				if (targetacc-dropratio)>minacc:
					dropratio+=dropchangerate
				print('Nope, dropratio is '+str(dropratio)+', new acc target is '+str(targetacc-dropratio))
				print('Layers:'+str(layerz)+' Nodes:'+str(nodez)+' trainDF length:'+str(len(trainDF)))
			if new_net==True:
				break
		if new_net==True:
			break

donetime=datetime.datetime.now().strftime('%d/%m/%y %H:%M')
print('Done at '+str(donetime)+' :D')
