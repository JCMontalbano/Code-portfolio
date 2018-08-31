#example call:
#python3 4.trainClassifierNetwork.py rapid7 10000
#############################################
#This script loads the vectorDF from 3.vectorizeText.py and then trains 
#a neural net to distinguish the two, using TensorFlow and Keras.
#It cycles through a set of hyperparameters which I've found 
#typically work for binary classifier problems like this.
#load NLTK vectors as a target array
#select random 20% of array, 50% class balanced, load it as training data
#train a network using parameters until you get a target accuracy threshold
import sys
import pandas as pd
#Neural networks:
import datetime
import time
import keras
from keras.layers import Dense
from keras.models import Sequential
from keras.utils import to_categorical

#procedurally generated filenames which work through the whole process:
#_KEY='rapid7';_LIMIT=10000 #these must address a previously produced scan file
_KEY=sys.argv[1];_LIMIT=sys.argv[2] 
vectorName=str(_KEY)+'.'+str(_LIMIT)+'.vector.csv'
net_name=str(_KEY)+'.'+str(_LIMIT)+'.h5'
reportfile='4.trainClassifierlog.txt'

#########################
#	HYPERPARAMETERS 	#
#########################

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

VectorDF=pd.read_csv(vectorName)
targetcolumn='whichCorpus' #which corpus it came from? Line 107 in 3.vectorizeText.py

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

#After this script runs, you'll have a custom-named neural network.
#You'll then need a separate script to test that network, and to generate
#new data for it to assess.