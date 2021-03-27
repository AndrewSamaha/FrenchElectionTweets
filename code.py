import pyspark as ps    # for the pyspark suite
from pyspark.sql.functions import col, array_contains
import datetime
from pyspark.sql.functions import year, month, dayofmonth
import pandas as pd
import matplotlib.pyplot as plt


spark = ps.sql.SparkSession.builder \
            .master("local[2]") \
            .appName("Spark Session Intro") \
            .getOrCreate()

sc = spark.sparkContext 

frenchtweets_df = spark.read.json('data/french_tweets.json')
df = frenchtweets_df.toPandas()
tweets_df = df[['created_at','text']]
tweets_df['Time Period'] = pd.to_datetime(tweets_df['created_at']).dt.strftime('%d-%H')

tweet_group = tweets_df.groupby('Time Period').count()
ax = tweet_group.plot(kind='line',figsize=(10,5),legend=None)
ax.set_xlabel('Day-Hour')
ax.set_ylabel('Number of Tweets');
ax.set_title('Number of Tweets Per Hour')
fig = ax.get_figure()
fig.savefig("alltweets.png")

def candidatesearch(lst):
    return '|'.join(lst)

search_macron  = ['macron','emmanuel', 'marche','République','Republique']
search_lepen = ['marine', 'national','rally', 'le pen', 'lepen']
pd.options.display.max_colwidth = 1000
tweets_df.loc[tweets_df['text'].str.contains(candidatesearch(search_macron), case=False, na=False), 'macron'] = True
tweets_df.loc[tweets_df['text'].str.contains(candidatesearch(search_lepen), case=False, na=False), 'lepen'] = True
macron_tweets = tweets_df[tweets_df['macron'] == True].groupby('Time Period').count()
lepen_tweets = tweets_df[tweets_df['lepen'] == True].groupby('Time Period').count()
both_tweets = tweets_df[(tweets_df['lepen'] == True) & (tweets_df['macron'] == True)].groupby('Time Period').count()

fig, ax2 = plt.subplots(1,1,figsize=(10,5))
ax2.plot(macron_tweets['created_at'],label='Macron')
ax2.plot(lepen_tweets['created_at'],label='Le Pen')
ax2.plot(both_tweets['created_at'],label='Both')
ax2.set_xlabel('Day-Hour')
ax2.set_ylabel('Number of Tweets');
ax2.set_title('Number of Tweets Per Hour')
ax2.set_xticks(('26-13', '27-01', '27-13', '28-01', '28-13', '29-01'))
ax2.legend()

fig = ax2.get_figure()
fig.savefig("mentions.png")
