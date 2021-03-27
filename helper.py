#import pyspark as ps    # for the pyspark suite
#import datetime
#import pandas as pd
#import matplotlib.pyplot as plt

#from pyspark.sql.functions import col, array_contains
#from pyspark.sql.functions import year, month, dayofmonth


def candidatesearch(lst):
    return '|'.join(lst)


def candidate_count(search_macron, search_lepen):
    
    pd.options.display.max_colwidth = 1000
    
    tweets_df.loc[tweets_df['text'].str.contains(candidatesearch(search_macron), case=False, na=False), 'macron'] = True
    tweets_df.loc[tweets_df['text'].str.contains(candidatesearch(search_lepen), case=False, na=False), 'lepen'] = True
    
    macron_tweets = tweets_df[tweets_df['macron'] == True].groupby('Time Period').count()
    lepen_tweets = tweets_df[tweets_df['lepen'] == True].groupby('Time Period').count()
    lepen_tweets = lepen_tweets.drop(['27-00'])
    
    both_tweets = tweets_df[(tweets_df['lepen'] == True) & (tweets_df['macron'] == True)].groupby('Time Period').count()
    
    return macron_tweets, lepen_tweets, both_tweets

def graph_tweet_count(tweets_df):
    tweet_group = tweets_df.groupby('Time Period').count()
    ax = tweet_group.plot(kind='line',figsize=(10,5),legend=None)
    ax.set_xlabel('Day-Hour')
    ax.set_ylabel('Number of Tweets');
    ax.set_title('Number of Tweets Per Hour')
    fig = ax.get_figure()
    fig.savefig("alltweets.png")
    
    return ax

def graph_candidate_count(m, l, b):
    fig, ax2 = plt.subplots(1,1,figsize=(10,5))
    ax2.plot(m['created_at'],label='Macron')
    ax2.plot(l['created_at'],label='Le Pen')
    ax2.plot(b['created_at'],label='Both')
    ax2.set_xlabel('Day-Hour')
    ax2.set_ylabel('Number of Tweets');
    ax2.set_title('Number of Tweets Per Hour')
    ax2.set_xticks(('26-13', '27-01', '27-13', '28-01', '28-13', '29-01'))
    ax2.legend()

    fig = ax2.get_figure()
    fig.savefig("mentions.png")
    
    return ax2

if __name__ == "__main__":
    print("this file must be imported")
    