
# coding: utf-8

# In[1]:

from pyspark import SparkContext, SparkConf
sc = SparkContext(appName="AudioScrobbler")


# In[2]:

#load the data
rawuserartistdata = sc.textFile("s3://aws-logs-648564116187-us-east-1/audiofiles/user_artist_data.txt")


# In[3]:

#check if maximum user and artist IDs are smaller than 2147483647
rawuserartistdata.map(lambda x: float(x.split()[0])).stats()


# In[4]:

rawuserartistdata.map(lambda x: float(x.split()[1])).stats()


# In[5]:

# split data in 1:9 ratio for test and training respectively
#weights = [.1, .9]
#seed = 10000
#sample, test = rawuserartistdata.randomSplit(weights, seed)
#sample.cache()
rawuserartistdata.cache()


# In[6]:

rawartistdata=sc.textFile('s3://aws-logs-648564116187-us-east-1/audiofiles/artist_data.txt')
def splitlines(singlePair):
    words = singlePair.rsplit('\t')
    if len(words) != 2:
        return []
    else:
        try:
            return [(int(words[0]), words[1])]
        except:
            return []

artistByID = dict(rawartistdata.flatMap(lambda x: splitlines(x)).collect())


# In[7]:

rawAliasdata = sc.textFile('s3://aws-logs-648564116187-us-east-1/audiofiles/artist_alias.txt')
artistAlias = rawAliasdata.flatMap(lambda x: splitlines(x)).collectAsMap()


# In[8]:

from pyspark.mllib import recommendation
from pyspark.mllib.recommendation import *

bartistAlias = sc.broadcast(artistAlias)

def mapAlias(x):
    userID, artistID, count = map(lambda lineItem: int(lineItem), x.split())
    finalArtistID = bartistAlias.value.get(artistID)
    if finalArtistID is None:
        finalArtistID = artistID
    return Rating(userID, finalArtistID, count)

trainData = rawuserartistdata.map(lambda x: mapAlias(x))
trainData.cache()


# In[58]:

# training the ALS model with hyperparameters
model = ALS.trainImplicit(trainData, rank=50, iterations=5, lambda_=1.0, alpha=40.0)


# In[60]:

#recommendations for user id #2093760
testUserID = 2093760
artistByIDBroadcast = sc.broadcast(artistByID)

artistsForUser = (trainData
                  .filter(lambda observation: observation.user == testUserID)
                  .map(lambda observation: artistByIDBroadcast.value.get(observation.product))
                  .collect())
print(artistsForUser)

# In[39]:

recommendationsForUser=model.recommendProducts(testUserID, 10)
#print (recommendationsForUser)
for rating in recommendationsForUser:
    print(artistByIDBroadcast.value.get(rating.product))


# In[11]:

#get_ipython().system(u'jupyter nbconvert --to python AudioScrobbler.ipynb')


# In[ ]:

sc.stop()


