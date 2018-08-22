import os
from time import sleep
import pandas as pd
from elasticsearch import Elasticsearch
import pandasticsearch

######################################################################
#The following are functions for working with Elasticsearch in Python#
######################################################################
#this has to be done for ES upload to work, you have to 
#upload each line with the heading reiterated
def prepData(DF): 
	prepData = []
	for index, row in DF.iterrows():
	    data_dict = {}
	    for i in range(len(row)):
	        data_dict[DF.columns[i]] = row[i]
	    op_dict = {
	        "index": {
	            "_index": _INDEX,
	            "_type": _TYPE,
	            "_id": str(index)#otherwise it gives a type error
	        }
	    }
	    prepData.append(op_dict)	#the headings
	    prepData.append(data_dict)	#the row's data
	return prepData

#Create a new index if it's not running yet on the ES server
def makeIndex(): 		#this could be procedurally built from a list 
	request_body = { 	#of column names, but since there's only one 
	    "settings" : {	#configuration here I didn't implement that yet.
	        "number_of_shards": 1,
	        "number_of_replicas": 1
	    },

	    'mappings': {
	        'examplecase': {
	            'properties': {
	                'Name': {'index': 'not_analyzed', 'type': 'string'},
	                'Games': {'index': 'not_analyzed', 'type': 'int'},
	                'Wins': {'index': 'not_analyzed', 'type': 'int'},
	            }}}
	}
	print('Creating'+_INDEX+' index...')
	es.indices.create(index = _INDEX, body = request_body)

#Check the server for a record for the given user, returns boolean, and a record list
def checkRecord(name):
	search = es.search(index=_INDEX, doc_type=_TYPE, body={"query": {"match": {"name": name}}})	
	if search['hits']['total']>0:
		name=search['hits']['hits'][0]['_source']['name']
		games=search['hits']['hits'][0]['_source']['games']
		wins=search['hits']['hits'][0]['_source']['wins']
		print('\tWelcome back, '+name+'! \n Career games:'+str(games)+'\t Career wins:'+str(games))
		return [name,games,wins]
	else: return [name,0,0] #these will become updated records

def updateRecord(name,games,wins):
	search = es.search(index=_INDEX, doc_type=_TYPE, body={"query": {"match": {"name": name}}})	
	if search['hits']['total']!=0:
		print('\tUpdating existing record for '+name+'\nGames:'+str(games)+' Wins:'+str(wins))
		_ID=search['hits']['hits'][0]['_id']
		es.delete(index=_INDEX,doc_type=_TYPE,id=_ID) #delete the old record, and replace
		es.index(index=_INDEX, doc_type=_TYPE,id=_ID, body={'name':name,'games':games,'wins':wins})
	else: print('\tCreating new record for '+name+'\nGames:'+str(games)+' Wins:'+str(wins))
	es.index(index=_INDEX, doc_type=_TYPE, body={'name':name,'games':games,'wins':wins})

#increments up the recordlists, updates records in the index
def winLose(winner):
	if winner==0: #if team 1 wins
		for i in range(len(recordlist1)):
			recordlist1[i][1]+=1 #games
			recordlist1[i][2]+=1 #wins
		for i in range(len(recordlist2)):
			recordlist2[i][1]+=1 #games
	if winner==1: #if team 2 wins
		for i in range(len(recordlist1)):
			recordlist1[i][1]+=1 #games
		for i in range(len(recordlist2)):
			recordlist2[i][1]+=1 #games
			recordlist2[i][2]+=1 #wins
	for recordlist in recordlist1,recordlist2:
		for record in recordlist:
			name=record[0]
			games=record[1]
			wins=record[2]
			updateRecord(name,games,wins)

def topThree():
	records=es.search(index=_INDEX,body={})['hits']['hits']
	recordDF = pd.DataFrame(records)
	newDF=pd.DataFrame(columns=['name','games','wins'])
	for record in recordDF.iterrows():
		name=record[1]['_source']['name']
		games=record[1]['_source']['games']
		wins=record[1]['_source']['wins']
		newrow=[name,games,wins]
		newDF.loc[len(newDF)]=newrow
	newDF['wins']=newDF['wins'].astype(int)
	print('TOP THREE CRICKET MASTERS')
	newDF=newDF.nlargest(3,'wins')
	for row in newDF.iterrows():
		name=row[1][0]
		wins=row[1][2]
		print(name+':\t'+str(wins)+' wins')

#####################################################################
#Functions for running the game:									#
#####################################################################
#Get teams: 
#I chose not to allow asymmetrical team numbers because
#the dart rules I saw implied that, but it would be easy to
#adapt the players= line to do that with two input() calls
#it accepts arbitrarily large numbers per team, which could
#be fun in real life, 30vs30 cricket
def getPlayers():
	print('How many players per team?')
	players=int(input())
	teamlist=[]
	for team in range(2):
		playerlist=[]
		for player in range(players):
			print('Input name for team '+str(team+1)+', player '+str(player+1))
			name=str(input())
			playerlist.append(name)
		teamlist.append(playerlist)
	return teamlist

#the ScoreDF has a column for each team, and a row for
#each target, including the bullseye
def initiateScoreDF():
	ScoreDF=pd.DataFrame(columns=['Team1','Team2'])
	ScoreDF.loc['Score']=0
	for target in targetlist:
		ScoreDF.loc[str(target)]=0
	return ScoreDF

#Define scorecard functions:
#I chose to reproduce the traditional Cricket scorecard
#as an ascii print. Printing the score card is a series
#of task-specific calls and string-formatting, so it makes 
#sense to break it up into functions per each line type

def printNames(Name1,Name2):
	namestring=Name1+'||'+Name2
	print(namestring.center(16, ' '))

def printScore(): 
	Score1=str(ScoreDF.loc['Score']['Team1'])
	Score2=str(ScoreDF.loc['Score']['Team2'])
	targetstring=Score1+'|Score |'+Score2
	print(targetstring.center(16, ' '))


def printX(Score): #interpret's a target's score for printing
	if Score==0:String=' '#printing the space makes ASCII work
	if Score==1:String='/'
	if Score==2:String='X'
	if Score==3:String='O'
	return String

def printTarget(target): #prints a line of 
	Score1=ScoreDF.loc[target]['Team1']
	Score2=ScoreDF.loc[target]['Team2']
	String1=printX(Score1)
	String2=printX(Score2)
	targetstring=String1+'|'+target+'|'+String2
	print(targetstring.center(16, ' '))

clear = lambda:os.system('clear')#resets screen at top of the terminal

def printBoard(Name1,Name2):
	clear() 
	printNames(Name1,Name2) #references positions in the loop, not fcn args
	printScore()
	for target in targetlist:
		printTarget(str(target))#goes down the list

#Parse score inputs:
#It handles errors and misses, and accepts numerals or strings
def parseShot(Name):
	print(Name+', throw the dart!')
	sleep(1)	
	validTarget=False;Bullseye=False;validMultiplier=False
	while validTarget==False:
		score=input('What did you get?')
		if score in ['20','twenty','Twenty']:
			target='20';validTarget=True
		if score in ['19','nineteen','Nineteen']:
			target='19';validTarget=True
		if score in ['18','eightteen','Eightteen','eighteen','Eighteen']:
			target='18';validTarget=True
		if score in ['17','seventeen','Seventeen']:
			target='17';validTarget=True
		if score in ['16','sixteen','Sixteen']:
			target='16';validTarget=True
		if score in ['15','fifteen','Fifteen']:
			target='15';validTarget=True
		if score in ['B','B ','bullseye','Bullseye','bull','b','50']:#it's easy to add new terms, or to use an updated term list somewhere else
			target='B ';validTarget=True
			Bullseye=True #affects the multiplier parse
		if validTarget==False:
			missInput=input("That's not a valid target, did you miss?[Y/n]")
			if missInput!=('n' or 'N' or 'no' or 'No'):
				target=0;multiplier=0
				validTarget=True;validMultiplier=True
	while validMultiplier==False:
		if Bullseye==False:
			multiplier=input('Single, double, or triple?')
		if Bullseye==True:
			multiplier=input('Single or double?') 		
		if multiplier in ['S','s','Single','single','1']:
			multiplier=1;validMultiplier=True
		if multiplier in ['D','d','Double','double','2']:
			multiplier=2;validMultiplier=True
		if (multiplier in ['T','t','Triple','triple','3']) & (Bullseye==False):
			multiplier=3;validMultiplier=True
		if validMultiplier==False:
			print("Sorry, I didn't understand that, please try again")
	return target, multiplier

def parseScore(team,target,multiplier):
	if target==0:return('Miss, no points')
	if team==0:otherTeam=1
	else:otherTeam=0	#to determine if a target is closed
	targetCount=ScoreDF.loc[target][team] #'target' is int now
	otherTeamCount=ScoreDF.loc[target][otherTeam]
	if target=='B ':targetValue=50#convert target to int
	else: targetValue=int(target)
	targetCount+=multiplier #increment up by number of hits
	if targetCount<3:#if you didn't close the target
		ScoreDF.loc[target][team]=targetCount
		pointScore=0
	if targetCount>=3:#if you did close it
		ScoreDF.loc[target][team]=3#reset it to 3 in the DF
		if otherTeamCount==3: #if the other team closed it already
			pointScore=0
			print('Target '+target+' is closed, no points.')
		if otherTeamCount<3: #if the other team hasn't closed it
			pointScore=(targetValue*(targetCount-3))
			print('You scored '+str(pointScore)+' points.')
		targetCount=3 #implemented in either case
	ScoreDF.iloc[0][team]+=pointScore #update the ScoreDF with points
	
#a single turn function puts the above functions together
def Turn(Name1,Name2):
	printBoard(Name1,Name2)
	print('Team 1 is up!');team=0
	print('Shot 1:')
	target,multiplier=parseShot(Name1) #one-liner doesn't work, otherwise
	parseScore(team,target,multiplier) #I would do parseScore(team,parseShot(Name1))
	print('Shot 2:')
	target,multiplier=parseShot(Name1)
	parseScore(team,target,multiplier)
	print('Shot 3:')
	target,multiplier=parseShot(Name1)
	parseScore(team,target,multiplier)
	printBoard(Name1,Name2)
	print('Team 2 is up!');team=1
	print('Shot 1:')
	target,multiplier=parseShot(Name2) #one-liner round call: UpdateTarget(team,parseShot(Name1))
	parseScore(team,target,multiplier)
	print('Shot 2:')
	target,multiplier=parseShot(Name2)
	parseScore(team,target,multiplier)
	print('Shot 3:')
	target,multiplier=parseShot(Name2)
	parseScore(team,target,multiplier)

#this compares the ScoreDF values to see if somebody has won	
def GameOver():
	Team1Score=ScoreDF.iloc[0,0]
	Team2Score=ScoreDF.iloc[0,1]
	Team1Count=ScoreDF.iloc[1:,0].sum()#if the 7 targets are
	Team2Count=ScoreDF.iloc[1:,1].sum()#at 3, 7*3=21
	if (Team1Count==21) & (Team1Score>Team2Score):
		print('Team 1 wins!')
		return(True,0)
	if (Team2Count==21) & (Team2Score>Team1Score):
		print('Team 2 wins!')
		return(True,1)
	else: return(False,0)#team 1 is the 'winner' but the game isn't over

def anotherGame():
	gamestring=input('Another game? [y/N]')
	if gamestring in ['Y','y','Yes','yes','1']:
			return(True)
	else: return(False)
		
#this is the actual game loop, most of the work is in Turn()
def Game():
	gameOver=False
	while gameOver==False:
		for i in range(len(teamlist[0])): #see printNames()
			Name1=teamlist[0][i];Name2=teamlist[1][i]
			Turn(Name1,Name2)
			gameOver,winner=GameOver()
			if gameOver==True:break
		if gameOver==True:break
	return winner

#####################################################################
#The below code runs the actual game:								#
#####################################################################

#Configure the Elastichost server
config = {'host': '127.0.0.1'}
es = Elasticsearch([config,], timeout=300)
_INDEX='jcmcricket' #these have to be lowercase for ES to work
_TYPE='cricketrecord'

#Detect if an index for this game exists. If not,
#automatically populate the server with starting records
fakedict=pd.DataFrame([
{'name':'Jimmy Carter','games':30,'wins':30},
{'name':'Kim Jong Il','games':20,'wins':15},
{'name':'Elvis','games':10,'wins':5},
{'name':'Bob','games':5,'wins':0},])

if es.indices.exists(index=_INDEX):
	print('Local cricket server found')
else:
	print('No cricket server found, initiating default DF')
	fakedata=prepData(fakedict)
	res = es.bulk(index = _INDEX, body = fakedata)

topThree()#print top three performers at start of game
#Taking player names:
teamlist=getPlayers()
recordlist1=[];recordlist2=[]
for name in teamlist[0]:
	recordlist1.append(checkRecord(name))

for name in teamlist[1]:
	recordlist2.append(checkRecord(name))

#initiate list of targets for the scorecard:
targetlist=list(range(15,21));targetlist.append('B ')


newGame=True
while newGame==True:
	ScoreDF=initiateScoreDF()
	winner=Game()
	del(ScoreDF)
	winLose(winner)
	newGame=anotherGame()

print('GAME OVER, see you next time!')
