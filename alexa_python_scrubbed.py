#!/usr/bin/env python
import requests
import json 
import ast
import tinys3
import uuid

sourcesList = ['bloomberg', 'google-news', 'independant', 'newsweek', 'reuters', 'the-new-york-times']
searchTerms = []
tempList= ['reuters', 'bloomberg', 'the-new-york-times']
apiKey = ''
SAVE_LOCATION = ''
S3_ACCESS_KEY = ''
S3_SECRET_KEY = ''
sendData = []
BUCKET = ''
FILE_NAME = ''
print "Alexa Python"
def getData(sourcesList, apiKey):
	totalData = []
	
	for source in sourcesList:
		url = 'https://newsapi.org/v2/top-headlines?sources='+source+'&apiKey='+ apiKey
		r = requests.get(url)
		jdata = json.loads(r.content)
		print jdata;
		totalData = totalData +jdata['articles'];
	return totalData;
		
def searchList(myDictList, lookupList):
	goodData = []
	for lookup in lookupList:
		goodData = goodData+search(myDictList, lookup)
	return goodData
def search(myDict, lookup):
	goodData = []
	for d in myDict:
		if (d['description'].find(lookup)!=-1):
			goodData.append(d);
	return goodData

def formatDict(myDictList):
	for elem in myDictList:
		if ('title' in elem):
			elem['titleText'] = elem.pop('title')
		if ('publishedAt' in elem):
			elem['updateDate'] = elem.pop('publishedAt')
		if('description' in elem):
			elem['mainText'] = elem.pop('description')
		elem['uid'] = str(uuid.uuid1())
		if('url' in elem):
			elem['redirectionUrl'] = elem.pop('url');
		if ('urlToImage' in elem):
			elem.pop('urlToImage')
		if ('author' in elem):
			elem.pop('author')

totalData = getData(tempList, apiKey)
sendData = searchList(totalData, searchTerms)
formatDict(sendData)
with open(SAVE_LOCATION,'w') as f:
    f.write(json.dumps(sendData))
f.close()

conn = tinys3.Connection(S3_ACCESS_KEY, S3_SECRET_KEY, tls=True)
f = open(SAVE_LOCATION,'rb')
conn.upload(FILE_NAME,f, BUCKET)